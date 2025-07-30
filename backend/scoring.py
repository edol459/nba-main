import pandas as pd
import math
from backend.config import STATS_TO_TRACK, WEIGHTS, TEAM_DIFF_STATS_TO_TRACK


#just replace min_diff with THRESHOLDS[] IN CONFIG
def percent_diff(actual, avg, threshold=0.2, min_diff=5, stat_name=None):
    if avg == 0:
        return 0
    

    # Adjust sensitivity for TS%
    if stat_name == "TS%":
        threshold = 0.05  # now allows 5% deviation (~0.05)


    raw_diff = abs(actual - avg)

    if stat_name != "TS%" and raw_diff < min_diff:
        return 0
    
    diff_ratio = (actual - avg) / avg
    if abs(diff_ratio) < threshold:
        return 0
    return max(min(diff_ratio, 10), -10)

def compute_scores(row: pd.Series, avg_row: pd.Series) -> dict:
    scores = {}
    for stat in STATS_TO_TRACK:
        x, mu = row.get(stat), avg_row.get(stat)
        if pd.isna(x) or pd.isna(mu):
            continue

        if stat == "TS%" or stat == "FG3_PCT":
            if row.get("FGA",0) < 5:            #minimum 5 FGA
                continue
        elif (stat != "TS%" and stat != "FG3_PCT") and (abs(x) < 3 or mu < 1):  # Ignore performances with too small actual value
            continue
        
        base_weight = WEIGHTS.get(stat, 1)
        adjusted_weight = base_weight * math.sqrt(mu + 1)  

        diff_score = percent_diff(x, mu, stat_name=stat)
        scores[stat] = adjusted_weight * diff_score
    return scores

def compute_team_diff_scores(team1: pd.Series, team2: pd.Series, league_diffs: pd.DataFrame) -> dict:
    diff_scores = {}

    for stat, config in TEAM_DIFF_STATS_TO_TRACK.items():
        val1 = team1.get(stat)
        val2 = team2.get(stat)
        try:
            val1 = float(val1)
            val2 = float(val2)
        except (TypeError, ValueError):
            continue
        
        if val1 is None or val2 is None:
            continue

        actual_diff = abs(val1 - val2)
        league_avg_diff = league_diffs.at[stat, "AVG_DIFF"]
        threshold = config["threshold"]
        weight = config.get("weight", 1.0)

        diff_from_avg = actual_diff - league_avg_diff
        score = diff_from_avg * weight

        if abs(diff_from_avg) >= threshold:
            outlier_team = team1["TEAM_NAME"] if val1 > val2 else team2["TEAM_NAME"]
            team_abbr = team1["TEAM_ABBREVIATION"] if val1 > val2 else team2["TEAM_ABBREVIATION"]
            key = f"{stat} differential"

            diff_scores[key] = {
                "type": "team_vs_team",
                "id": outlier_team,
                "team_abbr": team_abbr,
                "score": round(score, 3),
                "actual": round(actual_diff, 3),
                "avg": round(league_avg_diff, 3),
                "stat": key,
            }

    return diff_scores

def rank_scores(scores: dict, n: int):
    sorted_items=sorted(scores.items(), key=lambda x: x[1]["score"])
    neg = sorted_items[:n]
    pos = sorted_items[-n:]

    # Reverse pos to put highest score first
    pos = sorted(pos, key=lambda x: x[1]["score"], reverse=True)
    neg = sorted(neg, key=lambda x: x[1]["score"])

    return pos, neg
