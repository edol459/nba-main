import pandas as pd

# server.py
from flask import Flask, jsonify, send_from_directory
from backend.compute_outliers import compute_outliers

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path="",
    )

@app.route("/")
def serve_home(): 
    return send_from_directory("frontend","index.html")


@app.route("/api/games")
def get_available_games():
    team_logs = pd.read_csv("data/team_game_logs.csv")
    team_logs["GAME_ID"] = team_logs["GAME_ID"].astype(str).str.zfill(10)

    # Drop duplicates to get one row per game
    unique_games = team_logs.drop_duplicates(subset=["GAME_ID"])

    # Create list of game options
    games = []
    for _, row in unique_games.iterrows():
        games.append({
            "game_id": row["GAME_ID"],
            "date": row["GAME_DATE"],
            "matchup": row["MATCHUP"]
        })

    return jsonify(games)


@app.route('/api/games/<team_abbr>')
def get_games_for_team(team_abbr):
    game_logs = pd.read_csv("data/team_game_logs.csv")
    game_logs["GAME_ID"] = game_logs["GAME_ID"].astype(str).str.zfill(10)
    team_games = game_logs[game_logs["TEAM_ABBREVIATION"] == team_abbr]

    if team_games.empty:
        return jsonify({"error": "No games found for team"}), 404

    results = []
    for _, row in team_games.iterrows():
        opponent = row["MATCHUP"].replace(team_abbr + " vs. ", "").replace(team_abbr + " @ ", "")
        results.append({
            "game_id": row["GAME_ID"],
            "date": row["GAME_DATE"],
            "opponent": opponent
        })

    return jsonify(results)



@app.route("/api/outliers/<game_id>")
def outliers(game_id):
    try:
        result = compute_outliers(game_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)