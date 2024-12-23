""" Human and Computer classes"""

from evaluator import Evaluator
from config import WHITE, BLACK
from ai import AI
import random

def change_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK

class Human:

    """ Human player """
    def __init__(self, gui, color="black"):
        self.color = color
        self.gui = gui

    def get_move(self):
        """ Uses gui to handle mouse"""
        validMoves = self.current_board.get_valid_moves(self.color)
        print(f"Valid Moves Is: {set(validMoves)}")

        # Enters a loop where it waits for valid input from the GUI
        while True:
            move = self.gui.get_mouse_input()
            if move in validMoves:
                break
        # Once a valid move is selected, it applies the move to the board
        self.current_board.apply_move(move, self.color)
        return 0, self.current_board


    # Updates the current board state.
    def get_current_board(self, board):
        self.current_board = board


class Computer(object):
#  Initializes a computer player.
    def __init__(self, color, prune=3):
        self.depthLimit = prune
        evaluator = Evaluator()
        self.alphaBetaObj = AI(evaluator.score)
        self.color = color
        
# Updates the current board state.
    def get_current_board(self, board):
        self.current_board = board

# Determines the AI's next move using the Alpha-Beta pruning algorithm.
    def get_move(self):
        return self.alphaBetaObj.alphaBeta(self.current_board, None, self.depthLimit, self.color,
                                           change_color(self.color))
