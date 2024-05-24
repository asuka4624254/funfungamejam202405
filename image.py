import pyxel
from enum import IntEnum, auto

DEFAULT_FPS = 30


class ImageName(IntEnum):
    BearFace = auto()
    Tear = auto()
    Tweezers_01 = auto()
    Tweezers_02 = auto()
    Tweezers_03 = auto()
    TweezersUsed = auto()
    PenguinS_01 = auto()
    PenguinS_02 = auto()
    PenguinS_03 = auto()
    PenguinM_01 = auto()
    PenguinM_02 = auto()
    PenguinM_03 = auto()
    PenguinL_01 = auto()
    PenguinL_02 = auto()
    PenguinL_03 = auto()
    Logo_01 = auto()
    Logo_02 = auto()
    BG_01 = auto()
    Bear = auto()
    Bear_01 = auto()
    Bear_02 = auto()

    Prologue_Penguin_01 = auto()
    Prologue_Penguin_02 = auto()
    Prologue_BearFace_01 = auto()
    Prologue_BearFace_02 = auto()

    Reset_01 = auto()
    Reset_02 = auto()

    Clear_01 = auto()
    Clear_02 = auto()
    Miss_01 = auto()
    Miss_02 = auto()

    Curtain_01 = auto()
    Curtain_02 = auto()
    Curtain_03 = auto()
    Curtain_04 = auto()
    Curtain_05 = auto()

    Ready = auto()
    Go = auto()


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
        pyxel.images[2].load(0, 0, "assets/003.png")

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
        self.assets[ImageName.Tweezers_03] = ImageInfo(
            0, 129, 0, 16, 13
        )  # キラキラなし毛抜き
        self.assets[ImageName.TweezersUsed] = ImageInfo(
            0, 130, 13, 16, 13
        )  # 使用済み毛抜き

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

        self.assets[ImageName.Logo_01] = ImageInfo(0, 89, 29, 68, 31, ImageName.Logo_02)
        self.assets[ImageName.Logo_02] = ImageInfo(0, 112, 141, 68, 31)
        self.assets[ImageName.BG_01] = ImageInfo(0, 157, 0, 96, 128)
        self.assets[ImageName.Bear] = ImageInfo(0, 0, 141, 26, 37)
        self.assets[ImageName.Bear_01] = ImageInfo(0, 0, 141, 26, 37, ImageName.Bear_02)
        self.assets[ImageName.Bear_02] = ImageInfo(0, 26, 141, 26, 37)

        self.assets[ImageName.Prologue_Penguin_01] = ImageInfo(
            0, 52, 141, 30, 34, ImageName.Prologue_Penguin_02
        )
        self.assets[ImageName.Prologue_Penguin_02] = ImageInfo(0, 82, 141, 30, 34)
        self.assets[ImageName.Prologue_BearFace_01] = ImageInfo(
            0, 0, 178, 91, 44, ImageName.Prologue_BearFace_02
        )
        self.assets[ImageName.Prologue_BearFace_02] = ImageInfo(0, 91, 178, 91, 44)

        self.assets[ImageName.Reset_01] = ImageInfo(
            0, 0, 222, 36, 31, ImageName.Reset_02
        )
        self.assets[ImageName.Reset_02] = ImageInfo(0, 36, 222, 36, 31)

        self.assets[ImageName.Clear_01] = ImageInfo(2, 0, 0, 89, 55, ImageName.Clear_02)
        self.assets[ImageName.Clear_02] = ImageInfo(2, 89, 0, 89, 55)
        self.assets[ImageName.Miss_01] = ImageInfo(2, 0, 55, 75, 38, ImageName.Miss_02)
        self.assets[ImageName.Miss_02] = ImageInfo(2, 75, 55, 75, 38)

        self.assets[ImageName.Curtain_01] = ImageInfo(2, 0, 93, 96, 118)
        self.assets[ImageName.Curtain_02] = ImageInfo(2, 0, 93 + 20, 96, 118 - 20)
        self.assets[ImageName.Curtain_03] = ImageInfo(2, 0, 93 + 40, 96, 118 - 40)
        self.assets[ImageName.Curtain_04] = ImageInfo(2, 0, 93 + 60, 96, 118 - 60)
        self.assets[ImageName.Curtain_05] = ImageInfo(2, 0, 93 + 80, 96, 118 - 80)

        self.assets[ImageName.Ready] = ImageInfo(2, 96, 93, 66, 24)
        self.assets[ImageName.Go] = ImageInfo(2, 96, 117, 41, 24)
