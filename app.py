import pyxel
import time

from enum import Enum
from image import ImageManager, ImageName
from timeline import TimelineManager, TimelineName

DEFAULT_FPS = 30
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
        pyxel.init(
            SCREEN_WIDTH, SCREEN_HEIGHT, fps=DEFAULT_FPS, display_scale=DISPLAY_SCALE
        )

        self.state = GameState.SPLASH
        self.start_time = time.time()

        self.image = ImageManager()
        self.timeline = TimelineManager()

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
        self.image.draw(ImageName.BG_01, 0, 0)

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

    def show_splash(self):
        self.image.draw(ImageName.Bear_01, 36, 41)
        self.image.draw(ImageName.Logo, 14, 85)

    def show_prologue(self):
        pyxel.text(0, 0, "PROLOGUE", 10)
        self.timeline.play(TimelineName.Prologue)

    def show_game_start(self):
        pyxel.text(0, 0, "GAME START", 10)

    def start_game(self):
        pyxel.text(0, 0, "PLAY", 10)
        self.image.draw(ImageName.BearFace, 3, 84)
        self.image.draw(ImageName.Tweezers_01, 76, 32, animation_speed=0.8)
        self.image.draw(ImageName.Tweezers_01, 76, 46, animation_speed=0.8)
        self.image.draw(ImageName.Tweezers_01, 76, 60, animation_speed=0.8)
        self.image.draw(ImageName.PenguinS_02, 41, 17)

    def show_game_end(self):
        pyxel.text(0, 0, "WIN / LOSE", 10)
        self.image.draw(ImageName.CLEAR_BG_01, 3, 36)
        self.image.draw(ImageName.CLEAR, 17, 52)

    def show_result(self):
        pyxel.text(0, 0, "RESULT", 10)
        self.image.draw(ImageName.PenguinM_02, 34, 26)
        self.image.draw(ImageName.PenguinL_02, 23, 40)

    def show_retry(self):
        pyxel.text(0, 0, "RETRY ", 10)


App()
