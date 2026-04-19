from app.matrix import compute_pow, compute_weighted_score

SCENARIOS = {
    "base":        {"turnout": 0.65, "swing_factor": 1.0},
    "high_turnout":{"turnout": 0.80, "swing_factor": 1.1},
    "low_turnout": {"turnout": 0.50, "swing_factor": 0.9},
    "anti_wave":   {"turnout": 0.70, "swing_factor": 1.3},
}

def run_scenarios(candidates):
    results = {}
    for scenario_name, params in SCENARIOS.items():
        adjusted = []
        for c in candidates:
            import copy
            c2 = copy.copy(c)
            if c2.is_incumbent:
                c2.incumbency_score = c2.incumbency_score * (2 - params["swing_factor"])
            c2.personal_base = min(100, c2.personal_base * params["turnout"] * 1.4)
            adjusted.append(c2)
        results[scenario_name] = compute_pow(adjusted)
    return results