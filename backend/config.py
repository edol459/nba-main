from pathlib import Path

STATS_TO_TRACK = [
    'FGM', 'FG_PCT','FG3M','FG3_PCT',
    'FTM','FT_PCT','OREB','DREB','AST','TOV',
    'STL','BLK','PF','PFD','PTS'
]

WEIGHTS = {
            "PTS": 1.0,
            "AST": 0.8,
            "OREB": 0.5,
            "DREB": 0.3,
            "FG_PCT": 0.8,
            "FG3M": 0.9,
            "FG3_PCT": 1.0,
            "FTM": 0.4,
            "FT_PCT": 0.7,
            "STL": 1.2,
            "BLK": 1.0,
            "TOV": -0.5,
            "PF": -0.2,
            "PFD": 0.5,
}

N_BARS   = 5
DATA_DIR = Path("data")
OUT_DIR  = Path("backend/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
