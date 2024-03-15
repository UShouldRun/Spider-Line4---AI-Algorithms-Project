from game_settings import *
from bots import Bot1, Bot2, Bot3
from player import Player
from objects import Board, Button
from copy import deepcopy

class SpiderLine4:
    def __init__(self) -> None:
        self.screen = screen
        self.running = True

        # menus
        self.current_state = 1 
        self.states = {0: "main_menu", 1: "in_game"}

        # mouse
        self.mouse_pos = [0,0]

        # play button
        self.play_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "PLAY", TEXT_SIZE, MAIN_FONT)

        # game state variables
        self.game_state = 0
        self.turn = 0

        # board
        self.board = Board(N,M,WIDTH//2 - BOARD_WIDTH//2, HEIGHT//2 - BOARD_HEIGHT//2, BOARD_WIDTH, BOARD_HEIGHT)

        # entities
        self.selected_bot = 0
        self.bots = [Bot1(), Bot2(), Bot3()]

        self.player = Player()

    def isRunning(self) -> bool: return self.running

    def get_current_state(self) -> int: return self.current_state

    def update_mouse(self, event) -> None: self.mouse_pos = event.pos

    def get_game_state(self) -> int: return self.game_state
    def get_turn(self) -> int: return self.turn

    def get_selected_bot(self) -> int: return self.selected_bot
    def get_players(self) -> list: return [self.player, self.bots[self.get_selected_bot()]]

    def handle_events(self) -> None:
        match self.states[self.get_current_state()]:
            case "main_menu": pass
            case "in_game": pass

    def get_inputs(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEMOTION: self.update_mouse(event)
            if event.type == pygame.MOUSEMOTION:
                self.update_mouse(event)
                self.handle_events()

    def play(self) -> None:
        for player in self.get_players(): player.play()

    def resize(self) -> None: pass

    def cleanScreen(self) -> None: self.screen.fill(BACKGROUND)

    def draw_board(self) -> None:
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

    def draw_game(self) -> None:
        self.cleanScreen()
        self.draw_board()
        self.draw_chat()
        self.draw_clocks()

    def draw(self) -> None:
        match self.states[self.get_current_state()]:
            case "main_menu": self.draw_main_menu()
            case "in_game": self.draw_game()

    def run(self) -> None:
        while self.isRunning():
            self.get_inputs()
            self.play()
            self.draw()
            pygame.display.update()
