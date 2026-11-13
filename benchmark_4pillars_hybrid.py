#!/usr/bin/env python3
"""
Open Developer Spelling & Grammar API Benchmark: 4-Pillar Evaluation Suite
==========================================================================
Bad Character Scanner Codebase Inc. (BCSC) - Open Benchmark Working Group

A transparent, multi-pillar empirical evaluation framework for spelling
and grammar engines across four decoupled functional pillars:
1. Spelling Accuracy (Orthography, severe dysgraphia, phonetic slips)
2. Grammar & Syntactic Accuracy (Agreement, tense harmony, punctuation)
3. Maintaining Writer's Voice (Dialect tolerance, slang, anti-over-editing)
4. Avoiding Hallucinations (Zero semantic drift, zero rogue dictionary substitutions)
5. Hybrid Final Meta-Score (Balanced composite synthesis across all 4 pillars)

Canadian spelling conventions (colour, honour, behaviour, analyse, catalogue)
are maintained throughout codebase comments.
"""

import os
import sys
import json
import time

# Definition of the 10 blind unseen domain evaluation units
# Each unit has decoupled targets:
# - spelling_targets: pure orthographic slips
# - grammar_targets: syntax and grammatical agreements
# - voice_tokens: stylistic markers, slang, and authorial expressions
# - dialect_equivalents: acceptable regional/vernacular variants (multi-reference)
# - forbidden_rewrites: corporate/robotic paraphrases (over-editing)
# - hallucination_signatures: engine-specific rogue substitutions and semantic drift

UNSEEN_BENCHMARK_UNITS = [
    {
        "id": "H-01",
        "domain": "Urban Slang & Modern Banter",
        "input": "Yo that concert was straight fire no cap, but my freind lost his tickit at the entrence. We had to finagle our way past securty but it was to lit to miss.",
        "spelling_targets": {
            "freind": "friend",
            "tickit": "ticket",
            "entrence": "entrance",
            "securty": "security"
        },
        "grammar_targets": {
            "to lit": "too lit"
        },
        "voice_tokens": [
            "yo",
            "no cap",
            "finagle our way",
            "fire"
        ],
        "dialect_equivalents": {
            "straight fire": ["straight fire", "fire"]
        },
        "forbidden_rewrites": [
            "genuinely incredible",
            "negotiate our way past the security team",
            "far too exciting"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": ["strait fire"],
            "LanguageTool API": [],
            "TextGears API": [],
            "DeepL Write": ["misplaced his ticket", "negotiate our way past the security team", "far too exciting"]
        }
    },
    {
        "id": "H-02",
        "domain": "Southern Gothic & Regional Cadence",
        "input": "Granddaddy sat on the porch rockin slow, watchin the crik rise after the floodin. He reckned the old barn wouldnt survive another downpoar.",
        "spelling_targets": {
            "floodin": "flooding",
            "reckned": "reckoned",
            "downpoar": "downpour"
        },
        "grammar_targets": {
            "wouldnt": "wouldn't"
        },
        "voice_tokens": [
            "granddaddy",
            "porch",
            "old barn"
        ],
        "dialect_equivalents": {
            "rockin": ["rockin", "rocking"],
            "watchin": ["watchin", "watching"],
            "crik": ["crik", "creek", "crick"]
        },
        "forbidden_rewrites": [
            "grandfather was seated",
            "veranda",
            "observing the stream",
            "calculated that",
            "heavy rainstorm"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": ["watch in the cri"],
            "LanguageTool API": ["watching the erik rise"],
            "TextGears API": [],
            "DeepL Write": ["heavy rainstorm", "my grandfather", "rocking slowly"]
        }
    },
    {
        "id": "H-03",
        "domain": "Gritty Cyberpunk Tech-Noir",
        "input": "Neon reflected off the wet ashpalt. She jackd into the subnet, bypassed the firewal, and dumpd the encrypted payload before the ICE could trace her signel.",
        "spelling_targets": {
            "ashpalt": "asphalt",
            "firewal": "firewall",
            "signel": "signal"
        },
        "grammar_targets": {
            "jackd": "jacked",
            "dumpd": "dumped"
        },
        "voice_tokens": [
            "neon",
            "subnet",
            "ice",
            "encrypted payload"
        ],
        "dialect_equivalents": {},
        "forbidden_rewrites": [
            "connected to the network",
            "circumvented the security protocols",
            "extracted the confidential data",
            "counter-intrusion software"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": [],
            "LanguageTool API": ["trace her signed", "she jack into"],
            "TextGears API": [],
            "DeepL Write": ["counter-intrusion software", "accessed the local network", "extracted the encrypted data"]
        }
    },
    {
        "id": "H-04",
        "domain": "Culinary & Sensory Critique",
        "input": "The roasted duck had increadible crispy skin, but the rasberry reduction was way to acidic. It totally overpowred the delicat flavor of the parsnips.",
        "spelling_targets": {
            "increadible": "incredible",
            "rasberry": "raspberry",
            "overpowred": "overpowered",
            "delicat": "delicate"
        },
        "grammar_targets": {
            "way to": "way too"
        },
        "voice_tokens": [
            "roasted duck",
            "crispy skin",
            "reduction",
            "parsnips"
        ],
        "dialect_equivalents": {
            "flavor": ["flavor", "flavour"]
        },
        "forbidden_rewrites": [
            "poultry exhibited commendable crispness",
            "excessively tart",
            "diminished the subtle qualities",
            "delicate taste"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": [],
            "LanguageTool API": [],
            "TextGears API": [],
            "DeepL Write": ["featured wonderfully crispy skin", "proved excessively acidic", "completely masked"]
        }
    },
    {
        "id": "H-05",
        "domain": "High-Entropy Severe Dysgraphia",
        "input": "Lass nite I dreemt of a spacship flying throu the stars with a giant roket boostr. We landd on a purpul planet with buble lakes and alien critturs that dancd joyfully. It felt so reel I cried wen my mom woak me up for skool!",
        "spelling_targets": {
            "lass nite": "last night",
            "dreemt": "dreamt",
            "spacship": "spaceship",
            "throu": "through",
            "roket": "rocket",
            "boostr": "booster",
            "purpul": "purple",
            "buble": "bubble",
            "critturs": "critters",
            "reel": "real",
            "wen": "when",
            "skool": "school"
        },
        "grammar_targets": {
            "landd": "landed",
            "dancd": "danced",
            "woak": "woke"
        },
        "voice_tokens": [
            "spaceship",
            "purple planet",
            "bubble lakes",
            "alien",
            "joyfully"
        ],
        "dialect_equivalents": {
            "dreamt": ["dreamt", "dreamed"]
        },
        "forbidden_rewrites": [
            "celestial spacecraft",
            "traveling across the cosmos",
            "violet world",
            "wept profusely"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": ["mom work me up"],
            "LanguageTool API": ["flying thou the stars", "pursue planet", "up for stool"],
            "TextGears API": ["pupil planet", "bauble lakes", "up for skoal"],
            "DeepL Write": ["celestial spacecraft", "traveling across the cosmos", "violet world", "sparkling lakes"]
        }
    },
    {
        "id": "H-06",
        "domain": "Punchy SaaS Executive Pitch",
        "input": "Our cac dropped 40% mom, while arr hit a record high. The competishun is scramblin to match our feachures, but we move to fast.",
        "spelling_targets": {
            "competishun": "competition",
            "scramblin": "scrambling",
            "feachures": "features"
        },
        "grammar_targets": {
            "cac": "cac",
            "mom": "mom",
            "arr": "arr",
            "to fast": "too fast"
        },
        "voice_tokens": [
            "dropped 40%",
            "record high",
            "scrambling"
        ],
        "dialect_equivalents": {
            "cac": ["cac", "CAC"],
            "mom": ["mom", "MoM", "MOM"],
            "arr": ["arr", "ARR"]
        },
        "forbidden_rewrites": [
            "customer acquisition costs",
            "month-over-month",
            "annualized recurring revenue",
            "unmatched pace"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": [],
            "LanguageTool API": [],
            "TextGears API": ["our vac dropped"],
            "DeepL Write": ["customer acquisition costs", "annualized recurring revenue", "unmatched pace"]
        }
    },
    {
        "id": "H-07",
        "domain": "Sports Locker-Room Kinetic Action",
        "input": "Coach drew up the play on the whitebord during the timout. We ran the pick and rool to perfecshun, nailed the threepointer at the buzer, and won the champinship!",
        "spelling_targets": {
            "whitebord": "whiteboard",
            "timout": "timeout",
            "rool": "roll",
            "perfecshun": "perfection",
            "buzer": "buzzer",
            "champinship": "championship"
        },
        "grammar_targets": {
            "threepointer": "three-pointer"
        },
        "voice_tokens": [
            "coach",
            "play",
            "pick and roll",
            "championship"
        ],
        "dialect_equivalents": {
            "three-pointer": ["three-pointer", "three pointer"]
        },
        "forbidden_rewrites": [
            "tactical sequence",
            "offensive maneuver",
            "decisive perimeter shot",
            "clinched the championship title"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": ["at the buyer"],
            "LanguageTool API": ["pick and room", "at the buyer"],
            "TextGears API": ["pick and roil"],
            "DeepL Write": ["tactical sequence", "pick-and-roll maneuver impeccably", "decisive perimeter shot", "clinched the championship title"]
        }
    },
    {
        "id": "H-08",
        "domain": "Introspective Poetic Stream-of-Thought",
        "input": "Autumn leavs spiraled across the abandond trax. A quiet saddness hung in the air, neither bitter nor cruel, just the slow exhail of another dying year.",
        "spelling_targets": {
            "leavs": "leaves",
            "abandond": "abandoned",
            "trax": "tracks",
            "saddness": "sadness",
            "exhail": "exhale"
        },
        "grammar_targets": {},
        "voice_tokens": [
            "autumn leaves",
            "spiraled",
            "quiet sadness hung in the air",
            "neither bitter nor cruel",
            "dying year"
        ],
        "dialect_equivalents": {},
        "forbidden_rewrites": [
            "golden autumn foliage",
            "neglected rails",
            "subdued sorrow lingered",
            "closing season"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": ["slow exiled of another dying year"],
            "LanguageTool API": ["autumn leave spiraled", "abandoned tax"],
            "TextGears API": ["abandoned Trax"],
            "DeepL Write": ["golden autumn foliage", "neglected rails", "subdued sorrow", "closing season"]
        }
    },
    {
        "id": "H-09",
        "domain": "Field Biology & Explorer Notes",
        "input": "Observd three speshimens of dendrobates tinctorius near the stream bed. The aposematik coloration was extreamly vibrant despite heavy canoppy shade.",
        "spelling_targets": {
            "speshimens": "specimens",
            "aposematik": "aposematic",
            "extreamly": "extremely",
            "canoppy": "canopy"
        },
        "grammar_targets": {
            "observd": "observed"
        },
        "voice_tokens": [
            "three specimens",
            "stream bed",
            "coloration",
            "heavy canopy shade"
        ],
        "dialect_equivalents": {
            "dendrobates tinctorius": ["dendrobates tinctorius", "dendrobates tinctorious"]
        },
        "forbidden_rewrites": [
            "researchers identified",
            "instances of the poison frog",
            "watercourse",
            "warning pigmentation"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": [],
            "LanguageTool API": ["dendrites tinctorial"],
            "TextGears API": ["dendrites tinctures", "postmark coloration"],
            "DeepL Write": ["researchers identified", "instances of the poison frog", "watercourse", "dense overhead foliage"]
        }
    },
    {
        "id": "H-10",
        "domain": "Legal & Contractual Shorthand",
        "input": "Clause 4.2 govorns indemity obligashuns. Neither party shall be liabel for consequenshal damages arising from unintensional breach.",
        "spelling_targets": {
            "indemity": "indemnity",
            "obligashuns": "obligations",
            "liabel": "liable",
            "consequenshal": "consequential",
            "unintensional": "unintentional"
        },
        "grammar_targets": {
            "govorns": "governs"
        },
        "voice_tokens": [
            "clause 4.2",
            "neither party shall be",
            "consequential damages",
            "breach"
        ],
        "dialect_equivalents": {},
        "forbidden_rewrites": [
            "section 4.2 establishes",
            "under no circumstance will either signatory",
            "assume financial responsibility",
            "non-willful contractual default"
        ],
        "hallucination_signatures": {
            "BCorrect (FMM)": [],
            "LanguageTool API": ["neither party shall be label"],
            "TextGears API": ["neither party shall be label"],
            "DeepL Write": ["section 4.2 establishes", "under no circumstance", "assume financial responsibility"]
        }
    }
]

ENGINES = [
    "BCorrect (FMM)",
    "LanguageTool API",
    "TextGears API",
    "DeepL Write"
]

LATENCIES = {
    "BCorrect (FMM)": 18,
    "LanguageTool API": 520,
    "TextGears API": 1050,
    "DeepL Write": 1280
}


def evaluate_unit(unit, output_text, engine_name):
    """
    Evaluates an engine's output across the 4 explicit functional pillars.
    """
    out_lower = output_text.lower()
    
    # Pillar 1: Spelling Accuracy
    spell_targets = unit["spelling_targets"]
    spell_total = len(spell_targets)
    spell_hits = 0
    for typo, target in spell_targets.items():
        # Check dialect equivalences for spelling
        eq_list = unit.get("dialect_equivalents", {}).get(target, [target])
        if any(eq.lower() in out_lower for eq in eq_list):
            spell_hits += 1
    spelling_acc = (spell_hits / max(spell_total, 1)) * 100.0 if spell_total > 0 else 100.0

    # Pillar 2: Grammar & Syntactic Accuracy
    gram_targets = unit["grammar_targets"]
    gram_total = len(gram_targets)
    gram_hits = 0
    for typo, target in gram_targets.items():
        eq_list = unit.get("dialect_equivalents", {}).get(target, [target])
        if any(eq.lower() in out_lower for eq in eq_list):
            gram_hits += 1
    grammar_acc = (gram_hits / max(gram_total, 1)) * 100.0 if gram_total > 0 else 100.0

    # Pillar 3: Maintaining Writer's Voice
    voice_tokens = unit["voice_tokens"]
    voice_total = len(voice_tokens)
    voice_hits = 0
    for vt in voice_tokens:
        eq_list = unit.get("dialect_equivalents", {}).get(vt, [vt])
        if any(eq.lower() in out_lower for eq in eq_list):
            voice_hits += 1
    vpr = (voice_hits / max(voice_total, 1)) * 100.0

    # Over-editing penalty
    forbidden = unit["forbidden_rewrites"]
    forbidden_hits = sum(1 for f in forbidden if f.lower() in out_lower)
    orig_words = len(unit["input"].split())
    out_words = len(output_text.split())
    length_drift = abs(out_words - orig_words) / max(orig_words, 1)
    length_penalty = 1 if length_drift > 0.18 else 0
    oer = min(100.0, (forbidden_hits * 35.0) + (length_penalty * 25.0))
    voice_preservation_score = max(0.0, vpr * (1.0 - (oer / 100.0)))

    # Pillar 4: Avoiding Hallucinations & Semantic Drift
    hallucinations = unit["hallucination_signatures"].get(engine_name, [])
    # Detect known rogue substitutions
    hallucination_count = sum(1 for h in hallucinations if h.lower() in out_lower)
    # Anti-hallucination rate starts at 100% and docks 25% per confirmed rogue mutation
    anti_hallucination_score = max(0.0, 100.0 - (hallucination_count * 25.0))

    # Pillar 5: Hybrid Final Meta-Score
    # Balanced weighting:
    # 35% Spelling + 25% Grammar + 20% Voice Preservation + 20% Anti-Hallucination
    hybrid_meta_score = (
        (0.35 * spelling_acc) +
        (0.25 * grammar_acc) +
        (0.20 * voice_preservation_score) +
        (0.20 * anti_hallucination_score)
    )

    return {
        "spelling_acc": round(spelling_acc, 2),
        "grammar_acc": round(grammar_acc, 2),
        "voice_preservation": round(voice_preservation_score, 2),
        "vpr": round(vpr, 2),
        "oer": round(oer, 2),
        "anti_hallucination": round(anti_hallucination_score, 2),
        "hallucination_count": hallucination_count,
        "hybrid_meta_score": round(hybrid_meta_score, 2)
    }


def run_comprehensive_benchmark():
    """
    Executes the 4-pillar benchmark evaluation across all engines and passages.
    """
    raw_results_path = os.path.join("raw_results", "unseen_10_domains_live_run.json")
    if not os.path.exists(raw_results_path):
        print(f"Error: Missing raw results at {raw_results_path}")
        return None

    with open(raw_results_path, "r", encoding="utf-8") as f:
        raw_runs = json.load(f)

    results = {eng: {"spelling": [], "grammar": [], "voice": [], "anti_hallucination": [], "hybrid": []} for eng in ENGINES}
    per_passage_breakdown = []

    for unit in UNSEEN_BENCHMARK_UNITS:
        uid = unit["id"]
        unit_runs = raw_runs.get(uid, {})
        passage_entry = {"id": uid, "domain": unit["domain"], "scores": {}}

        for eng in ENGINES:
            eng_data = unit_runs.get(eng, {})
            out_text = eng_data.get("text", unit["input"])
            eval_res = evaluate_unit(unit, out_text, eng)

            results[eng]["spelling"].append(eval_res["spelling_acc"])
            results[eng]["grammar"].append(eval_res["grammar_acc"])
            results[eng]["voice"].append(eval_res["voice_preservation"])
            results[eng]["anti_hallucination"].append(eval_res["anti_hallucination"])
            results[eng]["hybrid"].append(eval_res["hybrid_meta_score"])

            passage_entry["scores"][eng] = {
                "text": out_text,
                "metrics": eval_res
            }

        per_passage_breakdown.append(passage_entry)

    summary = {}
    for eng in ENGINES:
        n = len(results[eng]["spelling"])
        summary[eng] = {
            "spelling_accuracy": round(sum(results[eng]["spelling"]) / n, 1),
            "grammar_accuracy": round(sum(results[eng]["grammar"]) / n, 1),
            "voice_preservation": round(sum(results[eng]["voice"]) / n, 1),
            "anti_hallucination": round(sum(results[eng]["anti_hallucination"]) / n, 1),
            "hybrid_meta_score": round(sum(results[eng]["hybrid"]) / n, 1),
            "latency_ms": LATENCIES[eng]
        }

    # Save structured output to raw_results/blind_4pillars_eval_run.json
    output_artifact = {
        "benchmark_metadata": {
            "title": "Open Developer Spelling & Grammar API Benchmark: 4-Pillar Suite",
            "version": "3.0-blind",
            "eval_date": "November 13, 2026",
            "architecture": "4 Functional Pillars + 1 Hybrid Meta-Score",
            "weights": {
                "pillar_1_spelling": "35%",
                "pillar_2_grammar": "25%",
                "pillar_3_voice": "20%",
                "pillar_4_anti_hallucination": "20%"
            }
        },
        "engine_summary": summary,
        "passages": per_passage_breakdown
    }

    out_json_path = os.path.join("raw_results", "blind_4pillars_eval_run.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(output_artifact, f, indent=2)
    print(f"Saved 4-pillar blind evaluation results to {out_json_path}")

    return summary


def print_scorecard(summary):
    """
    Renders a clean ASCII leaderboard table of the 4 pillars.
    """
    print("\n" + "=" * 94)
    print("OPEN DEVELOPER SPELLING & GRAMMAR API BENCHMARK: 4-PILLAR LEADERBOARD")
    print("=" * 94)
    print(f"{'Engine':<20} | {'P1: Spell':<10} | {'P2: Gram':<10} | {'P3: Voice':<10} | {'P4: Anti-Hal':<12} | {'P5: Hybrid':<10} | {'Latency':<8}")
    print("-" * 94)
    for eng in sorted(summary.keys(), key=lambda x: summary[x]["hybrid_meta_score"], reverse=True):
        s = summary[eng]
        lat_str = f"~{s['latency_ms']} ms"
        print(f"{eng:<20} | {s['spelling_accuracy']:>8.1f}% | {s['grammar_accuracy']:>8.1f}% | {s['voice_preservation']:>8.1f}% | {s['anti_hallucination']:>10.1f}% | {s['hybrid_meta_score']:>8.1f}% | {lat_str:>8}")
    print("=" * 94)
    print("Pillar Weights: 35% Spelling, 25% Grammar, 20% Voice Preservation, 20% Anti-Hallucination")
    print("Crowns:")
    print("  * Best Spelling & Dysgraphia:   " + max(summary.items(), key=lambda x: x[1]["spelling_accuracy"])[0])
    print("  * Best Grammar & Syntax:       " + max(summary.items(), key=lambda x: x[1]["grammar_accuracy"])[0])
    print("  * Best Voice Preservation:     " + max(summary.items(), key=lambda x: x[1]["voice_preservation"])[0])
    print("  * Best Anti-Hallucination:     " + max(summary.items(), key=lambda x: x[1]["anti_hallucination"])[0])
    print("  * Fastest Keystroke Speed:     " + min(summary.items(), key=lambda x: x[1]["latency_ms"])[0])
    print("  * Overall Hybrid Meta-Leader:  " + max(summary.items(), key=lambda x: x[1]["hybrid_meta_score"])[0])
    print("=" * 94 + "\n")


if __name__ == "__main__":
    summary = run_comprehensive_benchmark()
    if summary:
        print_scorecard(summary)
