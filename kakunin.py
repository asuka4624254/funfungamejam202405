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
HAIR_FALL_DURATION = 15  # 鼻毛が落下するフレーム数
HAIR_REGROW_DELAY = 30  # 鼻毛が再生するまでのフレーム数
TWEEZER_SLOWDOWN = 0.5  # 毛抜アイテム使用時のゲージ上昇減少倍率

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
tweezer_count = 3  # 毛抜アイテムの使用回数
tweezer_active = False  # 毛抜アイテムの使用状態

# 鼻毛の落下および再生を管理する変数
hair_falling = False
hair_fall_frame = 0
hair_regrow_frame = 0

def reset_game():
    global power, increasing, message, time_left, special_count, success_count, game_state, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_count, tweezer_active
    power = 0
    increasing = True
    message = ""
    time_left = TIME_INCREMENT
    special_count = 3
    success_count = 0
    game_state = STATE_PLAYING
    tweezer_count = 3
    tweezer_active = False
    hair_falling = False
    hair_fall_frame = 0
    hair_regrow_frame = 0

def update_power():
    global power, increasing, tweezer_active
    increment = random.randint(1, 3)
    if tweezer_active:
        increment = int(increment * TWEEZER_SLOWDOWN)

    if increasing:
        power += increment
        if power >= 100:
            increasing = False
    else:
        power -= increment
        if power <= 0:
            increasing = True

def handle_space_key():
    global message, success_count, time_left, hair_falling, hair_fall_frame, tweezer_active
    if 40 <= power <= 60:
        message = "やった！抜けた！"
        success_count += 1
        hair_falling = True
        hair_fall_frame = 0
        tweezer_active = False  # パワーゲージの上昇を元に戻す
    else:
        message = "イテテ・・・"
        time_left -= TIME_DECREMENT_ON_FAIL

def handle_special_key():
    global message, time_left, special_count
    if special_count > 0:
        time_left += TIME_INCREMENT
        special_count -= 1
        message = "Special used!"

def handle_tweezer_key():
    global message, tweezer_count, tweezer_active
    if tweezer_count > 0 and not tweezer_active:
        tweezer_active = True
        tweezer_count -= 1
        message = "毛抜使うよ！"

def update():
    global time_left, game_state, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_active

    if game_state == STATE_PLAYING:
        if time_left > 0:
            time_left -= 1
            update_power()

            if pyxel.btnp(pyxel.KEY_SPACE):
                handle_space_key()

            if pyxel.btnp(pyxel.KEY_S):
                handle_special_key()

            if pyxel.btnp(pyxel.KEY_T):
                handle_tweezer_key()

            if hair_falling:
                hair_fall_frame += 1
                if hair_fall_frame >= HAIR_FALL_DURATION:
                    hair_falling = False
                    hair_regrow_frame = 0
            else:
                if hair_regrow_frame < HAIR_REGROW_DELAY:
                    hair_regrow_frame += 1

        else:
            game_state = STATE_GAME_OVER
            message = "Game Over"
    elif game_state == STATE_GAME_OVER:
        if pyxel.btnp(pyxel.KEY_RETURN):
            reset_game()

def draw_power_meter():
    if power < 40:
        color = 12  # 青
    elif power > 60:
        color = 8  # 赤
    else:
        color = 10  # 黄色

    pyxel.rect(10, 10, GAUGE_WIDTH, GAUGE_HEIGHT, 5)
    gauge_fill_height = int(GAUGE_HEIGHT * (power / 100))
    pyxel.rect(10, 10 + (GAUGE_HEIGHT - gauge_fill_height), GAUGE_WIDTH, gauge_fill_height, color)

def show_mozinai(x, y, text, size, color):
    writer = puf.Writer("ipa_gothic.ttf")
    writer.draw(x, y, text, size, color)

def draw():
    pyxel.cls(0)

    if game_state == STATE_PLAYING:
        pyxel.rect(118, 140, 20, 20, 11)

        if not hair_falling and hair_regrow_frame >= HAIR_REGROW_DELAY:
            pyxel.circ(128, 150, 3, 6)
            pyxel.line(128, 153, 128, 165, 7)
        elif hair_falling:
            pyxel.line(128, 153 + hair_fall_frame * 2, 128, 165 + hair_fall_frame * 2, 7)

        draw_power_meter()

        # 成功・失敗のメッセージを描画
        writer = puf.Writer("ipa_gothic.ttf")
        writer.draw(110, 180, message, 14, 7)

        show_mozinai(350, 10, f"残り時間: {time_left // 30}", 14, 7)

        writer.draw(350, 50, f"スペシャル残数: {special_count}", 14, 7)
        
        show_mozinai(350, 30, f"抜いた鼻毛: {success_count}", 14, 7)

        # 毛抜アイテムの使用回数を表示
        writer.draw(350, 70, f"毛抜残数: {tweezer_count}", 14, 7)

    elif game_state == STATE_GAME_OVER:
        pyxel.text(100, 100, "Game Over", pyxel.frame_count % 16)
        pyxel.text(70, 120, "Press Enter to Continue", 7)

# Pyxelの初期化と実行
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
reset_game()
pyxel.run(update, draw)
