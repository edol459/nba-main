import time
import os
from nba_api.live.nba.endpoints import scoreboard
from backend.compute_outliers import compute_outliers
from backend.utils import save_json



USE_MOCK = True
if USE_MOCK:
    from backend.live.mock_scoreboard import MockScoreBoard as ScoreBoard
else:
    from nba_api.live.nba.endpoints import scoreboard
    ScoreBoard = scoreboard.ScoreBoard


OUTLIER_SAVE_FOLDER = "backend/output"
POLL_INTERVAL = 180  # seconds

def get_already_processed_game_ids():
    if not os.path.exists(OUTLIER_SAVE_FOLDER):
        os.makedirs(OUTLIER_SAVE_FOLDER)
        return set()
    return {f.replace(".json", "") for f in os.listdir(OUTLIER_SAVE_FOLDER) if f.endswith(".json")}

def get_finished_games():
    try:
        board = ScoreBoard()
        games = board.get_dict()['scoreboard']['games']
        return [g['gameId'].zfill(10) for g in games if g['gameStatus'] == 3]
    except Exception as e:
        print(f"[ERROR] Failed to fetch scoreboard: {e}")
        return []

def main():
    print("Starting live scoreboard watcher...")
    processed = get_already_processed_game_ids()
    print(f"Already processed {len(processed)} games.")

    while True:
        finished_games = get_finished_games()
        new_games = [gid for gid in finished_games if gid not in processed]

        for game_id in new_games:
            print(f"📡 New finished game: {game_id} — processing...")
            try:
                outlier_data = compute_outliers(game_id)
                save_json(outlier_data)
                processed.add(game_id)
                print(f"✅ Saved outliers for game {game_id}")
            except Exception as e:
                print(f"[ERROR] Failed to process game {game_id}: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()