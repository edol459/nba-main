import pandas as pd

#establish columns to average
stats_to_average = [
    'MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT',
    'FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV',
    'STL','BLK','BLKA','PF','PFD','PTS'
]

#compute TEAM season averages

team_df= pd.read_csv("data/team_game_logs.csv") #store team game log CSV in dataframe
team_grouped = team_df.groupby('TEAM_NAME') #group data by team name
team_averages = team_grouped[stats_to_average].mean() #average selected stats
team_averages = team_averages.round(2)
team_averages.to_csv('data/team_averages.csv', index=True)

#compute PLAYER season averages

player_df= pd.read_csv('data/player_game_logs.csv')
player_grouped = player_df.groupby('PLAYER_ID')
player_averages= player_grouped[stats_to_average].mean()
player_averages = player_averages.round(2)

player_names = player_df.groupby('PLAYER_ID')['PLAYER_NAME'].first()
player_averages.insert(0, 'PLAYER_NAME', player_names)

player_averages.to_csv('data/player_averages.csv', index=True)
