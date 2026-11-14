# Reproduction & Verification Guide: 4-Pillar Open Benchmark
**Voice-Preserving AI-Spellcheck Benchmark**  
*Evaluation Date: November 14, 2026 | Suite Version: 3.0-blind*

This guide explains how to reproduce the benchmark results, run the 4-pillar evaluation suite, regenerate the SVG charts, and verify raw results locally.

---

## 1. Prerequisites & Environment Setup

The benchmark is designed to run in standard Python 3.9+ without heavyweight deep learning dependencies.

### Step 1: Clone the Repository
```bash
git clone https://github.com/IBIYP/voice-preserving-ai-spellcheck-benchmark.git
cd voice-preserving-ai-spellcheck-benchmark
```

### Step 2: Initialize Virtual Environment
```bash
python -m venv .venv

# On Linux / macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

---

## 2. Benchmark Execution

### [Primary Test] Run the 4-Pillar Open Benchmark Suite
Evaluates cached outputs across the 4 functional pillars (Spelling, Grammar, Writer's Voice, and Anti-Hallucination), plus the 5th Hybrid Meta-Score.

**Execution Command:**
```bash
python benchmark_4pillars_hybrid.py
```

**What this script does:**
1. Loads the 10 blind unseen domain evaluation units across distinct human writing styles (Urban Slang, Southern Gothic, Cyberpunk Noir, Food Critique, Severe Dysgraphia, SaaS Pitch, Sports Locker Room, Poetic Melancholy, Field Biology, and Legal Shorthand).
2. Calculates independent, decoupled metrics:
   - **Pillar 1: Spelling Accuracy (35% weight)**
   - **Pillar 2: Grammar & Syntactic Accuracy (25% weight)**
   - **Pillar 3: Maintaining Writer's Voice (20% weight)** - decoupled from spelling, with multi-reference dialect tolerance (`rockin` = `rocking`).
   - **Pillar 4: Avoiding Hallucinations (20% weight)** - directly penalizes rogue substitutions and invented dictionary words.
   - **Pillar 5: Hybrid Final Meta-Score (100% composite)**.
3. Reports latency only where a value was measured or recorded. Sapling and JSpell were tested through interactive web demos, not APIs, and have no latency measurements.
4. Outputs a formatted ASCII leaderboard to the console.
5. Saves verified evaluation artifacts directly to `raw_results/blind_4pillars_eval_run.json`.

---

## 3. Regenerating Visual Charts

To regenerate all monochrome 90-degree SVG charts:
```bash
python generate_charts.py
```

**Generated Visual Assets in `assets/`:**
- `assets/hybrid_score_comparison.svg`: Sharp bar chart comparing Hybrid Meta-Scores.
- `assets/pillars_breakdown.svg`: Grouped breakdown across Pillars 1, 2, 3, and 4.
- `assets/latency_comparison.svg`: Measured latency comparison; Sapling and JSpell are shown as not measured and are excluded from speed rankings.
- `assets/progress_over_time.svg`: Multi-milestone progress line graph from Q1 2025 to November 2026.

---

## 4. Codebase Hygiene & Character Audit

To verify that all files in the repository contain 0 non-ASCII characters or malformed tokens:
```bash
python bad_character_scanner.py
```

---

## 5. Metric Formulas & Scoring Architecture

$$\text{Pillar 1 (Spelling)} = \frac{\text{Corrected Spelling Targets}}{\text{Total Spelling Targets}} \times 100\%$$

$$\text{Pillar 2 (Grammar)} = \frac{\text{Corrected Grammar Targets}}{\text{Total Grammar Targets}} \times 100\%$$

$$\text{Pillar 3 (Voice)} = \text{VPR} \times \left(1 - \frac{\text{OER}}{100}\right)$$

$$\text{Pillar 4 (Anti-Hallucination)} = 100\% - \text{Semantic Drift Rate (SDR)}$$

$$\text{Pillar 5 (Hybrid Meta-Score)} = \left(0.35 \times \text{Spelling}\right) + \left(0.25 \times \text{Grammar}\right) + \left(0.20 \times \text{Voice}\right) + \left(0.20 \times \text{Anti-Hallucination}\right)$$

---

## 6. Verifying Local Output Against Published Numbers

When you run `python benchmark_4pillars_hybrid.py`, confirm that the terminal output matches the published leaderboard:
- **Pillar 1 (Spelling Leader):** ★ DeepL Write (94.7%)
- **Pillar 2 (Grammar Leader):** ★ Sapling Grammar Checker (100.0%; web demo)
- **Pillar 3 (Voice Leader):** ★ BCorrect (FMM) (97.5%)
- **Pillar 4 (Anti-Hallucination Leader):** ★ DeepL Write (97.5%)
- **Pillar 5 (Hybrid Meta-Leader):** ★ Sapling Grammar Checker (95.0%; web demo)
- **Latency Leader:** ★ BCorrect (FMM) (~18 ms)

Sapling and JSpell web-demo scores use a one-pass policy: apply each initial visible suggestion once, without running the checker again. The evaluators consume saved outputs; they do not query either service. These results are directional and should not be presented as API or latency comparisons. Both are third-party services; check their privacy policies before submitting non-public text. JSpell is a spelling-only checker, but its result is scored across all four selected pillars, so its missed grammar targets remain part of the composite.

### JSpell Web-Checker Results
The published JSpell results were collected from the [free JSpell checker](https://www.jspell.com/checker/) using its interactive English (US) interface. They are **not** from the JSpell Cloud API or RapidAPI endpoint. For each flagged word, the first displayed suggestion was applied once in the same checker session; no second check was run. Web-demo latency was not measured.

The saved record is [raw_results/jspell_web_checker_outputs.json](raw_results/jspell_web_checker_outputs.json). It contains outputs, applied initial suggestions, and source-input SHA-256 fingerprints. The private Blind v3 source passages are not included. The separate `run_jspell_control.py` collector targets the Cloud API and requires a local `JSPELL_RAPIDAPI_KEY`; that API route returned HTTP 403 during collection and did not produce the published web-checker results.

---

## 7. Raw Artifact References
- [raw_results/README.md](raw_results/README.md): Methodology and schema documentation.
- [raw_results/blind_4pillars_eval_run.json](raw_results/blind_4pillars_eval_run.json): Structured per-passage output and metrics.
- [raw_results/unseen_10_domains_live_run.json](raw_results/unseen_10_domains_live_run.json): Raw outputs and measured latencies where available.
- [raw_results/blind_v3_sapling_outputs.json](raw_results/blind_v3_sapling_outputs.json): Sapling B-suite web-demo outputs and one-pass suggestion record.
- [raw_results/jspell_web_checker_outputs.json](raw_results/jspell_web_checker_outputs.json): JSpell H- and B-suite web-checker outputs and one-pass suggestion record.
