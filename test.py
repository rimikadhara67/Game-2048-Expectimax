"""
Test the improved expectimax agent
This should show much better performance
"""

from game import Game2048
from expectimax_agent import ExpectimaxAgent
import time

def test_single_game_verbose():
    """Run one game with detailed output"""
    print("="*60)
    print("TESTING IMPROVED AGENT - SINGLE GAME")
    print("="*60)
    
    game = Game2048()
    agent = ExpectimaxAgent(depth=4)
    
    print("Starting game with depth=4...")
    print("Initial board:")
    print(game)
    
    moves = 0
    milestone_tiles = {128, 256, 512, 1024, 2048}
    reached_tiles = set()
    
    while not game.is_game_over() and moves < 3000:
        move = agent.get_best_move(game)
        if move is None:
            break
        
        moved, points = game.move(move)
        if moved:
            game.add_random_tile()
            moves += 1
            
            max_tile = game.get_max_tile()
            
            # Report when reaching milestones
            if max_tile in milestone_tiles and max_tile not in reached_tiles:
                reached_tiles.add(max_tile)
                print(f"\n🎯 Reached {max_tile} tile! (Move {moves}, Score: {game.score})")
            
            # Progress update every 100 moves
            if moves % 100 == 0:
                print(f"Move {moves}: Score={game.score}, Max Tile={max_tile}")
    
    print("\n" + "="*60)
    print("GAME OVER")
    print("="*60)
    print(game)
    print(f"\nFinal Score: {game.score}")
    print(f"Max Tile: {game.get_max_tile()}")
    print(f"Total Moves: {moves}")
    print(f"Reached 2048: {'YES! 🎉' if game.get_max_tile() >= 2048 else 'No'}")
    print("="*60)

def test_quick_benchmark():
    """Run 5 games quickly to check performance"""
    print("="*60)
    print("QUICK BENCHMARK - 5 GAMES (Depth 4)")
    print("="*60)
    
    agent = ExpectimaxAgent(depth=4)
    results = []
    
    for i in range(5):
        print(f"\nGame {i+1}/5...")
        game = Game2048()
        moves = 0
        start = time.time()
        
        while not game.is_game_over() and moves < 3000:
            move = agent.get_best_move(game)
            if move is None:
                break
            moved, _ = game.move(move)
            if moved:
                game.add_random_tile()
                moves += 1
        
        elapsed = time.time() - start
        
        results.append({
            'score': game.score,
            'max_tile': game.get_max_tile(),
            'moves': moves,
            'time': elapsed
        })
        
        won = "🎉 WON!" if game.get_max_tile() >= 2048 else ""
        print(f"  Score: {game.score:6} | Max Tile: {game.get_max_tile():4} | Moves: {moves:4} | Time: {elapsed:.1f}s {won}")
    
    # Summary
    avg_score = sum(r['score'] for r in results) / len(results)
    avg_tile = sum(r['max_tile'] for r in results) / len(results)
    max_tile = max(r['max_tile'] for r in results)
    won_2048 = sum(1 for r in results if r['max_tile'] >= 2048)
    won_1024 = sum(1 for r in results if r['max_tile'] >= 1024)
    won_512 = sum(1 for r in results if r['max_tile'] >= 512)
    avg_time = sum(r['time'] for r in results) / len(results)
    
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    print(f"Average Score:      {avg_score:.1f}")
    print(f"Average Max Tile:   {avg_tile:.1f}")
    print(f"Highest Tile:       {max_tile}")
    print(f"Average Time:       {avg_time:.1f}s")
    print(f"\nTile Achievement Rates:")
    print(f"  Reached 512:      {won_512}/5 ({won_512*20}%)")
    print(f"  Reached 1024:     {won_1024}/5 ({won_1024*20}%)")
    print(f"  Reached 2048:     {won_2048}/5 ({won_2048*20}%)")
    print("="*60)
    
    if won_2048 >= 3:
        print("\n✓ EXCELLENT! Agent is performing as expected.")
        print("  Ready for full experiments!")
    elif won_1024 >= 4:
        print("\n✓ GOOD! Agent reaching 1024 consistently.")
        print("  Should reach 2048 in longer runs.")
    elif won_512 >= 4:
        print("\n⚠ Moderate performance. Agent reaching 512.")
        print("  Performance is better but may need more tuning.")
    else:
        print("\n⚠ Performance still needs improvement.")
        print("  The agent is working but not optimal yet.")

def compare_depths():
    """Compare different search depths"""
    print("="*60)
    print("DEPTH COMPARISON")
    print("="*60)
    
    for depth in [3, 4, 5]:
        print(f"\n--- Testing Depth {depth} (2 games) ---")
        agent = ExpectimaxAgent(depth=depth)
        
        scores = []
        max_tiles = []
        times = []
        
        for i in range(2):
            game = Game2048()
            moves = 0
            start = time.time()
            
            while not game.is_game_over() and moves < 2000:
                move = agent.get_best_move(game)
                if move is None:
                    break
                moved, _ = game.move(move)
                if moved:
                    game.add_random_tile()
                    moves += 1
            
            elapsed = time.time() - start
            scores.append(game.score)
            max_tiles.append(game.get_max_tile())
            times.append(elapsed)
            
            print(f"  Game {i+1}: Score={game.score:5}, Max Tile={game.get_max_tile():4}, Time={elapsed:.1f}s")
        
        avg_score = sum(scores) / len(scores)
        avg_tile = sum(max_tiles) / len(max_tiles)
        avg_time = sum(times) / len(times)
        
        print(f"  Average: Score={avg_score:.0f}, Max Tile={avg_tile:.0f}, Time={avg_time:.1f}s")
    
    print("\n" + "="*60)
    print("Depth 4-5 should show best performance!")
    print("="*60)

if __name__ == "__main__":
    print("\nImproved Agent Test Suite")
    print("="*60)
    print("Choose test:")
    print("1. Single game with verbose output (~2-5 min)")
    print("2. Quick benchmark (5 games, ~10-15 min)")
    print("3. Compare depths 3, 4, 5 (6 games, ~15-20 min)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        test_single_game_verbose()
    elif choice == "2":
        test_quick_benchmark()
    elif choice == "3":
        compare_depths()
    else:
        print("Exiting...")