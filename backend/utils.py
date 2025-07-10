import json, pandas as pd
from config import DATA_DIR

def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)

def save_json(payload: dict, path):
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)