import sys
import pandas as pd
from backend.advanced_stats import add_all_adv
from pathlib import Path
from backend.config import OUT_DIR, N_BARS
from backend.utils import load_csv, save_json
from backend.scoring import compute_scores, rank_scores, compute_team_diff_scores


def compute_outliers(game_id: str):
    team_logs   = load_csv("team_game_logs.csv")
    player_logs = load_csv("player_game_logs.csv")
    team_avg    = load_csv("team_averages.csv").set_index("TEAM_NAME")
    player_avg  = load_csv("player_averages.csv").set_index("PLAYER_ID")
    league_diffs = load_csv("league_differentials.csv").set_index("STAT")



    #Advanced Stats
    player_logs = add_all_adv(player_logs)
    player_avg = add_all_adv(player_avg)


    team_logs["GAME_ID"] = team_logs["GAME_ID"].astype(str).str.zfill(10)
    teams_in_game = team_logs[team_logs["GAME_ID"] == str(game_id)]

    game_out = {"game_id": game_id, "teams": teams_in_game["TEAM_ABBREVIATION"].tolist(), "outliers": []}

    # Compute winner and final score
    if len(teams_in_game) == 2:
        team1 = teams_in_game.iloc[0]
        team2 = teams_in_game.iloc[1]
        
        team1_score = int(team1["PTS"])
        team2_score = int(team2["PTS"])

        final_score = {
            team1["TEAM_ABBREVIATION"]: team1_score,
            team2["TEAM_ABBREVIATION"]: team2_score
        }

        if team1_score > team2_score:
            winner = team1["TEAM_ABBREVIATION"]
        elif team2_score > team1_score:
            winner = team2["TEAM_ABBREVIATION"]
        else:
            winner = "TIE"

        game_out["final_score"] = final_score
        game_out["winner"] = winner


    #TEAM STAT OUTLIERS
    team_scores={}

    for _, team_row in teams_in_game.iterrows():
        tname = team_row["TEAM_NAME"]
        team_avg_row = team_avg.loc[tname]
        t_scores = compute_scores(team_row, team_avg_row)
        team_abbr = team_row["TEAM_ABBREVIATION"]

    

        for stat,score in t_scores.items():
            key = f"{tname} - {stat}"
            team_scores[key] = {
                "type": "team",
                "id": tname,
                "score": score,
                "actual": team_row[stat],
                "avg": team_avg_row[stat],
                "team_abbr": team_abbr
            }
    

    #PLAYER STAT OUTLIERS
    player_logs["GAME_ID"] = player_logs["GAME_ID"].astype(str).str.zfill(10)
    players_in_game = player_logs[player_logs["GAME_ID"] == str(game_id)]
    player_scores = {}

    for _, player_row in players_in_game.iterrows():
        name = player_row["PLAYER_NAME"]
        pid = player_row["PLAYER_ID"]
        player_team = player_row["TEAM_NAME"]
        player_avg_row = player_avg.loc[pid]
        p_scores = compute_scores(player_row,player_avg_row)

        for stat, score in p_scores.items():
            key = f"{name} - {stat}"
            player_scores[key] = {
                "type": "player",
                "id": name,
                "team": player_team,
                "score": score,
                "actual": player_row[stat],
                "avg": player_avg_row[stat],
                "player_id": pid,
            }


    # TEAM DIFF SCORES

    diff_scores = {}
    if len(teams_in_game) == 2:
        team1, team2 = teams_in_game.iloc[0], teams_in_game.iloc[1]
        diff_scores = compute_team_diff_scores(team1, team2, league_diffs)

    # COMBINE & RANK
    merged = {**team_scores, **player_scores, **diff_scores}
    pos, neg = rank_scores(merged, N_BARS)

    payload = {
                "positive": [
            {
                "type": info["type"],
                "name": info["id"],
                "stat": stat,
                "score": round(info["score"], 3),
                "actual": info["actual"],
                "avg": round(info["avg"], 3),
                **({"player_id": info["player_id"]} if "player_id" in info else {}),
                **({"team_abbr": info["team_abbr"]} if "team_abbr" in info else {}),
            } for stat, info in pos
        ],
        "negative": [
            {
                "type": info["type"],
                "name": info["id"],
                "stat": stat,
                "score": round(info["score"], 3),
                "actual": info["actual"],
                "avg": round(info["avg"], 3),
                **({"player_id": info["player_id"]} if "player_id" in info else {}),
                **({"team_abbr": info["team_abbr"]} if "team_abbr" in info else {}),
            } for stat, info in neg
        ]
    }

    print(payload)
    game_out["outliers"].append(payload)


    save_json(game_out, OUT_DIR / f"{game_id}.json")
    print("✅ saved", OUT_DIR / f"{game_id}.json")

    return game_out
