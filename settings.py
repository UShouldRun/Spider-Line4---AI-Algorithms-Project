from screeninfo import get_monitors
import pygame

pygame.init()

monitor = get_monitors()[0]
RESIZE_FACTOR = 0.75
WIDTH, HEIGHT = RESIZE_FACTOR * monitor.width, RESIZE_FACTOR * monitor.height
TITLE = "SpiderLine4"

SIZE = 50
MAIN_FONT = pygame.font.SysFont("comic sans", SIZE)

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
    'light_wood': (220, 192, 139),
    'dark_wood': (101, 67, 33),
    'beige': (245, 245, 220)
}

BACKGROUND = COLORS["gray"]

BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH//4, HEIGHT//5
BUTTON_COLOR = COLORS["dark_wood"]

FONT_COLOR = COLORS["beige"]
TEXT_SIZE = int(BUTTON_WIDTH//8)
MAIN_FONT = "comic sans"

N, M = 8, 8
SQUARE_SIZE = HEIGHT/M
SQUARE_COLOR = COLORS["light_wood"]

BOARD_WIDTH, BOARD_HEIGHT = SQUARE_SIZE * M, SQUARE_SIZE * N
BOARD_COLOR = COLORS["dark_wood"]

PLAYER_COLORS = {"1": COLORS["white"],"2": COLORS["black"]}

FPS = 100


BG_IMAGE = pygame.transform.scale(pygame.image.load("resources/assets/PNG/UI board Large  parchment.png"), (WIDTH * 1.25, HEIGHT * 1.25))
BUTTON_IMAGE = pygame.image.load("resources/assets/PNG/TextBTN_Medium.png")
CLOCK_IMAGE = pygame.image.load("resources/assets/PNG/UI board Small  stone.png")
SOUND_IMAGE=pygame.image.load("resources/assets/PNG/button_sound_on.png")
SOUND_OFF_IMAGE=pygame.image.load("resources/assets/PNG/button_sound_off.png")

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
