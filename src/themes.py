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
        display_name="🌙 Midnight Navy (Ergonomic Dark)",
        is_dark=True,
        page_bg="#0a0f1d",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(99, 102, 241, 0.16), transparent 45%), radial-gradient(circle at 90% 20%, rgba(6, 182, 212, 0.12), transparent 38%), #0a0f1d",
        sidebar_bg="linear-gradient(180deg, #0e1526 0%, #0a0f1d 100%)",
        sidebar_border="rgba(148, 163, 184, 0.22)",
        surface_card="rgba(17, 26, 46, 0.94)",
        card_border="rgba(148, 163, 184, 0.22)",
        card_hover_border="rgba(129, 140, 248, 0.6)",
        card_hover_shadow="0 12px 28px rgba(0, 0, 0, 0.42), 0 0 16px rgba(99, 102, 241, 0.2)",
        card_shadow="0 4px 18px rgba(0, 0, 0, 0.3)",
        text_primary="#ffffff",
        text_secondary="#cbd5e1",
        text_muted="#94a3b8",
        accent_primary="#6366f1",
        accent_secondary="#06b6d4",
        accent_gradient="linear-gradient(135deg, #6366f1, #06b6d4)",
        hero_bg="linear-gradient(135deg, #131c38 0%, #1a2550 50%, #0e374d 100%)",
        hero_border="rgba(129, 140, 248, 0.35)",
        hero_text="#ffffff",
        hero_subtitle="#e2e8f0",
        hero_eyebrow="#38bdf8",
        input_bg="#10172a",
        input_border="rgba(148, 163, 184, 0.32)",
        input_text="#ffffff",
        tag_bg="rgba(99, 102, 241, 0.26)",
        tag_text="#e0e7ff",
        bullish_color="#10b981",
        bullish_bg="rgba(16, 185, 129, 0.18)",
        bearish_color="#f43f5e",
        bearish_bg="rgba(244, 63, 94, 0.18)",
        live_dot_color="#10b981",
        fab_gradient="linear-gradient(135deg, #6366f1, #06b6d4)",
        fab_shadow="0 8px 24px rgba(99, 102, 241, 0.42)",
    ),
    "Clean Light": ThemeConfig(
        name="Clean Light",
        display_name="☀️ Clean Light (Glare-Free Paper)",
        is_dark=False,
        page_bg="#f3f4f6",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(99, 102, 241, 0.05), transparent 42%), radial-gradient(circle at 95% 15%, rgba(14, 165, 233, 0.04), transparent 36%), #f3f4f6",
        sidebar_bg="linear-gradient(180deg, #eaecef 0%, #f3f4f6 100%)",
        sidebar_border="rgba(203, 213, 225, 0.95)",
        surface_card="rgba(255, 255, 255, 0.95)",
        card_border="rgba(218, 224, 233, 0.95)",
        card_hover_border="rgba(79, 70, 229, 0.45)",
        card_hover_shadow="0 10px 24px rgba(15, 23, 42, 0.07)",
        card_shadow="0 2px 10px rgba(15, 23, 42, 0.04)",
        text_primary="#0f172a",
        text_secondary="#334155",
        text_muted="#64748b",
        accent_primary="#4f46e5",
        accent_secondary="#0284c7",
        accent_gradient="linear-gradient(135deg, #4f46e5, #0284c7)",
        hero_bg="linear-gradient(135deg, #243048 0%, #1e293b 60%, #1a2234 100%)",
        hero_border="rgba(255, 255, 255, 0.16)",
        hero_text="#ffffff",
        hero_subtitle="#e2e8f0",
        hero_eyebrow="#38bdf8",
        input_bg="#ffffff",
        input_border="rgba(203, 213, 225, 0.95)",
        input_text="#0f172a",
        tag_bg="rgba(79, 70, 229, 0.12)",
        tag_text="#3730a3",
        bullish_color="#047857",
        bullish_bg="rgba(16, 185, 129, 0.14)",
        bearish_color="#be123c",
        bearish_bg="rgba(225, 29, 72, 0.14)",
        live_dot_color="#10b981",
        fab_gradient="linear-gradient(135deg, #4f46e5, #0ea5e9)",
        fab_shadow="0 8px 24px rgba(79, 70, 229, 0.35)",
    ),
    "Obsidian Noir": ThemeConfig(
        name="Obsidian Noir",
        display_name="🖤 Obsidian Noir (OLED Sharp)",
        is_dark=True,
        page_bg="#08090d",
        page_gradient="radial-gradient(circle at 12% 0%, rgba(168, 85, 247, 0.14), transparent 45%), radial-gradient(circle at 88% 22%, rgba(236, 72, 153, 0.09), transparent 40%), #08090d",
        sidebar_bg="linear-gradient(180deg, #10121a 0%, #08090d 100%)",
        sidebar_border="rgba(255, 255, 255, 0.14)",
        surface_card="rgba(20, 22, 32, 0.94)",
        card_border="rgba(255, 255, 255, 0.12)",
        card_hover_border="rgba(168, 85, 247, 0.55)",
        card_hover_shadow="0 14px 34px rgba(0, 0, 0, 0.65), 0 0 20px rgba(168, 85, 247, 0.22)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.45)",
        text_primary="#ffffff",
        text_secondary="#e2e8f0",
        text_muted="#a1a1aa",
        accent_primary="#a855f7",
        accent_secondary="#ec4899",
        accent_gradient="linear-gradient(135deg, #a855f7, #ec4899)",
        hero_bg="linear-gradient(135deg, #181424 0%, #251636 52%, #1b0f30 100%)",
        hero_border="rgba(168, 85, 247, 0.35)",
        hero_text="#ffffff",
        hero_subtitle="#e4e4e7",
        hero_eyebrow="#c084fc",
        input_bg="#141620",
        input_border="rgba(255, 255, 255, 0.18)",
        input_text="#ffffff",
        tag_bg="rgba(168, 85, 247, 0.22)",
        tag_text="#f3e8ff",
        bullish_color="#34d399",
        bullish_bg="rgba(52, 211, 153, 0.18)",
        bearish_color="#fb7185",
        bearish_bg="rgba(251, 113, 133, 0.18)",
        live_dot_color="#a855f7",
        fab_gradient="linear-gradient(135deg, #a855f7, #ec4899)",
        fab_shadow="0 8px 24px rgba(168, 85, 247, 0.45)",
    ),
    "Emerald Wealth": ThemeConfig(
        name="Emerald Wealth",
        display_name="🌲 Emerald Wealth (Calm Pine)",
        is_dark=True,
        page_bg="#05130b",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(16, 185, 129, 0.15), transparent 45%), radial-gradient(circle at 90% 25%, rgba(245, 158, 11, 0.09), transparent 38%), #05130b",
        sidebar_bg="linear-gradient(180deg, #091e13 0%, #05130b 100%)",
        sidebar_border="rgba(16, 185, 129, 0.25)",
        surface_card="rgba(12, 32, 22, 0.94)",
        card_border="rgba(16, 185, 129, 0.24)",
        card_hover_border="rgba(16, 185, 129, 0.6)",
        card_hover_shadow="0 14px 32px rgba(0, 0, 0, 0.45), 0 0 18px rgba(16, 185, 129, 0.2)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.3)",
        text_primary="#ffffff",
        text_secondary="#d1fae5",
        text_muted="#86efac",
        accent_primary="#10b981",
        accent_secondary="#f59e0b",
        accent_gradient="linear-gradient(135deg, #10b981, #059669)",
        hero_bg="linear-gradient(135deg, #0a2c1f 0%, #0f4431 50%, #13553c 100%)",
        hero_border="rgba(16, 185, 129, 0.4)",
        hero_text="#ffffff",
        hero_subtitle="#d1fae5",
        hero_eyebrow="#6ee7b7",
        input_bg="#0a2317",
        input_border="rgba(16, 185, 129, 0.32)",
        input_text="#f0fdf4",
        tag_bg="rgba(16, 185, 129, 0.24)",
        tag_text="#d1fae5",
        bullish_color="#34d399",
        bullish_bg="rgba(52, 211, 153, 0.18)",
        bearish_color="#f87171",
        bearish_bg="rgba(248, 113, 113, 0.18)",
        live_dot_color="#34d399",
        fab_gradient="linear-gradient(135deg, #10b981, #059669)",
        fab_shadow="0 8px 24px rgba(16, 185, 129, 0.42)",
    ),
    "Cyber Terminal": ThemeConfig(
        name="Cyber Terminal",
        display_name="⚡ Cyber Terminal (Contrast Neon)",
        is_dark=True,
        page_bg="#060d15",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(0, 255, 163, 0.12), transparent 42%), radial-gradient(circle at 90% 20%, rgba(0, 229, 255, 0.12), transparent 38%), #060d15",
        sidebar_bg="linear-gradient(180deg, #0a1622 0%, #060d15 100%)",
        sidebar_border="rgba(0, 229, 255, 0.25)",
        surface_card="rgba(13, 26, 38, 0.94)",
        card_border="rgba(0, 229, 255, 0.22)",
        card_hover_border="rgba(0, 255, 163, 0.6)",
        card_hover_shadow="0 14px 34px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 255, 163, 0.24)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.35)",
        text_primary="#ffffff",
        text_secondary="#e0f2fe",
        text_muted="#7dd3fc",
        accent_primary="#00ffa3",
        accent_secondary="#00e5ff",
        accent_gradient="linear-gradient(135deg, #00ffa3, #00e5ff)",
        hero_bg="linear-gradient(135deg, #0c212e 0%, #0c3845 52%, #084c52 100%)",
        hero_border="rgba(0, 229, 255, 0.4)",
        hero_text="#ffffff",
        hero_subtitle="#e0f2fe",
        hero_eyebrow="#00ffa3",
        input_bg="#0d1b28",
        input_border="rgba(0, 229, 255, 0.32)",
        input_text="#f0f9ff",
        tag_bg="rgba(0, 229, 255, 0.2)",
        tag_text="#bae6fd",
        bullish_color="#00ffa3",
        bullish_bg="rgba(0, 255, 163, 0.18)",
        bearish_color="#ff3366",
        bearish_bg="rgba(255, 51, 102, 0.18)",
        live_dot_color="#00ffa3",
        fab_gradient="linear-gradient(135deg, #00ffa3, #00e5ff)",
        fab_shadow="0 8px 24px rgba(0, 229, 255, 0.46)",
    ),
    "Sunset Horizon": ThemeConfig(
        name="Sunset Horizon",
        display_name="🌅 Sunset Horizon (Warm Twilight)",
        is_dark=True,
        page_bg="#120c1a",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(244, 63, 94, 0.13), transparent 42%), radial-gradient(circle at 90% 25%, rgba(245, 158, 11, 0.1), transparent 38%), #120c1a",
        sidebar_bg="linear-gradient(180deg, #1b1226 0%, #120c1a 100%)",
        sidebar_border="rgba(244, 63, 94, 0.25)",
        surface_card="rgba(32, 22, 48, 0.94)",
        card_border="rgba(244, 63, 94, 0.24)",
        card_hover_border="rgba(244, 63, 94, 0.6)",
        card_hover_shadow="0 14px 34px rgba(0, 0, 0, 0.48), 0 0 20px rgba(244, 63, 94, 0.24)",
        card_shadow="0 6px 20px rgba(0, 0, 0, 0.32)",
        text_primary="#ffffff",
        text_secondary="#ffe4e6",
        text_muted="#fca5a5",
        accent_primary="#f43f5e",
        accent_secondary="#f59e0b",
        accent_gradient="linear-gradient(135deg, #f43f5e, #f59e0b)",
        hero_bg="linear-gradient(135deg, #321746 0%, #4a1946 50%, #5e1c3b 100%)",
        hero_border="rgba(244, 63, 94, 0.4)",
        hero_text="#ffffff",
        hero_subtitle="#ffe4e6",
        hero_eyebrow="#fb7185",
        input_bg="#211534",
        input_border="rgba(244, 63, 94, 0.32)",
        input_text="#fff1f2",
        tag_bg="rgba(244, 63, 94, 0.24)",
        tag_text="#ffe4e6",
        bullish_color="#34d399",
        bullish_bg="rgba(52, 211, 153, 0.18)",
        bearish_color="#f43f5e",
        bearish_bg="rgba(244, 63, 94, 0.18)",
        live_dot_color="#f59e0b",
        fab_gradient="linear-gradient(135deg, #f43f5e, #f59e0b)",
        fab_shadow="0 8px 24px rgba(244, 63, 94, 0.46)",
    ),
    "Arctic Frost": ThemeConfig(
        name="Arctic Frost",
        display_name="❄️ Arctic Frost (Nordic Mist)",
        is_dark=False,
        page_bg="#edf1f5",
        page_gradient="radial-gradient(circle at 10% 0%, rgba(6, 182, 212, 0.06), transparent 45%), radial-gradient(circle at 90% 20%, rgba(59, 130, 246, 0.05), transparent 38%), #edf1f5",
        sidebar_bg="linear-gradient(180deg, #e4e9ef 0%, #edf1f5 100%)",
        sidebar_border="rgba(203, 213, 225, 0.95)",
        surface_card="rgba(255, 255, 255, 0.95)",
        card_border="rgba(214, 222, 232, 0.95)",
        card_hover_border="rgba(6, 182, 212, 0.55)",
        card_hover_shadow="0 10px 24px rgba(15, 23, 42, 0.08)",
        card_shadow="0 2px 10px rgba(15, 23, 42, 0.04)",
        text_primary="#0f172a",
        text_secondary="#334155",
        text_muted="#64748b",
        accent_primary="#0284c7",
        accent_secondary="#0d9488",
        accent_gradient="linear-gradient(135deg, #0284c7, #0d9488)",
        hero_bg="linear-gradient(135deg, #1e2d42 0%, #152234 60%, #0a3d54 100%)",
        hero_border="rgba(255, 255, 255, 0.18)",
        hero_text="#ffffff",
        hero_subtitle="#e2e8f0",
        hero_eyebrow="#38bdf8",
        input_bg="#ffffff",
        input_border="rgba(203, 213, 225, 0.95)",
        input_text="#0f172a",
        tag_bg="rgba(2, 132, 199, 0.13)",
        tag_text="#0369a1",
        bullish_color="#047857",
        bullish_bg="rgba(16, 185, 129, 0.14)",
        bearish_color="#be123c",
        bearish_bg="rgba(225, 29, 72, 0.14)",
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
    """Generate cohesive, high-contrast, glare-free, and eye-friendly CSS for the dashboard."""
    t = resolve_theme(theme_input)

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    .block-container {{
        max-width: 1440px !important;
        padding-top: 1.8rem !important;
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

    /* Universal typography overrides for absolute clarity */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--ui-text-primary) !important;
        font-weight: 750 !important;
    }}

    p, span, label {{
        color: inherit;
    }}

    .stMarkdown p {{
        color: var(--ui-text-secondary);
        font-size: 0.95rem;
        line-height: 1.55;
    }}

    /* Sidebar styling with high contrast readability */
    section[data-testid="stSidebar"] {{
        background: var(--ui-sidebar) !important;
        border-right: 1px solid var(--ui-sidebar-border) !important;
        backdrop-filter: blur(14px);
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--ui-text-primary);
    }}

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {{
        color: var(--ui-text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
    section[data-testid="stSidebar"] .stCaption {{
        color: var(--ui-text-secondary) !important;
        font-size: 0.82rem !important;
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
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }}

    .brand-caption {{
        color: var(--ui-text-secondary) !important;
        font-size: 0.65rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }}

    /* Hero Panel with gentle eye-friendly contrast */
    .hero-panel {{
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 2rem;
        margin-bottom: 1.75rem;
        padding: 2rem 2.25rem;
        border: 1px solid var(--ui-hero-border);
        border-radius: 1.4rem;
        background: var(--ui-hero-bg);
        box-shadow: 0 1rem 2.5rem rgba(0, 0, 0, 0.25);
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
        background: radial-gradient(circle, rgba(255, 255, 255, 0.12), transparent 70%);
        pointer-events: none;
    }}

    .hero-copy {{
        position: relative;
        z-index: 1;
    }}

    .hero-copy h1 {{
        margin: 0.2rem 0 0.45rem 0 !important;
        font-size: clamp(1.8rem, 3.2vw, 2.8rem) !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        color: var(--ui-hero-text) !important;
        -webkit-text-fill-color: var(--ui-hero-text) !important;
        background: none !important;
    }}

    .hero-copy p {{
        margin: 0;
        color: var(--ui-hero-subtitle) !important;
        font-size: 1.02rem;
        font-weight: 450;
        line-height: 1.5;
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
        50% {{ transform: scale(1.3); opacity: 0.7; }}
    }}

    .hero-stats-row {{
        display: flex;
        gap: 0.85rem;
        position: relative;
        z-index: 1;
        flex-wrap: wrap;
    }}

    .hero-stat-card {{
        min-width: 8rem;
        padding: 0.85rem 1.15rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 0.95rem;
        background: rgba(255, 255, 255, 0.09);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
    }}

    .hero-stat-card strong {{
        display: block;
        font-size: 1.75rem;
        font-weight: 800;
        line-height: 1;
        color: #ffffff !important;
    }}

    .hero-stat-card span {{
        display: block;
        margin-top: 0.35rem;
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 0.76rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Global Stock Listings Radio Button / Pills styling */
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] p,
    [data-testid="stRadio"] span,
    [data-testid="stRadio"] div {{
        color: var(--ui-text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }}

    [data-testid="stRadio"] > div {{
        gap: 0.55rem !important;
        flex-wrap: wrap !important;
    }}

    [data-testid="stRadio"] label[data-baseweb="radio"] {{
        background: var(--ui-surface-card) !important;
        padding: 0.4rem 0.85rem !important;
        border-radius: 0.75rem !important;
        border: 1px solid var(--ui-card-border) !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
    }}

    [data-testid="stRadio"] label[data-baseweb="radio"]:hover {{
        border-color: var(--ui-accent-primary) !important;
        transform: translateY(-1px) !important;
    }}

    /* Workspace Tabs with high contrast active state */
    [data-testid="stTabs"] button {{
        color: var(--ui-text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.96rem !important;
        padding: 0.65rem 1.25rem !important;
        transition: all 0.15s ease !important;
    }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: var(--ui-text-primary) !important;
        font-weight: 800 !important;
        border-bottom: 3px solid var(--ui-accent-primary) !important;
    }}

    /* Section Headings */
    .section-heading {{
        margin: 1.5rem 0 0.85rem;
    }}

    .overview-heading {{
        margin-top: 2.25rem;
    }}

    .section-kicker {{
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--ui-accent-primary) !important;
    }}

    .section-title {{
        margin-top: 0.15rem;
        color: var(--ui-text-primary) !important;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }}

    .section-subtitle {{
        color: var(--ui-text-secondary) !important;
        font-size: 0.92rem;
        font-weight: 500;
    }}

    /* Stock Metric Cards - Sharp & Crisp Typography */
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
        transform: translateY(-3px) !important;
        border-color: var(--ui-card-hover-border) !important;
        box-shadow: var(--ui-card-hover-shadow) !important;
    }}

    div[data-testid="stMetricLabel"] * {{
        color: var(--ui-text-secondary) !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em !important;
    }}

    div[data-testid="stMetricValue"] * {{
        color: var(--ui-text-primary) !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        font-family: 'JetBrains Mono', monospace, sans-serif !important;
    }}

    div[data-testid="stMetricDelta"] * {{
        font-size: 0.88rem !important;
        font-weight: 700 !important;
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
        font-weight: 500 !important;
    }}

    [data-baseweb="select"] *,
    [data-testid="stTextInput"] input::placeholder {{
        color: var(--ui-text-secondary) !important;
    }}

    /* Multiselect tag pills */
    [data-baseweb="tag"] {{
        background: var(--ui-tag-bg) !important;
        color: var(--ui-tag-text) !important;
        border: 1px solid var(--ui-card-border) !important;
        border-radius: 0.5rem !important;
        font-weight: 700 !important;
    }}

    [data-baseweb="tag"] span {{
        color: var(--ui-tag-text) !important;
    }}

    /* Buttons */
    [data-testid="stButton"] button,
    [data-testid="stFormSubmitButton"] button {{
        border-radius: 0.75rem !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        border: 1px solid var(--ui-card-border) !important;
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
        transform: scale(1.08) !important;
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
        font-weight: 650;
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
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--ui-card-border);
    }}

    .context-label {{
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--ui-text-secondary) !important;
    }}

    .context-ticker {{
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        padding: 0.15rem 0.45rem;
        border-radius: 0.4rem;
        background: var(--ui-tag-bg);
        color: var(--ui-tag-text) !important;
        border: 1px solid var(--ui-card-border);
        font-family: 'JetBrains Mono', monospace, sans-serif;
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
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08) !important;
        font-size: 0.92rem !important;
        line-height: 1.55 !important;
    }}

    [data-testid="stChatMessage"] p {{
        color: var(--ui-text-primary) !important;
    }}

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
        font-size: 0.72rem;
        color: var(--ui-text-secondary) !important;
        font-weight: 650;
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
        font-size: 0.92rem !important;
    }}

    .chat-footer-disclaimer {{
        font-size: 0.68rem;
        color: var(--ui-text-secondary) !important;
        text-align: center;
        margin-top: 0.45rem;
        line-height: 1.35;
        font-weight: 500;
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
