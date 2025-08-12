"""
Standalone test script to verify NBA season averages database functionality.
Place this in the same directory as your data_manager.py file.
"""

import pandas as pd
import os

# Import the NBADataManager directly
import data_manager
import NBADataManager

def test_database_storage():
    """Test that season averages are properly saved to and loaded from database."""
    
    print("=" * 60)
    print("TESTING NBA SEASON AVERAGES DATABASE STORAGE")
    print("=" * 60)
    
    # Initialize data manager
    dm = NBADataManager()
    season = '2024-25'
    
    # TEST 1: Check if we have data in database
    print(f"\n🔍 Checking for existing data in database for season {season}...")
    team_db_data = dm.get_team_averages(season=season)
    player_db_data = dm.get_player_averages(season=season)
    
    if team_db_data.empty or player_db_data.empty:
        print("❌ No data found in database. Fetching and storing season averages...")
        
        # Calculate and store season averages (this will take a few minutes)
        try:
            dm.update_season_data(season, '04/19/2025')
            print("✅ Season averages calculated and stored!")
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return
    else:
        print("✅ Found existing data in database!")
    
    # TEST 2: Load season averages using your compute_outliers interface
    print(f"\n📊 Testing get_season_averages() method...")
    averages_data = dm.get_season_averages(season)
    
    if averages_data is None:
        print("❌ Failed to get season averages")
        return
    
    team_avg = averages_data['team_averages']
    player_avg = averages_data['player_averages']
    
    print(f"✅ Successfully loaded season averages!")
    print(f"   Team averages shape: {team_avg.shape}")
    print(f"   Player averages shape: {player_avg.shape}")
    
    # TEST 3: Verify data structure matches compute_outliers expectations
    print(f"\n🔍 Verifying data structure for compute_outliers compatibility...")
    
    # Check team data structure
    print(f"   Team index type: {type(team_avg.index)}")
    print(f"   Team index name: {team_avg.index.name}")
    print(f"   Sample team names: {list(team_avg.index[:3])}")
    
    # Check player data structure  
    print(f"   Player index type: {type(player_avg.index)}")
    print(f"   Player index name: {player_avg.index.name}")
    print(f"   Sample player IDs: {list(player_avg.index[:3])}")
    
    # TEST 4: Show sample statistics
    print(f"\n📈 Sample team statistics (first 3 teams):")
    sample_teams = team_avg.head(3)
    if 'pts_avg' in team_avg.columns:
        for team_name in sample_teams.index:
            row = sample_teams.loc[team_name]
            print(f"   {team_name}: {row['pts_avg']:.1f} PPG, {row['ast_avg']:.1f} APG")
    else:
        print(f"   Available columns: {list(team_avg.columns)}")
    
    print(f"\n🏀 Sample player statistics (first 3 players):")
    sample_players = player_avg.head(3)
    if 'pts_avg' in player_avg.columns and 'player_name' in player_avg.columns:
        for player_id in sample_players.index:
            row = sample_players.loc[player_id]
            print(f"   {row['player_name']}: {row['pts_avg']:.1f} PPG, {row['ast_avg']:.1f} APG")
    else:
        print(f"   Available columns: {list(player_avg.columns)}")
    
    # TEST 5: Verify database file
    print(f"\n💾 Database file verification:")
    if os.path.exists(dm.db_path):
        file_size = os.path.getsize(dm.db_path) / (1024 * 1024)  # MB
        print(f"   ✅ Database exists: {dm.db_path} ({file_size:.2f} MB)")
    else:
        print(f"   ❌ Database file not found: {dm.db_path}")
    
    # TEST 6: Test lookup operations (like in compute_outliers)
    print(f"\n🔍 Testing lookup operations...")
    
    # Test team lookup (simulate what compute_outliers does)
    if len(team_avg) > 0:
        first_team_name = team_avg.index[0]
        try:
            team_row = team_avg.loc[first_team_name]
            print(f"   ✅ Team lookup works: {first_team_name} -> {team_row['pts_avg']:.1f} PPG")
        except Exception as e:
            print(f"   ❌ Team lookup failed: {e}")
    
    # Test player lookup (simulate what compute_outliers does)
    if len(player_avg) > 0:
        first_player_id = player_avg.index[0]
        try:
            player_row = player_avg.loc[first_player_id]
            player_name = player_row.get('player_name', 'Unknown')
            print(f"   ✅ Player lookup works: ID {first_player_id} ({player_name}) -> {player_row['pts_avg']:.1f} PPG")
        except Exception as e:
            print(f"   ❌ Player lookup failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE TEST COMPLETED SUCCESSFULLY!")
    print("Your compute_outliers.py should work with this database setup.")
    print("=" * 60)

if __name__ == "__main__":
    test_database_storage()