"""
Module 5: Capstone Autonomous AI Test Suite Runner
-------------------------------------------------
Executes YAML test scenarios using an LLM (nemotron-3-super:cloud)
and Playwright MCP tools, compiling results into a comprehensive test report.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from playwright.sync_api import sync_playwright, Page, Browser

# UTF-8 for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


BROWSER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "browser_navigate",
            "description": "Navigate browser to a URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_snapshot",
            "description": "Capture the accessibility ARIA tree of the current page",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_click",
            "description": "Click an element by visible text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Visible text to click"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_type",
            "description": "Type text into an input field",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {"type": "string", "description": "Placeholder or label"},
                    "text": {"type": "string", "description": "Text to enter"}
                },
                "required": ["field", "text"]
            }
        }
    }
]


class OllamaClient:
    def __init__(self, model: str, base_url: str = "http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    return res.get("message", {})
            except urllib.error.HTTPError as e:
                if e.code in (500, 502, 503, 504) and attempt < 2:
                    time.sleep(3)
                    continue
                return {"role": "assistant", "content": f"Ollama Connection Error: {e}"}
            except urllib.error.URLError as e:
                return {"role": "assistant", "content": f"Ollama Connection Error: {e}"}
        return {"role": "assistant", "content": "Ollama Connection Error: Max retries exceeded"}


class BrowserMCPExecutor:
    def __init__(self, page: Page):
        self.page = page

    def execute(self, name: str, args: Dict[str, Any]) -> str:
        try:
            if name == "browser_navigate":
                url = args.get("url", "http://localhost:8501")
                self.page.goto(url, wait_until="domcontentloaded", timeout=45000)
                time.sleep(3)
                return f"Navigated to {url}. Ready."

            elif name == "browser_snapshot":
                tree = self.page.locator("body").aria_snapshot()
                truncated = tree[:3000] if len(tree) > 3000 else tree
                return f"ARIA Snapshot:\n{truncated}"

            elif name == "browser_click":
                txt = args.get("text", "")
                loc = self.page.get_by_text(txt, exact=False).first
                if loc.is_visible():
                    loc.click(force=True)
                    time.sleep(2)
                    return f"Clicked element matching '{txt}'."
                return f"Element '{txt}' not visible to click."

            elif name == "browser_type":
                field = args.get("field", "")
                val = args.get("text", "")
                inp = self.page.get_by_placeholder(field, exact=False).first
                if not inp.is_visible():
                    inp = self.page.get_by_label(field, exact=False).first
                if inp.is_visible():
                    inp.fill(val)
                    inp.press("Enter")
                    time.sleep(2)
                    return f"Typed '{val}' into '{field}'."
                return f"Input field matching '{field}' not visible."

            return f"Unknown tool: {name}"
        except Exception as e:
            return f"Tool execution failed: {e}"


def run_scenario(scenario: Dict[str, Any], model_name: str, p: Any, report_dir: Path) -> Dict[str, Any]:
    sc_id = scenario["id"]
    name = scenario["name"]
    instructions = scenario["instructions"]

    print(f"\n[{sc_id}] Running: {name}")
    print("-" * 60)

    start_time = time.time()
    client = OllamaClient(model=model_name)

    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    executor = BrowserMCPExecutor(page)

    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are an automated web QA test runner using Playwright MCP tools.\n"
                "Execute the given test scenario step by step.\n"
                "Always take an ARIA snapshot first to inspect the page.\n"
                "When all steps are finished, summarize your evaluation and state explicitly:\n"
                "VERDICT: PASS or VERDICT: FAIL followed by your rationale."
            ),
        },
        {"role": "user", "content": instructions},
    ]

    action_log = []
    final_message = ""

    for turn in range(1, 8):
        resp = client.chat(messages, tools=BROWSER_TOOLS)
        messages.append(resp)

        content = resp.get("content", "")
        tool_calls = resp.get("tool_calls", [])

        if content:
            final_message = content

        if not tool_calls:
            break

        for tc in tool_calls:
            fn = tc.get("function", {})
            t_name = fn.get("name")
            t_args = fn.get("arguments", {})
            if isinstance(t_args, str):
                try:
                    t_args = json.loads(t_args)
                except Exception:
                    t_args = {}

            print(f"  Step {turn}: {t_name}({t_args})")
            obs = executor.execute(t_name, t_args)
            action_log.append(f"{t_name}: {obs[:120]}")

            messages.append({
                "role": "tool",
                "name": t_name,
                "content": obs,
            })

    duration = round(time.time() - start_time, 2)

    # Save screenshot
    screenshot_file = report_dir / f"screenshot_{sc_id}.png"
    page.screenshot(path=str(screenshot_file))
    browser.close()

    # Determine PASS/FAIL from final message
    passed = "VERDICT: FAIL" not in final_message.upper() and ("PASS" in final_message.upper() or "SUCCESS" in final_message.upper())

    verdict_str = "PASS" if passed else "FAIL"
    print(f"  Status: {'✅' if passed else '❌'} {verdict_str} ({duration}s)")

    return {
        "id": sc_id,
        "name": name,
        "priority": scenario.get("priority", "Medium"),
        "status": verdict_str,
        "passed": passed,
        "duration": duration,
        "summary": final_message.strip(),
        "action_log": action_log,
        "screenshot": screenshot_file.name,
    }


def generate_markdown_report(suite_data: Dict[str, Any], results: List[Dict[str, Any]], report_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_file = report_dir / "test_report.md"

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    content = [
        f"# 🧪 {suite_data.get('test_suite', 'AI QA Test Report')}",
        f"**Date:** {timestamp}  ",
        f"**Model:** `{suite_data.get('model', 'nemotron-3-super:cloud')}`  ",
        f"**Target:** {suite_data.get('base_url', 'http://localhost:8501')}  ",
        "",
        "## 📊 Executive Summary",
        f"| Total Tests | Passed | Failed | Success Rate |",
        f"| :---: | :---: | :---: | :---: |",
        f"| **{total}** | <font color='green'>**{passed}**</font> | <font color='red'>**{failed}**</font> | **{round((passed/total)*100, 1)}%** |",
        "",
        "## 📋 Detailed Results",
        "| ID | Test Scenario | Priority | Duration | Status |",
        "| :--- | :--- | :---: | :---: | :---: |",
    ]

    for r in results:
        badge = "🟢 **PASS**" if r["passed"] else "🔴 **FAIL**"
        content.append(f"| `{r['id']}` | {r['name']} | {r['priority']} | {r['duration']}s | {badge} |")

    content.append("\n## 🔍 Individual Scenario Breakdowns\n")
    for r in results:
        status_icon = "✅ PASS" if r["passed"] else "❌ FAIL"
        content.append(f"### [{r['id']}] {r['name']} — {status_icon}")
        content.append(f"**Duration:** {r['duration']}s | **Priority:** {r['priority']}\n")
        content.append(f"**Agent Evaluation:**\n\n> {r['summary'].replace(chr(10), chr(10) + '> ')}\n")
        content.append(f"**Key Actions Taken:**")
        for act in r["action_log"]:
            content.append(f"- `{act}`")
        content.append(f"\n**Captured Visual Evidence:**\n")
        content.append(f"![{r['id']} Screenshot]({r['screenshot']})\n")
        content.append("---\n")

    report_file.write_text("\n".join(content), encoding="utf-8")
    return report_file


def main():
    scenario_path = Path("tests/ai_agent/test_scenarios.yaml")
    if not scenario_path.exists():
        print(f"Error: {scenario_path} not found.")
        sys.exit(1)

    with open(scenario_path, "r", encoding="utf-8") as f:
        suite = yaml.safe_load(f)

    report_dir = Path("tests/ai_agent/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print(f"🌟 STARTING AI TEST SUITE: {suite.get('test_suite')}")
    print(f"🤖 Model: {suite.get('model')}")
    print(f"📁 Scenarios to run: {len(suite.get('scenarios', []))}")
    print("=" * 65)

    results = []
    with sync_playwright() as p:
        for sc in suite.get("scenarios", []):
            res = run_scenario(sc, suite.get("model", "nemotron-3-super:cloud"), p, report_dir)
            results.append(res)

    report_path = generate_markdown_report(suite, results, report_dir)
    print("\n" + "=" * 65)
    print(f"🎉 SUITE EXECUTION COMPLETE!")
    print(f"📄 Report generated at: {report_path.resolve()}")
    print("=" * 65)


if __name__ == "__main__":
    main()
