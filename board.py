""" Game logic."""
from config import WHITE, BLACK, EMPTY
from copy import deepcopy


# Defines the Board class, which represents the game state and contains methods 
# to handle game logic, such as valid moves, board updates, and game status.
class Board:
# Initializes the board and its default state.

    """ Rules of the game """
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE
        self.valid_moves = []

# Allows accessing a specific position on the board using board[i, j] syntax.
    def __getitem__(self, i, j):
        return self.board[i][j]

#  lookup and Finds valid positions to place a piece of the given color starting from (row, column).
    def lookup(self, row, column, color):

        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []

        if row < 0 or row > 7 or column < 0 or column > 7:
            return places # return blank list

        # For each direction search for possible positions to put a piece.
        directions = [
            (0, 1),      
            (0, -1),     
            (-1, 1),     
            (1, 1),      
            (1, -1),     
            (-1, -1),     
            (1, 0),      
            (-1, 0),     
        ]
# Collects all valid positions and returns them as a list
        for (x, y) in directions:
            pos = self.check_direction(row, column, x, y, other)
            if pos:
                places.append(pos)
        return places

# Checks in a specific direction if a move can flip opponent's pieces.
    def check_direction(self, row, column, row_add, column_add, other_color):

# Directional increments for row and column.
        i = row + row_add
        j = column + column_add
        if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
            i += row_add
            j += column_add
            while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
                i += row_add
                j += column_add              
            if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == EMPTY):                
                return (i, j)

#  Identifies all valid moves for a player of the given color.
    def get_valid_moves(self, color):

        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []
    # Iterate through the board to find all positions of the given color.
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    # Look up valid moves from the current position and add them to the list.
                    places = places + self.lookup(i, j, color)

    # Remove duplicate positions and update the valid moves.
        places = list(set(places))
        self.valid_moves = places
        return places

# Applies a move to the board and flips opponent's pieces.
    def apply_move(self, move, color):

        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            for i in range(1, 9):
                self.flip(i, move, color)

# Flips opponent's pieces in a specific direction after a valid move.

    def flip(self, direction, position, color):

        if direction == 1:
            # north
            row_inc = -1
            col_inc = 0
        elif direction == 2:
            # northeast
            row_inc = -1
            col_inc = 1
        elif direction == 3:
            # east
            row_inc = 0
            col_inc = 1
        elif direction == 4:
            # southeast
            row_inc = 1
            col_inc = 1
        elif direction == 5:
            # south
            row_inc = 1
            col_inc = 0
        elif direction == 6:
            # southwest
            row_inc = 1
            col_inc = -1
        elif direction == 7:
            # west
            row_inc = 0
            col_inc = -1
        elif direction == 8:
            # northwest
            row_inc = -1
            col_inc = -1

        places = []     # pieces to flip
        i = position[0] + row_inc
        j = position[1] + col_inc

        if color == WHITE:
            other = BLACK
        else:
            other = WHITE

        if i in range(8) and j in range(8) and self.board[i][j] == other:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(8) and j in range(8) and self.board[i][j] == other:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(8) and j in range(8) and self.board[i][j] == color:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    # flips
                    self.board[pos[0]][pos[1]] = color


    def get_changes(self):
        """ Return the current board state , black and white counters. """

        whites, blacks, empty = self.count_stones()

        return (self.board, blacks, whites)

    def game_ended(self):
        """ Is the game ended? """
        # board full or wipeout
        whites, blacks, empty = self.count_stones()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        if self.get_valid_moves(BLACK) == [] and \
                self.get_valid_moves(WHITE) == []:
            return True

        return False

    def count_stones(self):
        """ Returns the number of white pieces, black pieces and empty squares, in this order."""
        whites = 0
        blacks = 0
        empty = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == WHITE:
                    whites += 1
                elif self.board[i][j] == BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

#  Compares two boards and highlights the differences.
    def compare(self, otherBoard):
        """Return a board containing only the squares that are empty in one
        of the boards and not empty on the other."""
        diffBoard = Board()
        diffBoard.board[3][4] = 0
        diffBoard.board[3][3] = 0
        diffBoard.board[4][3] = 0
        diffBoard.board[4][4] = 0

# Creates a new board showing only the positions where the two boards differ.
        for i in range(8):
            for j in range(8):
                if otherBoard.board[i][j] != self.board[i][j]:
                    diffBoard.board[i][j] = otherBoard.board[i][j]
        return otherBoard

# Counts empty spaces adjacent to the player's pieces.
    def get_adjacent_count(self, color):
        """Return how many empty squares there are on the board adjacent to
        the specified color."""
        adjCount = 0

# For each piece of the specified color, checks the surrounding 8 squares for empty spaces.
        for x, y in [(a, b) for a in range(8) for b in range(8) if self.board[a][b] == color]:
            for i, j in [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1]]:
                if 0 <= x + i <= 7 and 0 <= y + j <= 7:
                    if self.board[x + i][y + j] == EMPTY:
                        adjCount += 1
        return adjCount

# Generates all possible board states resulting from valid moves for the given color.
    def next_states(self, color):
        """Given a player's color return all the boards resulting from moves
        that this player cand do. It's implemented as an iterator."""
        valid_moves = self.get_valid_moves(color)
        for move in valid_moves:
            newBoard = deepcopy(self)
            newBoard.apply_move(move, color)
            yield newBoard