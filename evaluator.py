from config import BLACK, WHITE, EMPTY

# Defines the Evaluator class, which contains methods to calculate a heuristic score for a game board in a strategy game
class Evaluator(object):
    WIPEOUT_SCORE = 1000  # a move that results a player losing all pieces
    PIECE_COUNT_WEIGHT = [0, 0, 0, 4, 1]
    POTENTIAL_MOBILITY_WEIGHT = [5, 4, 3, 2, 0]
    MOBILITY_WEIGHT = [7, 6, 5, 4, 0]
    CORNER_WEIGHT = [35, 35, 35, 35, 0]
    EDGE_WEIGHT = [0, 3, 4, 5, 0]
    XSQUARE_WEIGHT = [-8, -8, -8, -8, 0]

# Calculates the score based on the difference in the number of pieces for each player.
    def get_piece_differential(self, deltaBoard, band):
        """Return the piece differential score Given a board resultant of the
        difference between the initial board and the board after the
        move and a weight band returns the count of the pieces the
        player has gained minus the same count for the opponent.

        """
        if Evaluator.PIECE_COUNT_WEIGHT[band] != 0:

            # Counts the number of white, black, and empty pieces on the deltaBoard.
            whites, blacks, empty = deltaBoard.count_stones()

            # Determines the score based on the current player.
            if self.player == WHITE:
                myScore = whites   
                yourScore = blacks
            else:
                myScore = blacks
                yourScore = whites

            # Returns the weighted score difference.
            return Evaluator.PIECE_COUNT_WEIGHT[band] * (myScore - yourScore)
        return 0

    # Calculates the score based on corners owned by each player.
    def get_corner_differential(self, deltaCount, deltaBoard, band):
        """Return the corner differential score Given a board resultant of
        the difference between the initial board and the board after
        the move and a weight band returns the count of the corner the
        player has gained minus the same count for the opponent.

        """
        if Evaluator.CORNER_WEIGHT[band] != 0:
            # corner differential
            myScore = 0
            yourScore = 0
            # Loops over corner coordinates.
            for i in [0, 7]:
                for j in [0, 7]:
                    # Updates the scores based on who owns the corner.
                    if deltaBoard.board[i][j] == self.player:
                        myScore += 1
                    elif deltaBoard.board[i][j] == self.enemy:
                        yourScore += 1
                    if myScore + yourScore >= deltaCount:
                        break
                if myScore + yourScore >= deltaCount:
                    break
            # Returns the weighted corner score difference.
            return Evaluator.CORNER_WEIGHT[band] * (myScore - yourScore)
        return 0

# Calculates the score for pieces on edges (not corners).
    def get_edge_differential(self, deltaCount, deltaBoard, band):
        """Return the piece differential score Given a board resultant of the
        difference between the initial board and the board after the
        move and a weight band returns the count of the A-squares and
        B-squares the player has gained minus the same count for the
        opponent.  A-squares are the (c1, f1, a3, a6, h3, h6, c8, f8).
        B-squares are the (d1, e1, a4, a5, h4, h5, d8, e8).

        """
        if Evaluator.EDGE_WEIGHT[band] != 0:
            myScore = 0
            yourScore = 0

            # Defines edge squares.
            squares = [(a, b) for a in [0, 7] for b in range(1, 7)] \
                + [(a, b) for a in range(1, 7) for b in [0, 7]]
            # Updates scores based on who owns the edge squares.
            for x, y in squares:
                if deltaBoard.board[x][y] == self.player:
                    myScore += 1
                elif deltaBoard.board[x][y] == self.enemy:
                    yourScore += 1
                if myScore + yourScore >= deltaCount:
                    break
            # Returns the weighted edge score difference.
            return Evaluator.EDGE_WEIGHT[band] * (myScore - yourScore)
        return 0

# Calculates the score for "X-squares" (squares adjacent to corners).
    def get_xsquare_differential(self, startBoard, currentBoard, deltaBoard, band):
        """ Return the difference of x-squares owned between the players
        A x-square is the square in front of each corner. Consider only new pieces, not flipped
        ones and only squares next to open corner.
        startBoard - board before the move
        currentBoard - board after the move
        deltaBoard - differential board between startBoard and currentBoard
        """
        if Evaluator.XSQUARE_WEIGHT[band] != 0:
            myScore = 0
            yourScore = 0
            # Iterates over "X-square" positions.
            for x, y in [(a, b) for a in [1, 6] for b in [1, 6]]:
                if deltaBoard.board[x][y] != EMPTY and startBoard.board[x][y] == EMPTY:
                    # if the piece is new consider this square if the nearest
                    # corner is open
                    cornerx = x
                    cornery = y
                    if cornerx == 1:
                        cornerx = 0
                    elif cornerx == 6:
                        cornerx = 7
                    if cornery == 1:
                        cornery = 0
                    elif cornery == 6:
                        cornery = 7
                    # Considers only X-squares next to empty corners.
                    if currentBoard.board[cornerx][cornery] == EMPTY:
                        if currentBoard.board[x][y] == self.player:
                            myScore += 1
                        elif currentBoard.board[x][y] == self.enemy:
                            yourScore += 1
            # Returns the weighted X-square score difference.
            return Evaluator.XSQUARE_WEIGHT[band] * (myScore - yourScore)
        return 0

# Calculates the score based on frontier pieces (pieces adjacent to empty spaces).
    def get_potential_mobility_differential(self, startBoard, currentBoard, band):
        """ Return the difference between opponent and player number of frontier pieces.
        startBoard - board before the move
        currentBoard - board after the move
        band - weight
        """
        if Evaluator.POTENTIAL_MOBILITY_WEIGHT[band] != 0:
            # Computes changes in the number of frontier pieces.
            myScore = currentBoard.get_adjacent_count(
                self.enemy) - startBoard.get_adjacent_count(self.enemy)
            yourScore = currentBoard.get_adjacent_count(
                self.player) - startBoard.get_adjacent_count(self.player)
            # Returns the weighted frontier piece score difference.
            return Evaluator.POTENTIAL_MOBILITY_WEIGHT[band] * (myScore - yourScore)
        return 0

# Calculates the score based on the number of valid moves.
    def get_mobility_differential(self, startBoard, currentBoard, band):
        """ Return the difference of number of valid moves between the player and his opponent.
        startBoard - board before the move
        currentBoard - board after the move
        band - weight
        """
        # Computes changes in valid move counts.
        myScore = len(currentBoard.get_valid_moves(self.player)) - \
            len(startBoard.get_valid_moves(self.player))
        yourScore = len(currentBoard.get_valid_moves(
            self.enemy)) - len(startBoard.get_valid_moves(self.enemy))
        
        # Returns the weighted mobility score difference.
        return Evaluator.MOBILITY_WEIGHT[band] * (myScore - yourScore)

# The main method to compute a heuristic score for a board state.
    def score(self, startBoard, board, currentDepth, player, opponent):
        """ Determine the score of the given board for the specified player.
        - startBoard the board before any move is made
        - board the board to score
        - currentDepth depth of this leaf in the game tree
        - searchDepth depth used for searches.
        - player current player's color
        - opponent opponent's color
        """
        # Sets the current player and opponent.
        self.player = player
        self.enemy = opponent
        sc = 0
        whites, blacks, empty = board.count_stones()

        # Computes the differences between the starting and current boards.
        deltaBoard = board.compare(startBoard)
        deltaCount = sum(deltaBoard.count_stones())

        # Handles "wipeout" scenarios where one player loses all pieces.
        if (self.player == WHITE and whites == 0) or (self.player == BLACK and blacks == 0):
            return -Evaluator.WIPEOUT_SCORE
        if (self.enemy == WHITE and whites == 0) or (self.enemy == BLACK and blacks == 0):
            return Evaluator.WIPEOUT_SCORE

        # Determines the weight band based on the total piece count.
        piece_count = whites + blacks
        band = 0
        if piece_count <= 16:
            band = 0
        elif piece_count <= 32:
            band = 1
        elif piece_count <= 48:
            band = 2
        elif piece_count <= 64 - currentDepth:
            band = 3
        else:
            band = 4

        # Adds the scores from various heuristic components.
        sc += self.get_piece_differential(deltaBoard, band)
        sc += self.get_corner_differential(deltaCount, deltaBoard, band)
        sc += self.get_edge_differential(deltaCount, deltaBoard, band)
        sc += self.get_xsquare_differential(startBoard,
                                            board, deltaBoard, band)
        sc += self.get_potential_mobility_differential(startBoard, board, band)
        sc += self.get_mobility_differential(startBoard, board, band)

        # Returns the final computed score.
        return sc
