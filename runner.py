import json
import time
from datetime import datetime
from game import Game2048
from expectimax_agent import ExpectimaxAgent, GreedyAgent
from tqdm import tqdm

class ExperimentRunner:
    """Run experiments and collect performance data"""
    
    def __init__(self, output_file="results.json"):
        self.output_file = output_file
        self.results = []
    
    def run_single_game(self, agent, max_moves=10000, verbose=False):
        """
        Run a single game with the given agent.
        
        Returns:
            Dict with game statistics
        """
        game = Game2048()
        moves = 0
        total_time = 0
        total_nodes = 0
        move_history = []
        
        while not game.is_game_over() and moves < max_moves:
            if verbose and moves % 100 == 0:
                print(f"\nMove {moves}:")
                print(game)
            
            move = agent.get_best_move(game)
            if move is None:
                break
            
            moved, points = game.move(move)
            if moved:
                game.add_random_tile()
                moves += 1
                
                # Collect stats
                stats = agent.get_stats()
                total_time += stats.get('time_taken', 0)
                total_nodes += stats.get('nodes_explored', 0)
                
                move_history.append({
                    'move': move,
                    'score': game.score,
                    'max_tile': game.get_max_tile()
                })
        
        result = {
            'final_score': game.score,
            'max_tile': game.get_max_tile(),
            'moves': moves,
            'won_2048': game.get_max_tile() >= 2048,
            'won_4096': game.get_max_tile() >= 4096,
            'total_time': total_time,
            'total_nodes': total_nodes,
            'avg_time_per_move': total_time / moves if moves > 0 else 0,
            'avg_nodes_per_move': total_nodes / moves if moves > 0 else 0,
            'board': game.board
        }
        
        if verbose:
            print("\n" + "="*50)
            print("GAME OVER")
            print(game)
            print(f"Max Tile: {result['max_tile']}")
            print(f"Final Score: {result['final_score']}")
            print(f"Total Moves: {result['moves']}")
            print(f"Avg Time/Move: {result['avg_time_per_move']:.3f}s")
            print("="*50)
        
        return result
    
    def run_experiments(self, agent_config, num_games=50, verbose=False):
        """
        Run multiple games with the same agent configuration.
        
        Args:
            agent_config: Dict with 'type' and 'params' for agent
            num_games: Number of games to run
            verbose: Whether to print progress
        """
        print(f"\nRunning {num_games} games with {agent_config['type']}...")
        print(f"Configuration: {agent_config['params']}")
        
        experiment_results = {
            'agent_type': agent_config['type'],
            'agent_params': agent_config['params'],
            'num_games': num_games,
            'timestamp': datetime.now().isoformat(),
            'games': []
        }
        
        # Create agent based on config
        if agent_config['type'] == 'expectimax':
            agent = ExpectimaxAgent(**agent_config['params'])
        elif agent_config['type'] == 'greedy':
            agent = GreedyAgent()
        else:
            raise ValueError(f"Unknown agent type: {agent_config['type']}")
        
        # Run games with progress bar
        for i in tqdm(range(num_games), desc="Games"):
            result = self.run_single_game(agent, verbose=verbose)
            result['game_number'] = i + 1
            experiment_results['games'].append(result)
        
        # Compute aggregate statistics
        experiment_results['statistics'] = self._compute_statistics(experiment_results['games'])
        
        self.results.append(experiment_results)
        self._save_results()
        
        return experiment_results
    
    def _compute_statistics(self, games):
        """Compute aggregate statistics from game results"""
        if not games:
            return {}
        
        scores = [g['final_score'] for g in games]
        max_tiles = [g['max_tile'] for g in games]
        moves = [g['moves'] for g in games]
        times = [g['avg_time_per_move'] for g in games]
        
        # Count tile achievements
        tile_counts = {}
        for tile in [128, 256, 512, 1024, 2048, 4096, 8192]:
            tile_counts[f'reached_{tile}'] = sum(1 for t in max_tiles if t >= tile)
        
        return {
            'avg_score': sum(scores) / len(scores),
            'max_score': max(scores),
            'min_score': min(scores),
            'avg_max_tile': sum(max_tiles) / len(max_tiles),
            'highest_tile': max(max_tiles),
            'avg_moves': sum(moves) / len(moves),
            'avg_time_per_move': sum(times) / len(times),
            'win_rate_2048': sum(1 for g in games if g['won_2048']) / len(games),
            'win_rate_4096': sum(1 for g in games if g['won_4096']) / len(games),
            **tile_counts
        }
    
    def _save_results(self):
        """Save results to JSON file"""
        with open(self.output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {self.output_file}")
    
    def print_summary(self, experiment_results):
        """Print a summary of experiment results"""
        stats = experiment_results['statistics']
        
        print("\n" + "="*60)
        print(f"EXPERIMENT SUMMARY: {experiment_results['agent_type']}")
        print("="*60)
        print(f"Number of games: {experiment_results['num_games']}")
        print(f"\nScore Statistics:")
        print(f"  Average Score: {stats['avg_score']:.1f}")
        print(f"  Max Score: {stats['max_score']}")
        print(f"  Min Score: {stats['min_score']}")
        print(f"\nTile Achievements:")
        print(f"  Average Max Tile: {stats['avg_max_tile']:.1f}")
        print(f"  Highest Tile Reached: {stats['highest_tile']}")
        print(f"  Reached 2048: {stats['reached_2048']}/{experiment_results['num_games']} ({stats['win_rate_2048']*100:.1f}%)")
        print(f"  Reached 4096: {stats['reached_4096']}/{experiment_results['num_games']} ({stats['win_rate_4096']*100:.1f}%)")
        print(f"\nPerformance:")
        print(f"  Average Moves: {stats['avg_moves']:.1f}")
        print(f"  Avg Time per Move: {stats['avg_time_per_move']:.3f}s")
        print("="*60)


def main():
    """Run experiments with different configurations"""
    runner = ExperimentRunner(output_file="results.json")
    
    # Experiment 1: Expectimax with depth 3
    print("\n### EXPERIMENT 1: Expectimax (Depth 3) ###")
    config1 = {
        'type': 'expectimax',
        'params': {'depth': 3}
    }
    results1 = runner.run_experiments(config1, num_games=20, verbose=False)
    runner.print_summary(results1)
    
    # Experiment 2: Expectimax with depth 4
    print("\n### EXPERIMENT 2: Expectimax (Depth 4) ###")
    config2 = {
        'type': 'expectimax',
        'params': {'depth': 4}
    }
    results2 = runner.run_experiments(config2, num_games=20, verbose=False)
    runner.print_summary(results2)
    
    # Experiment 3: Greedy baseline
    print("\n### EXPERIMENT 3: Greedy Baseline ###")
    config3 = {
        'type': 'greedy',
        'params': {}
    }
    results3 = runner.run_experiments(config3, num_games=20, verbose=False)
    runner.print_summary(results3)
    
    # Experiment 4: Ablation study - No smoothness
    print("\n### EXPERIMENT 4: Ablation - No Smoothness ###")
    config4 = {
        'type': 'expectimax',
        'params': {
            'depth': 3,
            'heuristic_weights': {
                'empty_tiles': 2.7,
                'monotonicity': 1.0,
                'smoothness': 0.0,
                'max_tile': 1.0
            }
        }
    }
    results4 = runner.run_experiments(config4, num_games=10, verbose=False)
    runner.print_summary(results4)
    
    print("\n✓ All experiments complete!")
    print(f"Results saved to {runner.output_file}")


if __name__ == "__main__":
    main()