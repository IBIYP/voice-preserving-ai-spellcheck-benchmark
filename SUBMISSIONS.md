# Engine Submission Protocol & Legal Liability Waiver
**Voice-Preserving AI-Spellcheck Benchmark - Open Working Group**  
*Effective Date: November 13, 2026 | Protocol Version: 1.0*

This document defines the submission protocol, evaluation criteria, credential safety requirements, and binding legal terms for engine creators, API providers, and independent researchers who wish to evaluate their spelling, grammar, or writing assistance systems on the Voice-Preserving AI-Spellcheck Benchmark.

---

## 1. Submission Eligibility & Requirements

Any software system, developer API, commercial REST service, or open-source library that provides spelling correction, grammar checking, or text editing may be submitted for official benchmark inclusion.

### Eligible Architectures:
- **Dedicated Developer Spelling & Grammar APIs** (e.g., LanguageTool, TextGears, BCorrect, Sapling).
- **Rule-Based & Statistical N-Gram Engines** (e.g., Hunspell, SymSpell, LanguageTool Core).
- **Neural Text Rewriters & Large Language Models** (e.g., DeepL Write, GPT-based writing assistants, Claude, Grammarly).
- **Offline / Local SDKs & Libraries** (must be runnable in a standard Linux/macOS/Windows x86_64 or ARM64 container).

---

## 2. The 4-Pillar Evaluation Protocol

Every submitted engine is evaluated under identical blind conditions across **4 decoupled functional pillars**, synthesized into the official **Hybrid Meta-Score**:

```
+-----------------------------------------------------------------------------+
|        VOICE-PRESERVING AI-SPELLCHECK BENCHMARK: 4-PILLAR META-INDEX        |
+-----------------------------------------------------------------------------+
| 1. Spelling Accuracy (35%)       - Orthography, severe dysgraphia, typos    |
| 2. Grammar & Syntax (25%)        - Agreement, tense harmony, punctuation    |
| 3. Writer's Voice (20%)          - Slang, regional dialect, zero rewriting  |
| 4. Anti-Hallucination (20%)      - Zero rogue substitutions on valid words  |
+=============================================================================+
| 5. Composite Meta-Score (100%)   - Balanced real-world utility index        |
+-----------------------------------------------------------------------------+
```

### Benchmark SLAs & Technical Constraints:
- **Maximum Request Timeout:** 5,000 milliseconds (5.0 seconds). Requests exceeding 5.0 seconds receive an automatic failure score for that query.
- **Query Corpus Size:** The complete unseen test run consists of 10 to 50 curated human writing passages (fewer than 2,500 total words per run). Total compute expenditure per engine is typically under $0.02 USD.
- **Decoupled Scoring:** Stylistic choices and regional dialects (e.g., `rockin` / `rocking`, `flavour` / `flavor`) are supported via multi-reference equivalences so non-standard vernacular is never penalized as a grammatical error.
- **Academic Metrics (v3.1+):** Submitted engines are also scored on **SARI-Keep (n=1..3)** and **Protected-Span Retention Rate (PSRR)** to quantify minimal-edit precision against destructive rewrites. Full specifications are in [ROADMAP.md](ROADMAP.md).

---

## 3. Safe API Key Handshake Rules (Zero Financial Risk)

To prevent financial exposure, billing overages, and security vulnerabilities, submitters must strictly adhere to the following four rules:

### Rule 1: Mandatory Spend Cap ($1.00 USD Maximum)
- The submitting party **MUST** generate a dedicated, isolated API key restricted to a hard spend limit of **$1.00 USD** (or a strict rate limit of 1,000 total requests).
- **NEVER submit an unrestricted production key.** If your API platform does not support hard spending limits, do not provide an API key; instead, coordinate with benchmark maintainers to arrange an IP-whitelisted test endpoint.

### Rule 2: Ephemeral Lifecycle & Immediate Revocation
- Test keys are used solely for the duration of the automated benchmark run (typically under 60 seconds).
- The submitting party is instructed and expected to **immediately revoke, deactivate, or delete the test API key** once raw output artifacts are delivered or upon PR publication.

### Rule 3: Single-Endpoint Read-Only Permissions
- Keys must have the absolute minimum permission scope required to call the text-checking endpoint (e.g., `check` or `correction` only).
- Keys with administrative, account management, billing, or organization-level permissions will be immediately rejected without execution.

### Rule 4: Zero Public Key Transmission
- **DO NOT post API keys in public GitHub issues, pull requests, comments, or repository files.**
- Keys must only be transmitted via encrypted one-time secrets or private maintainer channels communicated upon issue registration.

---

## 4. Comprehensive Legal Terms & Limitation of Liability

> **IMPORTANT LEGAL NOTICE: READ CAREFULLY BEFORE SUBMITTING.**  
> By submitting an API, credential, endpoint, software package, or pull request to this repository, the Submitting Party expressly agrees to be bound by the terms, disclaimers, and liability limitations set forth below.

### 4.1 Complete Disclaimer of Financial and Operational Liability
1. **Zero Financial Responsibility:** The AuthorVoice Benchmark Working Group, its individual maintainers, contributors, and affiliated corporate entities (collectively, "Benchmark Maintainers") shall have **NO LIABILITY WHATSOEVER** for any costs, charges, fees, overages, billing disputes, or invoices incurred on the Submitting Party's API account, hosting infrastructure, cloud provider, or network carrier.
2. **Third-Party Key Leakage & Interception:** Benchmark Maintainers exercise standard industry precautions regarding credential handling; however, Benchmark Maintainers do not warrant, guarantee, or insure against security breaches, network interception, unauthorized third-party access, or accidental leakage. The Submitting Party assumes sole and exclusive responsibility for credential security.

### 4.2 Submitting Party Assumption of Sole Liability & Risk
1. **Sole Responsibility for Spend Protections:** The Submitting Party bears sole and exclusive responsibility for enforcing spending limits, hard billing caps, IP whitelisting, and quota restrictions on any provided credentials. If the Submitting Party fails to implement a $1.00 spend cap, or provides an unmetered or unrestricted credential, the Submitting Party expressly assumes all resulting financial consequences, liabilities, and damages.
2. **Duty to Revoke:** The Submitting Party agrees to revoke the test credential immediately following the completion of the benchmark execution. Benchmark Maintainers have no duty or obligation to remind or enforce key revocation.

### 4.3 Indemnification and Hold Harmless
The Submitting Party agrees to defend, indemnify, and hold harmless Benchmark Maintainers, their officers, contributors, and agents from and against any and all claims, liabilities, losses, damages, costs, or expenses (including reasonable attorney fees) arising out of or related to:
- Any credential submitted by or on behalf of the Submitting Party.
- Any billing disputes, excessive charges, or provider claims associated with the submitted credentials.
- Any alleged infringement, data privacy violation, or terms of service violation resulting from evaluating the submitted endpoint.

### 4.4 Public Disclosure & Open Data Authorization
1. **Verbatim Output Publication:** The Submitting Party acknowledges and explicitly authorizes Benchmark Maintainers to publish all raw text outputs, scores, response timings, error logs, and comparative charts generated during the benchmark evaluation under the open-source MIT License in the `raw_results/` directory.
2. **No Right of Retraction for Accurate Benchmark Data:** While submitters may request re-testing following software revisions or bug fixes, accurately recorded benchmark evaluation logs will not be scrubbed, suppressed, or altered retroactively.

### 4.5 Nominative Fair Use and Trademark Disclaimer
All product names, logos, trademarks, and registered trademarks referenced in this benchmark (including but not limited to LanguageTool, TextGears, DeepL, BCorrect, Sapling, and Grammarly) are the property of their respective owners. Their use herein is strictly for nominative, educational, comparative, and non-commercial academic evaluation purposes only and does not imply endorsement, affiliation, or sponsorship.

---

## 5. Step-by-Step Submission Instructions

### Step 1: Open an Engine Submission Issue
Open an issue on GitHub using the **New Engine Submission** template, providing:
- Engine / Project Name.
- Organization or Primary Author.
- Architectural Category (Geometric Manifold, Statistical N-Gram, Rule-Based, Neural LLM).
- Public Endpoint URL and JSON Request Schema.
- Latency / Hardware SLA Claim (e.g., "Sub-50ms CPU" or "Cloud REST").

### Step 2: Credential Handshake
- Do **NOT** paste your API key in the issue.
- A maintainer will provide a secure private channel (e.g., encrypted one-time secret link or private GitHub secret) for key transmission.
- Verify that the key is hard-capped at **$1.00 USD**.

### Step 3: Automated Smoke Test & Verification
Benchmark maintainers will execute a 3-query sanity check to ensure the endpoint returns valid HTTP 200 responses and matches the expected JSON schema.

### Step 4: Official Blind Evaluation Run
The automated suite executes the 4-pillar blind test corpus against the endpoint, recording:
- Spelling Accuracy (Pillar 1).
- Grammar & Syntactic Accuracy (Pillar 2).
- Voice Preservation Rate (Pillar 3).
- Anti-Hallucination Rate (Pillar 4).
- Response Latency (Milliseconds).

### Step 5: Verification & Pull Request Publication
1. The maintainer opens a pull request containing:
   - `raw_results/submissions/<engine-name>.json` (Verbatim inputs and outputs).
   - Updated Leaderboard table in `README.md`.
   - Updated SVG charts in `assets/`.
2. The Submitting Party reviews the raw JSON log to confirm execution accuracy.
3. The PR is merged, publishing the new official standings to the global leaderboard.
