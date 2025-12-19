import random
import copy

class Game2048:
    """Core 2048 game logic"""
    
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
    
    def add_random_tile(self):
        """Add a random tile (2 with 90% probability, 4 with 10%)"""
        empty_cells = [(i, j) for i in range(self.size) 
                       for j in range(self.size) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            return True
        return False
    
    def get_empty_cells(self):
        """Return list of empty cell coordinates"""
        return [(i, j) for i in range(self.size) 
                for j in range(self.size) if self.board[i][j] == 0]
    
    def clone(self):
        """Create a deep copy of the game state"""
        new_game = Game2048(self.size)
        new_game.board = copy.deepcopy(self.board)
        new_game.score = self.score
        return new_game
    
    def move(self, direction):
        """
        Attempt to move in the given direction.
        Returns (success, points_earned)
        Directions: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
        """
        original = copy.deepcopy(self.board)
        points = 0
        
        if direction == 0:  # UP
            points = self._move_up()
        elif direction == 1:  # RIGHT
            points = self._move_right()
        elif direction == 2:  # DOWN
            points = self._move_down()
        elif direction == 3:  # LEFT
            points = self._move_left()
        
        moved = (original != self.board)
        if moved:
            self.score += points
        
        return moved, points
    
    def _move_left(self):
        """Move all tiles left and merge"""
        points = 0
        for i in range(self.size):
            # Compress: move all non-zero tiles left
            row = [x for x in self.board[i] if x != 0]
            # Merge adjacent equal tiles
            merged = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    merged.append(row[j] * 2)
                    points += row[j] * 2
                    skip = True
                else:
                    merged.append(row[j])
            # Pad with zeros
            merged += [0] * (self.size - len(merged))
            self.board[i] = merged
        return points
    
    def _move_right(self):
        """Move all tiles right and merge"""
        self._reverse_board()
        points = self._move_left()
        self._reverse_board()
        return points
    
    def _move_up(self):
        """Move all tiles up and merge"""
        self._transpose_board()
        points = self._move_left()
        self._transpose_board()
        return points
    
    def _move_down(self):
        """Move all tiles down and merge"""
        self._transpose_board()
        points = self._move_right()
        self._transpose_board()
        return points
    
    def _transpose_board(self):
        """Transpose the board (swap rows and columns)"""
        self.board = [list(row) for row in zip(*self.board)]
    
    def _reverse_board(self):
        """Reverse each row of the board"""
        self.board = [row[::-1] for row in self.board]
    
    def get_available_moves(self):
        """Return list of valid move directions"""
        moves = []
        for direction in range(4):
            test_game = self.clone()
            moved, _ = test_game.move(direction)
            if moved:
                moves.append(direction)
        return moves
    
    def is_game_over(self):
        """Check if no moves are available"""
        return len(self.get_available_moves()) == 0
    
    def get_max_tile(self):
        """Return the maximum tile value on the board"""
        return max(max(row) for row in self.board)
    
    def __str__(self):
        """String representation of the board"""
        s = f"Score: {self.score}\n"
        s += "-" * (self.size * 6 + 1) + "\n"
        for row in self.board:
            s += "|" + "|".join(f"{cell:5}" if cell else "     " for cell in row) + "|\n"
        s += "-" * (self.size * 6 + 1)
        return s