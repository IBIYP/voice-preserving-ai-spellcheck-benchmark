---
name: New Engine Submission
about: Submit an AI spelling, grammar, or writing assistant API for official benchmark inclusion
title: "[SUBMISSION]: <Engine Name> Evaluation Request"
labels: ["engine-submission", "benchmark-audit"]
assignees: []
---

### ⚠️ CRITICAL CREDENTIAL SAFETY NOTICE
> **DO NOT POST API KEYS OR CONFIDENTIAL CREDENTIALS IN THIS PUBLIC ISSUE.**  
> Any issue containing an API key will be immediately closed and scrubbed for your safety. Secure transmission instructions for spend-capped test keys will be provided privately by maintainers after registration.

---

### 1. Engine Information
- **Engine / Service Name:** 
- **Developer / Organization:** 
- **Project URL or Documentation:** 
- **Architectural Category:**
  - [ ] Dedicated Geometric / Deterministic Manifold
  - [ ] Classical Rule-Based / Hunspell Engine
  - [ ] Statistical N-Gram API
  - [ ] Neural Language Model / Seq2Seq Transformer
  - [ ] Local Offline Library / Container

---

### 2. Technical API Endpoint Specification
- **Base Endpoint URL:** `https://...`
- **HTTP Method:** `POST` (or specify)
- **Authentication Method:** `Authorization: Bearer <TOKEN>` or `x-api-key`
- **Request Payload Schema (JSON Example):**
```json
{
  "text": "The sample sentence to be checked.",
  "language": "en-US"
}
```
- **Expected Response Schema (JSON Example):**
```json
{
  "corrected_text": "The corrected sentence output."
}
```

---

### 3. Performance & Hardware Claims
- **Claimed Average Latency:** (e.g. `~25 ms` or `~600 ms`)
- **Execution Target:** (e.g. `1 vCPU Single Core`, `Local GPU`, `Cloud REST API`)

---

### 4. Legal Acknowledgement & Liability Agreement
*Please review [SUBMISSIONS.md](SUBMISSIONS.md) and check every box below to proceed with evaluation:*

- [ ] **I have read and agree to the [Submission Protocol & Legal Liability Waiver](SUBMISSIONS.md).**
- [ ] **I confirm that any test API key provided will have a strict hard spending limit of $1.00 USD (or equivalent low request quota).**
- [ ] **I acknowledge that Benchmark Maintainers bear ZERO liability for any API charges, overages, billing disputes, or key security issues, and that our organization assumes 100% sole liability for provided credentials.**
- [ ] **I agree that all evaluation results, verbatim text outputs, latency metrics, and comparative charts will be published openly under the MIT License in the public `raw_results/` directory.**
- [ ] **I understand that I am responsible for revoking the test credential immediately following the completion of the benchmark evaluation.**
