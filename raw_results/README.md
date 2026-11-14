# Raw Benchmark Test Results & Empirical Output Logs
**Bad Character Scanner Codebase Inc. (BCSC)**  
*Last Updated: November 14, 2026*
*Evaluated Systems: BCorrect API, LanguageTool API, TextGears API, DeepL Write, Sapling web demo, JSpell web checker*

---

**JSpell status:** Scores and one-pass outputs from JSpell's free web checker are included. They are not results from the Cloud API or RapidAPI endpoint; that separate API route returned HTTP 403 during collection.

## 1. Directory Structure

This directory contains raw benchmark outputs and latency recordings where they were collected. Sapling and JSpell are full participants in both sub-benchmarks, with manually collected one-pass web-demo outputs rather than API calls. Their latency is unavailable (`n/a`; JSON `null`), not assumed or estimated.

| File | Description | Source / Methodology |
| :--- | :--- | :--- |
| **`unseen_10_domains_live_run.json`** | Raw response text and response latencies across 10 unseen writing domains | Direct live REST queries to `api.languagetool.org`, `bcorrect-api.fly.dev`, and RapidAPI TextGears |
| **`blind_v3_sapling_outputs.json`** | Sapling's B-suite output text and initial suggestion record | Interactive free web demo; apply initial suggestions once at original offsets; no recheck; latency not measured |
| **`jspell_web_checker_outputs.json`** | JSpell H- and B-suite output text, source hashes, and initial suggestion record | Interactive free web checker; first displayed suggestion applied once; no recheck; latency not measured |
| **`jspell_control_outputs.json`** *(not collected)* | Optional JSpell Cloud API/RapidAPI collector output | `python run_jspell_control.py`; requires `JSPELL_RAPIDAPI_KEY` and the private B-suite cache; API returned HTTP 403 during this collection |
| **`norvig_birkbeck_30_pairs.json`** | Orthographic spelling recovery on 30 standard human misspellings | Evaluated against Norvig and Birkbeck spelling corpora |

---

## 2. API Endpoints & How Systems Were Queried

### 1. LanguageTool API (Free Open-Source REST Endpoint)
- **Endpoint:** `https://api.languagetool.org/v2/check`
- **Method:** `POST`
- **Payload:** `{"text": "<input_string>", "language": "en-US"}`
- **Authentication:** None (LanguageTool provides a public, zero-cost REST endpoint with IP-based rate limiting of 20-30 requests/min).
- **Correction Application:** Matches are sorted in reverse offset order and the top replacement suggestion (`replacements[0].value`) is spliced directly into the text.

### 2. BCorrect API (Fly.dev Production Instance)
- **Endpoint:** `https://bcorrect-api.fly.dev/api/v1/check`
- **Method:** `POST`
- **Headers:** `{"Content-Type": "application/json", "X-API-Key": "<BCORRECT_API_KEY>"}`
- **Payload:** `{"text": "<input_string>"}`
- **Authentication:** Direct API key supplied via `.env` (`BCORRECT_API_KEY`).

### 3. TextGears API (RapidAPI Developer Gateway)
- **Endpoint:** `https://textgears-textgears-v1.p.rapidapi.com/spelling`
- **Method:** `POST`
- **Headers:** `{"Content-Type": "application/x-www-form-urlencoded", "X-RapidAPI-Key": "<TEXTGEARS_API_KEY>"}`
- **Payload:** `{"text": "<input_string>", "language": "en-US"}`
- **Authentication:** Commercial RapidAPI key supplied via `.env` (`TEXTGEARS_API_KEY`).

### 4. DeepL Write (Neural Rewriter Baseline)
- **Endpoint:** Web / REST Interface
- **Method:** Evaluated across identical input strings in November 2026.

### 5. Sapling Grammar Checker (Interactive Web Demo)
- **URL:** `https://sapling.ai/grammar-check`
- **Method:** Initial visible suggestions were applied once at their original offsets. The checker was not rerun after applying edits, so edits did not trigger a second suggestion pass.
- **Latency:** Not measured; the result is recorded as `null` (`n/a` in reports) and excluded from speed comparisons.
- **Scope:** This is a manually exercised web-demo result, not a production API evaluation.
- **Privacy:** Input text was submitted to a third-party service; check Sapling's privacy policy before submitting non-public text.
- **Text encoding:** The H-06 contraction apostrophe is normalized to ASCII in the saved output.

### 6. JSpell Free Web Checker
- **URL:** `https://www.jspell.com/checker/`
- **Method:** Interactive English (US) checker; this is not the Cloud API or RapidAPI service.
- **Correction application:** For each visible spelling error, apply the first displayed suggestion once in the same session, without rechecking. The saved record retains corrected text, ordered initial suggestions, and SHA-256 fingerprints of source inputs.
- **Scope:** Dictionary spelling only; it does not check grammar or rewrite text. Because the selected benchmark composite includes all four pillars, missed grammar targets are scored as misses.
- **Latency:** Not measured; the result is recorded as `null` (`n/a` in reports) and excluded from speed comparisons.
- **Privacy and source data:** JSpell states that submitted text is checked and discarded. The Blind v3 input passages are omitted from the public result file; only their fingerprints and outputs are included.

The separate Cloud API collector is retained for a future attempt, but its HTTP 403 responses mean no API output or score is included here.

---

## 3. Scoring Method

The evaluation passages and expected corrections are fixed, curated data; no essays are generated or randomized during evaluation. Each engine receives the same passage text. H-suite inputs and annotations are public; B-suite source passages are private locally, but much of the scoring logic is public, so neither should be described as an adversarially secure hidden test set. Outputs are checked against annotated spelling and grammar targets, accepted voice/dialect variants, over-edit phrases, and known hallucination signatures. Target checks are case-insensitive whole-phrase matches with word boundaries, but do not verify the exact edit location. These rules are deterministic heuristics; hallucination signatures are manually specified and are not a general semantic-drift detector.

The local evaluator reads the saved outputs and annotations and calculates the published scores without contacting the engines. The Blind v3 source passages remain in a private local cache and are not included in this public repository.

---

## 4. JSON Schema: `unseen_10_domains_live_run.json`

Each entry corresponds to a test passage ID (`H-01` through `H-10`) containing the recorded outputs for each engine. API latency fields are available where measured. Sapling and JSpell web-demo entries have no latency measurements; their initial suggestion records are stored in separate files:

```json
{
  "H-01": {
    "BCorrect (FMM)": {
      "text": "Yo that concert was strait fire no cap, but my friend lost his ticket at the entrance...",
      "lat": 2007.5
    },
    "LanguageTool API": {
      "text": "Yo that concert was straight fire no cap, but my friend lost his ticket at the entrance...",
      "lat": 611.8
    },
    "TextGears API": {
      "text": "Yo that concert was straight fire no cap, but my friend lost his ticket at the entrance...",
      "lat": 952.3
    }
  }
}
```

---

## 5. Reproducing the Scored Results

The evaluation scripts score the checked-in cached outputs without querying external services:
```bash
python benchmark_4pillars_hybrid.py
python evaluate_blind_v3.py --mode cached
```

The original API calls and web-demo interaction are not replayed by those commands. Any new live collection should be recorded separately, with credentials kept out of the repository and web-demo latency left unavailable unless actually measured.
