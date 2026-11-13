# Third-Party Engine Submissions Directory
**AuthorVoice Benchmark (AV-Bench)**

This directory contains verified, timestamped evaluation logs for third-party engine submissions that have completed the official 4-pillar benchmark protocol.

## Directory Schema
Each verified engine has a corresponding JSON artifact:
```
raw_results/submissions/<engine_name>_<version>_<eval_date>.json
```

## Structure of Submission Artifacts
Each JSON file contains:
- `submission_metadata`: Submitter organization, architecture category, hardware environment, and evaluation timestamp.
- `pillar_scores`: Independent scores for Spelling (35%), Grammar (25%), Voice Preservation (20%), and Anti-Hallucination (20%).
- `hybrid_meta_score`: Composite 100% index.
- `latency_summary`: Average, median, and 95th percentile query latency in milliseconds.
- `passage_runs`: Verbatim input, output, and target correction breakdown across all benchmark evaluation passages.

All evaluation logs published herein are released under the MIT License for independent verification and community reproduction.
