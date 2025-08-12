#!/usr/bin/env python3
"""
Simple NBA BoxScore to Database Setup
Uses boxscoretraditionalv2 endpoint to fetch and cache game data
"""

import sys
from backend.data_manager import get_data_manager

def simple_boxscore_setup():
    print("🏀 Simple NBA BoxScore Setup")
    print("=" * 40)
    
    data_manager = get_data_manager()
    
    # Test NBA API import
    try:
        from nba_api.stats.endpoints import boxscoretraditionalv2
        print("✅ NBA API imported successfully")
    except ImportError:
        print("❌ NBA API not installed. Run: pip install nba_api")
        return False
    
    # Clear existing data
    print("🗑️  Clearing database...")
    data_manager.clear_cache()
    print("✅ Database cleared")
    
    # Test with a known game ID
    test_game_id = "0022400001"  # First game of 2024-25 season
    
    print(f"🧪 Testing with game ID: {test_game_id}")
    
    try:
        # Fetch boxscore data
        print("📊 Fetching boxscore data...")
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=test_game_id)
        
        # Get the data as DataFrames first to understand structure
        player_df = boxscore.player_stats.get_data_frame()
        team_df = boxscore.team_stats.get_data_frame()
        
        print(f"✅ Retrieved data:")
        print(f"  - Player stats: {len(player_df)} players")
        print(f"  - Team stats: {len(team_df)} teams")
        
        # Convert to list of dictionaries for JSON storage
        player_stats_list = player_df.to_dict('records')
        team_stats_list = team_df.to_dict('records')
        
        # Format for our cache
        game_data = {
            'game_id': test_game_id,
            'player_stats': player_stats_list,
            'team_stats': team_stats_list,
            'game_date': '2024-10-22',  # You can extract this from the data
            'status': 'Final'
        }
        
        # Cache it
        print("💾 Caching game data...")
        data_manager.cache_game_data(test_game_id, game_data)
        
        # Verify it worked
        cached_data = data_manager.get_cached_game_data(test_game_id)
        if cached_data:
            print("✅ Data successfully cached!")
            print(f"  - Cached {len(cached_data['player_stats'])} player records")
            print(f"  - Cached {len(cached_data['team_stats'])} team records")
            
            # Show sample data
            if cached_data['player_stats']:
                sample_player = cached_data['player_stats'][0]
                player_name = sample_player.get('PLAYER_NAME', 'Unknown')
                team = sample_player.get('TEAM_ABBREVIATION', 'UNK')
                points = sample_player.get('PTS', 0)
                print(f"  - Sample player: {player_name} ({team}) - {points} pts")
        else:
            print("❌ Caching failed!")
            return False
        
        print("\n" + "=" * 40)
        print("🎉 SETUP COMPLETE!")
        print("\nWhat works now:")
        print("1. ✅ NBA API connection")
        print("2. ✅ BoxScore data fetching")
        print("3. ✅ Database caching")
        print("4. ✅ Data retrieval")
        
        print(f"\n💡 Next steps:")
        print("1. Your data_manager.get_game_data() now works!")
        print("2. Run your Flask server")
        print("3. Games will be fetched and cached on-demand")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fetching game data: {e}")
        print("\nPossible issues:")
        print("- Game ID might not exist")
        print("- NBA API might be rate limited")
        print("- Network connection issues")
        return False

def test_data_manager_integration():
    """Test that data_manager.get_game_data() works with the new setup"""
    print("\n🔧 Testing data manager integration...")
    
    data_manager = get_data_manager()
    
    # Test getting the cached game
    test_game_id = "0022400001"
    game_data = data_manager.get_game_data(test_game_id)
    
    if game_data:
        print("✅ data_manager.get_game_data() works!")
        print(f"   Returns {len(game_data['player_stats'])} players")
        return True
    else:
        print("❌ data_manager.get_game_data() failed")
        return False

if __name__ == "__main__":
    success = simple_boxscore_setup()
    
    if success:
        test_data_manager_integration()
        print("\n🚀 Your NBA app is ready!")
    else:
        print("\n🔧 Setup failed - check errors above")
    
    sys.exit(0 if success else 1)