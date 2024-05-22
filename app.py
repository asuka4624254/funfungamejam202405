import pyxel
import time

from enum import Enum
import PyxelUniversalFont as puf
from image import Image, ImageAsset


SCREEN_WIDTH = 96  # 480
SCREEN_HEIGHT = 128  # 640
DISPLAY_SCALE = 5


class GameState(Enum):
    SPLASH = 1
    PROLOGUE = 2
    GAME_START = 3
    PLAY = 4
    GAME_END = 5
    RESULT = 6
    RETRY = 7


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, display_scale=DISPLAY_SCALE)

        self.state = GameState.SPLASH
        self.start_time = time.time()

        self.image = Image()

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == GameState.SPLASH:
            self.check_click(GameState.PROLOGUE)
        elif self.state == GameState.PROLOGUE:
            self.check_click(GameState.GAME_START)
        elif self.state == GameState.GAME_START:
            self.check_click(GameState.PLAY)
        elif self.state == GameState.PLAY:
            self.check_click(GameState.GAME_END)
        elif self.state == GameState.GAME_END:
            self.check_click(GameState.RESULT)
        elif self.state == GameState.RESULT:
            self.check_click(GameState.RETRY)
        elif self.state == GameState.RETRY:
            self.check_click(GameState.SPLASH)

    def check_transition(self, next_status, transition_seconds):
        if time.time() - self.start_time > transition_seconds:
            self.state = next_status
            self.start_time = time.time()

    def check_click(self, next_status):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = next_status

    def draw(self):
        pyxel.cls(0)
        self.image.draw(ImageAsset.BG_01, 0, 0)

        if self.state == GameState.SPLASH:
            self.show_splash()
        elif self.state == GameState.PROLOGUE:
            self.show_prologue()
        elif self.state == GameState.GAME_START:
            self.show_game_start()
        elif self.state == GameState.PLAY:
            self.start_game()
        elif self.state == GameState.GAME_END:
            self.show_game_end()
        elif self.state == GameState.RESULT:
            self.show_result()
        elif self.state == GameState.RETRY:
            self.show_retry()

    def show_mozi(self, x, y, text, size, color):
        writer = puf.Writer("ipa_gothic.ttf")
        writer.draw(x, y, text, size, color)

    def show_splash(self):
        self.image.draw(ImageAsset.BEAR, 36, 41)
        self.image.draw(ImageAsset.LOGO, 14, 85)

    def show_prologue(self):
        self.show_mozi(0, 0, "PROLOGUE", 10, 0)

    def show_game_start(self):
        self.show_mozi(0, 0, "GAME START", 10, 0)

    def start_game(self):
        self.show_mozi(0, 0, "PLAY", 10, 0)

    def show_game_end(self):
        self.show_mozi(0, 0, "WIN / LOSE", 10, 0)

    def show_result(self):
        self.show_mozi(0, 0, "RESULT", 10, 0)

    def show_retry(self):
        self.show_mozi(0, 0, "RETRY ", 10, 0)


App()
