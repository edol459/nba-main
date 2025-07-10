from nba_api.stats.endpoints import teamgamelogs, playergamelogs

#set season year
SEASON = '2024-25'

# Fetch team game logs
team_logs = teamgamelogs.TeamGameLogs(season_nullable=SEASON, season_type_nullable='Regular Season') #create API object
team_df = team_logs.get_data_frames()[0]    #API object -> pandas dataframe
team_df.to_csv('data/team_game_logs.csv', index=False)  #saves df to CSV file 

# Fetch player game logs
player_logs = playergamelogs.PlayerGameLogs(season_nullable=SEASON, season_type_nullable='Regular Season')
player_df = player_logs.get_data_frames()[0]
player_df.to_csv('data/player_game_logs.csv', index=False)

print("Raw game logs saved.")
