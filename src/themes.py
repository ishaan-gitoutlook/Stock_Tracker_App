"""Theme definitions, color palettes, and dynamic CSS styling for the StockPulse dashboard."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ThemeConfig:
    """Design tokens and color palettes for a dashboard theme."""

    name: str
    display_name: str
    is_dark: bool

    # Page & Layout
    page_bg: str
    page_gradient: str
    sidebar_bg: str
    sidebar_border: str

    # Card & Glassmorphic Surfaces
    surface_card: str
    card_border: str
    card_hover_border: str
    card_hover_shadow: str
    card_shadow: str

    # Typography
    text_primary: str
    text_secondary: str
    text_muted: str

    # Accents & Brand
    accent_primary: str
    accent_secondary: str
    accent_gradient: str

    # Hero Panel
    hero_bg: str
    hero_border: str
    hero_text: str
    hero_subtitle: str
    hero_eyebrow: str

    # Form Controls & Inputs
    input_bg: str
    input_border: str
    input_text: str
    tag_bg: str
    tag_text: str

    # Financial Deltas & Indicators
    bullish_color: str
    bullish_bg: str
    bearish_color: str
    bearish_bg: str
    live_dot_color: str

    # Floating Assistant Button
    fab_gradient: str
    fab_shadow: str


THEMES: Dict[str, ThemeConfig] = {
    "Midnight Navy": ThemeConfig(
        name="Midnight Navy",
        display_name="🌙 Midnight Navy (Default Dark)",
        is_dark=True,
        page_bg="#0a0f1d",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(99, 102, 241, 0.18), transparent 45%), radial-gradient(circle at 90% 20%, rgba(6, 182, 212, 0.14), transparent 38%), #0a0f1d",
        sidebar_bg="linear-gradient(180deg, #0f1629 0%, #0a0f1d 100%)",
        sidebar_border="rgba(99, 102, 241, 0.22)",
        surface_card="rgba(17, 25, 46, 0.78)",
        card_border="rgba(99, 102, 241, 0.2)",
        card_hover_border="rgba(99, 102, 241, 0.55)",
        card_hover_shadow="0 14px 32px rgba(0, 0, 0, 0.45), 0 0 20px rgba(99, 102, 241, 0.22)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.28)",
        text_primary="#f8fafc",
        text_secondary="#94a3b8",
        text_muted="#64748b",
        accent_primary="#6366f1",
        accent_secondary="#06b6d4",
        accent_gradient="linear-gradient(135deg, #6366f1, #06b6d4)",
        hero_bg="linear-gradient(135deg, #111a36 0%, #1c2454 48%, #0d3b52 100%)",
        hero_border="rgba(99, 102, 241, 0.32)",
        hero_text="#ffffff",
        hero_subtitle="#cbd5e1",
        hero_eyebrow="#38bdf8",
        input_bg="#0e162a",
        input_border="rgba(99, 102, 241, 0.26)",
        input_text="#f8fafc",
        tag_bg="rgba(99, 102, 241, 0.22)",
        tag_text="#c7d2fe",
        bullish_color="#10b981",
        bullish_bg="rgba(16, 185, 129, 0.16)",
        bearish_color="#f43f5e",
        bearish_bg="rgba(244, 63, 94, 0.16)",
        live_dot_color="#10b981",
        fab_gradient="linear-gradient(135deg, #6366f1, #06b6d4)",
        fab_shadow="0 8px 24px rgba(99, 102, 241, 0.42)",
    ),
    "Clean Light": ThemeConfig(
        name="Clean Light",
        display_name="☀️ Clean Light (Default Light)",
        is_dark=False,
        page_bg="#f8fafc",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(99, 102, 241, 0.08), transparent 42%), radial-gradient(circle at 95% 15%, rgba(14, 165, 233, 0.07), transparent 36%), #f8fafc",
        sidebar_bg="linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%)",
        sidebar_border="rgba(203, 213, 225, 0.85)",
        surface_card="rgba(255, 255, 255, 0.88)",
        card_border="rgba(226, 232, 240, 0.95)",
        card_hover_border="rgba(99, 102, 241, 0.45)",
        card_hover_shadow="0 14px 30px rgba(15, 23, 42, 0.09), 0 0 16px rgba(99, 102, 241, 0.12)",
        card_shadow="0 4px 16px rgba(15, 23, 42, 0.05)",
        text_primary="#0f172a",
        text_secondary="#475569",
        text_muted="#94a3b8",
        accent_primary="#4f46e5",
        accent_secondary="#0284c7",
        accent_gradient="linear-gradient(135deg, #4f46e5, #0284c7)",
        hero_bg="linear-gradient(135deg, #1e293b 0%, #0f172a 60%, #1e1b4b 100%)",
        hero_border="rgba(255, 255, 255, 0.15)",
        hero_text="#ffffff",
        hero_subtitle="#cbd5e1",
        hero_eyebrow="#38bdf8",
        input_bg="#ffffff",
        input_border="rgba(203, 213, 225, 0.95)",
        input_text="#0f172a",
        tag_bg="rgba(99, 102, 241, 0.12)",
        tag_text="#4338ca",
        bullish_color="#059669",
        bullish_bg="rgba(16, 185, 129, 0.12)",
        bearish_color="#e11d48",
        bearish_bg="rgba(225, 29, 72, 0.12)",
        live_dot_color="#10b981",
        fab_gradient="linear-gradient(135deg, #4f46e5, #0ea5e9)",
        fab_shadow="0 8px 24px rgba(79, 70, 229, 0.35)",
    ),
    "Obsidian Noir": ThemeConfig(
        name="Obsidian Noir",
        display_name="🖤 Obsidian Noir (OLED Dark)",
        is_dark=True,
        page_bg="#050608",
        page_gradient="radial-gradient(circle at 12% 0%, rgba(168, 85, 247, 0.14), transparent 45%), radial-gradient(circle at 88% 22%, rgba(236, 72, 153, 0.1), transparent 40%), #050608",
        sidebar_bg="linear-gradient(180deg, #0a0b10 0%, #050608 100%)",
        sidebar_border="rgba(255, 255, 255, 0.09)",
        surface_card="rgba(18, 19, 28, 0.82)",
        card_border="rgba(255, 255, 255, 0.08)",
        card_hover_border="rgba(168, 85, 247, 0.5)",
        card_hover_shadow="0 14px 34px rgba(0, 0, 0, 0.7), 0 0 20px rgba(168, 85, 247, 0.22)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.55)",
        text_primary="#ffffff",
        text_secondary="#a1a1aa",
        text_muted="#71717a",
        accent_primary="#a855f7",
        accent_secondary="#ec4899",
        accent_gradient="linear-gradient(135deg, #a855f7, #ec4899)",
        hero_bg="linear-gradient(135deg, #120f1b 0%, #1f122d 52%, #140b24 100%)",
        hero_border="rgba(168, 85, 247, 0.35)",
        hero_text="#ffffff",
        hero_subtitle="#d4d4d8",
        hero_eyebrow="#c084fc",
        input_bg="#111219",
        input_border="rgba(255, 255, 255, 0.14)",
        input_text="#ffffff",
        tag_bg="rgba(168, 85, 247, 0.2)",
        tag_text="#e9d5ff",
        bullish_color="#34d399",
        bullish_bg="rgba(52, 211, 153, 0.16)",
        bearish_color="#fb7185",
        bearish_bg="rgba(251, 113, 133, 0.16)",
        live_dot_color="#a855f7",
        fab_gradient="linear-gradient(135deg, #a855f7, #ec4899)",
        fab_shadow="0 8px 24px rgba(168, 85, 247, 0.45)",
    ),
    "Emerald Wealth": ThemeConfig(
        name="Emerald Wealth",
        display_name="🌲 Emerald Wealth (Fintech Green)",
        is_dark=True,
        page_bg="#03120b",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(16, 185, 129, 0.16), transparent 45%), radial-gradient(circle at 90% 25%, rgba(245, 158, 11, 0.11), transparent 38%), #03120b",
        sidebar_bg="linear-gradient(180deg, #061a11 0%, #03120b 100%)",
        sidebar_border="rgba(16, 185, 129, 0.22)",
        surface_card="rgba(8, 29, 21, 0.78)",
        card_border="rgba(16, 185, 129, 0.2)",
        card_hover_border="rgba(16, 185, 129, 0.55)",
        card_hover_shadow="0 14px 32px rgba(0, 0, 0, 0.5), 0 0 20px rgba(16, 185, 129, 0.22)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.32)",
        text_primary="#f0fdf4",
        text_secondary="#86efac",
        text_muted="#4ade80",
        accent_primary="#10b981",
        accent_secondary="#f59e0b",
        accent_gradient="linear-gradient(135deg, #10b981, #059669)",
        hero_bg="linear-gradient(135deg, #062419 0%, #0a3828 50%, #124b35 100%)",
        hero_border="rgba(16, 185, 129, 0.36)",
        hero_text="#ffffff",
        hero_subtitle="#bbf7d0",
        hero_eyebrow="#6ee7b7",
        input_bg="#061c13",
        input_border="rgba(16, 185, 129, 0.26)",
        input_text="#f0fdf4",
        tag_bg="rgba(16, 185, 129, 0.22)",
        tag_text="#a7f3d0",
        bullish_color="#34d399",
        bullish_bg="rgba(52, 211, 153, 0.16)",
        bearish_color="#f87171",
        bearish_bg="rgba(248, 113, 113, 0.16)",
        live_dot_color="#34d399",
        fab_gradient="linear-gradient(135deg, #10b981, #059669)",
        fab_shadow="0 8px 24px rgba(16, 185, 129, 0.42)",
    ),
    "Cyber Terminal": ThemeConfig(
        name="Cyber Terminal",
        display_name="⚡ Cyber Terminal (Matrix / Neon)",
        is_dark=True,
        page_bg="#050a10",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(0, 255, 163, 0.13), transparent 42%), radial-gradient(circle at 90% 20%, rgba(0, 229, 255, 0.13), transparent 38%), #050a10",
        sidebar_bg="linear-gradient(180deg, #09131d 0%, #050a10 100%)",
        sidebar_border="rgba(0, 229, 255, 0.22)",
        surface_card="rgba(10, 20, 30, 0.78)",
        card_border="rgba(0, 229, 255, 0.19)",
        card_hover_border="rgba(0, 255, 163, 0.55)",
        card_hover_shadow="0 14px 34px rgba(0, 0, 0, 0.55), 0 0 22px rgba(0, 255, 163, 0.26)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.38)",
        text_primary="#e0f2fe",
        text_secondary="#7dd3fc",
        text_muted="#38bdf8",
        accent_primary="#00ffa3",
        accent_secondary="#00e5ff",
        accent_gradient="linear-gradient(135deg, #00ffa3, #00e5ff)",
        hero_bg="linear-gradient(135deg, #081822 0%, #072a34 52%, #043c40 100%)",
        hero_border="rgba(0, 229, 255, 0.36)",
        hero_text="#ffffff",
        hero_subtitle="#bae6fd",
        hero_eyebrow="#00ffa3",
        input_bg="#08141f",
        input_border="rgba(0, 229, 255, 0.26)",
        input_text="#e0f2fe",
        tag_bg="rgba(0, 229, 255, 0.16)",
        tag_text="#7dd3fc",
        bullish_color="#00ffa3",
        bullish_bg="rgba(0, 255, 163, 0.16)",
        bearish_color="#ff3366",
        bearish_bg="rgba(255, 51, 102, 0.16)",
        live_dot_color="#00ffa3",
        fab_gradient="linear-gradient(135deg, #00ffa3, #00e5ff)",
        fab_shadow="0 8px 24px rgba(0, 229, 255, 0.46)",
    ),
    "Sunset Horizon": ThemeConfig(
        name="Sunset Horizon",
        display_name="🌅 Sunset Horizon (Warm Twilight)",
        is_dark=True,
        page_bg="#100b1a",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(244, 63, 94, 0.15), transparent 42%), radial-gradient(circle at 90% 25%, rgba(245, 158, 11, 0.13), transparent 38%), #100b1a",
        sidebar_bg="linear-gradient(180deg, #181028 0%, #100b1a 100%)",
        sidebar_border="rgba(244, 63, 94, 0.22)",
        surface_card="rgba(28, 19, 46, 0.78)",
        card_border="rgba(244, 63, 94, 0.2)",
        card_hover_border="rgba(244, 63, 94, 0.55)",
        card_hover_shadow="0 14px 34px rgba(0, 0, 0, 0.52), 0 0 22px rgba(244, 63, 94, 0.26)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.36)",
        text_primary="#fff1f2",
        text_secondary="#fda4af",
        text_muted="#f43f5e",
        accent_primary="#f43f5e",
        accent_secondary="#f59e0b",
        accent_gradient="linear-gradient(135deg, #f43f5e, #f59e0b)",
        hero_bg="linear-gradient(135deg, #281338 0%, #3f153b 50%, #521832 100%)",
        hero_border="rgba(244, 63, 94, 0.36)",
        hero_text="#ffffff",
        hero_subtitle="#fecdd3",
        hero_eyebrow="#fb7185",
        input_bg="#19102a",
        input_border="rgba(244, 63, 94, 0.26)",
        input_text="#fff1f2",
        tag_bg="rgba(244, 63, 94, 0.2)",
        tag_text="#fda4af",
        bullish_color="#34d399",
        bullish_bg="rgba(52, 211, 153, 0.16)",
        bearish_color="#f43f5e",
        bearish_bg="rgba(244, 63, 94, 0.16)",
        live_dot_color="#f59e0b",
        fab_gradient="linear-gradient(135deg, #f43f5e, #f59e0b)",
        fab_shadow="0 8px 24px rgba(244, 63, 94, 0.46)",
    ),
    "Arctic Frost": ThemeConfig(
        name="Arctic Frost",
        display_name="❄️ Arctic Frost (Cool Crisp Light)",
        is_dark=False,
        page_bg="#f1f5f9",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(6, 182, 212, 0.11), transparent 45%), radial-gradient(circle at 90% 20%, rgba(59, 130, 246, 0.09), transparent 38%), #f1f5f9",
        sidebar_bg="linear-gradient(180deg, #ffffff 0%, #e2e8f0 100%)",
        sidebar_border="rgba(148, 163, 184, 0.45)",
        surface_card="rgba(255, 255, 255, 0.92)",
        card_border="rgba(203, 213, 225, 0.85)",
        card_hover_border="rgba(6, 182, 212, 0.52)",
        card_hover_shadow="0 14px 30px rgba(15, 23, 42, 0.09), 0 0 16px rgba(6, 182, 212, 0.16)",
        card_shadow="0 4px 16px rgba(15, 23, 42, 0.05)",
        text_primary="#0f172a",
        text_secondary="#334155",
        text_muted="#64748b",
        accent_primary="#0284c7",
        accent_secondary="#0d9488",
        accent_gradient="linear-gradient(135deg, #0284c7, #0d9488)",
        hero_bg="linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0369a1 100%)",
        hero_border="rgba(255, 255, 255, 0.18)",
        hero_text="#ffffff",
        hero_subtitle="#e2e8f0",
        hero_eyebrow="#38bdf8",
        input_bg="#ffffff",
        input_border="rgba(203, 213, 225, 0.85)",
        input_text="#0f172a",
        tag_bg="rgba(2, 132, 199, 0.13)",
        tag_text="#0369a1",
        bullish_color="#059669",
        bullish_bg="rgba(16, 185, 129, 0.12)",
        bearish_color="#e11d48",
        bearish_bg="rgba(225, 29, 72, 0.12)",
        live_dot_color="#0284c7",
        fab_gradient="linear-gradient(135deg, #0284c7, #0d9488)",
        fab_shadow="0 8px 24px rgba(2, 132, 199, 0.35)",
    ),
}

# Aliases for backwards compatibility with "Dark" and "Light"
THEME_ALIASES: Dict[str, str] = {
    "Dark": "Midnight Navy",
    "Light": "Clean Light",
}

THEME_NAMES: List[str] = list(THEMES.keys())
THEME_DISPLAY_OPTIONS: List[str] = [t.display_name for t in THEMES.values()]
DISPLAY_TO_NAME: Dict[str, str] = {t.display_name: name for name, t in THEMES.items()}
NAME_TO_DISPLAY: Dict[str, str] = {name: t.display_name for name, t in THEMES.items()}


def resolve_theme(theme_identifier: Optional[str]) -> ThemeConfig:
    """Resolve a theme name, display name, or alias to a ThemeConfig."""
    if not theme_identifier:
        return THEMES["Midnight Navy"]

    if theme_identifier in THEMES:
        return THEMES[theme_identifier]

    if theme_identifier in DISPLAY_TO_NAME:
        return THEMES[DISPLAY_TO_NAME[theme_identifier]]

    if theme_identifier in THEME_ALIASES:
        resolved_name = THEME_ALIASES[theme_identifier]
        return THEMES[resolved_name]

    return THEMES["Midnight Navy"]


def build_theme_css(theme_input: str) -> str:
    """Generate cohesive, modern, and polished CSS for the dashboard."""
    t = resolve_theme(theme_input)

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {{
        --ui-page: {t.page_bg};
        --ui-page-gradient: {t.page_gradient};
        --ui-sidebar: {t.sidebar_bg};
        --ui-sidebar-border: {t.sidebar_border};
        --ui-surface-card: {t.surface_card};
        --ui-card-border: {t.card_border};
        --ui-card-hover-border: {t.card_hover_border};
        --ui-card-hover-shadow: {t.card_hover_shadow};
        --ui-card-shadow: {t.card_shadow};
        --ui-text-primary: {t.text_primary};
        --ui-text-secondary: {t.text_secondary};
        --ui-text-muted: {t.text_muted};
        --ui-accent-primary: {t.accent_primary};
        --ui-accent-secondary: {t.accent_secondary};
        --ui-accent-gradient: {t.accent_gradient};
        --ui-hero-bg: {t.hero_bg};
        --ui-hero-border: {t.hero_border};
        --ui-hero-text: {t.hero_text};
        --ui-hero-subtitle: {t.hero_subtitle};
        --ui-hero-eyebrow: {t.hero_eyebrow};
        --ui-input-bg: {t.input_bg};
        --ui-input-border: {t.input_border};
        --ui-input-text: {t.input_text};
        --ui-tag-bg: {t.tag_bg};
        --ui-tag-text: {t.tag_text};
        --ui-bullish: {t.bullish_color};
        --ui-bullish-bg: {t.bullish_bg};
        --ui-bearish: {t.bearish_color};
        --ui-bearish-bg: {t.bearish_bg};
        --ui-live-dot: {t.live_dot_color};
        --ui-fab-gradient: {t.fab_gradient};
        --ui-fab-shadow: {t.fab_shadow};
    }}

    /* Global typography & layout */
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}

    .block-container {{
        max-width: 1440px !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}

    /* App container backgrounds */
    [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background: var(--ui-page-gradient) !important;
        color: var(--ui-text-primary) !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: var(--ui-sidebar) !important;
        border-right: 1px solid var(--ui-sidebar-border) !important;
        backdrop-filter: blur(12px);
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--ui-text-primary);
    }}

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {{
        color: var(--ui-text-secondary) !important;
        font-weight: 500 !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {{
        color: var(--ui-text-muted) !important;
    }}

    /* Brand Header */
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
        margin: 0.2rem 0 1.5rem;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid var(--ui-sidebar-border);
    }}

    .brand-mark {{
        display: grid;
        width: 2.6rem;
        height: 2.6rem;
        place-items: center;
        border-radius: 0.8rem;
        color: #ffffff !important;
        background: var(--ui-accent-gradient);
        font-size: 0.95rem;
        font-weight: 900;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        letter-spacing: -0.04em;
    }}

    .brand-info {{
        display: flex;
        flex-direction: column;
    }}

    .brand-name {{
        color: var(--ui-text-primary) !important;
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }}

    .brand-caption {{
        color: var(--ui-text-muted) !important;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }}

    /* Hero Panel */
    .hero-panel {{
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 2rem;
        margin-bottom: 2rem;
        padding: 2.2rem 2.5rem;
        border: 1px solid var(--ui-hero-border);
        border-radius: 1.5rem;
        background: var(--ui-hero-bg);
        box-shadow: 0 1.25rem 3rem rgba(0, 0, 0, 0.28);
        overflow: hidden;
        position: relative;
    }}

    .hero-panel::after {{
        content: "";
        position: absolute;
        width: 20rem;
        height: 20rem;
        right: -5rem;
        top: -9rem;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.15), transparent 70%);
        pointer-events: none;
    }}

    .hero-copy {{
        position: relative;
        z-index: 1;
    }}

    .hero-copy h1 {{
        margin: 0.25rem 0 0.5rem 0 !important;
        font-size: clamp(2rem, 3.8vw, 3.4rem) !important;
        font-weight: 800 !important;
        letter-spacing: -0.05em !important;
        color: var(--ui-hero-text) !important;
        -webkit-text-fill-color: var(--ui-hero-text) !important;
        background: none !important;
    }}

    .hero-copy p {{
        margin: 0;
        color: var(--ui-hero-subtitle) !important;
        font-size: 1.05rem;
        font-weight: 400;
    }}

    .eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--ui-hero-eyebrow) !important;
    }}

    .live-dot {{
        width: 0.52rem;
        height: 0.52rem;
        border-radius: 50%;
        background: var(--ui-live-dot);
        box-shadow: 0 0 0.65rem var(--ui-live-dot);
        animation: live-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }}

    @keyframes live-pulse {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.3); opacity: 0.65; }}
    }}

    .hero-stats-row {{
        display: flex;
        gap: 1rem;
        position: relative;
        z-index: 1;
        flex-wrap: wrap;
    }}

    .hero-stat-card {{
        min-width: 8rem;
        padding: 0.9rem 1.25rem;
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
    }}

    .hero-stat-card strong {{
        display: block;
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1;
        color: #ffffff !important;
    }}

    .hero-stat-card span {{
        display: block;
        margin-top: 0.35rem;
        color: rgba(255, 255, 255, 0.75) !important;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Section Headings */
    .section-heading {{
        margin: 1.5rem 0 1rem;
    }}

    .overview-heading {{
        margin-top: 2.5rem;
    }}

    .section-kicker {{
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--ui-accent-primary);
    }}

    .section-title {{
        margin-top: 0.15rem;
        color: var(--ui-text-primary) !important;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }}

    .section-subtitle {{
        color: var(--ui-text-secondary) !important;
        font-size: 0.9rem;
    }}

    /* Stock Metric Cards */
    div[data-testid="stMetric"] {{
        background: var(--ui-surface-card) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--ui-card-border) !important;
        border-radius: 1.15rem !important;
        padding: 1.15rem 1.25rem !important;
        box-shadow: var(--ui-card-shadow) !important;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                    box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                    border-color 0.2s ease !important;
        min-height: 7.5rem;
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px) !important;
        border-color: var(--ui-card-hover-border) !important;
        box-shadow: var(--ui-card-hover-shadow) !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: var(--ui-text-secondary) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: var(--ui-text-primary) !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        font-family: 'JetBrains Mono', monospace, sans-serif !important;
    }}

    div[data-testid="stMetricDelta"] {{
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        font-family: 'JetBrains Mono', monospace, sans-serif !important;
    }}

    /* Market Overview Table */
    [data-testid="stDataFrame"] {{
        border: 1px solid var(--ui-card-border) !important;
        border-radius: 1.15rem !important;
        overflow: hidden !important;
        background: var(--ui-surface-card) !important;
        box-shadow: var(--ui-card-shadow) !important;
        backdrop-filter: blur(16px);
    }}

    /* Form Controls & Inputs */
    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div,
    [data-testid="stTextInput"] input {{
        background: var(--ui-input-bg) !important;
        color: var(--ui-input-text) !important;
        border-color: var(--ui-input-border) !important;
        border-radius: 0.75rem !important;
    }}

    [data-baseweb="select"] *,
    [data-testid="stTextInput"] input::placeholder {{
        color: var(--ui-text-secondary) !important;
    }}

    /* Multiselect tag pills */
    [data-baseweb="tag"] {{
        background: var(--ui-tag-bg) !important;
        color: var(--ui-tag-text) !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
    }}

    [data-baseweb="tag"] span {{
        color: var(--ui-tag-text) !important;
    }}

    /* Buttons */
    [data-testid="stButton"] button,
    [data-testid="stFormSubmitButton"] button {{
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        border-color: var(--ui-card-border) !important;
        background: var(--ui-surface-card) !important;
        color: var(--ui-text-primary) !important;
    }}

    [data-testid="stButton"] button:hover,
    [data-testid="stFormSubmitButton"] button:hover {{
        transform: translateY(-2px);
        border-color: var(--ui-accent-primary) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15) !important;
    }}

    [data-testid="stFormSubmitButton"] button {{
        background: var(--ui-accent-gradient) !important;
        color: #ffffff !important;
        border: none !important;
    }}

    /* Floating AI Assistant FAB & Launcher */
    .st-key-assistant_launcher {{
        position: fixed !important;
        right: 1.5rem !important;
        bottom: 1.5rem !important;
        z-index: 999999 !important;
    }}

    .st-key-assistant_launcher > div,
    .st-key-assistant_launcher [data-testid="stPopover"] {{
        width: max-content !important;
        min-width: 0 !important;
        max-width: max-content !important;
        background: transparent !important;
        border: 0 !important;
    }}

    .st-key-assistant_launcher button[data-testid="stPopoverButton"],
    .st-key-assistant_launcher > div > button {{
        width: 3.5rem !important;
        min-width: 3.5rem !important;
        max-width: 3.5rem !important;
        height: 3.5rem !important;
        min-height: 3.5rem !important;
        padding: 0 !important;
        border-radius: 999px !important;
        border: 2px solid rgba(255, 255, 255, 0.45) !important;
        color: #ffffff !important;
        background: var(--ui-fab-gradient) !important;
        box-shadow: var(--ui-fab-shadow) !important;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease !important;
        animation: assistant-pulse-ring 3.5s ease-in-out infinite !important;
        display: grid !important;
        place-items: center !important;
    }}

    .st-key-assistant_launcher button[data-testid="stPopoverButton"]:hover,
    .st-key-assistant_launcher > div > button:hover {{
        transform: scale(1.1) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45) !important;
    }}

    @keyframes assistant-pulse-ring {{
        0%, 100% {{
            box-shadow: var(--ui-fab-shadow);
        }}
        50% {{
            box-shadow: 0 0 0 12px rgba(99, 102, 241, 0.2), var(--ui-fab-shadow);
        }}
    }}

    /* Popover Modal Container Sizing & Styling */
    div[data-testid="stPopoverBody"] {{
        width: 500px !important;
        min-width: 320px !important;
        max-width: calc(100vw - 2.5rem) !important;
        max-height: calc(85vh - 2rem) !important;
        border-radius: 1.35rem !important;
        background: var(--ui-surface-card) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid var(--ui-card-border) !important;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.48), 0 0 1px rgba(255, 255, 255, 0.18) !important;
        padding: 1.25rem 1.4rem !important;
        overflow-y: auto !important;
    }}

    /* Modern Chat UI Components */
    .chat-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
        padding-bottom: 0.85rem;
        border-bottom: 1px solid var(--ui-card-border);
    }}

    .chat-header-left {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .chat-avatar {{
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 0.75rem;
        background: var(--ui-accent-gradient);
        display: grid;
        place-items: center;
        font-size: 1.15rem;
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }}

    .chat-title-group {{
        display: flex;
        flex-direction: column;
    }}

    .chat-title {{
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--ui-text-primary) !important;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}

    .chat-status {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--ui-bullish) !important;
    }}

    .chat-status-dot {{
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 50%;
        background: var(--ui-bullish);
        box-shadow: 0 0 6px var(--ui-bullish);
        display: inline-block;
        animation: live-pulse 2s infinite;
    }}

    .chat-context-bar {{
        display: flex;
        align-items: center;
        gap: 0.4rem;
        flex-wrap: wrap;
        margin-bottom: 0.75rem;
        padding: 0.45rem 0.75rem;
        border-radius: 0.75rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--ui-card-border);
    }}

    .context-label {{
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--ui-text-muted) !important;
    }}

    .context-ticker {{
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 0.15rem 0.45rem;
        border-radius: 0.4rem;
        background: var(--ui-tag-bg);
        color: var(--ui-tag-text) !important;
        border: 1px solid var(--ui-card-border);
        font-family: 'JetBrains Mono', monospace, sans-serif;
    }}

    .chat-empty-card {{
        padding: 1.25rem 1rem;
        text-align: center;
        border: 1px dashed var(--ui-card-border);
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.02);
        margin: 0.4rem 0 0.85rem;
    }}

    .chat-empty-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.35rem;
    }}

    .chat-empty-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--ui-text-primary);
        margin-bottom: 0.2rem;
    }}

    .chat-empty-desc {{
        font-size: 0.78rem;
        color: var(--ui-text-secondary);
        max-width: 320px;
        margin: 0 auto;
        line-height: 1.4;
    }}

    /* Chat Messages styling */
    [data-testid="stChatMessage"] {{
        background: var(--ui-surface-card) !important;
        border: 1px solid var(--ui-card-border) !important;
        border-radius: 1rem !important;
        padding: 0.75rem 0.95rem !important;
        margin-bottom: 0.65rem !important;
        color: var(--ui-text-primary) !important;
        backdrop-filter: blur(14px) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
    }}

    /* Differentiate user and assistant bubbles */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
        border-left: 3px solid var(--ui-accent-primary) !important;
        background: rgba(99, 102, 241, 0.08) !important;
    }}

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
        border-left: 3px solid var(--ui-accent-secondary) !important;
    }}

    .chat-message-meta {{
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin-top: 0.35rem;
        font-size: 0.7rem;
        color: var(--ui-text-muted) !important;
        font-weight: 600;
    }}

    /* Dock chat input cleanly inside popover */
    [data-testid="stPopoverBody"] [data-testid="stChatInput"] {{
        position: relative !important;
        bottom: auto !important;
        left: auto !important;
        right: auto !important;
        width: 100% !important;
        padding: 0 !important;
        margin-top: 0.6rem !important;
    }}

    [data-testid="stChatInput"] {{
        border-color: var(--ui-input-border) !important;
        border-radius: 0.75rem !important;
    }}

    [data-testid="stChatInput"] textarea {{
        background: var(--ui-input-bg) !important;
        color: var(--ui-input-text) !important;
    }}

    .chat-footer-disclaimer {{
        font-size: 0.64rem;
        color: var(--ui-text-muted) !important;
        text-align: center;
        margin-top: 0.45rem;
        line-height: 1.3;
    }}

    /* Responsive design */
    @media (max-width: 768px) {{
        .hero-panel {{
            flex-direction: column;
            align-items: flex-start;
            padding: 1.5rem;
            gap: 1.25rem;
        }}
        .hero-stats-row {{
            width: 100%;
        }}
        .hero-stat-card {{
            flex: 1;
        }}
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
    }}
    </style>
    """
