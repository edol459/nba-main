# live/game_watcher.py

import time
import os
from nba_api.live.nba.endpoints import scoreboard
from backend.compute_outliers import compute_outliers
from backend.utils import save_json
from tests.mocks import get_finished_games

OUTLIER_SAVE_FOLDER = "backend/output"
POLL_INTERVAL = 180  # seconds (3 minutes)




# Keep track of already-processed game IDs (from saved JSONs)
def get_already_processed_game_ids():
    if not os.path.exists(OUTLIER_SAVE_FOLDER):
        os.makedirs(OUTLIER_SAVE_FOLDER)
        return set()
    return {f.replace(".json", "") for f in os.listdir(OUTLIER_SAVE_FOLDER) if f.endswith(".json")}




# Get all games from today's scoreboard
def get_finished_games():
    try:
        board = scoreboard.ScoreBoard()
        games = board.get_dict()['scoreboard']['games']
        finished = []
        for game in games:
            game_id = game['gameId'].zfill(10)
            if game['gameStatus'] == 3:  # 3 = Final
                finished.append(game_id)
        return finished
    except Exception as e:
        print(f"[ERROR] Failed to fetch scoreboard: {e}")
        return []

def main():
    print("Starting live game watcher...")
    processed = get_already_processed_game_ids()
    print(f"Found {len(processed)} already-processed games.")

    while True:
        finished_games = get_finished_games()
        new_games = [gid for gid in finished_games if gid not in processed]

        for game_id in new_games:
            print(f"[INFO] New finished game: {game_id} — processing...")
            try:
                outlier_data = compute_outliers(game_id)
                save_json(outlier_data)
                processed.add(game_id)
                print(f"[SUCCESS] Processed and saved outliers for game {game_id}")
            except Exception as e:
                print(f"[ERROR] Failed to process game {game_id}: {e}")

        time.sleep(POLL_INTERVAL)


def main():
    finished_games = get_finished_games()
    new_games = [gid for gid in finished_games]

    for game_id in new_games:
        print(f"Processing mock game {game_id}")
        try:
            outlier_data = compute_outliers(game_id)
            save_json(outlier_data)
            print("Saved mock outlier data ✅")
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main
