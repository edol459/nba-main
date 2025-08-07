import os
import pandas as pd

def test_team_game_logs_exists():
    assert os.path.exists("data/team_game_logs.csv"), "Team game logs file missing"
    df = pd.read_csv("data/team_game_logs.csv")
    assert not df.empty, "Team game logs CSV is empty"
    assert "TEAM_NAME" in df.columns, "Expected column missing in team logs"

def test_player_game_logs_exists():
    assert os.path.exists("data/player_game_logs.csv"), "Player game logs file missing"
    df = pd.read_csv("data/player_game_logs.csv")
    assert not df.empty, "Player game logs CSV is empty"
    assert "PLAYER_NAME" in df.columns, "Expected column missing in player logs"