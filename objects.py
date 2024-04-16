from pygame import Rect, draw, font, transform
from copy import deepcopy
from settings import BUTTON_IMAGE, CLOCK_IMAGE,SOUND_IMAGE,SOUND_OFF_IMAGE,COLORS
from collections import defaultdict
import numpy as np
import time, threading

class Board:
    def __init__(self, n, m, x, y, width, height) -> None:
        self.n, self.m = n, m
        self.matrix = np.empty((n,m), dtype = str)
        self.matrix.fill("0")

        self.rect = Rect(x,y,width,height)

    def get_rows(self) -> int: return self.matrix.shape[0]
    def get_columns(self) -> int: return self.matrix.shape[1]
    def get_matrix(self): return deepcopy(self.matrix)
    def get_rect(self): return self.rect

    def __eq__(self, other) -> bool:
        if other == None: return False
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i,j] != other.matrix[i,j]: return False
        return True

    def update(self, matrix) -> None: self.matrix = matrix
    def place_piece(self, piece_type: str, move: tuple[int, int]) -> None: self.matrix[move[0],move[1]] = piece_type
    def set_rect(self, x: int, y: int, width: int, height: int) -> None: Rect(x,y,width,height)

    @staticmethod
    def place(board, piece_type: str, move: tuple[int, int]) -> None:
        board.matrix[move[0],move[1]] = piece_type

class Button:
    def __init__(self, screen, x: int, y: int, width: int, height: int, color: tuple[int,int,int], font_color: tuple[int,int,int], text: str, text_size: int, _font: str) -> None:
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color, self.font_color = color, font_color
        self.text, self.text_size = text, text_size
        self.font = font.SysFont(_font, self.text_size)
        self.rect = Rect(x,y,width,height)

    def getSurface(self):
        text = self.text() if type(self.text) != str else self.text
        return self.font.render(text, True, self.font_color)
    def getRect(self): return Rect(self.x, self.y, self.width, self.height)

    def isClicked(self, mouse) -> bool: return 0 <= mouse[0] - self.x <= self.width and 0 <= mouse[1] - self.y <= self.height

    def draw(self) -> None:
        # draw.rect(self.screen, self.color, self.getRect())
        self.screen.blit(transform.scale(BUTTON_IMAGE, (self.getRect().width, self.getRect().height)), (self.getRect().x, self.getRect().y))
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))

    def draw_sound(self)->None:
        self.screen.blit(transform.scale(SOUND_IMAGE, (self.getRect().width, self.getRect().height)), (self.getRect().x, self.getRect().y))
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))

    def draw_no_sound(self)->None:
        self.screen.blit(transform.scale(SOUND_OFF_IMAGE, (self.getRect().width, self.getRect().height)), (self.getRect().x, self.getRect().y))
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))

    def draw_label(self, turn: str)->None:
        if turn == "1": draw.rect(self.screen, COLORS["white"] , self.getRect())
        else: draw.rect(self.screen, COLORS["black"] , self.getRect())
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))

class Clock(): 
    def __init__(self, screen, x: int, y: int, width: int, height: int, color: tuple[int,int,int], font_color: tuple[int,int,int], time: int, text_size: int, _font: str) ->None:

        # display variables
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color, self.font_color = color, font_color
        self.text, self.text_size = "", text_size
        self.font = font.SysFont(_font, self.text_size)
        self.rect = Rect(x,y,width,height)

        # timer variables
        self.paused = True  
        self.running = False
        self.time = time
        self.end=False

        self.built = False

    def get_time(self) -> int: return self.time
    def set_time(self, time: int) -> None: self.time = time

    def is_running(self) -> bool: return self.running
    def run_switch(self, state: bool = None) -> None:
        if state is not None: self.running = state
        else: self.running = not self.running
    def is_paused(self) -> bool: return self.paused
    def pause_switch(self, state: bool = None) -> None:
        if state is not None: self.paused = state
        else: self.paused = not self.paused

    def is_built(self) -> bool: return self.built
    def set_built(self, state: bool) -> None: self.built = state
    def get_destroyed(self) -> bool: return self.destroy
    def set_destroyed(self, state: bool) -> None: self.destroy = state

    def build_clock(self) -> None:
        self.set_destroyed(False)
        self.timer_thread = threading.Thread(target = self.tick)
        self.timer_thread.daemon = True
        self.set_built(True)

    def kill(self) -> None:
        if self.is_built():
            self.set_destroyed(True)
            self.run_switch(False)
            self.pause_switch(False)

    def pause(self):
        while self.is_paused(): time.sleep(1)

    def start(self) -> None:
        self.build_clock()
        self.timer_thread.start()

    def tick(self)->None:
        self.pause_switch(False)
        self.run_switch(True)

        for timer in range(self.time, -1, -1):
            if self.get_destroyed():
                self.set_built(False)
                break
            if self.is_paused(): self.pause()
            seconds = timer % 60
            minutes = timer // 60  
            self.text = f"{minutes:02}:{seconds:02}"
            time.sleep(1)
            if timer == 0: 
                self.end=True
                break

    def getSurface(self): return self.font.render(self.text, True, self.font_color)
    def getRect(self): return Rect(self.x, self.y, self.width, self.height)

    def draw(self) -> None:
        # draw.rect(self.screen, self.color, self.getRect())
        self.screen.blit(transform.scale(BUTTON_IMAGE, (self.getRect().width, self.getRect().height)), (self.getRect().x, self.getRect().y))
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))

class Node:
    next_node_id = 0
    visits = defaultdict(lambda: 0)

    def reset() -> None:
        Node.next_node_id = 0
        Node.visits = defaultdict(lambda: 0)

    def __init__(self, state, parent = None, action = None, reward: float = .0):
        self.state = state
        self.parent = parent
        self.children = set()

        self.reward = reward
        self.action = action

        self.terminal = False

        self.id = Node.next_node_id
        Node.next_node_id += 1

    def __str__(self) -> str: return f"Node (Id/Gen): {self.get_id()}/{self.get_generation()}; State: {self.get_state()}; Parent: {self.get_parent()}; Children: {set([child.get_id() for child in self.get_children()])}; Reward: {self.get_reward()}; Visits: {self.get_visits()}"

    def is_root(self) -> bool: return self.get_parent() == None
    def is_terminal(self) -> bool: return self.terminal

    def get_id(self) -> int: return self.id
    def get_visits(self) -> int: return Node.visits[self.get_state()]
    def get_reward(self) -> float: return self.reward

    def get_parent(self): return self.parent
    def get_children(self) -> set: return self.children
    def get_generation(self) -> int:
        node = self
        generation = 0
        while node.get_parent() != None:
            node = node.get_parent()
            generation += 1
        return generation

    def get_state(self): return self.state
    def get_action(self): return self.action

    def increase_visits(self, amount: int = 1) -> None: Node.visits[self.get_state()] += amount
    def increase_reward(self, amount: float = 1) -> None: self.reward += amount

    def set_reward(self, reward: int) -> None: self.reward = reward
    def set_action(self, action) -> None: self.action = action
    def set_children(self, children: set) -> None: self.children = children
    def set_terminal(self, terminal: bool) -> None: self.terminal = terminal
