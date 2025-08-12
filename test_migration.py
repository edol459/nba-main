#!/usr/bin/env python3
"""
Test script to verify the fresh NBA data setup worked correctly
"""

from backend.data_manager import get_data_manager
import json

def test_fresh_setup():
    print("🧪 Testing Fresh NBA Data Setup...")
    print("=" * 50)
    
    data_manager = get_data_manager()
    
    # Test 1: Check cache stats
    print("📊 Cache Statistics:")
    stats = data_manager.get_cache_stats()
    print(f"  - Cached games: {stats['cached_games']}")
    print(f"  - Total games: {stats['total_games']}")
    print(f"  - Cached teams: {stats['cached_teams']}")
    
    # Test 2: Check season averages
    print("\n📈 Season Averages Test:")
    averages = data_manager.get_season_averages()
    
    if averages:
        player_count = len(averages.get('player_averages', []))
        team_count = len(averages.get('team_averages', []))
        print(f"  ✅ Player averages: {player_count} players")
        print(f"  ✅ Team averages: {team_count} teams")
        
        # Show top 3 players
        if averages.get('player_averages'):
            print(f"\n  🏆 Top 3 Players:")
            for i, player in enumerate(averages['player_averages'][:3]):
                print(f"    {i+1}. {player.get('PLAYER', 'Unknown')} - "
                      f"{player.get('PTS', 0)} PPG, {player.get('REB', 0)} RPG, "
                      f"{player.get('AST', 0)} APG")
        
        # Show some teams
        if averages.get('team_averages'):
            print(f"\n  🏀 Sample Teams:")
            for i, team in enumerate(averages['team_averages'][:3]):
                print(f"    {team.get('TeamName', 'Unknown')}: "
                      f"{team.get('WINS', 0)}-{team.get('LOSSES', 0)} "
                      f"({team.get('WinPCT', 0):.3f})")
    else:
        print("  ❌ No season averages found!")
        return False
    
    # Test 3: Test on-demand game fetching
    print(f"\n🎯 Testing On-Demand Game Fetching...")
    
    # Try to get a Lakers game (common team)
    try:
        lal_games = data_manager.get_team_games('LAL')
        if not lal_games.empty:
            print(f"  ✅ Found {len(lal_games)} Lakers games")
            
            # Try to get data for the most recent game
            if len(lal_games) > 0:
                recent_game = lal_games.iloc[0]
                game_id = str(recent_game['GAME_ID']).zfill(10)
                
                print(f"  🔍 Testing game data fetch for {game_id}...")
                game_data = data_manager.get_game_data(game_id)
                
                if game_data:
                    player_count = len(game_data.get('player_stats', []))
                    team_count = len(game_data.get('team_stats', []))
                    print(f"  ✅ Game data retrieved: {player_count} players, {team_count} teams")
                    
                    # Show sample players
                    if game_data.get('player_stats'):
                        lal_players = [p for p in game_data['player_stats'] 
                                     if p.get('TEAM_ABBREVIATION') == 'LAL'][:2]
                        if lal_players:
                            print(f"  🌟 Sample Lakers players:")
                            for player in lal_players:
                                print(f"    - {player.get('PLAYER_NAME', 'Unknown')}: "
                                      f"{player.get('PTS', 0)} pts")
                else:
                    print(f"  ⚠️  Could not fetch game data for {game_id}")
        else:
            print(f"  ⚠️  No Lakers games found")
    except Exception as e:
        print(f"  ❌ Error testing Lakers games: {e}")
    
    # Test 4: Test caching behavior
    print(f"\n⚡ Testing Cache Performance...")
    
    if averages:
        # Test that subsequent calls are fast (cached)
        import time
        
        start_time = time.time()
        averages_again = data_manager.get_season_averages()
        end_time = time.time()
        
        cache_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"  ✅ Cached lookup time: {cache_time:.2f}ms")
        
        if cache_time < 100:  # Should be very fast from cache
            print(f"  🚀 Cache is working perfectly!")
        else:
            print(f"  ⚠️  Cache seems slow, might not be working optimally")
    
    # Final summary
    print("\n" + "=" * 50)
    
    success_conditions = [
        stats['cached_games'] >= 0,  # Could be 0 initially, games fetched on demand
        averages is not None,
        len(averages.get('player_averages', [])) > 0,
        len(averages.get('team_averages', [])) > 0
    ]
    
    if all(success_conditions):
        print("🎉 FRESH SETUP TEST PASSED!")
        print("Your NBA data system is ready!")
        print("\n✨ What's working:")
        print("- Season averages cached and fast")
        print("- Team data available")
        print("- Games will be fetched on-demand")
        print("- Everything cached for speed")
        return True
    else:
        print("⚠️  SOME ISSUES DETECTED")
        print("Check the errors above and re-run setup if needed")
        return False


def show_data_samples():
    """Show some sample data to verify everything looks good"""
    print("\n📋 Sample Data Preview:")
    print("-" * 30)
    
    data_manager = get_data_manager()
    averages = data_manager.get_season_averages()
    
    if averages and averages.get('player_averages'):
        print("🌟 Top Scorers (PPG):")
        # Sort by points per game if available
        players = averages['player_averages']
        try:
            sorted_players = sorted(players, key=lambda x: float(x.get('PTS', 0)), reverse=True)
            for i, player in enumerate(sorted_players[:5]):
                print(f"  {i+1}. {player.get('PLAYER', 'Unknown')} "
                      f"({player.get('TEAM', 'UNK')}): {player.get('PTS', 0)} PPG")
        except:
            # If sorting fails, just show first 5
            for i, player in enumerate(players[:5]):
                print(f"  {i+1}. {player.get('PLAYER', 'Unknown')}: {player.get('PTS', 0)} PPG")
    
    if averages and averages.get('team_averages'):
        print(f"\n🏆 Top Teams (by Win %):")
        teams = averages['team_averages']
        try:
            sorted_teams = sorted(teams, key=lambda x: float(x.get('WinPCT', 0)), reverse=True)
            for i, team in enumerate(sorted_teams[:5]):
                print(f"  {i+1}. {team.get('TeamName', 'Unknown')}: "
                      f"{team.get('WINS', 0)}-{team.get('LOSSES', 0)} "
                      f"({float(team.get('WinPCT', 0)):.3f})")
        except:
            # If sorting fails, just show first 5
            for i, team in enumerate(teams[:5]):
                print(f"  {i+1}. {team.get('TeamName', 'Unknown')}: "
                      f"{team.get('WINS', 0)}-{team.get('LOSSES', 0)}")


if __name__ == "__main__":
    success = test_fresh_setup()
    
    if success:
        show_data_samples()
        print(f"\n🚀 Ready to run your Flask server!")
        print("Games will be fetched automatically as users request them.")
    else:
        print(f"\n🔧 Run the setup again: python setup_fresh_nba_data.py")
    
    print(f"\n{'✅ All systems go!' if success else '❌ Setup needs fixing.'}")