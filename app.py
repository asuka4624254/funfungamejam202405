import pyxel
import time
import random

from enum import Enum, auto
from image import ImageManager, ImageName
from timeline import TimelineManager, TimelineName

# 定数の定義
DEFAULT_FPS = 30
SCREEN_WIDTH = 96
SCREEN_HEIGHT = 128
DISPLAY_SCALE = 5

TIME_INCREMENT = 300
TIME_DECREMENT_ON_FAIL = 30
GAUGE_HEIGHT = 66
GAUGE_WIDTH = 4
HAIR_FALL_DURATION = 15
HAIR_REGROW_DELAY = 30
TWEEZER_SLOWDOWN = 0.5

HARD_MODE_MULTIPLIER = 5  # ハードモードのゲージ上昇速度倍率
HARD_MODE_HAIR_COUNT = 5  # ハードモードの抜く本数
NORMAL_MODE_HAIR_COUNT = 10


# ゲーム状態の定義
class GameState(Enum):
    SPLASH = auto()
    PROLOGUE = auto()
    READY = auto()
    GAME_START = auto()
    PLAY = auto()
    GAME_CLEAR = auto()
    GAME_MISS = auto()
    RETRY = auto()


# グローバル変数
power = 0
increasing = True
message = ""
time_left = TIME_INCREMENT
special_count = 3
hair_left = 0
tweezer_count = 3
tweezer_active = False
hair_falling = False
hair_fall_frame = 0
hair_regrow_frame = 0
last_state_change_time = time.time()
is_hard_mode = False
high_score = None  # ハイスコアを記録する変数を追加


# ゲームのメインクラス
class App:
    def __init__(self, n):
        global hair_left, last_state_change_time, is_hard_mode
        pyxel.init(
            SCREEN_WIDTH, SCREEN_HEIGHT, fps=DEFAULT_FPS, display_scale=DISPLAY_SCALE
        )
        pyxel.mouse(True)

        self.state = GameState.SPLASH
        self.start_time = time.time()

        self.image = ImageManager()
        self.timeline = TimelineManager()

        hair_left = n
        last_state_change_time = time.time()
        self.state_change_allowed = False
        is_hard_mode = False

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        global power, increasing, message, time_left, special_count, hair_left, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_count, tweezer_active, last_state_change_time, is_hard_mode
        power = 0
        increasing = True
        message = ""
        time_left = TIME_INCREMENT
        special_count = 3
        self.state = GameState.PLAY
        tweezer_count = 3
        tweezer_active = False
        hair_falling = False
        hair_fall_frame = 0
        hair_regrow_frame = HAIR_REGROW_DELAY  # 初期状態で鼻毛が描写されるように設定
        last_state_change_time = time.time()
        self.state_change_allowed = True
        hair_left = NORMAL_MODE_HAIR_COUNT
        self.start_time = time.time()  # ゲーム開始時のタイムスタンプをリセット
        if is_hard_mode:
            hair_left = HARD_MODE_HAIR_COUNT
            tweezer_count = 0  # ハードモードでは毛抜が使えない

    def update_power(self):
        global power, increasing, tweezer_active, is_hard_mode
        increment = random.randint(1, 3)
        if is_hard_mode:
            increment *= HARD_MODE_MULTIPLIER  # ハードモードではゲージの上昇が早い
        if tweezer_active:
            increment = int(increment * TWEEZER_SLOWDOWN)

        if increasing:
            power += increment
            if power >= 100:
                power = 100
                increasing = False
        else:
            power -= increment
            if power <= 0:
                power = 0
                increasing = True

    def handle_space_key(self):
        global message, hair_left, time_left, hair_falling, hair_fall_frame, tweezer_active
        if 40 <= power <= 60:
            message = "やった！抜けた！"
            hair_left -= 1
            hair_falling = True
            hair_fall_frame = 0
            tweezer_active = False
        else:
            message = "イテテ・・・"
            time_left -= TIME_DECREMENT_ON_FAIL

    def handle_special_key(self):
        global message, time_left, special_count
        if special_count > 0:
            time_left += TIME_INCREMENT
            special_count -= 1
            message = "Special used!"

    def handle_tweezer_key(self):
        global message, tweezer_count, tweezer_active
        if tweezer_count > 0 and not tweezer_active:
            tweezer_active = True
            tweezer_count -= 1
            message = "毛抜使うよ！"

    def update(self):
        global time_left, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_active, is_hard_mode, high_score

        allowed_seconds = 2 if self.state == GameState.SPLASH else 1
        if (
            not self.state_change_allowed
            and time.time() - last_state_change_time > allowed_seconds
        ):
            self.state_change_allowed = True

        if self.state == GameState.SPLASH:
            self.check_click(GameState.PROLOGUE)
        elif self.state == GameState.PROLOGUE:
            if pyxel.btn(pyxel.KEY_SHIFT):
                is_hard_mode = True
            self.check_click(GameState.READY)
            if self.timeline.is_play(TimelineName.Prologue) == False:
                self.state = GameState.READY
                self.timeline.reset()
        elif self.state == GameState.READY:
            if self.timeline.is_play(TimelineName.Ready) == False:
                self.state = GameState.GAME_START
                self.timeline.reset()
        elif self.state == GameState.GAME_START:
            self.reset_game()
            self.check_click(GameState.PLAY)
        elif self.state == GameState.PLAY:
            if time_left > 0:
                time_left -= 1
                self.update_power()

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.handle_space_key()

            if pyxel.btnp(pyxel.KEY_S):
                self.handle_special_key()

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and (
                (
                    tweezer_count >= 1
                    and (76 <= pyxel.mouse_x <= 92)
                    and (32 <= pyxel.mouse_y <= 43)
                )
                or (
                    tweezer_count >= 2
                    and (76 <= pyxel.mouse_x <= 92)
                    and (46 <= pyxel.mouse_y <= 57)
                )
                or (
                    (tweezer_count >= 3 and 76 <= pyxel.mouse_x <= 92)
                    and (60 <= pyxel.mouse_y <= 71)
                )
            ):
                self.handle_tweezer_key()

            if hair_falling:
                hair_fall_frame += 1
                if hair_fall_frame >= HAIR_FALL_DURATION:
                    hair_falling = False
                    hair_regrow_frame = 0
            else:
                if hair_regrow_frame < HAIR_REGROW_DELAY:
                    hair_regrow_frame += 1

            if hair_left <= 0:
                self.state = GameState.GAME_CLEAR
                self.set_state_change_time()

                # クリア時間を記録
                clear_time = time.time() - self.start_time
                if high_score is None or clear_time < high_score:
                    high_score = clear_time

            if time_left <= 0:
                self.state = GameState.GAME_MISS
                self.set_state_change_time()
        elif self.state == GameState.GAME_CLEAR:
            is_hard_mode = False
            self.check_click(GameState.RETRY)
        elif self.state == GameState.GAME_MISS:
            is_hard_mode = False
            self.check_click(GameState.RETRY)
        elif self.state == GameState.RETRY:
            is_hard_mode = False
            self.check_click(GameState.SPLASH)

    def draw_power_meter(self):
        if power < 40:
            color = 12
        elif power > 60:
            color = 12
        else:
            color = 10

        pyxel.rect(6, 8, GAUGE_WIDTH, GAUGE_HEIGHT, 5)
        gauge_fill_height = int(GAUGE_HEIGHT * (power / 100))
        pyxel.rect(
            6,
            8 + (GAUGE_HEIGHT - gauge_fill_height),
            GAUGE_WIDTH,
            gauge_fill_height,
            color,
        )

    def check_transition(self, next_status, transition_seconds):
        if time.time() - self.start_time > transition_seconds:
            self.state = next_status
            self.start_time = time.time()

    def check_click(self, next_status):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.state_change_allowed:
            self.state = next_status
            self.set_state_change_time()

    def set_state_change_time(self):
        global last_state_change_time
        last_state_change_time = time.time()
        self.state_change_allowed = False

    def draw(self):
        pyxel.cls(0)
        self.image.draw(ImageName.BG_01, 0, 0)

        if self.state == GameState.SPLASH:
            self.show_splash()
        elif self.state == GameState.PROLOGUE:
            self.show_prologue()
        elif self.state == GameState.READY:
            self.show_ready()
        elif self.state == GameState.GAME_START:
            self.show_game_start()
        elif self.state == GameState.PLAY:
            self.start_game()
        elif self.state == GameState.GAME_CLEAR:
            self.show_game_clear()
        elif self.state == GameState.GAME_MISS:
            self.show_game_miss()
        elif self.state == GameState.RETRY:
            self.show_retry()

    def show_splash(self):
        self.image.draw(ImageName.Bear_01, 36, 35)
        self.image.draw(ImageName.Logo_01, 14, 81)
        if high_score is not None:
            pyxel.text(
                4, 4, f"High Score: {high_score:.2f} sec", pyxel.COLOR_WHITE
            )  # ハイスコアを左上に表示

    def show_prologue(self):
        self.timeline.play(TimelineName.Prologue)

    def show_ready(self):
        self.timeline.play(TimelineName.Ready)

    def show_game_start(self):
        pass

    def start_game(self):
        self.draw_tweezer()
        self.draw_penguin()
        self.draw_bear()

        if not hair_falling and hair_regrow_frame >= HAIR_REGROW_DELAY:
            pyxel.line(52, 111, 53, 117, 1)
        elif hair_falling:
            pyxel.line(52, 111 + hair_fall_frame * 2, 53, 117 + hair_fall_frame * 2, 1)

        self.draw_power_meter()

        pyxel.text(110 / 5, 50, message, 1)

        pyxel.text(64, 8, f"TIME:{time_left // 30}", 1)
        pyxel.text(64, 15, f"LEFT:{hair_left}", 1)

    def draw_tweezer(self):
        if tweezer_count >= 1:
            if (76 <= pyxel.mouse_x <= 92) and (32 <= pyxel.mouse_y <= 43):
                self.image.draw(ImageName.Tweezers_01, 76, 32, animation_speed=0.8)
            else:
                self.image.draw(ImageName.Tweezers_03, 76, 32)

        if tweezer_count >= 2:
            if (76 <= pyxel.mouse_x <= 92) and (46 <= pyxel.mouse_y <= 57):
                self.image.draw(ImageName.Tweezers_01, 76, 46, animation_speed=0.8)
            else:
                self.image.draw(ImageName.Tweezers_03, 76, 46)

        if tweezer_count >= 3:
            if (76 <= pyxel.mouse_x <= 92) and (60 <= pyxel.mouse_y <= 71):
                self.image.draw(ImageName.Tweezers_01, 76, 60, animation_speed=0.8)
            else:
                self.image.draw(ImageName.Tweezers_03, 76, 60)

    def draw_penguin(self):
        if time_left > 200:
            self.image.draw(ImageName.PenguinS_02, 41, 17)
        elif time_left > 100:
            self.image.draw(ImageName.PenguinM_02, 34, 26)
        else:
            self.image.draw(ImageName.PenguinL_02, 23, 40)

    def draw_bear(self):
        if time_left < 30:
            self.image.draw(ImageName.Prologue_BearFace_01, 3, 84)
        else:
            self.image.draw(ImageName.BearFace, 3, 84)

    def show_game_clear(self):
        self.image.draw(ImageName.Clear_01, 3, 42)

    def show_game_miss(self):
        self.image.draw(ImageName.Miss_01, 12, 52)

    def show_retry(self):
        self.image.draw(ImageName.Reset_01, 30, 49)


# ゲーム開始時に n を指定する
n = NORMAL_MODE_HAIR_COUNT
App(n)
