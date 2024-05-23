import pyxel
from enum import IntEnum, auto
from image import ImageManager, ImageName
from text import TextManager, TextName

DEFAULT_FPS = 30


class TimelineName(IntEnum):
    Prologue = auto()


class TimelineManager:
    def __init__(self):
        self.timelines = {}
        self.set_timeline_events()

        self.text = TextManager()

        self.start_frame = 0  # 同時に1つしか再生できない

    def play(self, timeline_name):
        if self.start_frame == 0:
            self.start_frame = pyxel.frame_count

        events = self.timelines[timeline_name]
        sorted_events = sorted(events, key=lambda x: x[0])

        for event in sorted_events:
            current_frame = pyxel.frame_count - self.start_frame

            start_frame = event[0] * DEFAULT_FPS
            end_frame = event[1] * DEFAULT_FPS
            event_func = event[2]

            if current_frame >= start_frame and current_frame <= end_frame:
                event_func()

    def set_timeline_events(self):
        image = ImageManager()

        self.timelines[TimelineName.Prologue] = [
            # 開始秒数, 終了秒数, 実行内容
            # 開始秒数は、1文字0.1秒 + インターバル0.5秒（画面遷移時はインターバル1秒）
            # 「ペンギンさんとおでかけに…」
            [1, 6.2, lambda: self.text.draw_animation(TextName.Prologue_01_01)],
            [2.2, 6.2, lambda: self.text.draw_animation(TextName.Prologue_01_02)],
            [3.4, 6.2, lambda: self.text.draw_animation(TextName.Prologue_01_03)],
            [4.6, 6.2, lambda: self.text.draw_animation(TextName.Prologue_01_04)],
            # 「あ！ペンギンさんだ！…」
            [7.2, 10.1, lambda: self.text.draw_animation(TextName.Prologue_02_01)],
            [8.7, 10.1, lambda: self.text.draw_animation(TextName.Prologue_02_02)],
            # ペンギン表示
            [11.1, 14.1, lambda: image.draw(ImageName.Prologue_Penguin_01, 32, 19)],
            # 「わー、今日は楽しみだなぁ…」
            [14.1, 18.7, lambda: self.text.draw_animation(TextName.Prologue_03_01)],
            [15.2, 18.7, lambda: self.text.draw_animation(TextName.Prologue_03_02)],
            [17.4, 18.7, lambda: self.text.draw_animation(TextName.Prologue_03_03)],
            # 「ふっと、こおりにうつった…」
            [19.7, 24.2, lambda: self.text.draw_animation(TextName.Prologue_04_01)],
            [21, 24.2, lambda: self.text.draw_animation(TextName.Prologue_04_02)],
            [22.5, 24.2, lambda: self.text.draw_animation(TextName.Prologue_04_03)],
            # # しろくま表示
            [25.2, 30, lambda: image.draw(ImageName.Prologue_BearFace_01, 3, 84)],
            # # 「はなからア、アレが…」
            # [1, 6.2, lambda: self.text.draw_animation(TextName.Prologue_05_01)],
            # [2.2, 6.2, lambda: self.text.draw_animation(TextName.Prologue_05_02)],
            # # 「ペンギンさんに見られる前に…」
            # [1, 6.2, lambda: self.text.draw_animation(TextName.Prologue_06_01)],
            # [2.2, 6.2, lambda: self.text.draw_animation(TextName.Prologue_06_02)],
            # [3.4, 6.2, lambda: self.text.draw_animation(TextName.Prologue_06_03)],
            # # 「タイミングよく…」
            # [1, 6.2, lambda: self.text.draw_animation(TextName.Prologue_07_01)],
            # [2.2, 6.2, lambda: self.text.draw_animation(TextName.Prologue_07_02)],
            # [3.4, 6.2, lambda: self.text.draw_animation(TextName.Prologue_07_03)],
        ]
