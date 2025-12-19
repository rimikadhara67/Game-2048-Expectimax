from game import Game2048
from heuristics import Heuristics
import time
import random

class ExpectimaxAgent:
    """
    AI agent that uses Expectimax search to play 2048.
    Alternates between Max nodes (player moves) and Chance nodes (random tile placement).
    """
    
    def __init__(self, depth=4, heuristic_weights=None):
        """
        Initialize the Expectimax agent.
        
        Args:
            depth: Maximum search depth (number of plies)
            heuristic_weights: Dict of weights for heuristic evaluation
        """
        self.depth = depth
        self.heuristic_weights = heuristic_weights
        self.nodes_explored = 0
        self.time_taken = 0
    
    def get_best_move(self, game):
        """
        Determine the best move using Expectimax search.
        
        Args:
            game: Game2048 instance
            
        Returns:
            Best move direction (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT)
        """
        start_time = time.time()
        self.nodes_explored = 0
        
        available_moves = game.get_available_moves()
        if not available_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        
        for move in available_moves:
            # Simulate the move
            test_game = game.clone()
            test_game.move(move)
            
            # Evaluate using expectimax (chance node follows player move)
            score = self._expectimax(test_game, self.depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        self.time_taken = time.time() - start_time
        return best_move
    
    def _expectimax(self, game, depth, is_max_node):
        """
        Recursive Expectimax search.
        
        Args:
            game: Current game state
            depth: Remaining search depth
            is_max_node: True if this is a maximizing node (player's turn),
                        False if chance node (random tile placement)
        
        Returns:
            Expected utility of this state
        """
        self.nodes_explored += 1
        
        # Terminal conditions
        if depth == 0 or game.is_game_over():
            return Heuristics.evaluate(game.board, self.heuristic_weights)
        
        if is_max_node:
            # Maximizing node: player chooses best move
            return self._max_node(game, depth)
        else:
            # Chance node: random tile placement
            return self._chance_node(game, depth)
    
    def _max_node(self, game, depth):
        """
        Maximizing node: player tries to maximize score.
        """
        max_score = float('-inf')
        available_moves = game.get_available_moves()
        
        if not available_moves:
            return Heuristics.evaluate(game.board, self.heuristic_weights)
        
        for move in available_moves:
            test_game = game.clone()
            test_game.move(move)
            
            # After player moves, chance node follows
            score = self._expectimax(test_game, depth - 1, False)
            max_score = max(max_score, score)
        
        return max_score
    
    def _chance_node(self, game, depth):
        """
        Chance node: compute expected value over possible tile placements.
        Uses sampling for efficiency at deeper levels.
        """
        empty_cells = game.get_empty_cells()
        
        if not empty_cells:
            return Heuristics.evaluate(game.board, self.heuristic_weights)
        
        # For efficiency: sample cells if there are many empty cells
        num_empty = len(empty_cells)
        
        # If many empty cells and deep in tree, sample a subset
        if num_empty > 6 and depth < 2:
            # Sample up to 4 random positions
            sampled_cells = random.sample(empty_cells, min(4, num_empty))
        else:
            # Use all empty cells
            sampled_cells = empty_cells
        
        expected_score = 0
        
        # For each sampled cell, calculate expected value
        for i, j in sampled_cells:
            # Try placing a 2 (90% probability)
            test_game = game.clone()
            test_game.board[i][j] = 2
            score_2 = self._expectimax(test_game, depth - 1, True)
            
            # Try placing a 4 (10% probability)
            test_game = game.clone()
            test_game.board[i][j] = 4
            score_4 = self._expectimax(test_game, depth - 1, True)
            
            # Expected value for this cell
            cell_expected = 0.9 * score_2 + 0.1 * score_4
            expected_score += cell_expected
        
        # Average over sampled positions
        return expected_score / len(sampled_cells)
    
    def get_stats(self):
        """Return statistics about the last search"""
        return {
            'nodes_explored': self.nodes_explored,
            'time_taken': self.time_taken,
            'nodes_per_second': self.nodes_explored / self.time_taken if self.time_taken > 0 else 0
        }


class GreedyAgent:
    """Baseline greedy agent for comparison (always picks move with highest immediate score)"""
    
    def get_best_move(self, game):
        """Choose move that gives highest immediate score"""
        available_moves = game.get_available_moves()
        if not available_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        
        for move in available_moves:
            test_game = game.clone()
            _, points = test_game.move(move)
            score = points + Heuristics.evaluate(test_game.board)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_stats(self):
        return {'nodes_explored': 0, 'time_taken': 0, 'nodes_per_second': 0}