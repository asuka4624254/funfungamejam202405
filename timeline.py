import pyxel
from enum import IntEnum, auto
from image import ImageManager, ImageName

DEFAULT_FPS = 30


class TimelineName(IntEnum):
    Prologue = auto()


class TimelineManager:
    def __init__(self):
        self.timelines = {}
        self.set_timeline_events()

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
            [1, 3, lambda: image.draw(ImageName.PenguinM_02, 0, 0)],
            [3, 4, lambda: image.draw(ImageName.PenguinM_02, 0, 10)],
            [5, 6, lambda: image.draw(ImageName.PenguinM_02, 0, 20)],
            [7, 10, lambda: image.draw(ImageName.PenguinM_02, 0, 30)],
        ]
