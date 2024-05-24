import pyxel
from enum import IntEnum, auto

DEFAULT_FPS = 30
FONT_SIZE = 8  # 8 ピクセルのフォントを使用


class TextName(IntEnum):
    Prologue_01_01 = auto()
    Prologue_01_02 = auto()
    Prologue_01_03 = auto()
    Prologue_01_04 = auto()

    Prologue_02_01 = auto()
    Prologue_02_02 = auto()

    Prologue_03_01 = auto()
    Prologue_03_02 = auto()
    Prologue_03_03 = auto()

    Prologue_04_01 = auto()
    Prologue_04_02 = auto()
    Prologue_04_03 = auto()

    Prologue_05_01 = auto()
    Prologue_05_02 = auto()

    Prologue_06_01 = auto()
    Prologue_06_02 = auto()
    Prologue_06_03 = auto()

    Prologue_07_01 = auto()
    Prologue_07_02 = auto()
    Prologue_07_03 = auto()


class TextInfo:
    def __init__(self, x, y, image_y, image_index=1, image_x=0, animation_speed=0.1):
        self.x = x  # 文字の表示位置
        self.y = y
        self.image_index = image_index
        self.image_x = image_x
        self.image_y = image_y
        self.animation_speed = animation_speed

        self.start_frame = 0


class TextManager:
    def __init__(self):
        self.load_images()

        self.texts = {}
        self.set_texts()

    def load_images(self):
        pyxel.images[1].load(0, 0, "assets/002.png")

    def reset(self):
        for key in self.texts:
            self.texts[key].start_frame = 0

    def draw_animation(self, text_name):
        text = self.texts[text_name]
        if text.start_frame == 0:
            self.texts[text_name].start_frame = pyxel.frame_count

        current_frame = pyxel.frame_count - text.start_frame
        current_index = int(current_frame / (DEFAULT_FPS * text.animation_speed))

        pyxel.blt(
            x=text.x,
            y=text.y,
            img=text.image_index,
            u=text.image_x,
            v=text.image_y,
            w=8 * current_index,
            h=8,
            colkey=7,
        )

    def set_texts(self):
        self.texts[TextName.Prologue_01_01] = TextInfo(20, 62, 8 * 0)  # ペンギンさんと
        self.texts[TextName.Prologue_01_02] = TextInfo(20, 74, 8 * 1)  # おでかけに行く
        self.texts[TextName.Prologue_01_03] = TextInfo(20, 86, 8 * 2)  # 約束をしていた
        self.texts[TextName.Prologue_01_04] = TextInfo(24, 98, 8 * 3)  # しろくまさん

        self.texts[TextName.Prologue_02_01] = TextInfo(
            10, 74, 8 * 4
        )  # あ！ペンギンさんだ！
        self.texts[TextName.Prologue_02_02] = TextInfo(34, 86, 8 * 5)  # おーい！

        self.texts[TextName.Prologue_03_01] = TextInfo(24, 62, 8 * 6)  # わー、今日は
        self.texts[TextName.Prologue_03_02] = TextInfo(24, 74, 8 * 7)  # 楽しみだなぁ
        self.texts[TextName.Prologue_03_03] = TextInfo(36, 98, 8 * 8)  # …ん？

        self.texts[TextName.Prologue_04_01] = TextInfo(
            16, 68, 8 * 9
        )  # ふっと、こおりに
        self.texts[TextName.Prologue_04_02] = TextInfo(
            9, 80, 8 * 10
        )  # うつった自分のすがた
        self.texts[TextName.Prologue_04_03] = TextInfo(21, 92, 8 * 11)  # よーく見ると…

        self.texts[TextName.Prologue_05_01] = TextInfo(33, 54, 8 * 12)  # はなから
        self.texts[TextName.Prologue_05_02] = TextInfo(
            10, 66, 8 * 13
        )  # ア、アレが出てる…！

        self.texts[TextName.Prologue_06_01] = TextInfo(20, 44, 8 * 14)  # ペンギンさんに
        self.texts[TextName.Prologue_06_02] = TextInfo(24, 56, 8 * 15)  # 見られる前に
        self.texts[TextName.Prologue_06_03] = TextInfo(21, 68, 8 * 16)  # アレを抜こう！

        self.texts[TextName.Prologue_07_01] = TextInfo(22, 43, 8 * 17)  # タイミングよく
        self.texts[TextName.Prologue_07_02] = TextInfo(22, 55, 8 * 18)  # クリックすると
        self.texts[TextName.Prologue_07_03] = TextInfo(29, 67, 8 * 19)  # 抜けるよ！
