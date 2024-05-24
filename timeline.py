import pyxel
from enum import IntEnum, auto
from image import ImageManager, ImageName
from text import TextManager, TextName

DEFAULT_FPS = 30


class TimelineName(IntEnum):
    Prologue = auto()
    Ready = auto()


class TimelineManager:
    def __init__(self):
        self.timelines = {}
        self.set_timeline_events()

        self.text = TextManager()

        self.start_frame = 0  # 同時に1つしか再生できない

    def reset(self):
        self.start_frame = 0
        self.text.reset()

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

    def is_play(self, timeline_name):
        current_frame = pyxel.frame_count - self.start_frame
        elapsed_seconds = current_frame / DEFAULT_FPS
        end_seconds = self.timelines[timeline_name][-1][1]
        return elapsed_seconds < end_seconds

    def set_timeline_events(self):
        image = ImageManager()

        self.timelines[TimelineName.Prologue] = [
            # 開始秒数, 終了秒数, 実行内容
            # 開始秒数は、1文字0.1秒 + インターバル0.5秒（画面遷移時はインターバル1秒）
            # カーテン
            [0, 0.2, lambda: image.draw(ImageName.Curtain_01, 0, 0)],
            [0.2, 0.4, lambda: image.draw(ImageName.Curtain_02, 0, 0)],
            [0.4, 0.6, lambda: image.draw(ImageName.Curtain_03, 0, 0)],
            [0.6, 0.8, lambda: image.draw(ImageName.Curtain_04, 0, 0)],
            [0.8, 1, lambda: image.draw(ImageName.Curtain_05, 0, 0)],
            # 「ペンギンさんとおでかけに…」7, 7, 7, 6
            [1, 5.7, lambda: self.text.draw_animation(TextName.Prologue_01_01)],
            [2.2, 5.7, lambda: self.text.draw_animation(TextName.Prologue_01_02)],
            [3.4, 5.7, lambda: self.text.draw_animation(TextName.Prologue_01_03)],
            [4.6, 5.7, lambda: self.text.draw_animation(TextName.Prologue_01_04)],
            # 「あ！ペンギンさんだ！…」10, 4
            [5.7, 8.1, lambda: self.text.draw_animation(TextName.Prologue_02_01)],
            [7.2, 8.1, lambda: self.text.draw_animation(TextName.Prologue_02_02)],
            # ペンギン表示
            [8.1, 10.6, lambda: image.draw(ImageName.Prologue_Penguin_01, 32, 19)],
            # 「わー、今日は楽しみだなぁ…」6, 6, 3
            [10.6, 13.6, lambda: self.text.draw_animation(TextName.Prologue_03_01)],
            [11.7, 13.6, lambda: self.text.draw_animation(TextName.Prologue_03_02)],
            [12.8, 13.6, lambda: self.text.draw_animation(TextName.Prologue_03_03)],
            # 「ふっと、こおりにうつった…」8, 10, 7
            [13.6, 17.6, lambda: self.text.draw_animation(TextName.Prologue_04_01)],
            [14.9, 17.6, lambda: self.text.draw_animation(TextName.Prologue_04_02)],
            [16.4, 17.6, lambda: self.text.draw_animation(TextName.Prologue_04_03)],
            # 「はなからア、アレが…」4, 10
            [17.6, 23, lambda: self.text.draw_animation(TextName.Prologue_05_01)],
            [18.5, 23, lambda: self.text.draw_animation(TextName.Prologue_05_02)],
            # しろくま表示
            [20.5, 23, lambda: image.draw(ImageName.Prologue_BearFace_01, 3, 84)],
            # 「ペンギンさんに見られる前に…」7, 6, 7
            [23, 26.5, lambda: self.text.draw_animation(TextName.Prologue_06_01)],
            [24.2, 26.5, lambda: self.text.draw_animation(TextName.Prologue_06_02)],
            [25.3, 26.5, lambda: self.text.draw_animation(TextName.Prologue_06_03)],
            # 「タイミングよく…」7, 7, 5
            [
                26.5,
                31.4,
                lambda: self.text.draw_animation(TextName.Prologue_07_01),
            ],
            [27.7, 31.4, lambda: self.text.draw_animation(TextName.Prologue_07_02)],
            [28.9, 31.4, lambda: self.text.draw_animation(TextName.Prologue_07_03)],
        ]

        self.timelines[TimelineName.Ready] = [
            # Ready
            [1, 2.5, lambda: image.draw(ImageName.Ready, 15, 58)],
            # Go
            [2.7, 4.2, lambda: image.draw(ImageName.Go, 28, 58)],
        ]
