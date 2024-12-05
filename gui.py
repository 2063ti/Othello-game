""" Othello game GUI
"""

import pygame 
import sys
from pygame.locals import * # type: ignore
import time
from config import BLACK, WHITE, DEFAULT_LEVEL, HUMAN, COMPUTER
import os
import pygame_menu  
# from pip import pygame_menu


class Gui:
    def __init__(self):
        """ Initializes graphics. """

        pygame.init()

        # colors
        self.BLACK = (0, 0, 0)
        self.BACKGROUND = (62, 149, 195)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.LIGHTWHITE = (228, 230, 246)

        # display
        self.SCREEN_SIZE = (640, 480)
        self.BOARD_POS = (100, 20)
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # messages
        self.BLACK_LAB_POS = (5, self.SCREEN_SIZE[1] / 4)
        self.WHITE_LAB_POS = (560, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)
        self.scoreFont = pygame.font.SysFont("Times New Roman", 58)
        self.player_name = pygame.font.SysFont("Times New Roman", 18)

        # image files
        self.board_img = pygame.image.load(os.path.join(
            "images", "board.bmp")).convert()
        self.black_img = pygame.image.load(os.path.join(
            "images", "preta.bmp")).convert()
        self.white_img = pygame.image.load(os.path.join(
            "images", "branca.bmp")).convert()
        self.tip_img = pygame.image.load(os.path.join("images",
                                                      "tip.bmp")).convert()
        self.clear_img = pygame.image.load(os.path.join("images",
                                                        "nada.bmp")).convert()
        self.whiteimg = pygame.image.load(
            os.path.join("images", "white.bmp")).convert()
        self.blackimg = pygame.image.load(
            os.path.join("images", "black.bmp")).convert()

    def show_menu(self, start_cb):
        # default game settings
        self.level = DEFAULT_LEVEL
        self.player1 = HUMAN
        self.player2 = COMPUTER

        self.menu = pygame_menu.Menu(height=480, width=640,
                                     theme=pygame_menu.themes.THEME_BLUE, title="Othello")
        pygame.display.set_caption('Othello')
        self.menu.add.button('Play', lambda: start_cb(self.player1, self.player2, self.level))
        self.menu.add.selector('Difficulty: ', [['Medium', 2], ['Easy', 1], ('Hard', 3)],
                               onchange=self.set_difficulty)
        self.menu.add.selector('First player', [[HUMAN, 1], [COMPUTER, 2]],
                               onchange=self.set_player_1)
        self.menu.add.selector('Second player', [[COMPUTER, 2], [HUMAN, 1]],
                               onchange=self.set_player_2)
        self.menu.mainloop(self.screen)

    def set_player_1(self, value, player):

        self.player1 = [0, HUMAN, COMPUTER][player]

    def set_player_2(self, value, player):

        self.player2 = [0, HUMAN, COMPUTER][player]

    def set_difficulty(self, value, difficulty):
        self.level = difficulty

    def reset_menu(self):
        self.menu.disable()
        self.menu.reset(1)

    def show_winner(self, player_color):
        self.screen.fill(pygame.Color(self.BACKGROUND))
        font = pygame.font.SysFont("Times New Roman", 34)
        if player_color == WHITE:
            msg = font.render("White Player Wins", True, self.BLACK)
        elif player_color == BLACK:
            msg = font.render("Black Player Wins", True, self.BLACK)
        else:
            msg = font.render("Tie !", True, self.BLACK)
        self.screen.blit(
            msg, msg.get_rect(
                centerx=self.screen.get_width() / 2, centery=120))
        pygame.display.flip()

    def show_game(self):
        """ Game screen. """
        self.reset_menu()

        # draws initial screen
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACKGROUND)
        self.score_size = 50
        self.score1 = pygame.Surface((self.score_size, self.score_size))
        self.score2 = pygame.Surface((self.score_size, self.score_size))
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS,
                         self.board_img.get_rect())
        self.put_stone((3, 3), WHITE)
        self.put_stone((4, 4), WHITE)
        self.put_stone((3, 4), BLACK)
        self.put_stone((4, 3), BLACK)
        pygame.display.flip()

    def put_stone(self, pos, color):
        """ draws piece with given position and color """
        if pos == None:
            return

        # flip orientation (because xy screen orientation)
        pos = (pos[1], pos[0])

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        pygame.display.flip()

    def get_mouse_input(self):
        """ Get place clicked by mouse
        """
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # click was out of board, ignores
                    if mouse_x > self.BOARD_SIZE + self.BOARD[0] or \
                       mouse_x < self.BOARD[0] or \
                       mouse_y > self.BOARD_SIZE + self.BOARD[1] or \
                       mouse_y < self.BOARD[1]:
                        continue

                    # find place
                    position = ((mouse_x - self.BOARD[0]) // self.SQUARE_SIZE), \
                        ((mouse_y - self.BOARD[1]) // self.SQUARE_SIZE)
                    # flip orientation
                    position = (position[1], position[0])
                    return position

                elif event.type == QUIT:
                    sys.exit(0)

            time.sleep(.05)

    def update(self, board, blacks, whites, current_player_color):
        """Updates screen
        """
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    self.put_stone((i, j), board[i][j])

        # show score
        blacks_str = '%02d ' % int(blacks)
        whites_str = '%02d ' % int(whites)
        self.showScore(blacks_str, whites_str, current_player_color)
        # show player name
        p1 = self.player_name.render(self.player1, True, self.BLACK)
        p2 = self.player_name.render(self.player2, True, self.BLACK)
        self.screen.blit(p1, (15, 130))
        self.screen.blit(p2, (560, 130))
        # player stone
        self.screen.blit(self.blackimg, (15, 240), self.blackimg.get_rect())
        self.screen.blit(self.whiteimg, (570, 240), self.whiteimg.get_rect())

        pygame.display.flip()

    def showScore(self, blackStr, whiteStr, current_player_color):
        # indicating which player's turn
        black_background = self.LIGHTWHITE if current_player_color == WHITE else self.BACKGROUND
        white_background = self.LIGHTWHITE if current_player_color == BLACK else self.BACKGROUND
        # show score
        text = self.scoreFont.render(blackStr, True, self.BLACK,
                                     black_background)
        text2 = self.scoreFont.render(whiteStr, True, self.BLACK,
                                      white_background)
        self.screen.blit(
            text, (self.BLACK_LAB_POS[0], self.BLACK_LAB_POS[1] + 40))
        self.screen.blit(text2,
                         (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] + 40))

    def wait_quit(self):
        # wait user to close window
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                break
