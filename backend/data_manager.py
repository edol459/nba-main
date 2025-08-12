import pandas as pd
import os
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats, leaguegamefinder, teamgamelog
from typing import Optional

# Cache directory
CACHE_DIR = "cache"
SEASON_CACHE_DIR = os.path.join(CACHE_DIR, "seasons")

# In-memory cache for current session
_season_cache = {}

def init_cache_dirs():
    """Create cache directories if they don't exist."""
    os.makedirs(SEASON_CACHE_DIR, exist_ok=True)

def get_season_cache_files(season: str):
    """Get file paths for season cache files."""
    season_clean = season.replace('-', '_')
    return {
        'teams': os.path.join(SEASON_CACHE_DIR, f"team_averages_{season_clean}.csv"),
        'players': os.path.join(SEASON_CACHE_DIR, f"player_averages_{season_clean}.csv")
    }

def calculate_season_averages(season: str = '2024-25', date_to: Optional[str] = None):
    """Calculate team and player season averages using your exact logic."""
    print(f"Calculating season averages for {season}...")
    
    # Team stats
    teamstats = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        league_id_nullable='00',
        date_to_nullable=date_to
    )
    team_season_totals = teamstats.get_data_frames()[0]
    team_season_avgs = team_season_totals

    # Player stats
    playerstats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        league_id_nullable='00',
        date_to_nullable=date_to
    )
    player_season_totals = playerstats.get_data_frames()[0]
    player_season_avgs = player_season_totals

    # Calculate averages (your exact logic)
    headers = ['MIN', 'PTS', 'AST', 'DREB', 'OREB', 'STL', 'TOV', 'BLK', 'PF', 'PFD', 'FG3M', 'FTM']

    for col in headers:
        if col in team_season_avgs.columns:
            team_season_avgs[col] = team_season_avgs[col] / team_season_avgs['GP']
        if col in player_season_avgs.columns:
            player_season_avgs[col] = player_season_avgs[col] / player_season_avgs['GP']

    team_season_avgs[headers] = team_season_avgs[headers].round(2)
    player_season_avgs[headers] = player_season_avgs[headers].round(2)
    
    return team_season_avgs, player_season_avgs

def save_season_averages_to_csv(team_df: pd.DataFrame, player_df: pd.DataFrame, season: str):
    """Save season averages to CSV files."""
    init_cache_dirs()
    cache_files = get_season_cache_files(season)
    
    team_df.to_csv(cache_files['teams'], index=False)
    player_df.to_csv(cache_files['players'], index=False)
    
    print(f"saved season averages to:")
    print(f"   Teams: {cache_files['teams']}")
    print(f"   Players: {cache_files['players']}")

def load_season_averages_from_csv(season: str):
    """Load season averages from CSV cache."""
    cache_files = get_season_cache_files(season)
    
    if not (os.path.exists(cache_files['teams']) and os.path.exists(cache_files['players'])):
        return None
    
    try:
        team_df = pd.read_csv(cache_files['teams']).set_index('TEAM_NAME')
        player_df = pd.read_csv(cache_files['players']).set_index('PLAYER_ID')
        
        print(f"✅ Loaded season averages from CSV cache for {season}")
        return {
            'team_averages': team_df,
            'player_averages': player_df
        }
    except Exception as e:
        print(f"Error loading CSV cache: {e}")
        return None

def get_season_averages(season: str = '2024-25', force_refresh: bool = False):
    """
    Main function: Load from cache or calculate if needed.
    Returns dict with DataFrames indexed for compute_outliers.
    """
    global _season_cache
    
    # Check in-memory cache first (fastest)
    if not force_refresh and season in _season_cache:
        print(f"Using in-memory cache for {season}")
        return _season_cache[season]
    
    # Check CSV cache
    if not force_refresh:
        cached_data = load_season_averages_from_csv(season)
        if cached_data:
            _season_cache[season] = cached_data
            return cached_data
    
    # No cache or force refresh - calculate new
    team_avgs, player_avgs = calculate_season_averages(season)
    
    # Save to CSV cache
    save_season_averages_to_csv(team_avgs, player_avgs, season)
    
    # Store in memory cache with proper indices
    _season_cache[season] = {
        'team_averages': team_avgs.set_index('TEAM_NAME'),
        'player_averages': player_avgs.set_index('PLAYER_ID')
    }
    
    return _season_cache[season]


def get_team_id_from_abbr(team_abbr: str):
    """Convert team abbreviation to team ID for NBA API calls."""
    # NBA team mappings (abbreviation -> team_id)
    team_mappings = {
        'ATL': '1610612737', 'BOS': '1610612738', 'BKN': '1610612751', 'CHA': '1610612766',
        'CHI': '1610612741', 'CLE': '1610612739', 'DAL': '1610612742', 'DEN': '1610612743',
        'DET': '1610612765', 'GSW': '1610612744', 'HOU': '1610612745', 'IND': '1610612754',
        'LAC': '1610612746', 'LAL': '1610612747', 'MEM': '1610612763', 'MIA': '1610612748',
        'MIL': '1610612749', 'MIN': '1610612750', 'NOP': '1610612740', 'NYK': '1610612752',
        'OKC': '1610612760', 'ORL': '1610612753', 'PHI': '1610612755', 'PHX': '1610612756',
        'POR': '1610612757', 'SAC': '1610612758', 'SAS': '1610612759', 'TOR': '1610612761',
        'UTA': '1610612762', 'WAS': '1610612764'
    }
    
    return team_mappings.get(team_abbr.upper())


def get_team_games(team_id):
    """Get all games for a specific team in a season."""

    try:
        # Get team's game log for the season
        team_log = teamgamelog.TeamGameLog(
            league_id_nullable="00",
            team_id=team_id,
            season="2024-25",
            season_type_all_star="Regular Season"
        )
        
        games_df = team_log.get_data_frames()[0]
        print(games_df.head())
        
        # Format for dropdown: game_id, date, opponent, result
        games_list = []
        for _, game in games_df.iterrows():
            game_info = {
                'game_id': game['Game_ID'],
                'date': game['GAME_DATE'],
                'home_away': 'vs' if game['WL'] == 'W' else '@',  # Simplified - you might want to check MATCHUP column
                'result': game["WL"],
                'opponent': game['MATCHUP']
            }
            games_list.append(game_info)
        
        print(f"✅ Found {len(games_list)} games for team {team_id}")
        return games_list
        
    except Exception as e:
        print(f"❌ Error fetching games for team {team_id}: {e}")
        return []

def get_game_data(game_id):

    print(f"Fetching game data for {game_id}...")

    # Get team and player stats from the boxscore
    team_stats = leaguegamefinder.LeagueGameFinder(
        player_or_team_abbreviation='T',
        game_id_nullable=game_id
        )
    
    team_df = team_stats.get_data_frames()[0]
    
    player_stats = leaguegamefinder.LeagueGameFinder(
        player_or_team_abbreviation='P',
        game_id_nullable=game_id
    )

    player_df = player_stats.get_data_frames()[0]
    
    print(f"Loaded game data for {game_id}")
    
    return {
        'team_stats': team_df,
        'player_stats': player_df
    } 