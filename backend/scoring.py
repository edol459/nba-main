import pandas as pd
from config import STATS_TO_TRACK, WEIGHTS

def percent_diff(actual, avg, threshold=0.15):
    if avg == 0:
        return 0
    
    diff_ratio = (actual - avg) / avg
    if abs(diff_ratio) < threshold:
        return 0
    return max(min(diff_ratio, 5), -5)

def compute_scores(row: pd.Series, avg_row: pd.Series) -> dict:
    scores = {}
    for stat in STATS_TO_TRACK:
        x, mu = row.get(stat), avg_row.get(stat)
        if pd.isna(x) or pd.isna(mu):
            continue
        if abs(x) < 3 or mu < 1:  # Ignore performances with too small actual value
            continue
        scores[stat] = WEIGHTS.get(stat, 1) * percent_diff(x, mu)
    return scores

def rank_scores(scores: dict, n: int):
    sorted_items=sorted(scores.items(), key=lambda x: x[1]["score"])
    neg = sorted_items[:n]
    pos = sorted_items[-n:]

    # Reverse pos to put highest score first
    pos = sorted(pos, key=lambda x: x[1]["score"], reverse=True)
    neg = sorted(neg, key=lambda x: x[1]["score"])

    return pos, neg
