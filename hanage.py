import pyxel
import random
import PyxelUniversalFont as puf

# 定数の定義
SCREEN_WIDTH = 96 #解像度 実際はこれを５倍する
SCREEN_HEIGHT = 128 #解像度 実際はこれを５倍する
TIME_INCREMENT = 3000  #残り時間を定義する。(10秒=300フレーム)
TIME_DECREMENT_ON_FAIL = 30 #間違ったときのペナルティー時間
GAUGE_HEIGHT = 66 #パワーメータの高さ方向のピクセル数
GAUGE_WIDTH = 4 #パワーメータの横方向のピクセル数
HAIR_FALL_DURATION = 15  # 鼻毛が落下するフレーム数
HAIR_REGROW_DELAY = 30  # 鼻毛が再生するまでのフレーム数
TWEEZER_SLOWDOWN = 0.5  # 毛抜アイテム使用時のゲージ上昇減少倍率

# ゲーム状態の定義
STATE_PLAYING = 0
STATE_GAME_OVER = 1

# グローバル変数
power = 0 #パワーゲージの初期位置
increasing = True #パワーゲージが増加しているか減少しているかを示すフラグ。初期状態では増加。
message = "" #ゲーム中にプレイヤーに表示されるメッセージを保持するための変数
time_left = TIME_INCREMENT  # 制限時間（フレーム単位）
special_count = 3  # スペシャル技の使用回数
success_count = 0  # 成功回数
game_state = STATE_PLAYING  # ゲームの状態
tweezer_count = 3  # 毛抜アイテムの使用回数
tweezer_active = False  # 毛抜アイテムの使用状態
hair_falling = False #鼻毛が落下しているかどうかを示すフラグを False に設定します。
hair_fall_frame = 0 #鼻毛の落下フレーム数を0に設定します。
hair_regrow_frame = 0 #鼻毛の再生フレーム数を0に設定します

def reset_game(): #機械の定義　機械は関数 ゲームの状態を初期化するための関数です。ゲームをリセットし、新しいゲームを開始できるように、すべてのグローバル変数を初期状態に戻します
# globalはグローバル変数を使う宣言
    global power, increasing, message, time_left, special_count, success_count, game_state, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_count, tweezer_active
    power = 0 #パワーゲージの初期位置を0に設定します。
    increasing = True #パワーゲージが増加する状態に設定します（True）。
    message = "" #メッセージを空文字列に設定します。
    time_left = TIME_INCREMENT #制限時間を初期値（TIME_INCREMENT）に設定します。
    special_count = 3 #スペシャル技の使用回数をnに設定します。
    success_count = 0 #成功回数をnに設定します。
    game_state = STATE_PLAYING #ゲームの状態をプレイ中（STATE_PLAYING）に設定します。
    tweezer_count = 3 #毛抜アイテムの使用回数を3に設定します。
    tweezer_active = False #毛抜アイテムの使用状態を未使用（False）に設定します。
    hair_falling = False #鼻毛が落下しているかどうかを示すフラグを False に設定します。
    hair_fall_frame = 0 #鼻毛の落下フレーム数を0に設定します。
    hair_regrow_frame = 0 #鼻毛の再生フレーム数を0に設定します

def update_power(): #ゲーム内のパワーゲージを更新するための関数。ゲージの増減、毛抜の増減を遅くする
    global power, increasing, tweezer_active #グローバル変数の呼び出し
    increment = random.randint(1, 3) #1から3 のランダムな値で初期化されます。
    if tweezer_active: #tweezer_active が True の場合、
        increment = int(increment * TWEEZER_SLOWDOWN) #increment は TWEEZER_SLOWDOWN の値（例えば0.5など）で減少されます。

    if increasing: #increasing フラグに応じて、increment の値を power に加算または減算します。
        power += increment #パワーを足していく
        if power >= 100:  #100以下かどうか確認
            increasing = False # パワーゲージが100に達したら、増加を停止して減少に切り替える
    else:
        power -= increment #パワーを減らしていく
        if power <= 0: #パワーが0よりも大きいか確認する
            increasing = True # パワーゲージが0に達したら、減少を停止して増加に切り替える

def handle_space_key(): #スペースキーを押したときの挙動を定義
    global message, success_count, time_left, hair_falling, hair_fall_frame, tweezer_active #グローバル変数の呼び出し
    if 40 <= power <= 60: #パワーの値を確認 40以上、60以下であれば、次の処理をする
        message = "やった！抜けた！" # 成功時のメッセージ
        success_count += 1 # 成功回数をn増やす
        hair_falling = True # 鼻毛が落下中であることを示すフラグを設定
        hair_fall_frame = 0 # 鼻毛の落下フレームをリセット
        tweezer_active = False  # パワーゲージの上昇を元に戻す
    else: #抜くのに失敗したときの処理 イテテと表示して秒数を減らす
        message = "イテテ・・・" # 失敗時のメッセージ
        time_left -= TIME_DECREMENT_ON_FAIL #ここで決められた秒数を減らす

def handle_special_key(): #スペシャルを押したときの挙動関数
    global message, time_left, special_count #グローバル変数の呼び出し
    if special_count > 0: #スペシャルの残数が0よりも多いか確認
        time_left += TIME_INCREMENT #時間を追加する
        special_count -= 1 #スペシャルの残数を1減らす
        message = "Special used!" #スペシャル使用時のメッセージを表示

def handle_tweezer_key(): #毛抜を使用時の関数を定義
    global message, tweezer_count, tweezer_active #グローバル変数の呼び出し メッセージ、毛抜カウント数、毛抜アイテムの使用状態
    if tweezer_count > 0 and not tweezer_active: #毛抜の残数が0よりも大きくなおかつ、毛抜を使っていない状態であること
        tweezer_active = True # 毛抜アイテムを使用するモードに切り替え
        tweezer_count -= 1 # 毛抜アイテムの残数を1減らす
        message = "毛抜使うよ！" # メッセージを設定して表示

def update(): #ゲームの進行状況を管理
#↓グローバル変数の呼び出し(残り時間、ゲーム状態、鼻毛落ちる、鼻毛落ちるフレーム、鼻毛生えるフレーム、毛抜の状態)
    global time_left, game_state, hair_falling, hair_fall_frame, hair_regrow_frame, tweezer_active

    if game_state == STATE_PLAYING: #ゲームがスタートしている状態かチェック
        if time_left > 0: #時間0秒以上か確認
            time_left -= 1 #そうであれば、タイムを1秒減らす
            update_power() #パワーゲージの関数を呼び出し

            if pyxel.btnp(pyxel.KEY_SPACE): #pyxelのライブラリ関数 スペースキーが押された瞬間の検出
                handle_space_key() #スペースキーを押されたときの関数を動かす(鼻毛を抜く)

            if pyxel.btnp(pyxel.KEY_S): #pyxelのライブラリ関数 Sキーが押された瞬間の検出
                handle_special_key() #スペシャルが押されたときの関数を動かす(スペシャル)

            if pyxel.btnp(pyxel.KEY_T): #pyxelのライブラリ関数 Tキーが押された瞬間の検出
                handle_tweezer_key() #毛抜ボタンが押されたときの関数を動かす(スペシャル)

            if hair_falling: #鼻毛が落ちている状態であれば
                hair_fall_frame += 1 #鼻毛の落ちるフレームを1足す
                if hair_fall_frame >= HAIR_FALL_DURATION: # 鼻毛の落下が終了したか確認
                    hair_falling = False # 鼻毛の落下を終了
                    hair_regrow_frame = 0 # 鼻毛の再生フレームをリセット
            else:
                if hair_regrow_frame < HAIR_REGROW_DELAY: # 鼻毛が再生中の場合
                    hair_regrow_frame += 1 # 鼻毛の再生フレーム数を1増やす

        else:
            game_state = STATE_GAME_OVER #ゲームの状態がGAME OVERになったときの分岐
            message = "Game Over" #ゲームオーバと表示させる
    elif game_state == STATE_GAME_OVER: #ゲームの状態がゲームオーバーであれば
        if pyxel.btnp(pyxel.KEY_RETURN): #pyxelのライブラリ関数でエンターをおしたなら
            reset_game() #リスタートゲームの関数を呼び出し

def draw_power_meter(): #パワーメータの関数を定義
    if power < 40: #パワーが40よりも大きい
        color = 12  # 青
    elif power > 60: #パワーが60よりも大きい
        color = 8  # 赤
    else: #それ以外なら
        color = 10  # 黄色

    pyxel.rect(6, 8, GAUGE_WIDTH, GAUGE_HEIGHT, 5) # 幅 GAUGE_WIDTH、高さ GAUGE_HEIGHT、色 5 の長方形を (10, 10) から四角形を描画します。
    gauge_fill_height = int(GAUGE_HEIGHT * (power / 100)) #power は0から100の範囲の値で、現在のパワーレベルを示します
    pyxel.rect(6, 8 + (GAUGE_HEIGHT - gauge_fill_height), GAUGE_WIDTH, gauge_fill_height, color) #Pyxelライブラリを使って画面上に矩形を描画するためのコードです。この特定のコードは、パワーゲージの充填部分を描画するために使用されています。
#10 + (GAUGE_HEIGHT - gauge_fill_height): 矩形の左上隅のY座標です。ここでは、矩形の左上隅が画面の縦方向に 10 + (GAUGE_HEIGHT - gauge_fill_height) ピクセルの位置に描画されます。この式は、パワーゲージが下から上に向かって充填されるようにするためのものです。
#10 はパワーゲージの枠のY座標です
#GAUGE_HEIGHT はパワーゲージの全体の高さです。
#gauge_fill_height は現在のパワーレベルに基づいて計算された充填部分の高さです。
#10 + (GAUGE_HEIGHT - gauge_fill_height) は、充填部分が枠の底から充填されるように位置を調整するための計算です。
#GAUGE_WIDTH: 矩形の幅です。パワーゲージの枠の幅と同じです。
#gauge_fill_height: 矩形の高さです。現在のパワーレベルに応じた高さを表します。
#color: 矩形の色です。この色はパワーレベルに応じて設定されます。

def show_mozinai(x, y, text, size, color): #日本語フォントの関数定義
    writer = puf.Writer("ipa_gothic.ttf") #pufのライブラリでフォントの指定(日本語のゴシック)
    writer.draw(x, y, text, size, color) #各場所とかサイズ、色を指定する

def draw():
    pyxel.cls(0) #画面全体をクリアして、色0（通常は黒）で塗りつぶします。

    if game_state == STATE_PLAYING: #ゲームがプレイ中のとき (STATE_PLAYING)
        pyxel.rect(43, 104, 12, 8, 11)# 位置(118(横方向), 140(高さ方向))に幅20、高さ20、色11の矩形を描画します。
#鼻毛の状態に応じた描画
        if not hair_falling and hair_regrow_frame >= HAIR_REGROW_DELAY: #hair_falling が False で hair_regrow_frame が HAIR_REGROW_DELAY 以上の場合、円（鼻毛の再生）を描画し、その下に線を引きます。
            #pyxel.circ(43 + 12, 104 + 8, 3, 6) # 鼻の穴の描写
            pyxel.line(53 , 111, 53, 117, 7) # 鼻毛を描画(横軸、縦軸から、横軸、縦軸までラインを引く)
        elif hair_falling:
            pyxel.line(53, 111 + hair_fall_frame * 2, 53, 117 + hair_fall_frame * 2, 7)

        draw_power_meter()  #パワーメーターの描画

        # 成功・失敗のメッセージを描画
        writer = puf.Writer("ipa_gothic.ttf")
        writer.draw(110 / 5, 180 / 5, message, 14, 7)

        show_mozinai(350 / 5, 10 / 5, f"残り時間: {time_left // 30}", 14, 7)

        writer.draw(350 / 5, 50 / 5, f"スペシャル残数: {special_count}", 14, 7)
        
        show_mozinai(350 / 5, 30 / 5, f"抜いた鼻毛: {success_count}", 14, 7)

        # 毛抜アイテムの使用回数を表示
        writer.draw(350, 70, f"毛抜残数: {tweezer_count}", 14, 7)

    elif game_state == STATE_GAME_OVER:
        pyxel.text(100, 100, "Game Over", pyxel.frame_count % 16)
        pyxel.text(70, 120, "Press Enter to Continue", 7)

# Pyxelの初期化と実行
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, display_scale=5)
reset_game()
pyxel.run(update, draw)
