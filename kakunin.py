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

# 追加: 鼻毛の落下および再生を管理する変数
hair_falling = False
hair_fall_frame = 0
hair_regrow_frame = 0

def reset_game():
    global power, increasing, message, time_left, special_count, success_count, game_state, hair_falling, hair_fall_frame, hair_regrow_frame
    power = 0
    increasing = True
    message = ""
    time_left = TIME_INCREMENT
    special_count = 3
    success_count = 0
    game_state = STATE_PLAYING
    # 追加: 鼻毛の状態をリセット
    hair_falling = False
    hair_fall_frame = 0
    hair_regrow_frame = 0

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
    global message, success_count, time_left, hair_falling, hair_fall_frame
    if 40 <= power <= 60:
        message = "Success!"
        success_count += 1
        # 追加: 鼻毛の落下を開始
        hair_falling = True
        hair_fall_frame = 0
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
    global time_left, game_state, hair_falling, hair_fall_frame, hair_regrow_frame

    if game_state == STATE_PLAYING:
        if time_left > 0:
            time_left -= 1
            update_power()

            if pyxel.btnp(pyxel.KEY_SPACE):
                handle_space_key()

            if pyxel.btnp(pyxel.KEY_S):
                handle_special_key()
            
            # 追加: 鼻毛の状態を更新
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
        if pyxel.btnp(pyxel.KEY_RETURN):  # 修正: KEY_ENTER を KEY_RETURN に変更
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

def show_mozinai(x, y, text, size, color):
    writer = puf.Writer("ipa_gothic.ttf")
    writer.draw(x, y, text, size, color)

def draw():
    pyxel.cls(0)

    if game_state == STATE_PLAYING:
        # キャラクターの顔を描画（中央よりやや下）
        pyxel.rect(118, 140, 20, 20, 11)  # 顔

        # 変更: 鼻毛が落下中かどうかを確認
        if not hair_falling and hair_regrow_frame >= HAIR_REGROW_DELAY:
            pyxel.circ(128, 150, 3, 6)        # 鼻
            pyxel.line(128, 153, 128, 165, 7) # 鼻毛
        elif hair_falling:
            pyxel.line(128, 153 + hair_fall_frame * 2, 128, 165 + hair_fall_frame * 2, 7) # 落下中の鼻毛

        draw_power_meter()

        # 成功・失敗のメッセージを描画
        pyxel.text(110, 180, message, 7)

        # 制限時間を表示
        show_mozinai(350, 10, f"残り時間: {time_left // 30}", 14, 7)

        # スペシャル技の使用回数を表示
        writer = puf.Writer("ipa_gothic.ttf")
        writer.draw(350, 50, f"スペシャル残数: {special_count}", 14, 7)  # デバッグ用

        # 抜いた鼻毛の数を表示
        show_mozinai(350, 30, f"抜いた鼻毛: {success_count}", 14, 7)

    elif game_state == STATE_GAME_OVER:
        pyxel.text(100, 100, "Game Over", pyxel.frame_count % 16)
        pyxel.text(70, 120, "Press Enter to Continue", 7)

# Pyxelの初期化と実行
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
reset_game()
pyxel.run(update, draw)
