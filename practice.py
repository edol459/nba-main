from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
from nba_api.stats.static import teams, players
import pandas as pd


teamstats = leaguedashteamstats.LeagueDashTeamStats(
    season= '2024-25',
    league_id_nullable='00',
    date_to_nullable='04/19/2025'
)

team_season_totals = teamstats.get_data_frames()[0]
team_season_avgs= team_season_totals.copy()

headers = ['MIN','PTS','AST','DREB','OREB','STL','TOV','BLK','PF','PFD','FG3M','FTM']

for col in headers:
    if col in team_season_avgs.columns:
        team_season_avgs[col] = team_season_avgs[col] / team_season_avgs['GP']


team_season_avgs[headers] = team_season_avgs[headers].round(2)

#now store in SQL db



playerstats = leaguedashplayerstats.LeagueDashPlayerStats(
    season= '2024-25',
    league_id_nullable='00',
    date_to_nullable='04/19/2025'
)

player_season_totals = playerstats.get_data_frames()[0]
player_season_avgs= player_season_totals.copy()

pheaders = ['MIN','PTS','AST','DREB','OREB','STL','TOV','BLK','PF','PFD','FG3M','FTM']

for col in pheaders:
    if col in player_season_avgs.columns:
        player_season_avgs[col] = player_season_avgs[col] / player_season_avgs['GP']


player_season_avgs[pheaders] = player_season_avgs[pheaders].round(2)

player_season_avgs.to_csv('player_season_avgs.csv',index=False)

#now store in SQL db