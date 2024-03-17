from game_settings import *
from bots import Bot1, Bot2, Bot3
from player import Player
from objects import Board, Button, Clock
from copy import deepcopy

class SpiderLine4:
    def __init__(self) -> None:
        '''Initializes all necessary variables.'''
        self.screen = screen
        self.running = True

        # menus
        self.current_state = 0 
        self.states = {0: "main_menu", 1: "in_game"}

        # mouse
        self.mouse_pos = [0,0]
        self.mouse_clicked = False

        # play button
        self.play_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "PLAY", TEXT_SIZE, MAIN_FONT)

        # game state variables
        self.game_state = 0
        self.turn = 1

        # board
        self.initialize_board()

        # entities
        self.selected_bot = 0
        self.bots = [Bot1(), Bot2(), Bot3()]

        self.player = Player(self.board, "1")
        self.player1 = self.player # by default the user is the player 1

    def initialize_board(self) -> None: self.board = Board(N,M,WIDTH//2 - BOARD_WIDTH//2, HEIGHT//2 - BOARD_HEIGHT//2, BOARD_WIDTH, BOARD_HEIGHT)

    def isRunning(self) -> bool:
        '''Returns True if the current game is still running.'''
        return self.running
    def get_current_state(self) -> int:
        '''Returns the current menu.'''
        return self.current_state

    def get_game_state(self) -> int:
        '''Returns 0 if the game is still on going, 1 if the player 1 won the game, 2 if the player 2 won the game and 3 if the game was a draw.'''
        return self.game_state
    def get_turn(self) -> int:
        '''Return the which player is supposed to play. 1 for player 1 and 2 for player 2.'''
        return self.turn

    def isMouseClicked(self) -> bool: return self.mouse_clicked
    def get_mouse_pos(self) -> tuple: return self.mouse_pos

    def get_selected_bot(self) -> int:
        '''Returns the current selected bot to play against the player. Notice that this returns player 2.'''
        return self.selected_bot
    def get_player1(self): return self.player1
    def get_player2(self): return self.bots[self.get_selected_bot()]
    def get_players(self) -> list:
        '''Returns a list with the player 1 and the player 2.'''
        return [self.get_player1(), self.get_player2()]

    def set_player1(self, entity) -> None:
        '''Sets who is playing, the player or one of the bots.'''
        self.player1 = entity
    def set_turn(self, turn: int) -> None:
        '''Defines which player is playing.'''
        self.turn = turn

    # Input Section

    def update_mouse(self, event) -> None: self.mouse_pos = event.pos

    def handle_events(self) -> None:
        '''Depending on which menu the user is, redefines variables to change the app state.'''
        match self.states[self.get_current_state()]:
            case "main_menu":
                if self.play_button.isClicked(self.get_mouse_pos()) and self.isMouseClicked(): self.current_state = 1
            case "in_game":
                if self.game_state != 0:
                    self.current_state = 0
                    self.initialize_board()
                if self.get_player1() == self.player and self.mouse_clicked:
                    board_pos = self.identify_board_click(self.get_mouse_pos())
                    if board_pos in self.get_legal_moves() and self.get_turn() == int(self.player.getPiece()): self.player.play(board_pos) 

    def get_inputs(self) -> None:
        '''Loops over all pygame events and handles the events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_clicked = True
            else: self.mouse_clicked = False
            if event.type == pygame.MOUSEMOTION: self.update_mouse(event)
        self.handle_events()

    # Process Input and Bot play

    def identify_board_click(self, pos: tuple[int,int]) -> tuple[int,int] || None: pass
    def get_legal_moves(self) -> list[tuple[int,int]]: pass

    def play(self) -> None:
        match self.get_turn():
            case 1:
                if self.get_player1() != self.player: self.player1.play()
            case 2: self.player2.play()

    # Draw on the screen section

    def resize(self) -> None:
        '''Resizes all objects in case the game enters full screen or goes to the default state.'''
        pass

    def cleanScreen(self) -> None: self.screen.fill(BACKGROUND)

    def draw_board(self) -> None:
        '''Draws a background. Loops over all the board positions and draws the colored squares on even i + j positions. If a place is on the board, then the code recognizes and draws a circle on that position.'''
        pygame.draw.rect(self.screen, BOARD_COLOR, self.board.get_rect())
        for i in range(self.board.get_rows()):
            for j in range(self.board.get_columns()):
                x, y = (self.board.get_rect().x + j * SQUARE_SIZE, self.board.get_rect().y + i * SQUARE_SIZE)
                if (i+j)%2 == 0: pygame.draw.rect(self.screen, SQUARE_COLOR, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))
                if self.board.get_matrix()[i,j] != "0": pygame.draw.circle(self.screen, PLAYER_COLORS[self.board.get_matrix()[i,j]], (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), SQUARE_SIZE//2)

    def draw_chat(self) -> None: pass
    def draw_clocks(self) -> None: pass

    def draw_main_menu(self) -> None:
        self.cleanScreen()
        self.play_button.draw()

    def draw_game(self) -> None:
        self.cleanScreen()
        self.draw_board()
        self.draw_chat() # needs to be built
        self.draw_clocks() # needs to be built

    def draw(self) -> None:
        match self.states[self.get_current_state()]:
            case "main_menu": self.draw_main_menu()
            case "in_game": self.draw_game()

    # main function

    def run(self) -> None:
        while self.isRunning():
            self.get_inputs()
            self.play()
            self.draw()
            pygame.display.update()
