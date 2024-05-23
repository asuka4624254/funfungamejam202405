import pyxel
from enum import IntEnum, auto

DEFAULT_FPS = 30


class ImageName(IntEnum):
    BearFace = auto()
    Tear = auto()
    Tweezers_01 = auto()
    Tweezers_02 = auto()
    PenguinS_01 = auto()
    PenguinS_02 = auto()
    PenguinS_03 = auto()
    PenguinM_01 = auto()
    PenguinM_02 = auto()
    PenguinM_03 = auto()
    PenguinL_01 = auto()
    PenguinL_02 = auto()
    PenguinL_03 = auto()
    LOGO = auto()
    BG_01 = auto()
    BEAR = auto()
    CLEAR_BG_01 = auto()
    CLEAR_BG_02 = auto()
    CLEAR = auto()


class ImageInfo:
    def __init__(self, index, u, v, w, h, animate_with=None):
        self.index = index
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.animate_with = animate_with


class ImageManager:
    def __init__(self):
        self.load_images()

        self.assets = {}
        self.set_image_info()

    def load_images(self):
        pyxel.images[0].load(0, 0, "assets/001.png")

    def draw(
        self, image_asset, x, y, animation_speed=0.4
    ):  # animation_speed は小さい方が早くなる
        asset = self.assets[image_asset]
        if asset.animate_with is not None:
            asset = (
                self.assets[image_asset]
                if int(pyxel.frame_count / (DEFAULT_FPS * animation_speed)) % 2 == 0
                else self.assets[asset.animate_with]
            )

        pyxel.blt(
            x=x,
            y=y,
            img=asset.index,
            u=asset.u,
            v=asset.v,
            w=asset.w,
            h=asset.h,
            colkey=0,
        )

    def set_image_info(self):
        self.assets[ImageName.BearFace] = ImageInfo(0, 0, 0, 91, 44)
        self.assets[ImageName.Tear] = ImageInfo(0, 91, 0, 6, 11)

        self.assets[ImageName.Tweezers_01] = ImageInfo(
            0, 97, 0, 16, 13, ImageName.Tweezers_02
        )
        self.assets[ImageName.Tweezers_02] = ImageInfo(0, 113, 0, 16, 13)

        self.assets[ImageName.PenguinS_01] = ImageInfo(0, 91, 13, 13, 16)
        self.assets[ImageName.PenguinS_02] = ImageInfo(
            0, 104, 13, 13, 16, ImageName.PenguinS_03
        )
        self.assets[ImageName.PenguinS_03] = ImageInfo(0, 117, 13, 13, 16)

        self.assets[ImageName.PenguinM_01] = ImageInfo(0, 0, 44, 28, 34)
        self.assets[ImageName.PenguinM_02] = ImageInfo(
            0, 28, 44, 28, 34, ImageName.PenguinM_03
        )
        self.assets[ImageName.PenguinM_03] = ImageInfo(0, 56, 44, 28, 34)

        self.assets[ImageName.PenguinL_01] = ImageInfo(0, 0, 78, 50, 63)
        self.assets[ImageName.PenguinL_02] = ImageInfo(
            0, 50, 78, 50, 63, ImageName.PenguinL_03
        )
        self.assets[ImageName.PenguinL_03] = ImageInfo(0, 100, 78, 50, 63)

        self.assets[ImageName.LOGO] = ImageInfo(0, 89, 29, 68, 30)
        self.assets[ImageName.BG_01] = ImageInfo(0, 157, 0, 96, 128)
        self.assets[ImageName.BEAR] = ImageInfo(0, 0, 141, 26, 37)

        self.assets[ImageName.CLEAR_BG_01] = ImageInfo(
            0, 26, 141, 89, 55, ImageName.CLEAR_BG_02
        )
        self.assets[ImageName.CLEAR_BG_02] = ImageInfo(0, 115, 141, 89, 55)
        self.assets[ImageName.CLEAR] = ImageInfo(0, 0, 196, 62, 24)
