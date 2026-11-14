# python script to generate clean responsive high contrast grayscale svg charts
# all charts honour a pure monochrome palette with strict 90 degree sharp corners and no rounded boxes
# font sizes are strictly standardized to exactly three sizes: 14px, 11px, and 10px
# benchmark date: november 14, 2026
# dataset: blind unseen suite v3.0
#
# design principles:
# - line graphs preferred for temporal data, horizontal bars for comparisons
# - wide spacious layouts that zoom cleanly with github native svg viewbox scaling
# - no boxes-in-boxes or grouped bar clusters that squish on small screens
# - generous whitespace, clear labels, readable at any zoom level

import os

os.makedirs("assets", exist_ok=True)

# typography scale enforced across all charts:
# - 14px: primary chart titles and primary score callouts
# - 11px: subtitles, engine names, category labels, callout badges, and legend text
# - 10px: axis ticks, latency subtext, milestone descriptions, and footnotes

# monochrome palette (github dark theme compatible):
# #0d1117 - background
# #161b22 - card/legend background
# #21262d - subtle grid
# #30363d - primary grid, borders
# #6e7681 - muted text, DeepL line
# #8b949e - secondary text, TextGears line
# #c9d1d9 - primary text, LanguageTool line
# #f0f6fc - bright text
# #ffffff - emphasis, BCorrect line


def build_hybrid_chart_svg():
    """chart 1: horizontal bar chart comparing overall hybrid meta-scores.
    wide layout, one bar per engine, easy to read at any zoom."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" style="background:#0d1117; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <rect x="1" y="1" width="1198" height="418" fill="none" stroke="#30363d" stroke-width="1"/>

  <text x="600" y="34" fill="#f0f6fc" font-size="14" font-weight="700" text-anchor="middle">OVERALL HYBRID META-SCORE (4-PILLAR EVALUATION)</text>
  <text x="600" y="54" fill="#8b949e" font-size="11" text-anchor="middle">H-01 to H-10 | 35% Spelling, 25% Grammar, 20% Voice, 20% Anti-Hallucination | November 14, 2026</text>

  <!-- vertical gridlines at 0%, 25%, 50%, 75%, 100% -->
  <line x1="280" y1="68" x2="280" y2="318" stroke="#30363d" stroke-width="1"/>
  <line x1="490" y1="68" x2="490" y2="318" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="700" y1="68" x2="700" y2="318" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="910" y1="68" x2="910" y2="318" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="1120" y1="68" x2="1120" y2="318" stroke="#30363d" stroke-width="1"/>

  <!-- x-axis tick labels -->
  <text x="280" y="340" fill="#8b949e" font-size="10" text-anchor="middle">0%</text>
  <text x="490" y="340" fill="#8b949e" font-size="10" text-anchor="middle">25%</text>
  <text x="700" y="340" fill="#8b949e" font-size="10" text-anchor="middle">50%</text>
  <text x="910" y="340" fill="#8b949e" font-size="10" text-anchor="middle">75%</text>
  <text x="1120" y="340" fill="#8b949e" font-size="10" text-anchor="middle">100%</text>

  <!-- bars are sorted by the 4-pillar hybrid meta-score -->
  <text x="270" y="88" fill="#f0f6fc" font-size="11" font-weight="700" text-anchor="end">Sapling (web demo)</text>
  <rect x="280" y="72" width="798" height="24" fill="#c9d1d9" stroke="#f0f6fc" stroke-width="1.5"/>
  <text x="1088" y="89" fill="#f0f6fc" font-size="11" font-weight="700">95.0%</text>

  <text x="270" y="128" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">DeepL Write</text>
  <rect x="280" y="112" width="732" height="24" fill="#30363d" stroke="#6e7681" stroke-width="1"/>
  <text x="1022" y="129" fill="#c9d1d9" font-size="11" font-weight="600">87.1%</text>

  <text x="270" y="168" fill="#ffffff" font-size="11" font-weight="700" text-anchor="end">BCorrect (FMM)</text>
  <rect x="280" y="152" width="693" height="24" fill="#e6edf3" stroke="#ffffff" stroke-width="1.5"/>
  <text x="983" y="169" fill="#ffffff" font-size="11" font-weight="700">82.5%</text>

  <text x="270" y="208" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">LanguageTool API</text>
  <rect x="280" y="192" width="676" height="24" fill="#8b949e" stroke="#c9d1d9" stroke-width="1"/>
  <text x="966" y="209" fill="#c9d1d9" font-size="11" font-weight="600">80.5%</text>

  <text x="270" y="248" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">TextGears API</text>
  <rect x="280" y="232" width="676" height="24" fill="#6e7681" stroke="#8b949e" stroke-width="1"/>
  <text x="966" y="249" fill="#c9d1d9" font-size="11" font-weight="600">80.5%</text>

  <text x="270" y="288" fill="#a3a3a3" font-size="11" font-weight="600" text-anchor="end">JSpell (web checker)</text>
  <rect x="280" y="272" width="564" height="24" fill="#21262d" stroke="#a3a3a3" stroke-width="1"/>
  <text x="854" y="289" fill="#a3a3a3" font-size="11" font-weight="600">67.2%</text>

  <!-- footer -->
  <text x="600" y="390" fill="#8b949e" font-size="10" text-anchor="middle">Sapling and JSpell used initial web-demo suggestions once; latency not measured. Same 10-domain scoring protocol | November 14, 2026</text>
</svg>"""
    with open("assets/hybrid_score_comparison.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated assets/hybrid_score_comparison.svg")


def build_pillars_breakdown_svg():
    """chart 2: 4-pillar breakdown as a multi-line dot chart.
    one line per engine across the 4 pillars on the x-axis, scores on the y-axis.
    spacious layout, no cramped grouped bars, easy to read at any zoom."""
    # pillar positions on x-axis (evenly spaced across wide chart)
    # p1 spelling: x=240, p2 grammar: x=480, p3 voice: x=720, p4 anti-hal: x=960
    # y-axis: 0% at y=400, 100% at y=100 -> scale = 3.0 px per %

    def y(pct):
        return 400 - pct * 3.0

    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" style="background:#0d1117; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <rect x="1" y="1" width="1198" height="518" fill="none" stroke="#30363d" stroke-width="1"/>

  <text x="600" y="34" fill="#f0f6fc" font-size="14" font-weight="700" text-anchor="middle">THE 4 EVALUATION PILLARS: ENGINE BREAKDOWN</text>
  <text x="600" y="54" fill="#8b949e" font-size="11" text-anchor="middle">H-01 to H-10 | Spelling, Grammar, Voice, and Anti-Hallucination | November 14, 2026</text>

  <!-- y-axis gridlines and labels -->
  <line x1="140" y1="400" x2="1060" y2="400" stroke="#30363d" stroke-width="1"/>
  <line x1="140" y1="325" x2="1060" y2="325" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="250" x2="1060" y2="250" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="175" x2="1060" y2="175" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="100" x2="1060" y2="100" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>

  <text x="130" y="404" fill="#8b949e" font-size="10" text-anchor="end">0%</text>
  <text x="130" y="329" fill="#8b949e" font-size="10" text-anchor="end">25%</text>
  <text x="130" y="254" fill="#8b949e" font-size="10" text-anchor="end">50%</text>
  <text x="130" y="179" fill="#8b949e" font-size="10" text-anchor="end">75%</text>
  <text x="130" y="104" fill="#8b949e" font-size="10" text-anchor="end">100%</text>

  <!-- pillar labels on x-axis -->
  <text x="240" y="425" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="middle">P1: Spelling</text>
  <text x="240" y="440" fill="#8b949e" font-size="10" text-anchor="middle">(35% weight)</text>
  <text x="480" y="425" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="middle">P2: Grammar</text>
  <text x="480" y="440" fill="#8b949e" font-size="10" text-anchor="middle">(25% weight)</text>
  <text x="720" y="425" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="middle">P3: Voice</text>
  <text x="720" y="440" fill="#8b949e" font-size="10" text-anchor="middle">(20% weight)</text>
  <text x="960" y="425" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="middle">P4: Anti-Halluc.</text>
  <text x="960" y="440" fill="#8b949e" font-size="10" text-anchor="middle">(20% weight)</text>

  <!-- vertical pillar guidelines -->
  <line x1="240" y1="90" x2="240" y2="400" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="480" y1="90" x2="480" y2="400" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="720" y1="90" x2="720" y2="400" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="960" y1="90" x2="960" y2="400" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>"""

    # engine data: [spelling, grammar, voice, anti_hal]
    engines = {
        "DeepL Write":      [94.7, 72.5, 81.8, 97.5],
        "LanguageTool API": [81.2, 77.5, 93.5, 70.0],
        "TextGears API":    [82.7, 71.7, 91.0, 77.5],
        "BCorrect (FMM)":   [84.8, 63.3, 97.5, 87.5],
        "Sapling (web demo)": [94.2, 100.0, 95.0, 90.0],
        "JSpell (web checker)": [76.8, 40.8, 95.5, 55.0],
    }

    # line styles per engine
    styles = {
        "DeepL Write":      {"stroke": "#6e7681", "dash": "3,3",     "fill": "#30363d", "text": "#6e7681", "w": "2"},
        "LanguageTool API": {"stroke": "#c9d1d9", "dash": "6,4",     "fill": "#0d1117", "text": "#c9d1d9", "w": "2"},
        "TextGears API":    {"stroke": "#8b949e", "dash": "4,2,1,2", "fill": "#8b949e", "text": "#8b949e", "w": "2"},
        "BCorrect (FMM)":   {"stroke": "#ffffff", "dash": "",        "fill": "#ffffff", "text": "#ffffff", "w": "3"},
        "Sapling (web demo)": {"stroke": "#f0f6fc", "dash": "2,3",    "fill": "#c9d1d9", "text": "#f0f6fc", "w": "2"},
        "JSpell (web checker)": {"stroke": "#a3a3a3", "dash": "1,3", "fill": "#0d1117", "text": "#a3a3a3", "w": "2"},
    }

    pillar_x = [240, 480, 720, 960]
    label_offsets = {
        "DeepL Write": [(0, -12), (0, -24), (0, -12), (0, -12)],
        "LanguageTool API": [(0, -12), (30, 14), (0, -12), (-15, -12)],
        "TextGears API": [(0, -12), (-30, 14), (-15, -12), (0, -12)],
        "BCorrect (FMM)": [(0, -12), (0, -12), (15, -12), (15, -12)],
        "Sapling (web demo)": [(20, 16), (0, 28), (0, -12), (0, -12)],
        "JSpell (web checker)": [(0, 14), (0, 14), (0, 28), (0, -12)],
    }

    for name, scores in engines.items():
        s = styles[name]
        points = " ".join(f"{pillar_x[i]},{y(scores[i]):.0f}" for i in range(4))
        dash_attr = f' stroke-dasharray="{s["dash"]}"' if s["dash"] else ""
        svg += f'\n\n  <!-- {name} line -->'
        svg += f'\n  <polyline points="{points}" fill="none" stroke="{s["stroke"]}" stroke-width="{s["w"]}"{dash_attr}/>'

        # dot markers at each pillar
        for i in range(4):
            cx, cy_val = pillar_x[i], y(scores[i])
            svg += f'\n  <rect x="{cx-5}" y="{cy_val-5}" width="10" height="10" fill="{s["fill"]}" stroke="{s["stroke"]}" stroke-width="1.5"/>'
            dx, dy = label_offsets[name][i]
            svg += f'\n  <text x="{cx+dx}" y="{cy_val+dy}" fill="{s["text"]}" font-size="10" font-weight="600" text-anchor="middle">{scores[i]:.0f}%</text>'

    # legend
    svg += """

  <!-- legend -->
  <rect x="40" y="465" width="1120" height="34" fill="#161b22" stroke="#30363d" stroke-width="1"/>

  <line x1="100" y1="482" x2="125" y2="482" stroke="#6e7681" stroke-width="2" stroke-dasharray="3,3"/>
  <rect x="109" y="478" width="8" height="8" fill="#30363d" stroke="#6e7681" stroke-width="1"/>
  <text x="135" y="486" fill="#6e7681" font-size="11">DeepL Write</text>

  <line x1="265" y1="482" x2="290" y2="482" stroke="#8b949e" stroke-width="2" stroke-dasharray="4,2,1,2"/>
  <rect x="274" y="478" width="8" height="8" fill="#8b949e"/>
  <text x="300" y="486" fill="#8b949e" font-size="11">TextGears API</text>

  <line x1="430" y1="482" x2="455" y2="482" stroke="#c9d1d9" stroke-width="2" stroke-dasharray="6,4"/>
  <rect x="439" y="478" width="8" height="8" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5"/>
  <text x="465" y="486" fill="#c9d1d9" font-size="11">LanguageTool API</text>

  <line x1="635" y1="482" x2="660" y2="482" stroke="#ffffff" stroke-width="3"/>
  <rect x="644" y="478" width="8" height="8" fill="#ffffff"/>
  <text x="670" y="486" fill="#ffffff" font-size="11" font-weight="700">BCorrect (FMM)</text>

  <line x1="820" y1="482" x2="845" y2="482" stroke="#f0f6fc" stroke-width="2" stroke-dasharray="2,3"/>
  <rect x="829" y="478" width="8" height="8" fill="#c9d1d9" stroke="#f0f6fc"/>
  <text x="855" y="486" fill="#f0f6fc" font-size="11">Sapling (web demo)</text>

  <line x1="1000" y1="482" x2="1025" y2="482" stroke="#a3a3a3" stroke-width="2" stroke-dasharray="1,3"/>
  <rect x="1009" y="478" width="8" height="8" fill="#0d1117" stroke="#a3a3a3"/>
  <text x="1035" y="486" fill="#a3a3a3" font-size="11">JSpell (web checker)</text>
</svg>"""

    with open("assets/pillars_breakdown.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated assets/pillars_breakdown.svg")


def build_latency_chart_svg():
    """chart 3: horizontal bar chart for latency comparison. wide and spacious."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" style="background:#0d1117; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <rect x="1" y="1" width="1198" height="358" fill="none" stroke="#30363d" stroke-width="1"/>

  <text x="600" y="34" fill="#f0f6fc" font-size="14" font-weight="700" text-anchor="middle">AVERAGE QUERY INFERENCE LATENCY (LOWER IS BETTER)</text>
  <text x="600" y="54" fill="#8b949e" font-size="11" text-anchor="middle">Measured runs only; Sapling and JSpell web-demo latency was not collected | November 14, 2026</text>

  <!-- 1. BCorrect (FMM): 18ms -> width = 18/1300 * 750 = 10px (min 14px for visibility) -->
  <text x="270" y="105" fill="#ffffff" font-size="11" font-weight="700" text-anchor="end">BCorrect (1 vCPU Local)</text>
  <rect x="280" y="88" width="14" height="26" fill="#e6edf3" stroke="#ffffff" stroke-width="1.5"/>
  <text x="304" y="105" fill="#ffffff" font-size="11" font-weight="700">~18 ms</text>
  <text x="370" y="105" fill="#8b949e" font-size="10">(Sub-Keystroke Baseline, 1.0x)</text>

  <!-- 2. LanguageTool API: 677ms -> width = 677/1300 * 750 = 391px -->
  <text x="270" y="155" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">LanguageTool API</text>
  <rect x="280" y="138" width="391" height="26" fill="#8b949e" stroke="#c9d1d9" stroke-width="1"/>
  <text x="681" y="155" fill="#c9d1d9" font-size="11" font-weight="600">~677 ms</text>
  <text x="745" y="155" fill="#8b949e" font-size="10">(37x slower)</text>

  <!-- 3. TextGears API: 967ms -> width = 967/1300 * 750 = 558px -->
  <text x="270" y="205" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">TextGears API</text>
  <rect x="280" y="188" width="558" height="26" fill="#6e7681" stroke="#8b949e" stroke-width="1"/>
  <text x="848" y="205" fill="#c9d1d9" font-size="11" font-weight="600">~967 ms</text>
  <text x="915" y="205" fill="#8b949e" font-size="10">(53x slower)</text>

  <!-- 4. DeepL Write: 1,280ms -> width = 1280/1300 * 750 = 738px -->
  <text x="270" y="255" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="end">DeepL Write</text>
  <rect x="280" y="238" width="738" height="26" fill="#30363d" stroke="#6e7681" stroke-width="1"/>
  <text x="1028" y="255" fill="#8b949e" font-size="11" font-weight="600">~1,280 ms</text>

  <text x="270" y="305" fill="#f0f6fc" font-size="11" font-weight="600" text-anchor="end">Sapling (web demo)</text>
  <text x="280" y="305" fill="#8b949e" font-size="11">Not measured - excluded from speed ranking</text>

  <!-- bottom scale line -->
  <line x1="280" y1="325" x2="1030" y2="325" stroke="#30363d" stroke-width="1"/>
  <text x="280" y="344" fill="#8b949e" font-size="10" text-anchor="middle">0 ms</text>
  <text x="568" y="344" fill="#8b949e" font-size="10" text-anchor="middle">500 ms</text>
  <text x="856" y="344" fill="#8b949e" font-size="10" text-anchor="middle">1000 ms</text>
  <text x="1030" y="344" fill="#8b949e" font-size="10" text-anchor="middle">1300 ms</text>
</svg>"""
    with open("assets/latency_comparison.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated assets/latency_comparison.svg")


def build_progress_chart_svg():
    """chart 4: multi-line chart showing historical progress over time.
    wide spacious layout with clear milestone markers.
    this is the primary temporal visualization."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 560" style="background:#0d1117; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <rect x="1" y="1" width="1398" height="558" fill="none" stroke="#30363d" stroke-width="1"/>

  <text x="700" y="34" fill="#f0f6fc" font-size="14" font-weight="700" text-anchor="middle">VOICE-PRESERVING AI-SPELLCHECK PROGRESS OVER TIME (2025 - 2026)</text>
  <text x="700" y="54" fill="#8b949e" font-size="11" text-anchor="middle">Historical Hybrid Meta-Score Progression Across Engineering Milestones | November 13, 2026</text>

  <!-- y-axis gridlines: 0% at y=430, 100% at y=90 -> range = 340px, scale = 3.4 px per % -->
  <line x1="140" y1="430" x2="1100" y2="430" stroke="#30363d" stroke-width="1.5"/>
  <line x1="140" y1="362" x2="1100" y2="362" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="294" x2="1100" y2="294" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="226" x2="1100" y2="226" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="158" x2="1100" y2="158" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="140" y1="90" x2="1100" y2="90" stroke="#21262d" stroke-width="1" stroke-dasharray="2,2"/>

  <text x="130" y="434" fill="#8b949e" font-size="10" font-weight="600" text-anchor="end">0%</text>
  <text x="130" y="366" fill="#8b949e" font-size="10" font-weight="600" text-anchor="end">20%</text>
  <text x="130" y="298" fill="#8b949e" font-size="10" font-weight="600" text-anchor="end">40%</text>
  <text x="130" y="230" fill="#8b949e" font-size="10" font-weight="600" text-anchor="end">60%</text>
  <text x="130" y="162" fill="#8b949e" font-size="10" font-weight="600" text-anchor="end">80%</text>
  <text x="130" y="96" fill="#8b949e" font-size="10" font-weight="600" text-anchor="end">100%</text>

  <!-- vertical milestone guidelines -->
  <line x1="260" y1="80" x2="260" y2="430" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="540" y1="80" x2="540" y2="430" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="820" y1="80" x2="820" y2="430" stroke="#21262d" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="1060" y1="80" x2="1060" y2="430" stroke="#30363d" stroke-width="1.5"/>

  <!-- milestone labels on x-axis -->
  <text x="260" y="452" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="middle">Q1 2025 (v1.0)</text>
  <text x="260" y="467" fill="#8b949e" font-size="10" text-anchor="middle">Initial Baseline</text>

  <text x="540" y="452" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="middle">Q3 2025 (v1.8)</text>
  <text x="540" y="467" fill="#8b949e" font-size="10" text-anchor="middle">Consonant Skeleton</text>

  <text x="820" y="452" fill="#c9d1d9" font-size="11" font-weight="600" text-anchor="middle">Early Fall 2026</text>
  <text x="820" y="467" fill="#8b949e" font-size="10" text-anchor="middle">30-50% Blind Test</text>

  <text x="1060" y="452" fill="#ffffff" font-size="11" font-weight="700" text-anchor="middle">Nov 2026 (v3.0)</text>
  <text x="1060" y="467" fill="#c9d1d9" font-size="10" font-weight="600" text-anchor="middle">4-Pillar Blind Suite</text>

  <!-- y-value helper: y = 430 - (pct * 3.4) -->

  <!-- 1. DeepL Write (dashed gray) -->
  <!-- 78% -> y=165, 80% -> y=158, 81.5% -> y=153, 85.1% -> y=141 -->
  <polyline points="260,165 540,158 820,153 1060,141" fill="none" stroke="#6e7681" stroke-width="2" stroke-dasharray="3,3"/>
  <rect x="255" y="160" width="10" height="10" fill="#30363d" stroke="#6e7681" stroke-width="1.5"/>
  <rect x="535" y="153" width="10" height="10" fill="#30363d" stroke="#6e7681" stroke-width="1.5"/>
  <rect x="815" y="148" width="10" height="10" fill="#30363d" stroke="#6e7681" stroke-width="1.5"/>
  <rect x="1055" y="136" width="10" height="10" fill="#30363d" stroke="#6e7681" stroke-width="1.5"/>

  <!-- 2. TextGears API (dash-dot gray) -->
  <!-- 64% -> y=212, 67.5% -> y=201, 70.5% -> y=190, 72% -> y=185 -->
  <polyline points="260,212 540,201 820,190 1060,187" fill="none" stroke="#8b949e" stroke-width="2" stroke-dasharray="4,2,1,2"/>
  <rect x="255" y="207" width="10" height="10" fill="#8b949e"/>
  <rect x="535" y="196" width="10" height="10" fill="#8b949e"/>
  <rect x="815" y="185" width="10" height="10" fill="#8b949e"/>
  <rect x="1055" y="182" width="10" height="10" fill="#8b949e"/>

  <!-- 3. LanguageTool API (dashed light gray) -->
  <!-- 65% -> y=209, 68% -> y=199, 70.2% -> y=191, 71.4% -> y=187 -->
  <polyline points="260,209 540,199 820,191 1060,187" fill="none" stroke="#c9d1d9" stroke-width="2" stroke-dasharray="6,4"/>
  <rect x="255" y="204" width="10" height="10" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5"/>
  <rect x="535" y="194" width="10" height="10" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5"/>
  <rect x="815" y="186" width="10" height="10" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5"/>
  <rect x="1055" y="182" width="10" height="10" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5"/>

  <!-- 4. BCorrect (solid white, bold trajectory) -->
  <!-- 32% -> y=321, 38.5% -> y=299, 38% -> y=301, 60.4% -> y=225 -->
  <polyline points="260,321 540,299 820,301 1060,225" fill="none" stroke="#ffffff" stroke-width="3"/>
  <rect x="254" y="315" width="12" height="12" fill="#ffffff" stroke="#0d1117" stroke-width="1"/>
  <text x="260" y="340" fill="#ffffff" font-size="10" font-weight="700" text-anchor="middle">32.0%</text>

  <rect x="534" y="293" width="12" height="12" fill="#ffffff" stroke="#0d1117" stroke-width="1"/>
  <text x="540" y="318" fill="#ffffff" font-size="10" font-weight="700" text-anchor="middle">38.5%</text>

  <rect x="814" y="295" width="12" height="12" fill="#ffffff" stroke="#0d1117" stroke-width="1"/>
  <text x="820" y="320" fill="#ffffff" font-size="10" font-weight="700" text-anchor="middle">38.0%</text>

  <rect x="1054" y="219" width="12" height="12" fill="#ffffff" stroke="#0d1117" stroke-width="1"/>

  <!-- right-margin callout badges -->
  <line x1="1060" y1="141" x2="1120" y2="129" stroke="#6e7681" stroke-width="1" stroke-dasharray="2,2"/>
  <rect x="1120" y="115" width="250" height="28" fill="#161b22" stroke="#6e7681" stroke-width="1"/>
  <text x="1132" y="134" fill="#c9d1d9" font-size="11" font-weight="600">DeepL Write: 85.1%</text>

  <line x1="1060" y1="187" x2="1120" y2="165" stroke="#8b949e" stroke-width="1" stroke-dasharray="2,2"/>
  <rect x="1120" y="155" width="250" height="28" fill="#161b22" stroke="#8b949e" stroke-width="1"/>
  <text x="1132" y="174" fill="#8b949e" font-size="11" font-weight="600">TextGears API: 71.5%</text>

  <line x1="1060" y1="187" x2="1120" y2="205" stroke="#c9d1d9" stroke-width="1" stroke-dasharray="2,2"/>
  <rect x="1120" y="195" width="250" height="28" fill="#161b22" stroke="#c9d1d9" stroke-width="1"/>
  <text x="1132" y="214" fill="#c9d1d9" font-size="11" font-weight="600">LanguageTool: 71.4%</text>

  <line x1="1060" y1="225" x2="1120" y2="245" stroke="#ffffff" stroke-width="1.5"/>
  <rect x="1120" y="235" width="250" height="28" fill="#21262d" stroke="#ffffff" stroke-width="1.5"/>
  <text x="1132" y="254" fill="#ffffff" font-size="11" font-weight="700">BCorrect (FMM): 60.4%</text>

  <!-- legend -->
  <rect x="140" y="490" width="960" height="34" fill="#161b22" stroke="#30363d" stroke-width="1"/>

  <line x1="160" y1="507" x2="190" y2="507" stroke="#6e7681" stroke-width="2" stroke-dasharray="3,3"/>
  <rect x="176" y="503" width="8" height="8" fill="#30363d" stroke="#6e7681"/>
  <text x="200" y="511" fill="#6e7681" font-size="11">DeepL Write</text>

  <line x1="380" y1="507" x2="410" y2="507" stroke="#8b949e" stroke-width="2" stroke-dasharray="4,2,1,2"/>
  <rect x="391" y="503" width="8" height="8" fill="#8b949e"/>
  <text x="420" y="511" fill="#8b949e" font-size="11">TextGears API</text>

  <line x1="600" y1="507" x2="630" y2="507" stroke="#c9d1d9" stroke-width="2" stroke-dasharray="6,4"/>
  <rect x="611" y="503" width="8" height="8" fill="#0d1117" stroke="#c9d1d9" stroke-width="1.5"/>
  <text x="640" y="511" fill="#c9d1d9" font-size="11" font-weight="600">LanguageTool API</text>

  <line x1="830" y1="507" x2="860" y2="507" stroke="#ffffff" stroke-width="3"/>
  <rect x="841" y="503" width="8" height="8" fill="#ffffff"/>
  <text x="870" y="511" fill="#ffffff" font-size="11" font-weight="700">BCorrect API (FMM)</text>
</svg>"""
    with open("assets/progress_over_time.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated assets/progress_over_time.svg")


if __name__ == "__main__":
    build_hybrid_chart_svg()
    build_pillars_breakdown_svg()
    build_latency_chart_svg()
    build_progress_chart_svg()
