"""
Module 4: Live AI Agent with Playwright + Ollama (nemotron-3-super:cloud)
-----------------------------------------------------------------------
This agent connects Ollama (`nemotron-3-super:cloud`) to a LIVE Chromium browser.
The AI reads the accessibility snapshot from the real page and interacts with it!
"""

import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional
from playwright.sync_api import sync_playwright, Page, Browser

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


BROWSER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "browser_navigate",
            "description": "Navigate the browser to a specific URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Target webpage URL"}
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_snapshot",
            "description": "Capture the current webpage's accessibility ARIA snapshot to see all text, headings, buttons, and inputs.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_click",
            "description": "Click an element or text on the page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "selector_text": {
                        "type": "string",
                        "description": "Visible text or label of the element to click",
                    },
                },
                "required": ["selector_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_type",
            "description": "Type text into a designated input or search field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "placeholder_or_label": {
                        "type": "string",
                        "description": "Placeholder or label of the input field",
                    },
                    "text": {
                        "type": "string",
                        "description": "Text string to type into the field",
                    },
                },
                "required": ["placeholder_or_label", "text"],
            },
        },
    },
]


class OllamaAgentClient:
    def __init__(self, model: str = "nemotron-3-super:cloud", base_url: str = "http://127.0.0.1:11434"):
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

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("message", {})
        except urllib.error.URLError as e:
            return {"role": "assistant", "content": f"Ollama Connection Error: {e}"}


class PlaywrightMCPSimulator:
    """Controls real Playwright browser based on MCP tool calls."""

    def __init__(self, page: Page):
        self.page = page

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        try:
            if tool_name == "browser_navigate":
                url = arguments.get("url", "http://localhost:8501")
                self.page.goto(url, wait_until="domcontentloaded", timeout=45000)
                time.sleep(3)
                return f"Successfully navigated to {url}."

            elif tool_name == "browser_snapshot":
                # Real live ARIA snapshot!
                snapshot = self.page.locator("body").aria_snapshot()
                # Limit length so Ollama doesn't overflow context
                truncated = snapshot[:3500] if len(snapshot) > 3500 else snapshot
                return f"Page ARIA Snapshot:\n{truncated}"

            elif tool_name == "browser_click":
                text = arguments.get("selector_text", "")
                # Try clicking by role/text with force=True to bypass sticky headers
                target = self.page.get_by_text(text, exact=False).first
                if target.is_visible():
                    target.click(force=True)
                    time.sleep(2)
                    return f"Clicked on element containing text: '{text}'."
                else:
                    return f"Could not find visible element with text: '{text}'."

            elif tool_name == "browser_type":
                field = arguments.get("placeholder_or_label", "")
                text_to_type = arguments.get("text", "")
                inp = self.page.get_by_placeholder(field, exact=False).first
                if not inp.is_visible():
                    inp = self.page.get_by_label(field, exact=False).first
                if inp.is_visible():
                    inp.fill(text_to_type)
                    inp.press("Enter")
                    time.sleep(2)
                    return f"Typed '{text_to_type}' into '{field}' and pressed Enter."
                return f"Could not locate input field matching '{field}'."

            return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Error executing {tool_name}: {e}"


def run_live_ai_agent(task_prompt: str, model: str = "nemotron-3-super:cloud", max_turns: int = 6):
    print("=" * 70)
    print(f"🚀 RUNNING LIVE PLAYWRIGHT + AI AGENT")
    print(f"🤖 Model: {model}")
    print(f"🎯 Objective: {task_prompt}")
    print("=" * 70)

    client = OllamaAgentClient(model=model)

    with sync_playwright() as p:
        # Launch real headed browser so you can watch!
        browser: Browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        executor = PlaywrightMCPSimulator(page)

        messages: List[Dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are an autonomous AI testing agent that drives a web browser.\n"
                    "Always call `browser_navigate` to load the application.\n"
                    "Always call `browser_snapshot` to read the accessibility tree before acting.\n"
                    "Use `browser_click` or `browser_type` to accomplish the goal.\n"
                    "When the goal is verified, summarize your findings directly."
                ),
            },
            {"role": "user", "content": task_prompt},
        ]

        for step in range(1, max_turns + 1):
            print(f"\n--- [Turn {step}/{max_turns}] Waiting for LLM Decision ---")
            resp = client.chat(messages, tools=BROWSER_TOOLS)
            messages.append(resp)

            thinking = resp.get("thinking")
            if thinking:
                print(f"🧠 [LLM Reasoning]: {thinking[:200]}...")

            content = resp.get("content")
            if content:
                print(f"💬 [LLM Message]: {content}")

            tool_calls = resp.get("tool_calls", [])
            if not tool_calls:
                print("\n🏁 Agent has completed the task!")
                break

            for call in tool_calls:
                fn = call.get("function", {})
                name = fn.get("name")
                args = fn.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}

                print(f"🔧 Tool Requested: {name}({args})")
                obs = executor.execute(name, args)
                print(f"📋 Observation:\n{obs[:250]}...\n")

                messages.append({
                    "role": "tool",
                    "name": name,
                    "content": obs,
                })

        # Capture evidence screenshot
        screenshot_path = "tests/e2e/screenshots/live_agent_output.png"
        page.screenshot(path=screenshot_path)
        print(f"\n📸 Final screenshot captured: {screenshot_path}")
        browser.close()


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else (
        "Navigate to http://localhost:8501, take an ARIA snapshot, inspect what stocks are listed, "
        "and tell me what the active universe is."
    )
    model_name = sys.argv[2] if len(sys.argv) > 2 else "nemotron-3-super:cloud"
    run_live_ai_agent(task, model=model_name)
