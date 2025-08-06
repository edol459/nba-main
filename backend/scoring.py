import pandas as pd
import math
from backend.config import STAT_RULES, STATS_TO_TRACK

def percent_diff(actual, avg, stat_name, entity_type="player"):

    if avg == 0 or stat_name not in STAT_RULES:
        return 0
    
    rules = STAT_RULES[stat_name]
    threshold = rules.get(f"{entity_type}_threshold", 0.2)
    min_diff = rules.get("min_diff", 1)

    raw_diff = abs(actual - avg)
    if raw_diff < min_diff:
        return 0
    
    diff_ratio = (actual - avg) / avg
    #diff_ratio = (diff_ratio * 0.9) #water down ratio effect
    if abs(diff_ratio) < threshold:
        return 0
    

    return max(min(diff_ratio, 10), -10)

def compute_scores(row: pd.Series, avg_row: pd.Series) -> dict:
    scores = {}
    for stat in STATS_TO_TRACK:
        x, mu = row.get(stat), avg_row.get(stat)
        if pd.isna(x) or pd.isna(mu):
            continue
        
        if stat == "FG3_PCT":
            if row.get("FG3A",0) < 5:
                continue

        if stat in ["TS_PCT","FG3_PCT"]:
            if row.get("FGA",0) < 5:            #minimum 5 FGA
                continue

        elif (stat not in ["TS_PCT","FG3_PCT"]) and (abs(x) < 3 or mu < 1):  # Ignore performances with too small actual value
            continue
        
        base_weight = STAT_RULES.get(stat, {}).get("weight", 1.0)
        adjusted_weight = base_weight * math.sqrt(mu + 1)  

        diff_score = percent_diff(x, mu, stat_name=stat)
        
        scores[stat] = adjusted_weight * diff_score
    return scores

def compute_team_diff_scores(team1: pd.Series, team2: pd.Series, league_diffs: pd.DataFrame) -> dict:
    diff_scores = {}

    for stat in STAT_RULES:
        rules = STAT_RULES[stat]
        if "team_diff_threshold" not in rules:
            continue

        val1 = team1.get(stat)
        val2 = team2.get(stat)
        try:
            val1 = float(val1)
            val2 = float(val2)
        except (TypeError, ValueError):
            continue

        actual_diff = abs(val1 - val2)
        league_avg_diff = league_diffs.at[stat, "AVG_DIFF"]
        diff_from_avg = actual_diff - league_avg_diff
        threshold = rules["team_diff_threshold"]
        weight = rules["team_diff_weight"]

        if abs(diff_from_avg) >= threshold:
            outlier_team = team1["TEAM_NAME"] if val1 > val2 else team2["TEAM_NAME"]
            team_abbr = team1["TEAM_ABBREVIATION"] if val1 > val2 else team2["TEAM_ABBREVIATION"]
            key = f"{stat} differential"

            diff_scores[key] = {
                "type": "team_vs_team",
                "id": outlier_team,
                "team_abbr": team_abbr,
                "score": round(diff_from_avg * weight, 3),
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
