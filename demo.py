"""
Quick demo script to test the 2048 Expectimax solver
Run this to see the agent play a single game with visualization
"""

from game import Game2048
from expectimax_agent import ExpectimaxAgent
import time

def play_demo_game(depth=3, max_moves=500, delay=0.5):
    """
    Play a demo game with visualization
    
    Args:
        depth: Search depth for Expectimax
        max_moves: Maximum number of moves to play
        delay: Delay between moves in seconds (for visualization)
    """
    print("="*60)
    print("2048 EXPECTIMAX SOLVER - DEMO")
    print("="*60)
    print(f"Configuration: Depth={depth}")
    print(f"Press Ctrl+C to stop early\n")
    
    game = Game2048()
    agent = ExpectimaxAgent(depth=depth)
    
    move_names = ["UP", "RIGHT", "DOWN", "LEFT"]
    
    print("Starting board:")
    print(game)
    print("\nPress Enter to start...")
    input()
    
    moves = 0
    total_time = 0
    
    try:
        while not game.is_game_over() and moves < max_moves:
            # Get best move from agent
            start = time.time()
            move = agent.get_best_move(game)
            elapsed = time.time() - start
            total_time += elapsed
            
            if move is None:
                break
            
            # Execute move
            moved, points = game.move(move)
            if moved:
                game.add_random_tile()
                moves += 1
                
                # Display
                print(f"\n{'='*60}")
                print(f"Move {moves}: {move_names[move]}")
                print(f"Time: {elapsed:.2f}s | Nodes: {agent.nodes_explored}")
                print(game)
                
                if delay > 0:
                    time.sleep(delay)
        
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user.")
    
    # Final summary
    print("\n" + "="*60)
    print("GAME OVER - FINAL RESULTS")
    print("="*60)
    print(f"Final Score: {game.score}")
    print(f"Max Tile: {game.get_max_tile()}")
    print(f"Total Moves: {moves}")
    print(f"Average Time/Move: {total_time/moves:.3f}s")
    print(f"Won (2048): {'YES! 🎉' if game.get_max_tile() >= 2048 else 'No'}")
    print("="*60)


def quick_benchmark():
    """Run a quick 5-game benchmark"""
    print("\n" + "="*60)
    print("QUICK BENCHMARK - 5 GAMES")
    print("="*60)
    
    agent = ExpectimaxAgent(depth=3)
    results = []
    
    for i in range(5):
        print(f"\nGame {i+1}/5...")
        game = Game2048()
        moves = 0
        
        while not game.is_game_over() and moves < 1000:
            move = agent.get_best_move(game)
            if move is None:
                break
            moved, _ = game.move(move)
            if moved:
                game.add_random_tile()
                moves += 1
        
        results.append({
            'score': game.score,
            'max_tile': game.get_max_tile(),
            'moves': moves
        })
        
        print(f"  Score: {game.score} | Max Tile: {game.get_max_tile()} | Moves: {moves}")
    
    # Summary
    avg_score = sum(r['score'] for r in results) / len(results)
    avg_tile = sum(r['max_tile'] for r in results) / len(results)
    won = sum(1 for r in results if r['max_tile'] >= 2048)
    
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    print(f"Average Score: {avg_score:.1f}")
    print(f"Average Max Tile: {avg_tile:.1f}")
    print(f"Games Reaching 2048: {won}/5 ({won*20}%)")
    print("="*60)


if __name__ == "__main__":
    import sys
    
    print("\n2048 EXPECTIMAX SOLVER")
    print("="*60)
    print("Choose an option:")
    print("1. Play demo game (watch agent play with visualization)")
    print("2. Quick benchmark (5 games, no visualization)")
    print("3. Exit")
    print("="*60)
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        # Ask for depth
        depth_input = input("\nEnter search depth (2-5, recommended 3): ").strip()
        try:
            depth = int(depth_input)
            depth = max(2, min(5, depth))
        except:
            depth = 3
            print(f"Invalid input, using depth={depth}")
        
        play_demo_game(depth=depth, delay=0.3)
    
    elif choice == "2":
        quick_benchmark()
    
    else:
        print("Exiting...")
        