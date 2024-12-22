# Implements minimax with alpha-beta
# prunning algorithm for games like chess or reversi.
INFINITY = 100000

class AI(object):

# Initializes an AI object with a heuristic evaluation function
    def __init__(self, heuristic_eval):
        """ Create a new minimax object
        player - current player's color opponent - opponent's color"""
        self.heuristic_eval = heuristic_eval

    # error: always return the same board in same cases
    def alphaBeta(self, board, parentBoard, depth, player, opponent,
                alfa=-INFINITY, beta=INFINITY):
        
# bestChild :=  This variable will be updated to store the best board state found during the search.
        bestChild = board
        if depth == 0:

# heuristic_eval := Returns a tuple containing the heuristic score and the board state.
            return (self.heuristic_eval(parentBoard, board, depth,
                                        player, opponent), board)
        
# Iterates through all possible board states (child) resulting from the current player's valid moves.
        for child in board.next_states(player):

# Recursively calls the alphaBeta function for the child state and 
# Swaps the roles of player and opponent for the next level of recursion..
            score, newChild = self.alphaBeta(
                child, board, depth - 1, opponent, player, -beta, -alfa)
            score = -score

# Checks if the current score is better than the best score found so far for the maximizing player (alfa).
            if score > alfa:
                alfa = score
                bestChild = child

# If the current branch cannot yield a better result for the minimizing player (beta ≤ alfa), it stops further exploration of this branch.
# Implements the Alpha-Beta pruning condition.
            if beta <= alfa: 
                break

# Returns a tuple containing the evaluation score and the best child board.
        return (self.heuristic_eval(board, board, depth, player,
                                    opponent), bestChild)
