import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_results(filename="results.json"):
    """Load experiment results from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def plot_score_distributions(results, save_path=os.path.join(RESULTS_DIR, "score_distributions.png")):
    """Plot score distributions for different agent configurations"""
    fig, axes = plt.subplots(1, len(results), figsize=(6*len(results), 5))
    
    if len(results) == 1:
        axes = [axes]
    
    for idx, experiment in enumerate(results):
        scores = [game['final_score'] for game in experiment['games']]
        
        axes[idx].hist(scores, bins=20, edgecolor='black', alpha=0.7)
        axes[idx].set_xlabel('Final Score', fontsize=12)
        axes[idx].set_ylabel('Frequency', fontsize=12)
        axes[idx].set_title(f"{experiment['agent_type']}\n(Depth: {experiment['agent_params'].get('depth', 'N/A')})", fontsize=14)
        axes[idx].axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(scores):.0f}')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_max_tile_distribution(results, save_path=os.path.join(RESULTS_DIR, "max_tile_distribution.png")):
    """Plot distribution of maximum tiles achieved"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    tile_values = [128, 256, 512, 1024, 2048, 4096, 8192]
    x = np.arange(len(tile_values))
    width = 0.8 / len(results)
    
    for idx, experiment in enumerate(results):
        max_tiles = [game['max_tile'] for game in experiment['games']]
        tile_counts = Counter(max_tiles)
        
        counts = [tile_counts[tile] for tile in tile_values]
        label = f"{experiment['agent_type']} (d={experiment['agent_params'].get('depth', 'N/A')})"
        
        ax.bar(x + idx * width, counts, width, label=label, alpha=0.8)
    
    ax.set_xlabel('Maximum Tile Achieved', fontsize=12)
    ax.set_ylabel('Number of Games', fontsize=12)
    ax.set_title('Distribution of Maximum Tiles Achieved', fontsize=14)
    ax.set_xticks(x + width * (len(results) - 1) / 2)
    ax.set_xticklabels(tile_values)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_performance_comparison(results, save_path=os.path.join(RESULTS_DIR, "performance_comparison.png")):
    """Compare key metrics across different configurations"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    agent_labels = [f"{exp['agent_type']}\n(d={exp['agent_params'].get('depth', 'N/A')})" 
                    for exp in results]
    
    # Average Score
    avg_scores = [exp['statistics']['avg_score'] for exp in results]
    axes[0, 0].bar(agent_labels, avg_scores, color='steelblue', alpha=0.7)
    axes[0, 0].set_ylabel('Average Score', fontsize=11)
    axes[0, 0].set_title('Average Final Score', fontsize=12)
    axes[0, 0].tick_params(axis='x', rotation=15)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # Win Rate (2048)
    win_rates = [exp['statistics']['win_rate_2048'] * 100 for exp in results]
    axes[0, 1].bar(agent_labels, win_rates, color='green', alpha=0.7)
    axes[0, 1].set_ylabel('Win Rate (%)', fontsize=11)
    axes[0, 1].set_title('Percentage Reaching 2048 Tile', fontsize=12)
    axes[0, 1].tick_params(axis='x', rotation=15)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Average Moves
    avg_moves = [exp['statistics']['avg_moves'] for exp in results]
    axes[1, 0].bar(agent_labels, avg_moves, color='orange', alpha=0.7)
    axes[1, 0].set_ylabel('Average Moves', fontsize=11)
    axes[1, 0].set_title('Average Game Length (Moves)', fontsize=12)
    axes[1, 0].tick_params(axis='x', rotation=15)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Time per Move
    avg_times = [exp['statistics']['avg_time_per_move'] * 1000 for exp in results]  # Convert to ms
    axes[1, 1].bar(agent_labels, avg_times, color='red', alpha=0.7)
    axes[1, 1].set_ylabel('Time per Move (ms)', fontsize=11)
    axes[1, 1].set_title('Average Time per Move', fontsize=12)
    axes[1, 1].tick_params(axis='x', rotation=15)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def plot_tile_achievement_rates(results, save_path=os.path.join(RESULTS_DIR, "tile_achievements.png")):
    """Plot achievement rates for different tile milestones"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    tiles = [128, 256, 512, 1024, 2048, 4096]
    x = np.arange(len(tiles))
    width = 0.8 / len(results)
    
    for idx, experiment in enumerate(results):
        stats = experiment['statistics']
        rates = []
        for tile in tiles:
            count = stats.get(f'reached_{tile}', 0)
            rate = (count / experiment['num_games']) * 100
            rates.append(rate)
        
        label = f"{experiment['agent_type']} (d={experiment['agent_params'].get('depth', 'N/A')})"
        ax.bar(x + idx * width, rates, width, label=label, alpha=0.8)
    
    ax.set_xlabel('Tile Value', fontsize=12)
    ax.set_ylabel('Achievement Rate (%)', fontsize=12)
    ax.set_title('Percentage of Games Reaching Each Tile', fontsize=14)
    ax.set_xticks(x + width * (len(results) - 1) / 2)
    ax.set_xticklabels(tiles)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 105])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()

def generate_all_visualizations(results_file="results.json"):
    """Generate all visualization plots from results"""
    print("Loading results...")
    results = load_results(results_file)
    
    print(f"Generating visualizations for {len(results)} experiments...")
    
    plot_score_distributions(results)
    plot_max_tile_distribution(results)
    plot_performance_comparison(results)
    plot_tile_achievement_rates(results)
    
    print("\n✓ All visualizations generated successfully!")

if __name__ == "__main__":
    generate_all_visualizations()
