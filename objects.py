from pygame import Rect, draw, font
from copy import deepcopy
import numpy as np
import time, threading

class Board:
    def __init__(self, n, m, x, y, width, height) -> None:
        self.matrix = np.empty((n,m), dtype = str)
        self.matrix.fill("0")

        self.rect = Rect(x,y,width,height)

    def get_rows(self) -> int: return self.matrix.shape[0]
    def get_columns(self) -> int: return self.matrix.shape[1]
    def get_matrix(self): return deepcopy(self.matrix)
    def get_rect(self): return self.rect

    def update(self, matrix) -> None: self.matrix = matrix
    def place_piece(self, piece_type: str, move: tuple[int, int]) -> None: self.matrix[move[0],move[1]] = piece_type
    def set_rect(self, x: int, y: int, width: int, height: int) -> None: pygame.Rect(x,y,width,height)

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
        draw.rect(self.screen, self.color, self.getRect())
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

    def getSurface(self): return self.font.render(self.text, True, self.font_color)
    def getRect(self): return Rect(self.x, self.y, self.width, self.height)

    def draw(self) -> None:
        draw.rect(self.screen, self.color, self.getRect())
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))
