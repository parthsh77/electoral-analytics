import numpy as np

WEIGHTS = {
    "incumbency_score": 0.15,
    "party_strength":   0.20,
    "past_work_score":  0.20,
    "personal_base":    0.15,
    "caste_base":       0.20,
    "digital_sentiment":0.10,
}

def compute_weighted_score(candidate):
    total = 0.0
    for factor, weight in WEIGHTS.items():
        score = getattr(candidate, factor, 50.0)
        total += score * weight
    return round(total, 2)

def compute_pow(candidates):
    """Softmax-based Probability of Win."""
    scores = np.array([compute_weighted_score(c) for c in candidates])
    exp_scores = np.exp(scores / 20)          # temperature=20 for spread
    pow_values = exp_scores / exp_scores.sum()
    return {c.name: round(float(p) * 100, 1) for c, p in zip(candidates, pow_values)}

def get_strategic_gaps(candidates):
    """Find where each candidate is weakest relative to rivals."""
    gaps = {}
    factors = list(WEIGHTS.keys())
    for cand in candidates:
        others_avg = {}
        for f in factors:
            others = [getattr(c, f, 50) for c in candidates if c.id != cand.id]
            others_avg[f] = np.mean(others) if others else 50
        cand_gaps = {f: round(others_avg[f] - getattr(cand, f, 50), 1) for f in factors}
        gaps[cand.name] = sorted(cand_gaps.items(), key=lambda x: x[1], reverse=True)[:3]
    return gaps