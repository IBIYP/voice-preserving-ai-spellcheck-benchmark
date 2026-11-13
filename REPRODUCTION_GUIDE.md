# Reproduction & Verification Guide: 4-Pillar Open Benchmark
**Voice-Preserving AI-Spellcheck Benchmark**  
*Evaluation Date: November 13, 2026 | Suite Version: 3.0-blind*

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
Evaluates developer engines across the 4 functional pillars (Spelling, Grammar, Writer's Voice, and Anti-Hallucination), plus the 5th Hybrid Meta-Score.

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
3. Measures average query latency per engine.
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
- `assets/latency_comparison.svg`: Query latency comparison (~18 ms vs ~520 ms vs ~1050 ms vs ~1280 ms).
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
- **Pillar 1 (Spelling Leader):** ★ BCorrect (FMM) (84.8%)
- **Pillar 2 (Grammar Leader):** ★ LanguageTool API (77.5%)
- **Pillar 3 (Voice Leader):** ★ BCorrect (FMM) (97.5%)
- **Pillar 4 (Anti-Hallucination Leader):** ★ DeepL Write (100.0%)
- **Pillar 5 (Hybrid Meta-Leader):** ★ BCorrect (FMM) (82.5%)
- **Latency Leader:** ★ BCorrect (FMM) (~18 ms)

---

## 7. Raw Artifact References
- [raw_results/README.md](raw_results/README.md): Methodology and schema documentation.
- [raw_results/blind_4pillars_eval_run.json](raw_results/blind_4pillars_eval_run.json): Structured per-passage output and metrics.
- [raw_results/unseen_10_domains_live_run.json](raw_results/unseen_10_domains_live_run.json): Verbatim raw outputs from live engine executions.
