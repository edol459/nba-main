from pathlib import Path

STATS_TO_TRACK = [
    'FG_PCT','FG3M','FG3_PCT',
    'FTM','FT_PCT','OREB','DREB','AST','TOV',
    'STL','BLK','PF','PFD','PTS', 'AST/TOV',
    'TS%'
]


THRESHOLDS = {
    "PTS": 7,
    "AST": 3,
    "OREB": 3,
    "DREB": 4,
    "FG_PCT": 0.50,
    "FG3_PCT": 0.50,
    "FT_PCT": 0.3,
    "TS%": 0.50,
    "PF": 2,
    "BLK": 2,
    'FG3M': 3,
    'TOV': 3,
    'STL': 3,
    'AST/TOV': 3,
    'FTM': 5,
    "PFD": 4
}

WEIGHTS = {
            "TS%": 0.5,
            "PTS": 0.8,
            "AST": 1.0,
            "OREB": 1.0,
            "DREB": 0.6,
            "FG3M": 0.5,
            "FG3_PCT": 0.5,
            "FTM": 0.5,
            "STL": 1.0,
            "BLK": 1.0,
            "TOV": -0.5,
            "PF": -0.2,
            "PFD": 0.5,
            "AST/TOV": 1.2,
}

N_BARS   = 5
DATA_DIR = Path("data")
OUT_DIR  = Path("backend/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
