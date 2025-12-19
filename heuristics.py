import math

class Heuristics:
    """Collection of heuristic evaluation functions for 2048 board states"""
    
    @staticmethod
    def evaluate(board, weights=None):
        """
        Combined heuristic evaluation of a board state.
        Higher scores indicate better positions.
        
        Args:
            board: 2D list representing the game board
            weights: Dict of weights for each heuristic component
        """
        if weights is None:
            weights = {
                'empty_tiles': 10.0,
                'monotonicity': 4.0,
                'smoothness': 0.5,
                'max_tile': 2.0,
                'corner_bonus': 1.0
            }
        
        score = 0
        score += weights['empty_tiles'] * Heuristics.empty_tiles(board)
        score += weights['monotonicity'] * Heuristics.monotonicity(board)
        score += weights['smoothness'] * Heuristics.smoothness(board)
        score += weights['max_tile'] * Heuristics.max_tile_score(board)
        score += weights.get('corner_bonus', 1.0) * Heuristics.corner_bonus(board)
        
        return score
    
    @staticmethod
    def empty_tiles(board):
        """Count empty tiles - more empty tiles is better"""
        count = sum(1 for row in board for cell in row if cell == 0)
        return count ** 2  # Square to emphasize importance
    
    @staticmethod
    def monotonicity(board):
        """
        Measure how monotonic the board is (tiles increase/decrease in order).
        Snake pattern: high values in corners, decreasing toward opposite corner.
        """
        size = len(board)
        totals = [0, 0, 0, 0]  # up, down, left, right
        
        # Check rows (left and right)
        for row in board:
            current_left = 0
            current_right = 0
            for j in range(size - 1):
                if row[j] != 0 and row[j+1] != 0:
                    current_left += (row[j] - row[j+1]) if row[j] > row[j+1] else 0
                    current_right += (row[j+1] - row[j]) if row[j+1] > row[j] else 0
            totals[2] += current_left
            totals[3] += current_right
        
        # Check columns (up and down)
        for j in range(size):
            current_up = 0
            current_down = 0
            for i in range(size - 1):
                if board[i][j] != 0 and board[i+1][j] != 0:
                    current_up += (board[i][j] - board[i+1][j]) if board[i][j] > board[i+1][j] else 0
                    current_down += (board[i+1][j] - board[i][j]) if board[i+1][j] > board[i][j] else 0
            totals[0] += current_up
            totals[1] += current_down
        
        return max(totals[0], totals[1]) + max(totals[2], totals[3])
    
    @staticmethod
    def smoothness(board):
        """
        Measure how smooth the board is (similar values adjacent).
        Lower difference between adjacent tiles is better.
        Returns negative value (penalty), so higher (closer to 0) is better.
        """
        size = len(board)
        smoothness = 0
        
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    value = math.log2(board[i][j])
                    
                    # Compare with right neighbor
                    if j < size - 1 and board[i][j+1] != 0:
                        target_value = math.log2(board[i][j+1])
                        smoothness -= abs(value - target_value)
                    
                    # Compare with bottom neighbor
                    if i < size - 1 and board[i+1][j] != 0:
                        target_value = math.log2(board[i+1][j])
                        smoothness -= abs(value - target_value)
        
        return smoothness
    
    @staticmethod
    def max_tile_score(board):
        """
        Reward for having high-value tiles.
        Uses log to prevent exponential growth dominating other heuristics.
        """
        max_tile = max(max(row) for row in board)
        if max_tile == 0:
            return 0
        return math.log2(max_tile)
    
    @staticmethod
    def corner_bonus(board):
        """
        Bonus for keeping the max tile in a corner.
        Helps maintain snake pattern.
        """
        max_tile = max(max(row) for row in board)
        size = len(board)
        corners = [
            board[0][0], 
            board[0][size-1], 
            board[size-1][0], 
            board[size-1][size-1]
        ]
        
        if max_tile in corners:
            return 20000
        return 0
    
    @staticmethod
    def merge_potential(board):
        """
        Count how many tiles can potentially merge.
        More merge opportunities is better.
        """
        size = len(board)
        merge_count = 0
        
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    # Check right
                    if j < size - 1 and board[i][j] == board[i][j+1]:
                        merge_count += 1
                    # Check down
                    if i < size - 1 and board[i][j] == board[i+1][j]:
                        merge_count += 1
        
        return merge_count