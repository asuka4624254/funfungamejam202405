import pyxel
import time

from enum import Enum
import PyxelUniversalFont as puf


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


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
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.state = GameState.SPLASH
        self.start_time = time.time()

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == GameState.SPLASH:
            self.check_transition(GameState.PROLOGUE, 5)
        elif self.state == GameState.PROLOGUE:
            self.check_transition(GameState.GAME_START, 5)
        elif self.state == GameState.GAME_START:
            self.check_transition(GameState.PLAY, 5)
        elif self.state == GameState.PLAY:
            self.check_click(GameState.GAME_END)
        elif self.state == GameState.GAME_END:
            self.check_transition(GameState.RESULT, 5)
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
        self.show_mozi(150, 100, "SPLASH SCREEN", 21, 7)

    def show_prologue(self):
        self.show_mozi(50, 60, "PROLOGUE", 21, 7)

    def show_game_start(self):
        self.show_mozi(50, 60, "GAME START", 21, 7)

    def start_game(self):
        self.show_mozi(50, 60, "PLAY ... PUSH SPACE", 21, 7)

    def show_game_end(self):
        self.show_mozi(50, 60, "WIN / LOSE", 21, 7)

    def show_result(self):
        self.show_mozi(50, 60, "RESULT ... PUSH SPACE", 21, 7)

    def show_retry(self):
        self.show_mozi(50, 60, "RETRY ... PUSH SPACE", 21, 7)


App()
