import sys
import pandas as pd
from backend.advanced_stats import add_all_adv
from pathlib import Path
from backend.config import OUT_DIR, N_BARS
from backend.utils import save_json
from backend.scoring import compute_scores, rank_scores, compute_team_diff_scores
from backend.data_manager import *

def compute_outliers(game_id):
    
    game_data = get_game_data(game_id)
    print(game_data)
    if not game_data:
        raise Exception(f"Could not load game data for {game_id}")

    #load team & player stats from specific game
    team_logs = game_data['team_stats']
    player_logs = game_data['player_stats']

    season = '2024-25'
    averages_data = get_season_averages(season)

    #load team & player season averages
    team_avgs = averages_data['team_averages']
    player_avgs = averages_data['player_averages']
    
    # Get or create league differentials
    league_diffs = get_league_differentials()

    # Apply advanced stats (unchanged from your original)
    player_logs = add_all_adv(player_logs)
    player_avgs = add_all_adv(player_avgs)

    # Ensure GAME_ID format (NBA API already returns this correctly)
    game_id = str(game_id).zfill(10)
    teams_in_game = pd.DataFrame(team_logs)

    game_out = {"game_id": game_id, "teams": teams_in_game.to_dict(orient="records"), "outliers": []}

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

    # TEAM STAT OUTLIERS
    team_scores = {}
    for _, team_row in teams_in_game.iterrows():
        tname = team_row["TEAM_NAME"]
        
        # Skip if team not in averages
        if tname not in team_avgs.index:
            continue
            
        team_avg_row = team_avgs.loc[tname]
        t_scores = compute_scores(team_row, team_avg_row)
        team_abbr = team_row["TEAM_ABBREVIATION"]

        for stat, score in t_scores.items():
            key = f"{tname} - {stat}"
            team_scores[key] = {
                "type": "team",
                "id": tname,
                "score": score,
                "actual": team_row[stat],
                "avg": team_avg_row[stat],
                "team_abbr": team_abbr
            }

    # PLAYER STAT OUTLIERS (almost unchanged from your original)
    players_in_game = player_logs
    player_scores = {}

    for _, player_row in players_in_game.iterrows():
        name = player_row["PLAYER_NAME"]
        pid = player_row["PLAYER_ID"]
        player_team = player_row["TEAM_NAME"]
        
        # Skip if player not in averages
        if pid not in player_avgs.index:
            continue
            
        player_avg_row = player_avgs.loc[pid]
        p_scores = compute_scores(player_row, player_avg_row)

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
    print("saved!", OUT_DIR / f"{game_id}.json")

    return game_out

def get_league_differentials():
    """Get league differentials - use existing file or create defaults"""
    try:
        return pd.read_csv("data/league_differentials.csv").set_index("STAT")
    except FileNotFoundError:
        # Create simple defaults and save them
        from backend.config import TEAM_DIFF_STATS_TO_TRACK
        
        default_values = {
            'PTS': 12.0, 'AST': 6.0, 'OREB': 3.0, 'DREB': 5.0, 
            'FG_PCT': 0.05, 'FG3_PCT': 0.07, 'FG3M': 3.5
        }
        
        df = pd.DataFrame([
            {"STAT": stat, "AVG_DIFF": default_values.get(stat, 5.0)}
            for stat in TEAM_DIFF_STATS_TO_TRACK
        ])
        
        df.to_csv("data/league_differentials.csv", index=False)
        return df.set_index("STAT")