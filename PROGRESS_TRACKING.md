# Progress Tracking Policy

The benchmark reports both current performance and change over time, without
treating scores from different test batches as if they were measured on the
same inputs.

## Two separate series

### Public anchor

Use the fixed H-suite as a public regression-control set. Run it with each
engine revision using the same evaluator and collection procedure. This series
is suitable for comparing an engine with its earlier versions, but the public
test and annotations can be learned or optimized against. It must not be
presented as a blind generalization score.

Record a point only when the engine revision and run are identifiable. If a
provider does not expose a version, record `not reported`; do not infer a
version from the run date.

### Weekly fresh challenge

Each weekly batch is a fresh, full-size challenge. Keep its score attached to
that batch ID and publish it as a dated snapshot. Because every engine is run
on the same batch, its within-week scores, rankings, and pairwise score gaps
are valid head-to-head comparisons, even when the batch is harder or easier
than the previous one.

Across weeks, report relative rankings and pairwise score gaps as a descriptive
measure of competitive position. Do not treat raw score changes as proof of
absolute improvement: engines can respond differently to changed difficulty,
domains, or error types. The public-anchor series is the controlled measure
for comparing an engine with its own earlier revisions on identical inputs.

Keep unreleased inputs and annotations private until their release. A weekly
report is final only after every planned participant has a result, including
manual web-checker runs. Clearly label incomplete results as pending and do not
silently omit a missing participant from a final comparison.

## Required run metadata

For each engine and evaluated suite, preserve:

- run date and immutable run ID;
- engine/provider name and reported version, or `not reported`;
- collection mode (`api`, `local`, or `web_demo`) and relevant interaction
  details;
- suite/batch ID, input digest, and evaluator revision;
- spelling, grammar, voice, anti-hallucination, and composite scores;
- latency only when measured under a documented procedure; otherwise `null`;
- completion status and any unavailable result reason.

Sapling and JSpell are full participants in every sub-benchmark. For web-only
checks, collect and record their output for every passage using the documented
one-pass procedure; do not omit them from a suite because collection is manual.
Represent unavailable latency as JSON `null` and display it as `n/a`. Never
estimate latency.

Never overwrite an earlier run to make a chart look smoother. Corrections to
recorded data should be traceable and explained.

## Interpretation

Use the public-anchor series for longitudinal engine-version comparisons and
the fresh-challenge series for current, less-overfit performance and
same-week head-to-head comparisons. Keep a consistent participant cohort when
reporting cross-week rank or score-gap trends; if the cohort changes, disclose
it. A change in one series does not imply the same change in the other. Keep
API, local, and web-demo results visibly separated; in particular, web-demo
latency is unavailable unless it was actually measured.

Scores from different evaluator or scoring revisions are not directly
comparable. Rerun the same saved outputs under one revision before making a
longitudinal comparison; otherwise mark the methodology break and keep the
legacy series separate.
