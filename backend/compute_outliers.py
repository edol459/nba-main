import sys
from pathlib import Path
from config import OUT_DIR, N_BARS
from utils import load_csv, save_json
from scoring import compute_scores, rank_scores

def main(game_id: str):
    team_logs   = load_csv("team_game_logs.csv")
    player_logs = load_csv("player_game_logs.csv")
    team_avg    = load_csv("team_averages.csv").set_index("TEAM_NAME")
    player_avg  = load_csv("player_averages.csv").set_index("PLAYER_ID")

    #dict
    #game_out = {"game_id": game_id, "teams": [], "outliers": []}

    team_logs["GAME_ID"] = team_logs["GAME_ID"].astype(str)
    teams_in_game = team_logs[team_logs["GAME_ID"] == str(game_id)]

    game_out = {"game_id": game_id, "teams": teams_in_game["TEAM_ABBREVIATION"].tolist(), "outliers": []}

    print(f"🧪 Found {len(teams_in_game)} teams for GAME_ID {game_id}")
    print("🧪 Sample GAME_IDs from CSV:", team_logs["GAME_ID"].unique()[:5])



    team_scores={}

    for _, team_row in teams_in_game.iterrows():
        tname = team_row["TEAM_NAME"]
        team_avg_row = team_avg.loc[tname]
        t_scores = compute_scores(team_row, team_avg_row)

    

        for stat,score in t_scores.items():
            key = f"{tname} - {stat}"
            team_scores[key] = {
                "type": "team",
                "id": tname,
                "score": score,
                "actual": team_row[stat],
                "avg": team_avg_row[stat]
            }
        
    player_logs["GAME_ID"] = player_logs["GAME_ID"].astype(str)
    players_in_game = player_logs[player_logs["GAME_ID"] == str(game_id)]
    player_scores = {}

    for _, player_row in players_in_game.iterrows():
        name = player_row["PLAYER_NAME"]
        pid = player_row["PLAYER_ID"]
        player_avg_row = player_avg.loc[pid]
        p_scores = compute_scores(player_row,player_avg_row)

        for stat, score in p_scores.items():
            key = f"{name} - {stat}"
            player_scores[key] = {
                "type": "player",
                "id": name,
                "score": score,
                "actual": player_row[stat],
                "avg": player_avg_row[stat]
            }



    merged_scores = team_scores | player_scores

    pos, neg = rank_scores(merged_scores, N_BARS)

    payload = {
        "positive": [
                {
                    "type": info["type"],
                    "name": info["id"],
                    "stat": stat,
                    "score": round(info["score"], 3),
                    "actual": info["actual"],
                    "avg": round(info["avg"], 3),
                }
                for stat,info in pos
        ],
        "negative": [
                {
                    "type": info["type"],
                    "name": info["id"],
                    "stat": stat,
                    "score": round(info["score"], 3),
                    "actual": info["actual"],
                    "avg": round(info["avg"], 3),
                }
                for stat,info in neg
        ],
    }

    
    game_out["outliers"].append(payload)


    save_json(game_out, OUT_DIR / f"{game_id}.json")
    print("✅ saved", OUT_DIR / f"{game_id}.json")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python backend/compute_outliers.py <GAME_ID>")
        sys.exit(1)
    main(sys.argv[1])
