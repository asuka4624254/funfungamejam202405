import pyxel
from enum import IntEnum, auto


class ImageAsset(IntEnum):
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
    BG_01 = auto()


class ImageInfo:
    def __init__(self, index, u, v, w, h):
        self.index = index
        self.u = u
        self.v = v
        self.w = w
        self.h = h


class Image:
    def __init__(self):
        self.load_images()

        self.assets = {}
        self.set_image_info()

    def load_images(self):
        pyxel.images[0].load(0, 0, "assets/001.png")

    def draw(self, image_asset, x, y):
        asset = self.assets[image_asset]
        pyxel.blt(
            x=x,
            y=y,
            img=asset.index,
            u=asset.u,
            v=asset.v,
            w=asset.w,
            h=asset.h,
            colkey=3,
        )

    def set_image_info(self):
        self.assets[ImageAsset.BearFace] = ImageInfo(0, 0, 0, 91, 44)
        self.assets[ImageAsset.Tear] = ImageInfo(0, 91, 0, 6, 11)  # FIXME: 表示されない
        self.assets[ImageAsset.Tweezers_01] = ImageInfo(0, 97, 0, 16, 13)
        self.assets[ImageAsset.Tweezers_02] = ImageInfo(0, 113, 0, 16, 13)
        self.assets[ImageAsset.PenguinS_01] = ImageInfo(0, 91, 13, 13, 15)
        self.assets[ImageAsset.PenguinS_02] = ImageInfo(0, 104, 13, 13, 15)
        self.assets[ImageAsset.PenguinS_03] = ImageInfo(0, 117, 13, 13, 15)
        self.assets[ImageAsset.PenguinM_01] = ImageInfo(0, 0, 44, 28, 33)
        self.assets[ImageAsset.PenguinM_02] = ImageInfo(0, 27, 44, 28, 33)
        self.assets[ImageAsset.PenguinM_03] = ImageInfo(0, 55, 44, 28, 33)
        self.assets[ImageAsset.PenguinL_01] = ImageInfo(0, 0, 77, 50, 61)
        self.assets[ImageAsset.PenguinL_02] = ImageInfo(0, 50, 77, 50, 61)
        self.assets[ImageAsset.PenguinL_03] = ImageInfo(0, 100, 77, 50, 61)
        self.assets[ImageAsset.BG_01] = ImageInfo(0, 150, 0, 96, 128)
