from pathlib import Path

STATS_TO_TRACK = [
    'FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT',
    'FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV',
    'STL','BLK','BLKA','PF','PFD','PTS','PLUS_MINUS'
]

WEIGHTS = {
    "PTS":      3.0,   # more is good
    "AST":      2.5,
    "REB":      2.0,
    "STL":      2.0,
    "BLK":      2.0,
    "FG_PCT":   3.0,
    "FG3_PCT":  3.0,
    "TOV":     -2.0,   # more is bad → negative weight
    "FOUL":    -1.5,
    "PF":      -1.5,
}

N_BARS   = 5
DATA_DIR = Path("data")
OUT_DIR  = Path("backend/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
