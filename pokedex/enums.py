from __future__ import annotations

import re
from enum import Enum, unique
from functools import total_ordering


@total_ordering
class OrderedEnum(Enum):
    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.order < other.order
        return NotImplemented

    @property
    def order(self) -> int:
        return list(self.__class__.__members__.values()).index(self)


@unique
class AbilitySlot(Enum):
    SLOT_1 = "1"
    SLOT_2 = "2"
    HIDDEN = "h"


@unique
class Game(OrderedEnum):
    RED = "red"
    BLUE = "blue"  # Japanese Green
    BLUE_JP = "blue-jp"
    YELLOW = "yellow"
    GOLD = "gold"
    SILVER = "silver"
    CRYSTAL = "crystal"
    RUBY = "ruby"
    SAPPHIRE = "sapphire"
    FIRE_RED = "fire-red"
    LEAF_GREEN = "leaf-green"
    EMERALD = "emerald"
    DIAMOND = "diamond"
    PEARL = "pearl"
    PLATINUM = "platinum"
    HEART_GOLD = "heart-gold"
    SOUL_SILVER = "soul-silver"
    BLACK = "black"
    WHITE = "white"
    BLACK_2 = "black-2"
    WHITE_2 = "white-2"
    X = "x"
    Y = "y"
    OMEGA_RUBY = "omega-ruby"
    ALPHA_SAPPHIRE = "alpha-sapphire"
    SUN = "sun"
    MOON = "moon"
    ULTRA_SUN = "ultra-sun"
    ULTRA_MOON = "ultra-moon"
    LETS_GO_PIKACHU = "lets-go-pikachu"
    LETS_GO_EEVEE = "lets-go-eevee"
    SWORD = "sword"
    SHIELD = "shield"
    BRILLIANT_DIAMOND = "brilliant-diamond"
    SHINING_PEARL = "shining-pearl"
    LEGENDS_ARCEUS = "legends-arceus"
    SCARLET = "scarlet"
    VIOLET = "violet"


@unique
class GameGroup(OrderedEnum):
    RB = "rb"
    Y = "y"
    GS = "gs"
    C = "c"
    RS = "rs"
    FRLG = "frlg"
    E = "e"
    DP = "dp"
    P = "p"
    HGSS = "hgss"
    BW = "bw"
    B2W2 = "b2w2"
    XY = "xy"
    ORAS = "oras"
    SM = "sm"
    USUM = "usum"
    LGPE = "lgpe"
    SS = "ss"
    BDSP = "bdsp"
    LA = "la"
    SV = "sv"

    @classmethod
    def get_default(cls) -> GameGroup:
        return cls.SV


@unique
class HeldItemSlot(Enum):
    COMMON = "common"
    RARE = "rare"
    RARER_DARK_GRASS = "rarer_dark_grass"


@unique
class Language(Enum):
    JAPANESE_KANA = "jp-kana"
    JAPANESE_KANJI = "jp-kanji"
    ENGLISH = "en"
    FRENCH = "fr"
    ITALIAN = "it"
    GERMAN = "de"
    SPANISH = "es"
    KOREAN = "ko"
    CHINESE_SIMPLIFIED = "zh-simp"
    CHINESE_TRADITIONAL = "zh-trad"

    @classmethod
    def get_default(cls) -> Language:
        return cls.ENGLISH

    @classmethod
    def get(cls, language: str) -> Language | None:
        language = re.sub(r"[^a-z]", "", language.lower())
        table = {
            "jp": cls.JAPANESE_KANA,
            "japanese": cls.JAPANESE_KANA,
            "kana": cls.JAPANESE_KANA,
            "jpkana": cls.JAPANESE_KANA,
            "japanesekana": cls.JAPANESE_KANA,
            "kanji": cls.JAPANESE_KANJI,
            "jpkanji": cls.JAPANESE_KANJI,
            "japanesekanji": cls.JAPANESE_KANJI,
            "fr": cls.FRENCH,
            "french": cls.FRENCH,
            "de": cls.GERMAN,
            "german": cls.GERMAN,
            "es": cls.SPANISH,
            "spanish": cls.SPANISH,
            "it": cls.ITALIAN,
            "italian": cls.ITALIAN,
            "en": cls.ENGLISH,
            "english": cls.ENGLISH,
            "ko": cls.KOREAN,
            "korean": cls.KOREAN,
            "zh": cls.CHINESE_SIMPLIFIED,
            "chinese": cls.CHINESE_SIMPLIFIED,
            "zhsimp": cls.CHINESE_SIMPLIFIED,
            "chinesesimplified": cls.CHINESE_SIMPLIFIED,
            "zhtrad": cls.CHINESE_TRADITIONAL,
            "chinesetraditional": cls.CHINESE_TRADITIONAL,
        }
        return table.get(language)
