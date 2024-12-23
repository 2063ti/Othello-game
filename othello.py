"""Game initialization and main loop"""
import pygame # type: ignore
import gui
import player
import board
from config import BLACK, WHITE, HUMAN

# The main class that encapsulates the Othello game's initialization, gameplay loop, and restart functionality.
class Othello:
    """Game main class."""

    def __init__(self):
        self.gui = gui.Gui()
        self.board = board.Board()
        self.gui.show_menu(self.start)

# initializes the game with the provided arguments:
    def start(self, *args):
        player1, player2, level = args

        if player1 == HUMAN:
            self.now_playing = player.Human(self.gui, BLACK)
        else:
            self.now_playing = player.Computer(BLACK, level + 3)

        if player2 == HUMAN:
            self.other_player = player.Human(self.gui, WHITE)
        else:
            self.other_player = player.Computer(WHITE, level + 3)

        self.gui.show_game()

        self.gui.update(self.board.board, 2, 2, self.other_player.color)

# clock: A pygame object that controls the frame rate, ensuring the game loop runs smoothly (at 60 FPS).
    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Limits the loop to run 60 times per second.
            clock.tick(60)
            # game end then set winner
            if self.board.game_ended():
                whites, blacks, empty = self.board.count_stones()
                if whites > blacks:
                    winner = WHITE
                elif blacks > whites:
                    winner = BLACK
                else:
                    winner = None
                break

            self.now_playing.get_current_board(self.board)
            valid_moves = self.board.get_valid_moves(self.now_playing.color)

            if valid_moves != []:
                # Executes a move (human input or computer calculation). Updates the board state and score.
                score, self.board = self.now_playing.get_move()

                # Counts the stones after the move.
                whites, blacks, empty = self.board.count_stones()
                # Updates the GUI with the new board state and scores.
                self.gui.update(self.board.board, blacks, whites,
                                self.now_playing.color)

            self.now_playing, self.other_player = self.other_player, self.now_playing

        self.gui.show_winner(winner)
        pygame.time.wait(2000)
        self.restart()

    def restart(self):
        self.board = board.Board()
        self.gui.show_menu(self.start)
        self.run()

def main():
    game = Othello()
    game.run()

if __name__ == '__main__':
    main()