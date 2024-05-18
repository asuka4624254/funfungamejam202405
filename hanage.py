import pyxel
import random

# 定数の定義
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
TIME_INCREMENT = 300  # 300フレーム = 10秒
TIME_DECREMENT_ON_FAIL = 30
GAUGE_HEIGHT = 200
GAUGE_WIDTH = 10

# ゲーム状態の定義
STATE_PLAYING = 0
STATE_GAME_OVER = 1

# グローバル変数
power = 0
increasing = True
message = ""
time_left = TIME_INCREMENT  # 制限時間（フレーム単位）
special_count = 3  # スペシャル技の使用回数
success_count = 0  # 成功回数
game_state = STATE_PLAYING  # ゲームの状態

def reset_game():
    global power, increasing, message, time_left, special_count, success_count, game_state
    power = 0
    increasing = True
    message = ""
    time_left = TIME_INCREMENT
    special_count = 3
    success_count = 0
    game_state = STATE_PLAYING

def update_power():
    global power, increasing
    if increasing:
        power += random.randint(1, 3)
        if power >= 100:
            increasing = False
    else:
        power -= random.randint(1, 3)
        if power <= 0:
            increasing = True

def handle_space_key():
    global message, success_count, time_left
    if 40 <= power <= 60:
        message = "Success!"
        success_count += 1
    else:
        message = "Fail!"
        time_left -= TIME_DECREMENT_ON_FAIL

def handle_special_key():
    global message, time_left, special_count
    if special_count > 0:
        time_left += TIME_INCREMENT
        special_count -= 1
        message = "Special used!"

def update():
    global time_left, game_state

    if game_state == STATE_PLAYING:
        if time_left > 0:
            time_left -= 1
            update_power()

            if pyxel.btnp(pyxel.KEY_SPACE):
                handle_space_key()

            if pyxel.btnp(pyxel.KEY_S):
                handle_special_key()
        else:
            game_state = STATE_GAME_OVER
            message = "Game Over"
    elif game_state == STATE_GAME_OVER:
        if pyxel.btnp(pyxel.KEY_ENTER):
            reset_game()

def draw_power_meter():
    # パワーゲージの色を設定
    if power < 40:
        color = 12  # 青
    elif power > 60:
        color = 8  # 赤
    else:
        color = 10  # 黄色

    # 縦長のパワーゲージを描画
    pyxel.rect(10, 10, GAUGE_WIDTH, GAUGE_HEIGHT, 5)  # ゲージの背景
    gauge_fill_height = int(GAUGE_HEIGHT * (power / 100))
    pyxel.rect(10, 10 + (GAUGE_HEIGHT - gauge_fill_height), GAUGE_WIDTH, gauge_fill_height, color)

def draw():
    pyxel.cls(0)

    if game_state == STATE_PLAYING:
        # キャラクターの顔を描画（中央よりやや下）
        pyxel.rect(118, 140, 20, 20, 11)  # 顔
        pyxel.circ(128, 150, 3, 6)        # 鼻
        pyxel.line(128, 153, 128, 165, 7) # 鼻毛

        draw_power_meter()

        # 成功・失敗のメッセージを描画
        pyxel.text(110, 180, message, 7)

        # 制限時間を表示
        pyxel.text(200, 10, f"Time left: {time_left // 30}", 7)

        # スペシャル技の使用回数を表示
        pyxel.text(200, 20, f"Specials left: {special_count}", 7)

        # 成功回数を表示
        pyxel.text(200, 30, f"Successes: {success_count}", 7)
    elif game_state == STATE_GAME_OVER:
        pyxel.text(100, 100, "Game Over", pyxel.frame_count % 16)
        pyxel.text(70, 120, "Press Enter to Continue", 7)

# Pyxelの初期化と実行
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
reset_game()
pyxel.run(update, draw)
