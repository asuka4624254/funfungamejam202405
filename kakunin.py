import pyxel
import random
import PyxelUniversalFont as puf

# 定数の定義
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
TIME_INCREMENT = 3000  # 300フレーム = 10秒
TIME_DECREMENT_ON_FAIL = 30
GAUGE_HEIGHT = 200
GAUGE_WIDTH = 10

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

def show_mozinai(x, y, text, size, color):
    writer = puf.Writer("ipa_gothic.ttf")
    writer.draw(x, y, text, size, color)

def draw():
    pyxel.cls(0)

    # キャラクターの顔を描画（中央よりやや下）
    pyxel.rect(118, 140, 20, 20, 11)  # 顔
    pyxel.circ(128, 150, 3, 6)        # 鼻
    pyxel.line(128, 153, 128, 165, 7) # 鼻毛

    draw_power_meter()

    # 成功・失敗のメッセージを描画
    pyxel.text(110, 180, message, 7)

    # 制限時間を表示
    show_mozinai(350, 10, f"残り時間: {time_left // 30}", 14, 7)

    # スペシャル技の使用回数を表示
    writer = puf.Writer("ipa_gothic.ttf")
    writer.draw(350, 50, f"スペシャル残数: {special_count}", 14, 7)

    # 抜いた鼻毛の数を表示
    show_mozinai(350, 30, f"抜いた鼻毛: {success_count}", 14, 7)

# Pyxelの初期化と実行
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
pyxel.run(update, draw)
