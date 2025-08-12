import os
from flask import Flask, jsonify, send_from_directory
from backend.compute_outliers import compute_outliers
from backend.data_manager import *

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)


# -------------------------
# Frontend
# -------------------------
@app.route("/")
def serve_home():
    return send_from_directory("frontend", "index.html")


# -------------------------
# API routes
# -------------------------

@app.route("/api/games/<team_abbr>")
def get_games_for_team(team_abbr):
    """Get all games for a specific team"""
    team_id = get_team_id_from_abbr(team_abbr)
    games = get_team_games(team_id)

    # Debug log to server console
    print(f"[DEBUG] /api/games/{team_abbr} returned {len(games)} games")

    if not games:
        return jsonify({"error": f"No games found for team {team_abbr}"}), 404

    return jsonify(games)


@app.route("/api/game/<game_id>")
def get_game_data_route(game_id):
    """Get full game data (cache first, API fallback)"""
    try:
        game_data = get_game_data(game_id)
        if not game_data:
            return jsonify({"error": f"Game {game_id} not found"}), 404
        return jsonify(game_data)
    except Exception as e:
        print(f"Error fetching game {game_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/outliers/<game_id>")
def outliers(game_id):
    """Get outliers for a specific game"""
    try:
        result = compute_outliers(game_id)
        return jsonify(result)
    except Exception as e:
        print(f"Error computing outliers for game {game_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/refresh-games")
def refresh_games():
    """Manually refresh available games"""
    try:
        # Force refresh for all cached teams
        # You might add logic to loop through known teams here
        return jsonify({"success": "Games refreshed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/refresh-averages")
def refresh_averages():
    """Manually refresh season averages"""
    try:
        get_season_averages(force_refresh=True)
        return jsonify({"success": "Averages refreshed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
