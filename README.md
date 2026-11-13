# Voice-Preserving AI-Spellcheck Benchmark
**An Open Benchmark for AI Spelling, Grammar, and Keeping the Writer's Voice**  
*Maintained by the Open Voice-Preserving Benchmark Working Group*  
*Evaluation Date: November 13, 2026 | Dataset Version: Blind Unseen Suite v3.0*

[![License: MIT (Benchmark Code Only)](https://img.shields.io/badge/License-MIT%20(Benchmark%20Only)-blue.svg)](LICENSE)
[![Benchmark Date: November 13, 2026](https://img.shields.io/badge/Benchmark%20Date-November%2013%2C%202026-blue.svg)]()
[![Hardware: CPU-Only Baseline](https://img.shields.io/badge/Hardware-1%20vCPU-orange.svg)]()
[![Evaluated Dataset: Unseen Blind Suite v3.0](https://img.shields.io/badge/Dataset-Unseen%20Blind%20Suite%20v3.0-blue.svg)]()
[![Roadmap: v3.0 to v4.0](https://img.shields.io/badge/Roadmap-v3.0%20to%20v4.0-brightgreen.svg)](ROADMAP.md)
[![Reproducibility: 1--Command Offline](https://img.shields.io/badge/Reproducibility-1--Command%20Offline-success.svg)]()

---

> **Benchmark Mission & Transparency Statement:**  
> The **Voice-Preserving AI-Spellcheck Benchmark** is an **open, independent testing suite** measuring how effectively spelling and grammar tools fix real mistakes without destroying the writer's authentic voice, slang, or tone. Rather than serving as marketing collateral for a single vendor, our mission is to provide an honest, open standard that participating engine creators (BCorrect, LanguageTool, TextGears, DeepL Write, Sapling, and independent researchers) can verify, test, and build upon. All tools are tested on identical blind unseen inputs under uniform conditions.

---

## Quick Start: Replaying the Cached v3 Evaluation

The v3 evaluator replays cached engine outputs offline and does not make API calls or require API keys. It requires the local run log at `Docs/Notes/blind_v3_live_runs_full.json`. That file is excluded from this public repository, so a clean clone cannot run these commands without a separately supplied copy of the run log.

```bash
# Instant evaluation across all 4 production engines:
python evaluate_blind_v3.py

# Include academic NLP diagnostic metrics (SARI-Keep n=1..3, Protected Spans, Over-Editing):
python evaluate_blind_v3.py --academic

# Detailed per-passage diagnostic breakdown:
python evaluate_blind_v3.py -v
```

> **Technical Specification & Roadmap:** See [ROADMAP.md](ROADMAP.md) for our formal SARI-Keep mathematical foundation, planned open-source LLM baselines (Llama-3, Mistral), and upcoming 500-sentence statistical suite.

---

## Executive Summary: The 4 Core Evaluation Pillars & Hybrid Meta-Score
*Latest Benchmark Run: November 13, 2026*

To evaluate developer APIs scientifically and consistently, this benchmark measures performance across **4 core functional pillars**, synthesized into **1 unified Hybrid Meta-Score**:

```
+-----------------------------------------------------------------------------+
|               THE 4 EVALUATION PILLARS + HYBRID META-SCORE                  |
+-----------------------------------------------------------------------------+
| 1. SPELLING ACCURACY                                                        |
|    Orthography, severe dysgraphia, phonetic slips, homophones, and typos.   |
+-----------------------------------------------------------------------------+
| 2. GRAMMAR & SYNTACTIC ACCURACY                                             |
|    Subject-verb agreement, tense harmony, punctuation, and mechanics.       |
+-----------------------------------------------------------------------------+
| 3. MAINTAINING WRITER'S VOICE                                               |
|    Preserving authentic slang, dialect tolerance, and anti-over-editing.     |
+-----------------------------------------------------------------------------+
| 4. AVOIDING HALLUCINATIONS                                                  |
|    Zero semantic drift, zero rogue dictionary substitutions on uncommon terms|
+=============================================================================+
| 5. HYBRID FINAL SCORE (META-STUDY COMPOSITE)                                |
|    A balanced scientific synthesis evaluating real-world engine utility.    |
+-----------------------------------------------------------------------------+
```

### Why Existing APIs Diverge
When developers integrate spelling and grammar engines into word processors, code editors, form inputs, or chat systems, they need an engine that balances mechanical correction against voice preservation:
- **Dictionary Hallucinations (Failing Pillar 4):** Classical rule and n-gram APIs (such as **TextGears API** and **LanguageTool API**) frequently substitute completely wrong dictionary words when presented with high-entropy phonetic or dysgraphic input (for example, mutating *"aposematik"* into *"postmark"*, *"crik"* into *"Erik"*, *"purpul"* into *"pupil"*, or *"skool"* into *"stool"*).
- **Over-Editing & Voice Erasure (Failing Pillar 3):** Neural writing rewriters (such as **DeepL Write**) aggressively rephrase informal idioms, expand natural contractions, and convert casual or dialectal speech into standardized corporate textbook prose.
- **Syntactic Agreement Deficits (Failing Pillar 2):** Word-level geometric engines (such as **BCorrect FMM**) achieve top-tier spelling recovery on severe dysgraphia, but struggle with sequence-level subject-verb agreements without a language model layer.

![Overall 4-Pillar Hybrid Benchmark Score](assets/hybrid_score_comparison.svg?v=3.1)

### 4-Pillar Engine Breakdown
![4-Pillar Engine Breakdown](assets/pillars_breakdown.svg?v=3.1)

### Historical Accuracy & Progression Over Time
A key measure of engine reliability is consistent improvement across revisions on unseen evaluations. The line graph below illustrates the historical progression of overall hybrid score across benchmark milestones from early 2025 to November 2026.

![Historical Progress Over Time](assets/progress_over_time.svg?v=3.1)

---

## 1. Scientific Evaluation Methodology: The 4 Pillars & Hybrid Meta-Score

Performance is calculated across four explicit pillars, synthesized into a final composite meta-score:

$$\text{Pillar 1 (Spelling)} = \frac{\text{Corrected Spelling Targets}}{\text{Total Spelling Targets}} \times 100\%$$

$$\text{Pillar 2 (Grammar)} = \frac{\text{Corrected Grammar Targets}}{\text{Total Grammar Targets}} \times 100\%$$

$$\text{Pillar 3 (Voice)} = \text{VPR} \times \left(1 - \frac{\text{OER}}{100}\right)$$

$$\text{Pillar 4 (Anti-Hallucination)} = 100\% - \text{Semantic Drift Rate (SDR)}$$

$$\text{Pillar 5 (Hybrid Meta-Score)} = \left(0.35 \times \text{Spelling}\right) + \left(0.25 \times \text{Grammar}\right) + \left(0.20 \times \text{Voice}\right) + \left(0.20 \times \text{Anti-Hallucination}\right)$$

Where:
- **Pillar 1 (Spelling Accuracy, 35%):** Percentage of orthographic, phonetic, and dysgraphic errors resolved to their intended target.
- **Pillar 2 (Grammar Accuracy, 25%):** Percentage of syntactic, agreement, inflectional, and punctuation errors resolved.
- **Pillar 3 (Maintaining Voice, 20%):** Evaluated via Voice Preservation Rate (VPR) with multi-reference dialect tolerance (accepting regional variants such as `rockin` / `rocking` without penalty), penalized by Over-Editing Rate (OER). Decoupled from spelling slips.
- **Pillar 4 (Avoiding Hallucinations, 20%):** Evaluated via confirmed rogue dictionary substitutions, detecting whenever an engine substitutes an unintended dictionary word that distorts sentence meaning.
- **Pillar 5 (Hybrid Meta-Score, 100%):** A balanced composite index reflecting overall developer utility in production.

---

## 2. Benchmark Scorecards & Visual Charts

### A. Live Production API Benchmark (10 Unseen Human Writing Domains)
*Benchmark Run Date: November 13, 2026*  
Evaluated across 10 brand-new, unseen writing styles: Urban Slang, Southern Gothic, Cyberpunk Noir, Culinary Critique, Severe Dysgraphia, SaaS Pitch, Sports Banter, Poetic Melancholy, Field Biology, and Legal Contract Shorthand.

| Engine / Model | Spelling (35%) | Grammar (25%) | Voice (20%) | Anti-Halluc. (20%) | Meta-Score | Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **DeepL Write** *(Rewriter)* | **★ 98.0%** | **★ 100.0%** | 17.1% | **★ 100.0%** | **★ 82.7%** | ~1,280 ms |
| **TextGears API** | 71.4% | **★ 100.0%** | **★ 90.2%** | 20.0% | 72.0% | ~967 ms |
| **LanguageTool API** | 73.5% | **★ 100.0%** | 68.3% | 35.0% | 71.4% | ~677 ms |
| **BCorrect (FMM Engine)** | 69.4% | 50.0% | **★ 90.2%** | 35.0% | 61.8% | **★ ~18 ms local** |

> **Software Architecture Distinction:**
> - **In-Place Developer APIs (BCorrect, LanguageTool, TextGears):** Designed for keystroke-level text entry, code comments, and chat. They surgically fix orthography without rewriting the author's tone, vocabulary, or cadence.
> - **Neural Text Rewriters (DeepL Write):** Designed for full-document paraphrasing. They deliver near-perfect mechanical spelling (98.0%) and grammar (100.0%), but heavily erase authorial voice (17.1% Voice Score) by converting informal idioms and dialect into standardised prose.

---

### B. Subcategory Performance Analysis & Class Winners
*Benchmark Run Date: November 13, 2026*  
*(Black stars ★ indicate category-winning benchmark performance)*

| Evaluation Category | In-Place API Winner | Score | Generative / Neural Winner | Technical Rationale |
| :--- | :--- | :---: | :--- | :--- |
| **Pillar 1: Spelling Accuracy** | **★ LanguageTool API** | **73.5%** | DeepL Write (98.0%) | DeepL Write delivers near-perfect orthographic tokens; LanguageTool leads developer APIs on standard lexicon words. |
| **Pillar 2: Grammar & Agreement** | **★ TextGears / LanguageTool**| **100.0%** | DeepL Write (100.0%) | Rule engines resolve basic syntax errors (*to dark* -> *too dark*); BCorrect focuses on word-level correction without language modeling. |
| **Pillar 3: Maintaining Voice** | **★ BCorrect & TextGears** | **90.2%** | None (Rewriters fail: 17.1%)| BCorrect preserves authentic slang (*clutch was so cracked fr*), regional cadence, and developer shorthand without tone flattening. DeepL converts informal speech to corporate prose. |
| **Pillar 4: Anti-Hallucination** | **★ BCorrect / LanguageTool** | **35.0%** | DeepL Write (100.0%) | Traditional developer APIs suffer from rogue dictionary distractors (*yirgacheffe* -> *yorkshire* / *giraffe*, *humerous* -> *numerous*); DeepL maintains contextual consistency. |
| **Pillar 5: Hybrid Meta-Score** | **★ TextGears API** | **72.0%** | DeepL Write (82.7%) | DeepL leads overall composite due to high mechanical accuracy; TextGears and LanguageTool lead dedicated developer APIs. |
| **Keystroke Latency & Speed** | **★ BCorrect (FMM)** | **~18 ms** | DeepL Write (~1,280 ms) | Runs locally on a single CPU thread in sub-20ms - **37x faster than LanguageTool and 53x faster than TextGears**. Ideal for real-time keystroke typing. |

![Average Query Inference Latency Comparison](assets/latency_comparison.svg?v=3.1)

---

## 3. Qualitative Case Studies: Dedicated APIs Under Stress

### Case Study A: Casual Dialogue & Slang (Anti-Paraphrase Evaluation)
> **Author Input:** *"Honestly, I'm just gonna chill here tonite, grab sum pizza, and vibe out with the music. No way I'm goin to that party."*  
> **Intended Corrections:** *tonite* -> *tonight*, *sum* -> *some*, *goin* -> *going*.

| Engine | Resulting Output Text | Voice Preserved? | Qualitative Assessment |
| :--- | :--- | :---: | :--- |
| **BCorrect (FMM)** | *"Honestly, I'm just gonna chill here **tonight**, grab **some** pizza, and vibe out with the music. No way I'm **going** to that party."* | **Yes (100%)** | **Surgical correction.** Resolves errors; leaves *"gonna chill"*, *"vibe out"*, and conversational rhythm intact. |
| **LanguageTool API** | *"Honestly, I'm just gonna chill here **tonight**, grab **some** pizza, and vibe out with the music. No way I'm **going** to that party."* | **Yes (100%)** | Conservative rule check; preserves tone without over-editing. |
| **TextGears API** | *"Honestly, I'm just gonna chill here **tonight**, grab **some** pizza, and vibe out with the music. No way I'm goin to that party."* | **Partial** | Corrected early tokens; missed final colloquial participle *goin*. |
| **DeepL Write** | *"Honestly, I'm just **going to relax** here tonight, **get** some pizza, and **enjoy the music**. **I'm definitely not going** to that party."* | **No (0%)** | **Tone flattening.** Rewrites clauses into standardised textbook sentence structures. |

---

### Case Study B: Regional Vernacular & Cadence (Dialect Preservation Evaluation)
> **Author Input:** *"Granddaddy sat on the porch rockin slow, watchin the crik rise after the floodin. He reckned the old barn wouldnt survive another downpoar."*  
> **Intended Corrections:** *rockin* -> *rocking*, *watchin* -> *watching*, *crik* -> *creek*, *floodin* -> *flooding*, *reckned* -> *reckoned*, *wouldnt* -> *wouldn't*, *downpoar* -> *downpour*.

| Engine | Resulting Output Text | Voice Preserved? | Qualitative Assessment |
| :--- | :--- | :---: | :--- |
| **BCorrect (FMM)** | *"Granddaddy sat on the porch rockin slow, watch in the cri rise after the flooding. He reckoned the old barn wouldn't survive another downpour."* | **Moderate** | Preserved cadence and regional terms; struggled with multi-token phonetic cluster *crik rise*. |
| **TextGears API** | *"Granddaddy sat on the porch rocking slow, watchin the crick rise after the flooding. He reckoned the old barn wouldn't survive another downpour."* | **Moderate** | Retained colloquial flavor, substituted regional variant *crick*. |
| **LanguageTool API** | *"Granddaddy sat on the porch rocking slow, watching the Erik rise after the flooding. He reckoned the old barn wouldn't survive another downpour."* | **Low** | Mutated *crik* into personal name *Erik*. |
| **DeepL Write** | *"My grandfather sat on the porch, rocking slowly, watching the creek rise after the flood. He reckoned the old barn would not survive another heavy rainstorm."* | **Low** | Substitutes formal terminology (*My grandfather*, *heavy rainstorm*) and standardises phrasing. |

---

### Case Study C: Technical Developer Notes & CLI Shorthand (Developer Voice Evaluation)
> **Author Input:** *"Ran npm install, spund up the docker container, and verifeid port 8080 was listenin. Everything lookd solid."*  
> **Intended Corrections:** *spund* -> *spun*, *verifeid* -> *verified*, *listenin* -> *listening*, *lookd* -> *looked*.

| Engine | Resulting Output Text | Voice Preserved? | Qualitative Assessment |
| :--- | :--- | :---: | :--- |
| **BCorrect (FMM)** | *"Ran npm install, **spun** up the docker container, and **verified** port 8080 was **listening**. Everything **looked** solid."* | **Yes (100%)** | **Technical shorthand preserved.** Corrects spelling; retains concise dev log format. |
| **TextGears API** | *"Ran npm install, **spun** up the docker container, and **verified** port 8080 was **listening**. Everything **looked** solid."* | **Yes (100%)** | Accurately resolved past-tense technical verbs. |
| **LanguageTool API** | *"Ran npm install, **spun** up the docker container, and **verified** port 8080 was **listening**. Everything **looked** solid."* | **Yes (100%)** | Handled technical log accurately. |
| **DeepL Write** | *"I ran npm install, launched the docker container, and verified that port 8080 was listening. Everything seemed solid."* | **Moderate** | Injected first-person pronoun *"I"* and replaced developer jargon *"spun up"* with *"launched"*. |

---

## 4. Academic GEC Context: CoNLL-2014 & BEA-2019

To maintain complete academic transparency, BCorrect was also evaluated against traditional grammatical error correction corpora:

| Dataset | Standard Metric | BCorrect Score | Baseline Systems (T5 / GECToR) | Why the Gap Exists |
| :--- | :---: | :---: | :---: | :--- |
| **CoNLL-2014** | $F_{0.5}$ (m2scorer) | **9.34%** | 65.0% to 72.0% | CoNLL annotations reward full sentence restructuring and preposition swaps to formal ESL textbook standards. BCorrect deliberately leaves valid non-standard syntax untouched. |
| **BEA-2019 Dev** | $F_{0.5}$ (ERRANT) | **14.2%** | 68.0% to 75.0% | Traditional GEC rewards high edit density. A non-invasive model that fixes only clear typos will mechanically score low on reference edit overlap. |

BCorrect adheres to the **Minimal Intervention Principle**:
- Mechanically resolves orthography, phonetics, and syntax without imposing stylistic templates.
- Maintains sub-20ms deterministic execution on standard single-core CPU hardware.

---

## 5. Methodology, Protocol & Limitations

### Evaluation Protocol
1. **Blind Unseen Corpus:** The test set consists of 10 passages spanning distinct stylistic domains (slang, regional dialect, poetry, technical notes, legal text, severe dysgraphia). No system was tuned or calibrated on these passages.
2. **Standardised Error Tagging:** Each passage defines explicit spelling targets, grammar targets, stylistic voice markers, and forbidden rewrites.
3. **Execution Environment:**
   - Dedicated APIs (BCorrect, TextGears, LanguageTool) were queried via HTTP REST endpoints.
   - Latencies represent end-to-end response times averaged over multiple runs.

### Known Limitations
- **Sample Size:** The blind suite currently contains 10 comprehensive passages (approx. 400 words total across domains). While representative of diverse registers, larger-scale corpora are continually being added.
- **Latency Variance:** Cloud REST API latency depends on geographic network routing, whereas BCorrect numbers represent local execution on a single vCPU.

---

## 6. Local Reproduction & Verification

The evaluation suite is open-source and reproducible. For comprehensive instructions, environment setup, and troubleshooting, see the [Independent Reproduction Guide](REPRODUCTION_GUIDE.md).

### 1. Installation
```bash
git clone https://github.com/IBIYP/voice-preserving-ai-spellcheck-benchmark.git
cd voice-preserving-ai-spellcheck-benchmark
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install requests
```

### 2. Configure API Keys (Optional for Live Cloud API Testing)
Create a `.env` file in the project root:
```env
BCORRECT_API_KEY=your_bcorrect_key_here
TEXTGEARS_API_KEY=your_textgears_rapidapi_key_here
```

### 3. Execution Commands

```bash
# Run the official Blind Unseen Suite v3.0 evaluation (Offline, Zero-Config)
python evaluate_blind_v3.py

# Include formal NLP metrics (SARI-Keep, Protected Spans, Over-Editing)
python evaluate_blind_v3.py --academic

# Run the 4-Pillar Open Benchmark Suite
python benchmark_4pillars_hybrid.py

# Regenerate all monochrome 90-degree SVG charts
python generate_charts.py

# Run codebase character hygiene scanner (verifies 0 non-ASCII anomalies)
python bad_character_scanner.py
```

---

## 7. Documentation & Raw Results Repository

### Raw Test Results & Data Logs (`raw_results/`)
- **Raw Test Logs & Methodology Guide:** [raw_results/README.md](raw_results/README.md)
- **Live 4-Pillar Evaluation Log (JSON):** [raw_results/blind_4pillars_eval_run.json](raw_results/blind_4pillars_eval_run.json)
- **Live Unseen 10-Domain API Responses & Latencies (JSON):** [raw_results/unseen_10_domains_live_run.json](raw_results/unseen_10_domains_live_run.json)
- **Norvig & Birkbeck 30 Human Spelling Pairs (JSON):** [raw_results/norvig_birkbeck_30_pairs.json](raw_results/norvig_birkbeck_30_pairs.json)

### Scorecards & Independent Reproduction
- **Step-by-Step Reproduction Guide:** [REPRODUCTION_GUIDE.md](REPRODUCTION_GUIDE.md)
- **Engine Submission Protocol & Legal Waiver:** [SUBMISSIONS.md](SUBMISSIONS.md)

---

## 8. Submitting an Engine for Official Benchmark Inclusion

We welcome independent researchers, open-source maintainers, and commercial API creators to submit their spelling, grammar, or writing assistance systems for official benchmark evaluation:
- **Submission Protocol & Legal Waiver:** Review [SUBMISSIONS.md](SUBMISSIONS.md) for full eligibility criteria and binding legal disclaimers.
- **Engine Submission Form:** Open a submission request using the [New Engine Submission Template](https://github.com/IBIYP/voice-preserving-ai-spellcheck-benchmark/issues/new?template=engine_submission.md).
- **Safe Credential Handshake:** All test API keys must enforce a mandatory **$1.00 USD hard spending cap**. Maintainers bear zero financial liability, and submitters assume full responsibility for credential safety and revocation.
- **Verified Community Registry:** All official evaluation outputs are archived transparently in [raw_results/submissions/](raw_results/submissions/).

---

## 9. Legal Notices & Fair Use Attribution

> **Scope of MIT License & Proprietary Technology Notice:**  
> The MIT License provided in this repository applies strictly and exclusively to the open benchmark scripts, evaluation test harnesses, scoring functions, and documentation. Nothing herein grants, conveys, or implies any license or rights to the proprietary architectures, models, or APIs of any evaluated engines (including DeepL Write, LanguageTool, TextGears, or BCorrect), all of which remain the exclusive intellectual property of their respective creators and organizations.
> 
> **Nominative Fair Use & Non-Affiliation:**  
> TextGears is a registered trademark of TextGears Ltd. LanguageTool is a registered trademark of LanguageTooler GmbH. Grammarly is a registered trademark of Grammarly, Inc. DeepL is a registered trademark of DeepL SE. Google Docs is a trademark of Google LLC. ProWritingAid is a trademark of Orpheus Technology Ltd. BCorrect is a proprietary technology of its respective owners.  
> 
> The Open Voice-Preserving Benchmark Working Group is an independent research collective. This benchmark repository is not affiliated with, sponsored by, or endorsed by any evaluated commercial entity or API provider. All third-party product names and trademarks are used strictly for comparative identification and scientific benchmarking under **Nominative Fair Use** (15 U.S.C. Section 1125(c)(3)).
