import pyxel
import random

power = 0
increasing = True
message = ""
time_left = 3000  # 制限時間（フレーム単位、例：300フレーム = 5秒）

def update():
    global power, increasing, message, time_left

    # 制限時間がまだ残っている場合のみ更新
    if time_left > 0:
        time_left -= 1  # フレームごとに制限時間を減少

        # パワーゲージの増減をランダムにする
        if increasing:
            power += random.randint(1, 3)
            if power >= 100:
                increasing = False
        else:
            power -= random.randint(1, 3)
            if power <= 0:
                increasing = True

        # 鼻毛を抜くタイミングでボタンを押す
        if pyxel.btnp(pyxel.KEY_SPACE):
            if 40 <= power <= 60:
                message = "Success!"
            else:
                message = "Fail!"
    else:
        message = "Game Over"

def draw():
    pyxel.cls(0)

    # キャラクターの顔を描画
    pyxel.rect(70, 40, 20, 20, 11)  # 顔
    pyxel.circ(80, 50, 3, 6)        # 鼻
    pyxel.line(80, 53, 80, 65, 7)   # 鼻毛

    # パワーゲージを描画
    pyxel.rect(10, 100, power, 5, 8)

    # 成功・失敗のメッセージを描画
    pyxel.text(60, 90, message, 7)

    # 制限時間を表示
    pyxel.text(10, 10, f"Time left: {time_left // 30}", 7)

# Pyxelの初期化と実行
pyxel.init(160, 120)
pyxel.run(update, draw)
