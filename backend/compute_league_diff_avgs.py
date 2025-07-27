import pandas as pd
from backend.config import TEAM_DIFF_STATS_TO_TRACK


#compute TEAM DIFF season averages

def compute_league_differentials(team_logs: pd.DataFrame) -> pd.DataFrame:
    team_logs["GAME_ID"] = team_logs["GAME_ID"].astype(str).str.zfill(10)
    game_groups = team_logs.groupby("GAME_ID")
    
    diffs = {stat: [] for stat in TEAM_DIFF_STATS_TO_TRACK}
    
    for game_id, group in game_groups:
        if len(group) != 2:
            continue  # Skip incomplete games

        team1, team2 = group.iloc[0], group.iloc[1]
        for stat in TEAM_DIFF_STATS_TO_TRACK:
            val1, val2 = team1.get(stat), team2.get(stat)
            if pd.isna(val1) or pd.isna(val2):
                continue
            diffs[stat].append(abs(val1 - val2))

    avg_diffs = {
        "STAT": [],
        "AVG_DIFF": []
    }

    for stat, values in diffs.items():
        if values:
            avg_diffs["STAT"].append(stat)
            avg_diffs["AVG_DIFF"].append(round(sum(values) / len(values), 4))

    return pd.DataFrame(avg_diffs)

# Generate and save league_differentials.csv
league_diffs_df = compute_league_differentials(team_df)
league_diffs_df.to_csv("data/league_differentials.csv", index=False)
print("✅ Saved league_differentials.csv")
