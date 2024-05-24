import pyxel
import time
import random

from enum import Enum
from image import ImageManager, ImageName
from timeline import TimelineManager, TimelineName

# 定数の定義
DEFAULT_FPS = 30
SCREEN_WIDTH = 96  # 480
SCREEN_HEIGHT = 128  # 640
DISPLAY_SCALE = 5

TIME_INCREMENT = 300  # 残り時間を定義する。(10秒=300フレーム)
TIME_DECREMENT_ON_FAIL = 30  # 間違ったときのペナルティー時間
GAUGE_HEIGHT = 66  # パワーメータの高さ方向のピクセル数
GAUGE_WIDTH = 4  # パワーメータの横方向のピクセル数
HAIR_FALL_DURATION = 15  # 鼻毛が落下するフレーム数
HAIR_REGROW_DELAY = 30  # 鼻毛が再生するまでのフレーム数
TWEEZER_SLOWDOWN = 0.5  # 毛抜アイテム使用時のゲージ上昇減少倍率


# ゲーム状態の定義
class GameState(Enum):
    SPLASH = 1
    PROLOGUE = 2
    GAME_START = 3
    PLAY = 4  # STATE_PLAYING から変更する
    GAME_END = 5  # STATE_GAME_OVERから変更する
    RESULT = 6
    RETRY = 7


# グローバル変数
power = 0  # パワーゲージの初期位置
increasing = (
    True  # パワーゲージが増加しているか減少しているかを示すフラグ。初期状態では増加。
)
message = ""  # ゲーム中にプレイヤーに表示されるメッセージを保持するための変数
time_left = TIME_INCREMENT  # 制限時間（フレーム単位）
special_count = 3  # スペシャル技の使用回数
success_count = 0  # 成功回数
tweezer_count = 3  # 毛抜アイテムの使用回数
tweezer_active = False  # 毛抜アイテムの使用状態
hair_falling = False  # 鼻毛が落下しているかどうかを示すフラグを False に設定します。
hair_fall_frame = 0  # 鼻毛の落下フレーム数を0に設定します。
hair_regrow_frame = 0  # 鼻毛の再生フレーム数を0に設定します


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

    def reset_game(
        self,
    ):  # 機械の定義　機械は関数 ゲームの状態を初期化するための関数です。ゲームをリセットし、新しいゲームを開始できるように、すべてのグローバル変数を初期状態に戻します
        # globalはグローバル変数を使う宣言
        global power, increasing, message, time_left, special_count, success_count, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_count, tweezer_active
        power = 0  # パワーゲージの初期位置を0に設定します。
        increasing = True  # パワーゲージが増加する状態に設定します（True）。
        message = ""  # メッセージを空文字列に設定します。
        time_left = TIME_INCREMENT  # 制限時間を初期値（TIME_INCREMENT）に設定します。
        special_count = 3  # スペシャル技の使用回数をnに設定します。
        success_count = 0  # 成功回数をnに設定します。
        self.state = GameState.PLAY  # ゲームの状態をプレイ中に設定します。
        tweezer_count = 3  # 毛抜アイテムの使用回数を3に設定します。
        tweezer_active = False  # 毛抜アイテムの使用状態を未使用に設定します。
        hair_falling = (
            False  # 鼻毛が落下しているかどうかを示すフラグを False に設定します。
        )
        hair_fall_frame = 0  # 鼻毛の落下フレーム数を0に設定します。
        hair_regrow_frame = 0  # 鼻毛の再生フレーム数を0に設定します

    def update_power(
        self,
    ):  # ゲーム内のパワーゲージを更新するための関数。ゲージの増減、毛抜の増減を遅くする
        global power, increasing, tweezer_active  # グローバル変数の呼び出し
        increment = random.randint(1, 3)  # 1から3 のランダムな値で初期化されます。
        if tweezer_active:  # tweezer_active が True の場合、
            increment = int(
                increment * TWEEZER_SLOWDOWN
            )  # increment は TWEEZER_SLOWDOWN の値（例えば0.5など）で減少されます。

        if (
            increasing
        ):  # increasing フラグに応じて、increment の値を power に加算または減算します。
            power += increment  # パワーを足していく
            if power >= 100:  # 100を超えたら
                power = 100  # パワーを100に固定
                increasing = (
                    False  # パワーゲージが100に達したら、増加を停止して減少に切り替える
                )
        else:
            power -= increment  # パワーを減らしていく
            if power <= 0:  # パワーが0以下になったら
                power = 0  # パワーを0に固定
                increasing = (
                    True  # パワーゲージが0に達したら、減少を停止して増加に切り替える
                )

    def handle_space_key(self):  # スペースキーを押したときの挙動を定義
        global message, success_count, time_left, hair_falling, hair_fall_frame, tweezer_active  # グローバル変数の呼び出し
        if 40 <= power <= 60:  # パワーの値を確認 40以上、60以下であれば、次の処理をする
            message = "やった！抜けた！"  # 成功時のメッセージ
            success_count += 1  # 成功回数をn増やす
            hair_falling = True  # 鼻毛が落下中であることを示すフラグを設定
            hair_fall_frame = 0  # 鼻毛の落下フレームをリセット
            tweezer_active = False  # パワーゲージの上昇を元に戻す
        else:  # 抜くのに失敗したときの処理 イテテと表示して秒数を減らす
            message = "イテテ・・・"  # 失敗時のメッセージ
            time_left -= TIME_DECREMENT_ON_FAIL  # ここで決められた秒数を減らす

    def handle_special_key(self):  # スペシャルを押したときの挙動関数
        global message, time_left, special_count  # グローバル変数の呼び出し
        if special_count > 0:  # スペシャルの残数が0よりも多いか確認
            time_left += TIME_INCREMENT  # 時間を追加する
            special_count -= 1  # スペシャルの残数を1減らす
            message = "Special used!"  # スペシャル使用時のメッセージを表示

    def handle_tweezer_key(self):  # 毛抜を使用時の関数を定義
        global message, tweezer_count, tweezer_active  # グローバル変数の呼び出し メッセージ、毛抜カウント数、毛抜アイテムの使用状態
        if (
            tweezer_count > 0 and not tweezer_active
        ):  # 毛抜の残数が0よりも大きくなおかつ、毛抜を使っていない状態であること
            tweezer_active = True  # 毛抜アイテムを使用するモードに切り替え
            tweezer_count -= 1  # 毛抜アイテムの残数を1減らす
            message = "毛抜使うよ！"  # メッセージを設定して表示

    def update(self):
        global time_left, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_active
        if self.state == GameState.SPLASH:
            self.timeline.reset()
            self.check_click(GameState.PROLOGUE)
        elif self.state == GameState.PROLOGUE:
            self.check_click(GameState.GAME_START)
        elif self.state == GameState.GAME_START:
            self.reset_game()  # TODO: 毎フレームリセットしてしまう
            self.check_click(GameState.PLAY)
        elif self.state == GameState.PLAY:
            if time_left > 0:  # 時間0秒以上か確認
                time_left -= 1  # そうであれば、タイムを1フレーム減らす
                self.update_power()  # パワーゲージの関数を呼び出し

            if pyxel.btnp(
                pyxel.KEY_SPACE
            ):  # pyxelのライブラリ関数 スペースキーが押された瞬間の検出
                self.handle_space_key()  # スペースキーを押されたときの関数を動かす(鼻毛を抜く)

            if pyxel.btnp(
                pyxel.KEY_S
            ):  # pyxelのライブラリ関数 Sキーが押された瞬間の検出
                self.handle_special_key()  # スペシャルが押されたときの関数を動かす(スペシャル)

            if pyxel.btnp(
                pyxel.KEY_T
            ):  # pyxelのライブラリ関数 Tキーが押された瞬間の検出
                self.handle_tweezer_key()  # 毛抜ボタンが押されたときの関数を動かす(スペシャル)

            if hair_falling:  # 鼻毛が落ちている状態であれば
                hair_fall_frame += 1  # 鼻毛の落ちるフレームを1足す
                if hair_fall_frame >= HAIR_FALL_DURATION:  # 鼻毛の落下が終了したか確認
                    hair_falling = False  # 鼻毛の落下を終了
                    hair_regrow_frame = 0  # 鼻毛の再生フレームをリセット
            else:
                if hair_regrow_frame < HAIR_REGROW_DELAY:  # 鼻毛が再生中の場合
                    hair_regrow_frame += 1  # 鼻毛の再生フレーム数を1増やす

            if time_left <= 0:  # 時間が0秒以下か確認
                self.state = GameState.GAME_END  # ゲームの状態をGAME_ENDに設定
        elif self.state == GameState.GAME_END:
            self.check_click(GameState.RESULT)
            if pyxel.btnp(
                pyxel.KEY_RETURN
            ):  # pyxelのライブラリ関数でエンターをおしたなら
                self.reset_game()  # リスタートゲームの関数を呼び出し
        elif self.state == GameState.RESULT:
            self.check_click(GameState.RETRY)
        elif self.state == GameState.RETRY:
            self.check_click(GameState.SPLASH)

    def draw_power_meter(self):  # パワーメータの関数を定義
        if power < 40:  # パワーが40よりも大きい
            color = 12  # 青
        elif power > 60:  # パワーが60よりも大きい
            color = 8  # 赤
        else:  # それ以外なら
            color = 10  # 黄色

        pyxel.rect(
            6, 8, GAUGE_WIDTH, GAUGE_HEIGHT, 5
        )  # 幅 GAUGE_WIDTH、高さ GAUGE_HEIGHT、色 5 の長方形を (10, 10) から四角形を描画します。
        gauge_fill_height = int(
            GAUGE_HEIGHT * (power / 100)
        )  # power は0から100の範囲の値で、現在のパワーレベルを示します
        pyxel.rect(
            6,
            8 + (GAUGE_HEIGHT - gauge_fill_height),
            GAUGE_WIDTH,
            gauge_fill_height,
            color,
        )  # Pyxelライブラリを使って画面上に矩形を描画するためのコードです。この特定のコードは、パワーゲージの充填部分を描画するために使用されています。

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

        # 鼻毛の状態に応じた描画
        if not hair_falling and hair_regrow_frame >= HAIR_REGROW_DELAY:
            pyxel.line(52, 111, 53, 117, 1)  # 鼻毛を描画
        elif hair_falling:
            pyxel.line(52, 111 + hair_fall_frame * 2, 53, 117 + hair_fall_frame * 2, 1)

        self.draw_power_meter()  # パワーメーターの描画

        # 成功・失敗のメッセージを描画
        pyxel.text(110 / 5, 180 / 5, message, 1)

        pyxel.text(350 / 5, 10 / 5, f"LEFT TIME: {time_left // 30}", 1)
        pyxel.text(350 / 5, 50 / 5, f"SPECIAL LEFT: {special_count}", 1)
        pyxel.text(350 / 5, 30 / 5, f"SUCCESS COUNT: {success_count}", 1)
        pyxel.text(350, 70, f"HAIR COUNT: {tweezer_count}", 1)

    def show_game_end(self):
        pyxel.text(0, 0, "GAME END", 1)

    def show_result(self):
        pyxel.text(0, 0, "RESULT", 10)
        self.image.draw(ImageName.PenguinM_02, 34, 26)
        self.image.draw(ImageName.PenguinL_02, 23, 40)

    def show_retry(self):
        pyxel.text(0, 0, "RETRY ", 10)


App()
