#!/usr/bin/env python3
"""Generates assets/*.svg and README.md for the GitHub profile.

Edit CONFIG below, run `python3 build.py`, commit, push.
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

# ───────────────────────── CONFIG ─────────────────────────
USER = "veraetogrex-portfolio"          # GitHub login = repo name
NAME = "Vyacheslav Larionov"
HANDLE = "veraetogrex"
TAGLINE = "AI AUTOMATION · AGENTS · SYSTEMS ANALYSIS"

TITLE = "AI Systems · Automation · Analysis"
SUBTITLE = "SYSTEMS ANALYST · AI ENGINEER"

STACK = [
    ("AI / LLM", ["Claude API", "OpenAI", "Gemini", "Whisper"]),
    ("AGENTS", ["Claude Code", "Codex CLI", "n8n"]),
    ("BACKEND", ["Python", "FastAPI", "TypeScript", "Node.js"]),
    ("DATA", ["PostgreSQL", "Qdrant", "ClickHouse", "Redis"]),
    ("OPS", ["Docker", "Traefik", "MinIO", "Grafana", "Metabase"]),
]

# (label, description, right-hand tag)
WORK = [
    ("BROWSER AGENT", "Claude CLI drives your Chrome via MV3 extension", "TYPESCRIPT"),
    ("MEETING RECORDER", "Meet, Telemost, Discord → diarized transcripts", "SELF-HOSTED"),
    ("LEAD ENRICHMENT", "Apollo → Perplexity → Gemini pipeline", "40 MIN → 2 MIN"),
    ("RAG CHAT AGENT", "Two-level semantic search · Qdrant · Claude", "LIVE CHAT"),
    ("SUPPORT TRIAGE", "Rules + one LLM call + validated JSON", "PYTHON"),
    ("N8N WORKFLOWS", "RAG bot · vision classification state machine", "500+ REQ/DAY"),
    ("NEWS AUTOPOSTER", "YouTube → Whisper → LLM → Telegram channel", "N8N"),
    ("AGENT CONSOLE", "VS Code extension · Claude Code + Codex", "TYPESCRIPT"),
    ("UI COMPONENTS", "10 animated widgets, zero dependencies", "VANILLA JS"),
    ("SUPPORT OPS", "AI rollout, QA, KPI · CSAT 20% → 85%+", "−45% COST/TICKET"),
]

# UI component series (one repo + GitHub Pages demo each). Rendered as real links in README.
SHOWCASE_URL = None  # set to f"https://{USER}.github.io/" once that repo is live
COMPONENTS = [
    ("orbit-otp", "Orbit OTP", "Code digits orbit and screw down into one verified tile"),
    ("stack-seal", "Stack Seal", "Six code cells stack into one seal"),
    ("meniscus-dock", "Meniscus Dock", "The dock melts around the active tab"),
    ("frost-desk", "Frost Desk", "Glass dashboard, every page blurs into the next"),
    ("upgrade-checkout", "Upgrade Checkout", "The card turns around when you need the CVV"),
    ("beacon-login", "Beacon Login", "Pull the cord, the login appears"),
    ("earn-it", "Earn It", "The Ship button runs away until you've earned it"),
    ("vault-meter", "Vault Meter", "Password strength from paperclip to bank vault"),
    ("drop-fill", "Drop & Fill", "Drop a brief, the form fills itself"),
    ("slot-booking", "Slot Booking", "Pick a day, pick a slot, booked"),
]

MODE = "wiring LLMs into real workflows"
TIMEZONE = "ICT · UTC+7"
CONTACT_TEXT = "ALL REPOSITORIES ↗"         # what the card shows
CONTACT_URL = "https://github.com/veraetogrex-portfolio?tab=repositories"  # where the footer click goes

# palettes: README shows the one matching the viewer's GitHub theme
THEMES = {
    "dark": dict(C1="#22D3EE", C2="#6366F1", C3="#C084FC",   # cyan → indigo → violet
                 BG="#0D1117", BORDER="#21262D", TEXT="#E6EDF3", MUTED="#6E7681",
                 SEP="#30363D", GRID="#161B22", GLOW=6),
    "light": dict(C1="#0891B2", C2="#4F46E5", C3="#9333EA",  # same hues, darker for white bg
                  BG="#FFFFFF", BORDER="#D0D7DE", TEXT="#1F2328", MUTED="#656D76",
                  SEP="#D0D7DE", GRID="#EAEEF2", GLOW=2.5),
}
C1 = C2 = C3 = BG = BORDER = TEXT = MUTED = SEP = GRID = GLOW = None  # set by use_theme()


def use_theme(name):
    globals().update(THEMES[name])
# ──────────────────────────────────────────────────────────

SANS = "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
W = 760
OUT = Path(__file__).parent / "assets"


def gradient(gid, vertical=True, animated=True, span=None):
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    units = ""
    if span:  # one gradient across the whole canvas instead of per shape
        x2, y2, units = str(span), "0", ' gradientUnits="userSpaceOnUse"'
    anim = ""
    if animated:
        anim = (
            "<style>"
            f".{gid}0{{animation:{gid}c0 4.2s ease-in-out infinite}}"
            f".{gid}1{{animation:{gid}c1 4.2s ease-in-out infinite}}"
            f".{gid}2{{animation:{gid}c2 4.2s ease-in-out infinite}}"
            f"@keyframes {gid}c0{{0%,100%{{stop-color:{C1}}}50%{{stop-color:{C3}}}}}"
            f"@keyframes {gid}c1{{0%,100%{{stop-color:{C2}}}50%{{stop-color:{C1}}}}}"
            f"@keyframes {gid}c2{{0%,100%{{stop-color:{C3}}}50%{{stop-color:{C2}}}}}"
            f"@media (prefers-reduced-motion:reduce){{.{gid}0,.{gid}1,.{gid}2{{animation:none}}}}"
            "</style>"
        )
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"{units}>'
        f'<stop class="{gid}0" offset="0%" stop-color="{C1}"/>'
        f'<stop class="{gid}1" offset="50%" stop-color="{C2}"/>'
        f'<stop class="{gid}2" offset="100%" stop-color="{C3}"/>'
        f"</linearGradient>{anim}"
    )


def svg(h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
        f'viewBox="0 0 {W} {h}" role="img" aria-label="{escape(label)}">\n{body}\n</svg>\n'
    )


# ── banner: name + animated agent pipeline ──
def banner():
    h = 220
    nodes = [("INPUT", 110), ("RETRIEVE", 245), ("LLM", 380), ("TOOLS", 515), ("OUTPUT", 650)]
    y = 168
    parts = [
        "<defs>",
        gradient("g", vertical=False),
        gradient("v"),
        '<filter id="glow" x="-20%" y="-60%" width="140%" height="220%">'
        f'<feGaussianBlur in="SourceGraphic" stdDeviation="{GLOW}" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        "<style>"
        ".dot{animation:run 3.2s linear infinite}"
        "@keyframes run{0%{transform:translateX(0);opacity:0}6%{opacity:1}94%{opacity:1}100%{transform:translateX(540px);opacity:0}}"
        ".n{animation:lit 3.2s linear infinite}"
        "@keyframes lit{0%,100%{stroke:" + SEP + "}2%,10%{stroke:" + C1 + "}22%{stroke:" + SEP + "}}"
        ".cur{animation:blink 1.1s steps(1,end) infinite}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "@media (prefers-reduced-motion:reduce){.dot,.n,.cur{animation:none}}"
        "</style>",
        "</defs>",
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<rect x="0" y="8" width="3" height="{h-16}" rx="1.5" fill="url(#v)"/>',
        # dotted grid
        f'<g fill="{GRID}">'
        + "".join(f'<circle cx="{x}" cy="{yy}" r="1"/>' for x in range(30, W, 24) for yy in range(18, 132, 24))
        + "</g>",
        f'<text x="380" y="72" text-anchor="middle" font-family="{SANS}" font-size="50" '
        f'font-weight="800" letter-spacing="3" fill="url(#g)" filter="url(#glow)">{escape(HANDLE)}</text>',
        f'<text x="380" y="104" text-anchor="middle" font-family="{MONO}" font-size="11" '
        f'letter-spacing="5" fill="{MUTED}">{escape(TAGLINE)}<tspan class="cur" fill="{C1}"> ▮</tspan></text>',
        f'<path d="M{nodes[0][1]} {y}H{nodes[-1][1]}" stroke="{SEP}" stroke-dasharray="3 5"/>',
    ]
    for i, (label, x) in enumerate(nodes):
        # dot covers 540px in 3.2s → reaches node i at i*0.8s
        delay = -(3.2 - i * 0.8) if i else 0
        parts.append(
            f'<rect class="n" style="animation-delay:{delay:.2f}s" x="{x-52}" y="{y-14}" width="104" '
            f'height="28" rx="14" fill="{BG}" stroke="{SEP}"/>'
            f'<text x="{x}" y="{y+4}" text-anchor="middle" font-family="{MONO}" font-size="10" '
            f'letter-spacing="1.6" fill="{TEXT}">{label}</text>'
        )
    for k, (r, op) in enumerate([(3, 1), (2.2, .5), (1.6, .25)]):
        parts.append(
            f'<circle class="dot" style="animation-delay:{k*0.06:.2f}s" cx="{nodes[0][1]}" cy="{y-21}" '
            f'r="{r}" fill="{C1}" fill-opacity="{op}" filter="url(#glow)"/>'
        )
    return svg(h, "\n".join(parts), f"{HANDLE}: {TAGLINE}")


# ── equalizer ──
def equalizer():
    rnd = random.Random(7)
    css, rects = [], []
    n, step = 47, 16
    for i in range(n):
        d = rnd.uniform(0.85, 1.9)
        dl = -rnd.uniform(0, 2)
        a, b, c, e = (round(rnd.uniform(*r), 2) for r in [(.1, .22), (.75, 1), (.25, .55), (.35, .7)])
        css.append(
            f".b{i}{{animation:k{i} {d:.2f}s {dl:.2f}s infinite cubic-bezier(.4,0,.6,1)}}"
            f"@keyframes k{i}{{0%,100%{{transform:scaleY({a})}}25%{{transform:scaleY({b})}}"
            f"50%{{transform:scaleY({c})}}75%{{transform:scaleY({e})}}}}"
        )
        rects.append(f'<rect class="b b{i}" x="{9 + i*step}" y="10" width="6" height="44" rx="3"/>')
    body = (
        "<defs>" + gradient("eq", vertical=False, span=W) +
        "<style>.b{fill:url(#eq);transform-box:fill-box;transform-origin:bottom}"
        + "".join(css) +
        "@media (prefers-reduced-motion:reduce){.b{animation:none!important;transform:scaleY(.45)}}</style></defs>\n"
        + "\n".join(rects)
    )
    return svg(64, body, "Equalizer")


# ── profile card: stack + selected work ──
def tspan_row(items):
    first, *rest = items
    out = escape(first)
    for it in rest:
        out += f'<tspan fill="{SEP}" dx="12">/</tspan><tspan fill="{TEXT}" dx="12">{escape(it)}</tspan>'
    return out


def profile():
    top = 124
    stack_y0 = top + 34
    row = 30
    stack_end = stack_y0 + (len(STACK) - 1) * row
    div2 = stack_end + 26
    work_head = div2 + 29
    work_y0 = work_head + 34
    wrow = 26
    h = work_y0 + (len(WORK) - 1) * wrow + 24

    p = [
        "<defs>" + gradient("a") + "</defs>",
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<rect x="0" y="8" width="3" height="{h-16}" rx="1.5" fill="url(#a)"/>',
        f'<text x="380" y="46" text-anchor="middle" font-family="{SANS}" font-size="21" font-weight="600" fill="{TEXT}">{escape(TITLE)}</text>',
        f'<text x="380" y="73" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1.8" fill="{C1}">{escape(SUBTITLE)}</text>',
        f'<path d="M34 96.5H726" stroke="{BORDER}"/>',
        f'<text x="34" y="{top}" font-family="{MONO}" font-size="10" letter-spacing="1.6" fill="{MUTED}">STACK</text>',
    ]
    for i, (lab, items) in enumerate(STACK):
        y = stack_y0 + i * row
        p.append(f'<text x="34" y="{y}" font-family="{MONO}" font-size="10.5" letter-spacing="1.2" fill="{MUTED}">{escape(lab)}</text>')
        p.append(f'<text x="176" y="{y+1}" font-family="{SANS}" font-size="15" fill="{TEXT}">{tspan_row(items)}</text>')
    p.append(f'<path d="M34 {div2}.5H726" stroke="{BORDER}"/>')
    p.append(f'<text x="34" y="{work_head}" font-family="{MONO}" font-size="10" letter-spacing="1.6" fill="{MUTED}">SELECTED WORK</text>')
    for i, (lab, desc, tag) in enumerate(WORK):
        y = work_y0 + i * wrow
        p.append(f'<text x="34" y="{y}" font-family="{MONO}" font-size="10.5" letter-spacing="1.2" fill="{MUTED}">{escape(lab)}</text>')
        p.append(f'<text x="176" y="{y+1}" font-family="{SANS}" font-size="14" fill="{TEXT}">{escape(desc)}</text>')
        p.append(f'<text x="726" y="{y}" text-anchor="end" font-family="{MONO}" font-size="9.5" letter-spacing="1.1" fill="{C1}">{escape(tag)}</text>')

    alt = (f"{TITLE}. Stack: " + "; ".join(f"{l}: {', '.join(i)}" for l, i in STACK)
           + ". Selected work: " + "; ".join(f"{l.title()} — {d}" for l, d, _ in WORK) + ".")
    return svg(h, "\n".join(p), alt), alt


# ── footer ──
def footer():
    body = f"""<defs>{gradient("a")}
<style>.cursor{{animation:blink 1.15s steps(1,end) infinite}}@keyframes blink{{0%,46%{{opacity:1}}47%,100%{{opacity:0}}}}@media (prefers-reduced-motion:reduce){{.cursor{{animation:none}}}}</style></defs>
<g>
  <rect x="0.5" y="0.5" width="375" height="75" rx="10" fill="{BG}" stroke="{BORDER}"/>
  <rect x="0" y="8" width="3" height="60" rx="1.5" fill="url(#a)"/>
  <text x="24" y="25" font-family="{MONO}" font-size="9" letter-spacing="1.5" fill="{MUTED}">CURRENT MODE</text>
  <text x="352" y="25" text-anchor="end" font-family="{MONO}" font-size="9" letter-spacing="1.3" fill="{MUTED}">{escape(TIMEZONE)}</text>
  <text x="24" y="53" font-family="{SANS}" font-size="16" fill="{TEXT}">{escape(MODE)}<tspan class="cursor" fill="{C1}"> ▮</tspan></text>
</g>
<g transform="translate(380,0)">
  <rect x="0.5" y="0.5" width="149" height="75" rx="10" fill="{BG}" stroke="{BORDER}"/>
  <text x="18" y="25" font-family="{MONO}" font-size="9" letter-spacing="1.5" fill="{MUTED}">BASED IN</text>
  <text x="18" y="53" font-family="{MONO}" font-size="11" letter-spacing="0.5" fill="{C3}">VIETNAM</text>
</g>
<g transform="translate(534,0)">
  <rect x="0.5" y="0.5" width="225" height="75" rx="10" fill="{BG}" stroke="{BORDER}"/>
  <text x="18" y="25" font-family="{MONO}" font-size="9" letter-spacing="1.5" fill="{MUTED}">PORTFOLIO</text>
  <text x="18" y="53" font-family="{MONO}" font-size="11" letter-spacing="0.4" fill="{C3}">{escape(CONTACT_TEXT)}</text>
</g>"""
    return svg(76, body, f"Current mode: {MODE}. {TIMEZONE}. Contact: {CONTACT_TEXT}")


def pic(name, width, alt):
    raw = f"https://raw.githubusercontent.com/{USER}/{USER}/main/assets"
    return (
        f'<picture>'
        f'<source media="(prefers-color-scheme: light)" srcset="{raw}/{name}-light.svg">'
        f'<img src="{raw}/{name}.svg" width="{width}" alt="{escape(alt)}">'
        f'</picture>'
    )


def components_block():
    cells = []
    for slug, name, line in COMPONENTS:
        demo = f"https://{USER}.github.io/{slug}/"
        code = f"https://github.com/{USER}/{slug}"
        cells.append(
            f'<td width="50%"><a href="{demo}"><b>{escape(name)}</b></a><br>'
            f'<sub>{escape(line)}</sub><br>'
            f'<sub><a href="{demo}">demo</a> · <a href="{code}">code</a></sub></td>'
        )
    rows = "\n".join(
        "  <tr>\n    " + "\n    ".join(cells[i:i + 2]) + "\n  </tr>"
        for i in range(0, len(cells), 2)
    )
    showcase = f'<br>\n  <a href="{SHOWCASE_URL}"><b>All demos on one page ↗</b></a>' if SHOWCASE_URL else ""
    return f"""<h3 align="center">UI components · a new one every day</h3>

<p align="center">
  <sub>Vanilla HTML/CSS/JS, zero dependencies, MIT. Click a name for the live demo.</sub>{showcase}
</p>

<div align="center">
<table>
{rows}
</table>
</div>"""


def readme(alt):
    return f"""<p align="center">
  {pic("banner", 760, f"{HANDLE} — {TAGLINE}")}
</p>

<p align="center">
  {pic("equalizer", 760, "")}
</p>

<p align="center">
  {pic("profile", 760, alt)}<br>
  <a href="{CONTACT_URL}">{pic("footer", 760, f"{MODE} · {TIMEZONE} · {CONTACT_TEXT}")}</a>
</p>

{components_block()}
"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for theme, suffix in [("dark", ""), ("light", "-light")]:
        use_theme(theme)
        (OUT / f"banner{suffix}.svg").write_text(banner())
        (OUT / f"equalizer{suffix}.svg").write_text(equalizer())
        prof, alt = profile()
        (OUT / f"profile{suffix}.svg").write_text(prof)
        (OUT / f"footer{suffix}.svg").write_text(footer())
    (Path(__file__).parent / "README.md").write_text(readme(alt))
    print("ok")
