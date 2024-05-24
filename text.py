import pyxel
from enum import IntEnum, auto

DEFAULT_FPS = 30


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
    def __init__(self, x, y, text, font_size=8, font_color=1, animation_speed=0.1):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.animation_speed = animation_speed

        self.start_frame = 0


class TextManager:
    def __init__(self):
        self.texts = {}
        self.set_texts()

    def draw_animation(self, text_name):
        text = self.texts[text_name]
        if text.start_frame == 0:
            self.texts[text_name].start_frame = pyxel.frame_count

        current_frame = pyxel.frame_count - text.start_frame
        current_index = int(current_frame / (DEFAULT_FPS * text.animation_speed))

        self.writer.draw(
            text.x, text.y, text.text[:current_index], text.font_size, text.font_color
        )

    def set_texts(self):
        self.texts[TextName.Prologue_01_01] = TextInfo(20, 62, "ペンギンさんと")
        self.texts[TextName.Prologue_01_02] = TextInfo(20, 74, "おでかけに行く")
        self.texts[TextName.Prologue_01_03] = TextInfo(20, 86, "約束をしていた")
        self.texts[TextName.Prologue_01_04] = TextInfo(20, 98, "しろくまさん")

        self.texts[TextName.Prologue_02_01] = TextInfo(10, 74, "あ！ペンギンさんだ！")
        self.texts[TextName.Prologue_02_02] = TextInfo(34, 86, "おーい！")

        self.texts[TextName.Prologue_03_01] = TextInfo(24, 62, "わー、今日は")
        self.texts[TextName.Prologue_03_02] = TextInfo(24, 74, "楽しみだなぁ")
        self.texts[TextName.Prologue_03_03] = TextInfo(36, 98, "…ん？")

        self.texts[TextName.Prologue_04_01] = TextInfo(16, 68, "ふっと、こおりに")
        self.texts[TextName.Prologue_04_02] = TextInfo(9, 80, "うつった自分のすがた")
        self.texts[TextName.Prologue_04_03] = TextInfo(21, 92, "よーく見ると…")

        self.texts[TextName.Prologue_05_01] = TextInfo(33, 54, "はなから")
        self.texts[TextName.Prologue_05_02] = TextInfo(10, 66, "ア、アレが出てる…！")

        self.texts[TextName.Prologue_06_01] = TextInfo(
            20, 44, "ペンギンさんに", font_color=9
        )
        self.texts[TextName.Prologue_06_02] = TextInfo(
            24, 56, "見られる前に", font_color=9
        )
        self.texts[TextName.Prologue_06_03] = TextInfo(
            21, 68, "アレを抜こう！", font_color=9
        )

        self.texts[TextName.Prologue_07_01] = TextInfo(
            22, 43, "タイミングよく", font_color=9
        )
        self.texts[TextName.Prologue_07_02] = TextInfo(
            9, 55, "スペースキーを押すと", font_color=9
        )
        self.texts[TextName.Prologue_07_03] = TextInfo(
            29, 67, "抜けるよ！", font_color=9
        )
