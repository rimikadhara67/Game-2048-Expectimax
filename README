# 2048 Expectimax Solver

An AI agent that solves the 2048 puzzle game using Expectimax search with optimized heuristics.

## Project Overview

This project implements an Expectimax search algorithm to play 2048 optimally. The agent models the game as alternating between:
- **Max nodes**: Player choosing the best move
- **Chance nodes**: Random tile placement (2 with 90% probability, 4 with 10%)

The agent uses a sophisticated evaluation function combining:
- Empty tile count
- Monotonicity (snake pattern)
- Smoothness (adjacent tile similarity)
- Maximum tile value

## File Structure

```
2048-expectimax-solver/
├── game.py                 # Core 2048 game logic
├── expectimax_agent.py     # Expectimax search algorithm
├── heuristics.py           # Evaluation functions
├── runner.py               # Run experiments and collect data
├── visualize.py            # Generate graphs and visualizations
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── report.pdf             # Final project report
```

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Requirements:
- Python 3.7+
- numpy
- matplotlib
- tqdm

## Running the Project

### Quick Test (Single Game)
To run a single game with visualization:

```python
python -c "
from game import Game2048
from expectimax_agent import ExpectimaxAgent

game = Game2048()
agent = ExpectimaxAgent(depth=3)

for i in range(100):
    if game.is_game_over():
        break
    move = agent.get_best_move(game)
    if move is not None:
        game.move(move)
        game.add_random_tile()
    if i % 10 == 0:
        print(f'\nMove {i}:')
        print(game)

print(f'\nFinal Score: {game.score}')
print(f'Max Tile: {game.get_max_tile()}')
"
```

### Full Experiments
To run all experiments (as specified in the proposal):

```bash
python runner.py
```

This will:
- Run 20 games with Expectimax (Depth 3)
- Run 20 games with Expectimax (Depth 4)
- Run 20 games with Greedy baseline
- Run 10 games with ablation study (no smoothness heuristic)
- Save results to `results.json`

**Note**: Full experiments may take 1-3 hours depending on your machine.

### Generate Visualizations
After running experiments:

```bash
python visualize.py
```

This generates:
- `score_distributions.png` - Score distributions
- `max_tile_distribution.png` - Max tiles achieved
- `performance_comparison.png` - Key metrics comparison
- `tile_achievements.png` - Tile achievement rates

## Customizing Experiments

You can modify `runner.py` to test different configurations:

```python
# Example: Test different search depths
config = {
    'type': 'expectimax',
    'params': {'depth': 5}  # Try depth 5
}
results = runner.run_experiments(config, num_games=10)
```

Or adjust heuristic weights:

```python
config = {
    'type': 'expectimax',
    'params': {
        'depth': 4,
        'heuristic_weights': {
            'empty_tiles': 3.0,  # Increased weight
            'monotonicity': 1.5,
            'smoothness': 0.1,
            'max_tile': 1.0
        }
    }
}
```

## Key Implementation Details

### Expectimax Algorithm
- **Max Node**: Player selects move maximizing expected utility
- **Chance Node**: Computes weighted average over all possible tile placements
- **Depth-Limited Search**: Searches 3-4 plies deep with heuristic evaluation at leaves

### Heuristics
1. **Empty Tiles**: Squared count to emphasize keeping board open
2. **Monotonicity**: Rewards snake-like tile arrangement (high to low)
3. **Smoothness**: Penalizes large differences between adjacent tiles
4. **Max Tile**: Log-scaled reward for achieving high tiles

### Performance Optimizations
- Board cloning for state simulation
- Early termination for terminal states
- Efficient move generation

## Expected Results

Based on the proposal and literature:
- **Depth 3**: ~70-80% win rate (reaching 2048)
- **Depth 4**: ~85-95% win rate
- **Greedy**: ~5-15% win rate
- **Ablation (no smoothness)**: ~50-60% win rate

Average scores should be 15,000-40,000 depending on configuration.

## References

1. Nie, H., Hou, A., & An, L. (2016). *AI Plays 2048*. Stanford CS229 Project Report.
2. Lee, K., & Ruan, S. (2019). *2048 optimization using Expectimax and reinforcement learning*. UC San Diego.
3. Xiao, Y., et al. (2014). *Mastering 2048 with Delayed Temporal Coherence Learning*. arXiv:1604.05085.

## Author

[Your Name]  
Final Project - AI/Search Course  
December 2025

## License

This project is for educational purposes.