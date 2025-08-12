from pathlib import Path

STATS_TO_TRACK = [
    'FG_PCT','FG3M','FG3_PCT',
    'FTM','FT_PCT','OREB','DREB','AST','TOV',
    'STL','BLK','PF','PFD','PTS', 'AST/TOV',
    'TS_PCT'
]


TEAM_DIFF_STATS_TO_TRACK = [
    'PTS', 'AST', 'OREB', 'DREB', 'FG_PCT', 'FG3_PCT', 'FG3M'
]


STAT_RULES = {
    "PTS": {
        "player_threshold": 0.25,  # 25% change
        "team_threshold": 0.10,
        "min_diff": 8,
        "weight": 0.8
    },
    "AST": {
        "player_threshold": 0.25,
        "team_threshold": 0.10,
        "min_diff": 4,
        "weight": 1.2
    },
    "OREB": {
        "player_threshold": 0.3,
        "team_threshold": 0.2,
        "team_diff_threshold": 8,
        "team_diff_weight": 1.0,
        "min_diff": 3,
        "weight": 1.2
    },
    "DREB": {
        "player_threshold": 0.3,
        "team_threshold": 0.2,
        "team_diff_threshold": 8,
        "team_diff_weight": 1.0,
        "min_diff": 4,
        "weight": 1.0
    },
    "FG_PCT": {
        "player_threshold": 1.00,
        "team_threshold": 0.2,
        "team_diff_threshold": 0.01,
        "team_diff_weight": 4.0,
        "min_diff": 0.05,
        "weight": 1.0
    },
    "FG3_PCT": {
        "player_threshold": 0.30,
        "team_threshold": 0.15,
        "team_diff_threshold": 0.05,
        "team_diff_weight": 2.0,
        "min_diff": 0.10,
        "weight": 1.0
    },
    "TS_PCT": {
        "player_threshold": 0.25,
        "team_threshold": 0.10,
        "min_diff": 0.10,
        "weight": 1.2
    },
    "FT_PCT": {
        "player_threshold": .30,
        "team_threshold": .20,
        "min_diff": 0.20,
        "weight": 1.0
    },
    "PF": {
        "player_threshold": 0.7,
        "team_threshold": 0.3,
        "min_diff": 3,
        "weight": -0.2
    },
    "TOV": {
        "player_threshold": 0.3,
        "team_threshold": 0.2,
        "min_diff": 3,
        "weight": -0.8
    },
    "STL": {
        "player_threshold": 0.4,
        "team_threshold": 0.25,
        "min_diff": 2,
        "weight": 1.0
    },
    "BLK": {
        "player_threshold": 0.4,
        "team_threshold": 0.25,
        "min_diff": 2,
        "weight": 1.0
    },
    "AST/TOV": {
        "player_threshold": 0.5,
        "team_threshold": 0.3,
        "min_diff": 3,
        "weight": 1.1
    },
    "FTM": {
        "player_threshold": 0.25,
        "team_threshold": 0.15,
        "min_diff": 5,
        "weight": 0.8
    },
    "FG3M": {
        "player_threshold": 0.3,
        "team_threshold": 0.2,
        "team_diff_threshold": 10,
        "team_diff_weight": 1.0,
        "min_diff": 3,
        "weight": 1.1
    },
    "PFD": {
        "player_threshold": 0.3,
        "team_threshold": 0.2,
        "min_diff": 3,
        "weight": 0.5
    }
}


N_BARS   = 5
DATA_DIR = Path("data")
OUT_DIR  = Path("backend/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
