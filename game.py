from settings import *
from mdp import MDP
from mdpfunctions import state_analysis, get_actions, execute, qfunction, qfunction1, qfunction3, qfunction4, heuristic1, softmax
from bots import Bot0, Bot1, Bot2, Bot3, AlphaBeta
from player import Player
from objects import Board, Button, Clock, Node

class SpiderLine4:
    def __init__(self) -> None:
        '''Initializes all necessary variables.'''
        self.screen = screen
        self.running = True

        # menus
        self.current_state = 0 
        self.states = {0: "main_menu", 1: "game_modes", 2: "win_label", 3: "vscomp", 4: "normal", 5: "bot_vs_bot", 6: "vscomp_ingame", 7: "bot_vs_bot_ingame",8:"time_menu"}
        # mouse
        self.mouse_pos = [0,0]
        self.mouse_clicked = False

        self.tested = False

        # play button
        self.play_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "PLAY", TEXT_SIZE, MAIN_FONT)
        self.legal_moves_button = Button(self.screen, (WIDTH//2 - BOARD_WIDTH//2)//2 - BUTTON_WIDTH//4, HEIGHT//16, BUTTON_WIDTH//2, BUTTON_HEIGHT//2, BUTTON_COLOR, FONT_COLOR, "DISPLAY MOVES", TEXT_SIZE//2, MAIN_FONT)
        self.exit_button = Button(self.screen, (WIDTH//2 - BOARD_WIDTH//2)//2 - BUTTON_WIDTH//4, BOARD_HEIGHT-HEIGHT//16-BUTTON_HEIGHT//2, BUTTON_WIDTH//2, BUTTON_HEIGHT//2, BUTTON_COLOR, FONT_COLOR, "EXIT", TEXT_SIZE//2, MAIN_FONT)
        self.back_button = Button(self.screen, (WIDTH//2 - BOARD_WIDTH//2)//2 - BUTTON_WIDTH//4, BOARD_HEIGHT-HEIGHT//16-BUTTON_HEIGHT//2, BUTTON_WIDTH//2, BUTTON_HEIGHT//2, BUTTON_COLOR, FONT_COLOR, "BACK", TEXT_SIZE//2, MAIN_FONT)

        # FPS
        self.ticks = 1000//FPS
        self.timer = 0

        #music
        pygame.mixer.music.load("resources/assets/Wii.mp3")
        pygame.mixer.music.play(-1)

        # board and game variables
        self.board = Board(N,M,WIDTH//2 - BOARD_WIDTH//2, HEIGHT//2 - BOARD_HEIGHT//2, BOARD_WIDTH, BOARD_HEIGHT)
        self.game_state = 0
        self.turn = 1
        self.display_switch = True

        def state(node: Node): return state_analysis(node, self.checkWin, self.checkDraw)
        def actions(node: Node): return get_actions(node, self.get_legal_moves)
        def qfunction2(node: Node, opponent: str): return qfunction(node, opponent, self.checkWin, self.checkDraw)

        # entities
        mdp = MDP(actions, state, execute, qfunction2)
        mdp1 = MDP(actions, state, execute, qfunction3)
        mdp2 = MDP(actions, state, execute, qfunction4)
        TIME, MAX_NODES = 10, 1000 
        UCT_CONST = .02 * TIME
        DEPTH_AB, DEPTH_N, DEPTH_M = 3, 2, 20
        self.mdp1 = MDP(actions, state, execute, qfunction3)

        self.bots = [Bot1(self.board, "NegaMax", DEPTH_N, mdp2), Bot2(self.board, "MiniMax", DEPTH_AB, mdp1), Bot3(self.board, "Monte Carlo", TIME, MAX_NODES, DEPTH_M, UCT_CONST, mdp)]
        self.eval_bot = AlphaBeta(self.board, 2, mdp2)
        self.bot1 = 0
        self.bot2 = 1
        self.selected_bot = 0

        self.player = Player(self.board, "1", "Player 1")
        self.opponent = Player(self.board, "2", "Player 2")
        self.users = [self.player, self.opponent]
        self.player1 = self.player # by default the user is the player 1
        self.player2 = self.opponent # by default the second user is the player 2

        # winning label
        self.win_label_clock = 0
        self.win_label_limit = 200
        self.win_player = 0
        self.win_font = pygame.font.SysFont(MAIN_FONT, TEXT_SIZE)

        # game modes
        self.normal_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 2*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "NORMAL", TEXT_SIZE, MAIN_FONT)
        self.hum_vs_bot_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "VS COMPUTER", TEXT_SIZE, MAIN_FONT)
        self.bot_vs_bot_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "COMP VS COMP", TEXT_SIZE, MAIN_FONT)

        self.select_bot1_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 2*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, self.text1, TEXT_SIZE, MAIN_FONT)
        self.select_bot2_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, self.text2, TEXT_SIZE, MAIN_FONT)
        self.bot_vs_bot_start_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "START", TEXT_SIZE, MAIN_FONT)
 
        self.min_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 2*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, self.get_bots()[0].get_name(), TEXT_SIZE, MAIN_FONT)
        self.min_ab_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, self.get_bots()[1].get_name(), TEXT_SIZE, MAIN_FONT)
        self.monte_carlo_button = Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, self.get_bots()[2].get_name(), TEXT_SIZE, MAIN_FONT)

        # Clocks
        self.clock1 = Clock(self.screen, (WIDTH//2 - BOARD_WIDTH//2)//2 - BUTTON_WIDTH//4, HEIGHT//8 + 2*BUTTON_HEIGHT, BUTTON_WIDTH//2, BUTTON_HEIGHT//2, BUTTON_COLOR, FONT_COLOR, self.get_clock1(), TEXT_SIZE//2, MAIN_FONT)
        self.clock2 = Clock(self.screen, (WIDTH//2 - BOARD_WIDTH//2)//2 - BUTTON_WIDTH//4, HEIGHT//8 + BUTTON_HEIGHT, BUTTON_WIDTH//2, BUTTON_HEIGHT//2, BUTTON_COLOR, FONT_COLOR, self.get_clock2(), TEXT_SIZE//2, MAIN_FONT)
        self.time_option_1=Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - 2*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "3:00", TEXT_SIZE, MAIN_FONT)
        self.time_option_2= Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "5:00", TEXT_SIZE, MAIN_FONT)
        self.time_option_3=Button(self.screen, WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, FONT_COLOR, "15:00", TEXT_SIZE, MAIN_FONT)

        self.sound = Button(self.screen, WIDTH - BUTTON_WIDTH//2, HEIGHT//2 + BUTTON_HEIGHT*2, BUTTON_WIDTH//6, BUTTON_HEIGHT//3, BUTTON_COLOR, FONT_COLOR, "", TEXT_SIZE//2, MAIN_FONT)
        self.sound_tick = 0

        # Labels
        self.wlabel_h = 0
        self.blabel_h = 0
        self.white_label = Button(self.screen, self.board.get_rect().x + self.board.get_rect().width + 10, HEIGHT//2, BUTTON_WIDTH//8, HEIGHT//2, BUTTON_COLOR, FONT_COLOR, "", TEXT_SIZE//2, MAIN_FONT)
        self.black_label = Button(self.screen, self.board.get_rect().x + self.board.get_rect().width + 10, 0, BUTTON_WIDTH//8, HEIGHT//2, BUTTON_COLOR, FONT_COLOR, "", TEXT_SIZE//2, MAIN_FONT)
        self.eval_font = pygame.font.SysFont(MAIN_FONT, int(self.black_label.width//2))
        self.previous_board = None

        # Hint
        self.hint_lable = Button(self.screen, (WIDTH//2 - BOARD_WIDTH//2)//2 - BUTTON_WIDTH//4, HEIGHT//2 - BUTTON_HEIGHT//2, BUTTON_WIDTH//2, BUTTON_HEIGHT//2, BUTTON_COLOR, FONT_COLOR, "HINT", TEXT_SIZE//2, MAIN_FONT)
        self.hint_istaken = False

    def initialize_board(self) -> None:
        self.board = Board(N, M, WIDTH//2 - BOARD_WIDTH//2, HEIGHT//2 - BOARD_HEIGHT//2, BOARD_WIDTH, BOARD_HEIGHT)
        self.game_state = 0
        self.turn = 1
        self.win_player = 0

        self.player1 = self.player
        self.player2 = self.opponent
        for user in self.get_users(): user.board = self.board
        for bot in self.get_bots(): bot.board = self.board

        self.clock1.kill()
        self.clock2.kill()

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
    def set_turn(self, turn: int) -> None:
        '''Defines which player is playing.'''
        self.turn = turn
    def get_display(self) -> bool:
        '''Returns True if the user wants to see the possible legal moves on the board.'''
        return self.display_switch
    def set_display(self, state: bool = None) -> None:
        if state is not None: self.display_switch = state
        else: self.display_switch = not self.display_switch

    def isMouseClicked(self) -> bool: return self.mouse_clicked
    def get_mouse_pos(self) -> tuple: return self.mouse_pos
    def mouse_switch(self, state: bool = None) -> None:
        if state is not None: self.mouse_clicked = state 
        else: self.mouse_clicked = not self.mouse_clicked

    def get_bots(self, bot: int = None) -> list:
        if bot is not None: return self.bots[bot]
        return self.bots

    def get_bot1(self) -> int: return self.bot1
    def get_bot2(self) -> int: return self.bot2
    def set_bot1(self, bot: int) -> None: self.bot1 = bot
    def set_bot2(self, bot: int) -> None: self.bot2 = bot

    def get_selected_bot(self) -> int:
        '''Returns the current selected bot to play against the player. Notice that this returns player 2.'''
        return self.selected_bot
    def set_selected_bot(self, bot: int) -> None: self.selected_bot = bot

    def get_minmax(self) -> int: return 0
    def get_minmax_ab(self) -> int: return 1
    def get_monte_carlo(self) -> int: return 2

    def text1(self) -> str:
        if type(self.get_player1()) == Player and type(self.get_player2()) == Player: return None
        if self.get_player1() != self.player: return self.get_player1().get_name()
        return self.get_player2().get_name()
    def text2(self) -> str:
        if type(self.get_player2()) == Player: return None
        return self.get_player2().get_name()

    def get_clock1(self) -> int: return 180
    def get_clock2(self) -> int: return 180

    def get_users(self, user: int = None):
        '''Returns the list of users. If the variable user is set to a number bigger than 0, it will return the user indexed to that number minus 1.'''
        if user is not None: return self.users[user - 1]
        return self.users

    def get_player1(self): return self.player1
    def get_player2(self): return self.player2
    def get_players(self) -> list:
        '''Returns a list with the player 1 and the player 2.'''
        return [self.get_player1(), self.get_player2()]

    def set_player1(self, entity) -> None:
        '''Sets who is playing, the player or one of the bots.'''
        self.player1 = entity
    def set_player2(self, entity = None) -> None:
        '''Sets the opponent, the second user or one of the bots. By default it's set to the selected bot.'''
        if entity is not None: self.player2 = entity
        else: self.player2 = self.bots[self.get_selected_bot()]

    def get_win_label_limit(self) -> int: return self.win_label_limit 
    def get_win_player(self) -> int: return self.win_player

    def print_board(self) -> None:
        '''Testing purposes.'''
        for row in self.board.get_matrix(): print(row)

    # Input Section

    def update_mouse(self, event) -> None: self.mouse_pos = event.pos

    def handle_events(self) -> None:
        '''Depending on which menu the user is, redefines variables to change the app state.'''

        def user_input(user: int) -> None:
            if self.isMouseClicked():
                if self.legal_moves_button.isClicked(self.get_mouse_pos()): self.set_display()
                elif self.exit_button.isClicked(self.get_mouse_pos()):
                    self.current_state = 1
                    self.initialize_board()

                board_pos = self.identify_board_click(self.get_mouse_pos())
                if board_pos in self.get_legal_moves():
                    self.get_users(user).play(board_pos)
                    self.check_game_status()
                    self.set_turn(user%2 + 1)

                self.mouse_switch()

        match self.states[self.get_current_state()]:

            case "main_menu":
                if self.isMouseClicked():
                    if self.play_button.isClicked(self.get_mouse_pos()) and self.isMouseClicked():
                        self.current_state = 1
                        self.mouse_switch()

                    elif self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1

            case "game_modes":
                if self.isMouseClicked():
                    if self.hum_vs_bot_button.isClicked(self.get_mouse_pos()): self.current_state = 3
                    elif self.normal_button.isClicked(self.get_mouse_pos()) and not self.clock1.is_built() and not self.clock2.is_built(): self.current_state = 8
                    elif self.bot_vs_bot_button.isClicked(self.get_mouse_pos()): self.current_state = 5
                    elif self.back_button.isClicked(self.get_mouse_pos()): self.current_state = 0
                    elif self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1
                    self.mouse_switch()

            case "time_menu":
                if self.isMouseClicked():
                    if self.back_button.isClicked(self.get_mouse_pos()):
                        self.current_state = 1
                    if self.time_option_1.isClicked(self.get_mouse_pos()): 
                        self.clock1.time = 180
                        self.clock2.time = 180
                        self.current_state = 4
                    elif self.time_option_2.isClicked(self.get_mouse_pos()): 
                        self.clock1.time = 300
                        self.clock2.time = 300
                        self.current_state = 4
                    elif self.time_option_3.isClicked(self.get_mouse_pos()): 
                        self.clock1.time = 900
                        self.clock2.time = 900
                        self.current_state = 4
                    elif self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1
                    self.mouse_switch()

            case "normal":
                if not self.clock1.is_running() or not self.clock2.is_running():
                    self.clock1.start()
                    self.clock2.start()
                if self.clock1.end:
                    self.winner = 2
                    self.current_state = 2

                elif self.clock2.end:
                    self.winner = 1
                    self.current_state = 2

                self.set_player1(self.player)
                self.set_player2(self.opponent)

                if self.isMouseClicked():
                    if self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1

                match self.get_turn():
                    case 1:
                        self.clock2.pause_switch(True)
                        self.clock1.pause_switch(False)
                        self.draw_hlabels()
                    case 2:
                        self.clock1.pause_switch(True)
                        self.clock2.pause_switch(False)
                        self.draw_hlabels()
                user_input(self.get_turn())

            case "vscomp":
                if self.isMouseClicked():
                    if self.back_button.isClicked(self.get_mouse_pos()): self.current_state = 1
                    if self.min_button.isClicked(self.get_mouse_pos()):
                        self.set_selected_bot(self.get_minmax())
                        self.current_state = 6
                    elif self.min_ab_button.isClicked(self.get_mouse_pos()):
                        self.set_selected_bot(self.get_minmax_ab())
                        self.current_state = 6
                    elif self.monte_carlo_button.isClicked(self.get_mouse_pos()):
                        self.set_selected_bot(self.get_monte_carlo())
                        self.current_state = 6
                    elif self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1
                    self.mouse_switch()

            case "vscomp_ingame":
                self.set_player2()
                if self.isMouseClicked():
                    if self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1
                    if self.hint_lable.isClicked(self.get_mouse_pos()):
                        self.hint_istaken = True
                if self.get_turn() == int(self.get_users()[0].getPiece()): user_input(self.get_turn())

            case "bot_vs_bot":
                if self.isMouseClicked():
                    if self.select_bot1_button.isClicked(self.get_mouse_pos()):
                        self.set_bot1((self.get_bot1() + 1)%len(self.get_bots()))
                    elif self.select_bot2_button.isClicked(self.get_mouse_pos()):
                        self.set_bot2((self.get_bot2() + 1)%len(self.get_bots()))
                    elif self.bot_vs_bot_start_button.isClicked(self.get_mouse_pos()):
                        self.current_state = 7
                    elif self.back_button.isClicked(self.get_mouse_pos()): self.current_state = 1
                    elif self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1
                    self.mouse_switch()

                self.set_player1(self.get_bots(self.get_bot1()))
                self.set_player2(self.get_bots(self.get_bot2()))

            case "bot_vs_bot_ingame":
                if self.isMouseClicked():
                    if self.exit_button.isClicked(self.get_mouse_pos()):
                        self.current_state = 1
                        self.initialize_board()
                        self.mouse_switch()
                    elif self.sound.isClicked(self.get_mouse_pos()):
                        self.sound_tick += 1

                self.set_player1(self.get_bots(self.get_bot1()))
                self.set_player2(self.get_bots(self.get_bot2()))

        if self.get_game_state() != 0:
            self.current_state = 2
            self.win_player = self.get_game_state()

    def get_inputs(self) -> None:
        '''Loops over all pygame events and handles the events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_switch(True)
            else: self.mouse_switch(False)
            if event.type == pygame.MOUSEMOTION: self.update_mouse(event)
        self.handle_events()

    # Process Input and Bot play

    def identify_board_click(self, pos: tuple[int,int]) -> tuple[int,int]:
        if pygame.Rect(pos[0],pos[1],0,0) not in self.board.get_rect(): return (-1,-1)
        return (int((pos[1] - self.board.get_rect().y)// SQUARE_SIZE), int((pos[0] - self.board.get_rect().x) // SQUARE_SIZE))

    def check_game_status(self) -> None:
        directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1),(1,-1),(-1,1)]
        for vector in directions:
            if self.checkWin(self.board.get_matrix(),vector,self.get_turn()): self.game_state = self.get_turn()
        if self.get_game_state() == 0 and self.checkDraw(self.board.get_matrix()): self.game_state = 3

    def checkWin(self, matrix, vector: tuple[int,int], turn: int) -> bool:
        def verify(i: int, j: int, vector: tuple[int,int], turn: int, count: int):
            if count == 4: return True
            elif not (-1 < i < len(matrix) and -1 < j < len(matrix[0])): return False
            elif matrix[i][j] != str(turn): return False
            return verify(i + vector[0], j + vector[1], vector, turn, count + 1)

        for i, row in enumerate(matrix):
            for j, entry in enumerate(row):
                if entry == str(turn):
                    check = verify(i, j, vector, turn, 0)
                    if check: return check
        return False

    def checkDraw(self, matrix) -> None:
        for row in matrix:
            for entry in row:
                if entry == "0": return False
        return True

    def get_legal_moves(self, board: Board = None) -> list[tuple[int,int]]:
        if board is None: board = self.board
        moves = []

        for i in {0, board.get_rows() - 1}:
            for j in range(board.get_columns()):
                for k in range(0, board.get_rows(), 1):
                    if i > 0: k = -k
                    if (i+k,j) in moves: break
                    if board.get_matrix()[i+k,j] == "0":
                        moves.append((i+k,j))
                        break

        for j in {0, board.get_columns() - 1}:
            for i in range(1, board.get_rows() - 1):
                for k in range(0, board.get_columns()):
                    if j > 0: k = -k
                    if (i,j+k) in moves: break
                    if board.get_matrix()[i,j+k] == "0":
                        moves.append((i,j+k))
                        break

        return moves

    def play_bot(self, bot, turn: str) -> None:
        bot.play(turn)
        self.check_game_status()
        turn = 1 if turn == "2" else 2
        self.set_turn(turn)

    def play(self) -> None:
        if self.get_game_state() == 0 and self.get_current_state() in {6,7}:
            match self.get_turn():
                case 1:
                    if self.get_player1() != self.player: self.play_bot(self.get_player1(), "1")
                case 2: self.play_bot(self.get_player2(), "2")

    # Draw on the screen section

    def cleanScreen(self) -> None:
        self.screen.fill(BACKGROUND)
        self.screen.blit(BG_IMAGE, (-0.15 * WIDTH, -0.15 * HEIGHT))

    def draw_board(self) -> None:
        '''Draws a background. Loops over all the board positions and draws the colored squares on even i + j positions. If a place is on the board, then the code recognizes and draws a circle on that position.'''
        pygame.draw.rect(self.screen, BOARD_COLOR, self.board.get_rect())
        for i in range(self.board.get_rows()):
            for j in range(self.board.get_columns()):
                x, y = (self.board.get_rect().x + j * SQUARE_SIZE, self.board.get_rect().y + i * SQUARE_SIZE)
                if (i+j) % 2 == 0: pygame.draw.rect(self.screen, SQUARE_COLOR, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))
                if self.board.get_matrix()[i,j] != "0": pygame.draw.circle(self.screen, PLAYER_COLORS[self.board.get_matrix()[i,j]], (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), SQUARE_SIZE//2)

    def display_legal_moves(self) -> None:
        for move in self.get_legal_moves():
            center = (self.board.get_rect().x + move[1] * SQUARE_SIZE + SQUARE_SIZE//2, self.board.get_rect().y + move[0] * SQUARE_SIZE + SQUARE_SIZE//2)
            color = COLORS["dark_dark_wood"] if (move[0] + move[1]) % 2 else COLORS["wood"]
            pygame.draw.circle(self.screen, color, center, SQUARE_SIZE//4)

    def draw_winning_label(self) -> None:
        self.cleanScreen()
        text = f"{self.get_player1().get_name() if self.get_win_player() == 1 else self.get_player2().get_name()} WON" if self.get_win_player() != 3 else "DRAW"
        label = self.win_font.render(text, True, COLORS["red"])
        self.screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))

        if self.win_label_clock == self.win_label_limit:
            self.win_label_clock = 0
            self.current_state = 0
            self.initialize_board()
        elif self.timer == self.ticks: self.win_label_clock += 1

    def draw_hlabels(self) -> None:
        if self.board == self.previous_board or self.previous_board == None:
            self.eval_bot.root_state = self.board
            root = self.eval_bot.minimax(f"{self.get_turn() % 2 + 1}", None, False)
            eval = max([child.get_reward() for child in root.get_children()])
            eval = -eval if self.get_turn() == 2 else eval
            eval_soft = round(softmax(eval), 1)

            white_height = HEIGHT * eval_soft
            black_height = HEIGHT - white_height

            self.black_label.height = black_height
            self.white_label.y = black_height
            self.white_label.height = white_height

            self.black_label.draw_label("2")
            self.white_label.draw_label("1")
            color = COLORS["black"] if black_height < HEIGHT - self.white_label.width//2 - 5 else COLORS["white"]
            eval_label = self.eval_font.render(f"{round(eval, 1)}", True, color)
            self.screen.blit(eval_label, (self.white_label.x + eval_label.get_width()//2, HEIGHT - eval_label.get_height() - 5))
            self.previous_board = self.board

    def draw_game_modes_menu(self) -> None:
        self.cleanScreen()
        self.normal_button.draw()
        self.hum_vs_bot_button.draw()
        self.bot_vs_bot_button.draw()
        self.back_button.draw()

    def draw_time_menu(self) -> None:
        self.cleanScreen()
        self.back_button.draw()
        self.time_option_1.draw()
        self.time_option_2.draw()
        self.time_option_3.draw()

    def draw_bot_select_menu(self) -> None:
        self.cleanScreen()
        self.min_ab_button.draw()
        self.min_button.draw()
        self.monte_carlo_button.draw()
        self.back_button.draw()

    def draw_bot_vs_bot_select_menu(self) -> None:
        self.cleanScreen()
        self.select_bot1_button.draw()
        self.select_bot2_button.draw()
        self.bot_vs_bot_start_button.draw()
        self.back_button.draw()

    def draw_clocks(self) -> None:
        self.clock1.draw()
        self.clock2.draw()

    def draw_sound_button(self)->None:
        if self.sound_tick % 2 == 0:
            self.sound.draw_sound()
            self.sound_tick = 0
            pygame.mixer.music.unpause()
        elif self.sound_tick == 1:
            pygame.mixer.music.pause()
            self.sound.draw_no_sound()

    def draw_main_menu(self) -> None:
        self.cleanScreen()
        self.play_button.draw()

    def draw_game(self) -> None:
        self.cleanScreen()
        self.draw_board()
        self.draw_hlabels()
        if self.get_display(): self.display_legal_moves()
        self.legal_moves_button.draw()

        if self.get_current_state() == 4: self.draw_clocks()
        self.exit_button.draw()
        if not self.hint_istaken and self.get_current_state() == 6: self.hint_lable.draw()

    def draw(self) -> None:
        match self.states[self.get_current_state()]:
            case "main_menu": self.draw_main_menu()
            case "game_modes": self.draw_game_modes_menu()
            case "win_label": self.draw_winning_label()
            case "vscomp": self.draw_bot_select_menu()
            case "bot_vs_bot": self.draw_bot_vs_bot_select_menu()
            case "time_menu": self.draw_time_menu()
            case _: self.draw_game()
        self.draw_sound_button()

    # main function

    def run(self) -> None:
        while self.isRunning():
            if self.timer == self.ticks:
                self.get_inputs()
                self.play()
                self.draw()
                pygame.display.update()
                self.timer = 0
            self.timer += 1
