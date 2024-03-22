from screeninfo import get_monitors
import pygame

pygame.init()

monitor = get_monitors()[0]
RESIZE_FACTOR = 0.75
WIDTH, HEIGHT = RESIZE_FACTOR * monitor.width, RESIZE_FACTOR * monitor.height
TITLE = "SpiderLine4"

SIZE = 36
MAIN_FONT = pygame.font.SysFont("comic sans",SIZE)

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
    'gray': (128, 128, 128),
    'brown': (165, 42, 42),
    'light_blue': (173, 216, 230),
    'light_green': (144, 238, 144),
    'light_gray': (211, 211, 211),
    'dark_gray': (169, 169, 169),
}

BACKGROUND = COLORS["gray"]

BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH//4, HEIGHT//5
BUTTON_COLOR = COLORS["dark_gray"]

FONT_COLOR = COLORS["white"]
TEXT_SIZE = 50
MAIN_FONT = "comic sans"

N, M = 8, 8
SQUARE_SIZE = HEIGHT/M
SQUARE_COLOR = COLORS["yellow"]

BOARD_WIDTH, BOARD_HEIGHT = SQUARE_SIZE * M, SQUARE_SIZE * N
BOARD_COLOR = COLORS["light_blue"]

PLAYER_COLORS = {"1": COLORS["white"],"2": COLORS["black"]}

FPS = 100

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
