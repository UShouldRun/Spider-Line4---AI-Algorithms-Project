from pygame import Rect, draw, font
from copy import deepcopy
import numpy as np

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
    def set_rect(self, x: int, y: int, width: int, height: int) -> None: pygame.Rect(x,y,width,height)

class Button:
    def __init__(self, screen, x: int, y: int, width: int, height: int, color: tuple[int,int,int], font_color: tuple[int,int,int], text: str, text_size: int, _font: str) -> None:
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color, self.font_color = color, font_color
        self.text, self.text_size = text, text_size
        self.font = font.SysFont(_font, self.text_size)
        self.rect = Rect(x,y,width,height)

    def getSurface(self): return self.font.render(self.text, True, self.font_color)
    def getRect(self): return Rect(self.x, self.y, self.width, self.height)
    def getClicked(self): return self.clicked

    def isClicked(self, event) -> bool: pass
        
    def setClicked(self, state: bool): self.clicked = state

    def draw(self) -> None:
        draw.rect(self.screen, self.color, self.getRect())
        self.screen.blit(self.getSurface(), (self.x + self.width//2 - self.getSurface().get_width()//2, self.y + self.height//2 - self.getSurface().get_height()//2))

