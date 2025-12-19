from game import Game2048
import math
import time
import random

class ExpectimaxAgent:
    """
    Expectimax agent for 2048 with heuristics
    """
    
    def __init__(self, depth=5, heuristic_weights=None):
        """
        Initialize the Expectimax agent.
        
        Args:
            depth: Maximum search depth (number of plies) - default 5 for good performance
            heuristic_weights: Dict of weights (kept for compatibility, but uses optimized defaults)
        """
        self.depth = depth
        self.heuristic_weights = heuristic_weights  # Kept for compatibility
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
            return self._evaluate(game.board)
        
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
            return self._evaluate(game.board)
        
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
        Tiles can be 2 (90% probability) or 4 (10% probability).
        """
        empty_cells = game.get_empty_cells()
        
        if not empty_cells:
            return self._evaluate(game.board)
        
        # More conservative sampling - only sample when really necessary
        num_empty = len(empty_cells)
        if num_empty > 10 and depth <= 1:
            # Only sample at very shallow depths with many empty cells
            sampled_cells = random.sample(empty_cells, min(8, num_empty))
        elif num_empty > 6:
            # Use more cells in mid-game
            sampled_cells = random.sample(empty_cells, min(num_empty, 6))
        else:
            # Use all cells when there aren't many
            sampled_cells = empty_cells
        
        expected_score = 0
        
        # For each cell, calculate expected value
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
    
    def _evaluate(self, board):
        """
        Optimized evaluation function for 2048 board states.
        
        Uses adaptive weights based on game phase:
        - Early game (many empty cells): prioritize space and smoothness
        - Late game (few empty cells): prioritize monotonicity
        
        Args:
            board: 2D list representing the game board
            
        Returns:
            Float score (higher is better)
        """
        empty = sum(1 for row in board for cell in row if cell == 0)
        
        # More aggressive adaptive weights
        if empty > 10:
            # Very early game
            w_empty = 150000.0
            w_mono = 3000.0
            w_smooth = 3000.0
        elif empty > 6:
            # Early-mid game
            w_empty = 200000.0
            w_mono = 8000.0
            w_smooth = 2000.0
        else:
            # Late game: monotonicity is critical
            w_empty = 300000.0
            w_mono = 15000.0
            w_smooth = 1000.0
        
        score = 0.0
        
        # 1. Empty tiles (squared for strong emphasis)
        score += w_empty * (empty ** 2)
        
        # 2. Monotonicity (snake pattern)
        score += w_mono * self._monotonicity(board)
        
        # 3. Smoothness (adjacent tile similarity)
        score += w_smooth * self._smoothness(board)
        
        # 4. Max tile value (log scale)
        max_tile = max(max(row) for row in board)
        if max_tile > 0:
            score += 2000.0 * math.log2(max_tile)
        
        # 5. Bonus for high tiles in corners (subtle, not dominating)
        max_tile = max(max(row) for row in board)
        corners = [board[0][0], board[0][3], board[3][0], board[3][3]]
        if max_tile in corners:
            score += 5000.0
        
        return score
    
    def _monotonicity(self, board):
        """
        Calculate monotonicity score.
        Rewards tiles that increase/decrease consistently in one direction.
        Uses log values to normalize across different tile magnitudes.
        """
        totals = [0.0, 0.0, 0.0, 0.0]  # up, down, left, right
        
        for i in range(4):
            for j in range(3):
                # Check rows (left/right monotonicity)
                if board[i][j] > 0 and board[i][j+1] > 0:
                    diff = math.log2(board[i][j]) - math.log2(board[i][j+1])
                    if diff > 0:
                        totals[2] += diff  # Left to right increasing
                    else:
                        totals[3] += -diff  # Right to left increasing
                
                # Check columns (up/down monotonicity)
                if board[j][i] > 0 and board[j+1][i] > 0:
                    diff = math.log2(board[j][i]) - math.log2(board[j+1][i])
                    if diff > 0:
                        totals[0] += diff  # Top to bottom increasing
                    else:
                        totals[1] += -diff  # Bottom to top increasing
        
        # Return best monotonicity direction (snake pattern)
        return max(totals[0], totals[1]) + max(totals[2], totals[3])
    
    def _smoothness(self, board):
        """
        Calculate smoothness score.
        Penalizes large differences between adjacent tiles.
        Uses log values for normalization.
        """
        smoothness = 0.0
        
        for i in range(4):
            for j in range(4):
                if board[i][j] > 0:
                    value = math.log2(board[i][j])
                    
                    # Compare with right neighbor
                    if j < 3 and board[i][j+1] > 0:
                        smoothness -= abs(value - math.log2(board[i][j+1]))
                    
                    # Compare with bottom neighbor
                    if i < 3 and board[i+1][j] > 0:
                        smoothness -= abs(value - math.log2(board[i+1][j]))
        
        return smoothness
    
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
            
            # Simple evaluation: immediate points + empty cells
            empty = sum(1 for row in test_game.board for cell in row if cell == 0)
            score = points + empty * 100
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_stats(self):
        return {'nodes_explored': 0, 'time_taken': 0, 'nodes_per_second': 0}