# Raw Benchmark Test Results & Empirical Output Logs
**Bad Character Scanner Codebase Inc. (BCSC)**  
*Run Date: November 12, 2026*  
*Evaluated Systems: BCorrect API, LanguageTool API, TextGears API, DeepL Write*

---

## 1. Directory Structure

This directory contains transparent, unedited raw output logs and latency recordings captured directly from live API responses.

| File | Description | Source / Methodology |
| :--- | :--- | :--- |
| **`unseen_10_domains_live_run.json`** | Raw response text and response latencies across 10 unseen writing domains | Direct live REST queries to `api.languagetool.org`, `bcorrect-api.fly.dev`, and RapidAPI TextGears |
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

---

## 3. JSON Schema: `unseen_10_domains_live_run.json`

Each entry corresponds to a test passage ID (`H-01` through `H-10`) containing the empirical outputs for each engine:

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

## 4. How to Re-Run and Regenerate Raw Results

To query live endpoints and regenerate the raw output log:
```bash
# 1. Ensure API keys are set in your local .env (never committed to git)
# BCORRECT_API_KEY=your_key
# TEXTGEARS_API_KEY=your_key

# 2. Run the live unseen test harness
python run_live_unseen_benchmark.py
```
Outputs will be written to `raw_results/unseen_10_domains_live_run.json`.
