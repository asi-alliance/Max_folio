import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TargetFact:
    id: str
    content: str
    source: str
    date: str
    cue_families: Dict[str, str]

@dataclass
class Distractor:
    id: str
    content: str
    near_miss: bool = False

@dataclass
class RecallResult:
    query: str
    cue_type: str
    hit_in_top3: bool
    source_recalled: bool
    near_miss_fp: bool

TARGETS_SIZE10 = [TargetFact("T1","Maxworld agents use ECAN for attention allocation","maxworld_docs","2026-03-15",{"exact":"ECAN attention allocation","paraphrase":"how do agents focus attention","sparse":"attention mechanism","related":"resource allocation in agents"}),TargetFact("T2","NAL revision merges beliefs with frequency-confidence pairs","nal_spec","2026-04-25",{"exact":"NAL revision formula","paraphrase":"how does belief merging work","sparse":"belief revision","related":"combining uncertain evidence"}),TargetFact("T3","MeTTaClaw persistent atomspace has 120-atom hard limit","mettaclaw_config","2026-05-03",{"exact":"persistent atomspace hard limit","paraphrase":"maximum atoms in persistent KB","sparse":"atomspace capacity","related":"knowledge base size constraints"})]

DISTRACTORS_SIZE10 = [Distractor("D1","Reinforcement learning uses reward signals for policy optimization"),Distractor("D2","Transformer attention uses scaled dot-product softmax"),Distractor("D3","Bayesian inference updates posteriors from likelihood and prior"),Distractor("D4","Prolog uses backward chaining for logical deduction"),Distractor("D5","Genetic algorithms evolve populations via crossover and mutation"),Distractor("D6","Kalman filters estimate state from noisy observations"),Distractor("D7","Decision trees split on information gain at each node"),Distractor("D8","Markov chains transition between states with fixed probabilities"),Distractor("D9","Neural backpropagation computes gradients via chain rule"),Distractor("NM1","Attention allocation in cognitive systems uses spreading activation",near_miss=True)]

def score_results(results: List[RecallResult]) -> Dict:
    total = len(results)
    hits = sum(1 for r in results if r.hit_in_top3)
    src = sum(1 for r in results if r.source_recalled)
    nm_fp = sum(1 for r in results if r.near_miss_fp)
    return {"total": total, "hit_rate": hits/max(total,1), "source_recall": src/max(total,1), "near_miss_fp": nm_fp}
