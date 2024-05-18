import pyxel
import random

# 定数の定義
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
TIME_INCREMENT = 300  # 300フレーム = 10秒
TIME_DECREMENT_ON_FAIL = 30

# グローバル変数
power = 0
increasing = True
message = ""
time_left = TIME_INCREMENT  # 制限時間（フレーム単位）
special_count = 3  # スペシャル技の使用回数
success_count = 0  # 成功回数

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
    global time_left

    if time_left > 0:
        time_left -= 1
        update_power()

        if pyxel.btnp(pyxel.KEY_SPACE):
            handle_space_key()

        if pyxel.btnp(pyxel.KEY_S):
            handle_special_key()
    else:
        message = "Game Over"

def draw_power_meter():
    if power < 40:
        color = 12  # 青
    elif power > 60:
        color = 8  # 赤
    else:
        color = 10  # 黄色
    pyxel.rect(10, 100, power, 5, color)

def draw():
    pyxel.cls(0)

    # キャラクターの顔を描画
    pyxel.rect(70, 40, 20, 20, 11)  # 顔
    pyxel.circ(80, 50, 3, 6)        # 鼻
    pyxel.line(80, 53, 80, 65, 7)   # 鼻毛

    draw_power_meter()

    # 成功・失敗のメッセージを描画
    pyxel.text(60, 90, message, 7)

    # 制限時間を表示
    pyxel.text(10, 10, f"Time left: {time_left // 30}", 7)

    # スペシャル技の使用回数を表示
    pyxel.text(10, 20, f"Specials left: {special_count}", 7)

    # 成功回数を表示
    pyxel.text(10, 30, f"Successes: {success_count}", 7)

# Pyxelの初期化と実行
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
pyxel.run(update, draw)
