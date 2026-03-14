from enum import Enum, auto, unique
from functools import total_ordering
from itertools import product
from typing import Self, override


@total_ordering
class OrderedEnum(Enum):
    @override
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        return name.lower()

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.order < other.order
        return NotImplemented

    @property
    def order(self) -> int:
        return list(self.__class__).index(self)


@unique
class GameGroup(OrderedEnum):
    RED_BLUE = auto()
    YELLOW = auto()
    GOLD_SILVER = auto()
    CRYSTAL = auto()
    RUBY_SAPPHIRE = auto()
    FIRE_RED_LEAF_GREEN = auto()
    EMERALD = auto()
    DIAMOND_PEARL = auto()
    PLATINUM = auto()
    HEART_GOLD_SOUL_SILVER = auto()
    BLACK_WHITE = auto()
    BLACK_2_WHITE_2 = auto()
    X_Y = auto()
    OMEGA_RUBY_ALPHA_SAPPHIRE = auto()
    SUN_MOON = auto()
    ULTRA_SUN_ULTRA_MOON = auto()
    LETS_GO_PIKACHU_EEVEE = auto()
    SWORD_SHIELD = auto()
    BRILLIANT_DIAMOND_SHINING_PEARL = auto()
    LEGENDS_ARCEUS = auto()
    SCARLET_VIOLET = auto()
    LEGENDS_ZA = auto()

    @property
    def games(self) -> "list[Game]":
        return [x for x in Game if self is x.game_group]

    @property
    def languages(self) -> "list[Language]":
        langs = {
            Language.ENGLISH,
            Language.FRENCH,
            Language.ITALIAN,
            Language.GERMAN,
            Language.SPANISH,
        }
        if self < GameGroup.LEGENDS_ARCEUS:
            langs.add(Language.JAPANESE_KANA)
        if self is GameGroup.GOLD_SILVER or self >= GameGroup.DIAMOND_PEARL:
            langs.add(Language.KOREAN)
        if self >= GameGroup.BLACK_WHITE:
            langs.add(Language.JAPANESE_KANJI)
        if self >= GameGroup.SUN_MOON:
            langs.update({Language.CHINESE_SIMPLIFIED, Language.CHINESE_TRADITIONAL})
        if self >= GameGroup.LEGENDS_ZA:
            langs.add(Language.SPANISH_LATAM)
        return sorted(langs)

    @property
    def games_languages(self) -> "list[tuple[Game, Language]]":
        combinations = set()
        for game, language in product(self.games, self.languages):
            if game is Game.BLUE_JP and language is not Language.JAPANESE_KANA:
                continue
            combinations.add((game, language))
        return sorted(combinations)

    @property
    def sorted_with_default(self) -> list[Self]:
        return sorted(
            GameGroup,
            key=lambda x: (x.order <= self.order, x.order),
            reverse=True,
        )

    @classmethod
    def get_default(cls) -> "GameGroup":
        return next(reversed(cls))


@unique
class Game(OrderedEnum):
    RED = auto(), GameGroup.RED_BLUE
    BLUE = auto(), GameGroup.RED_BLUE  # Japanese Green
    BLUE_JP = auto(), GameGroup.RED_BLUE
    YELLOW = auto(), GameGroup.YELLOW
    GOLD = auto(), GameGroup.GOLD_SILVER
    SILVER = auto(), GameGroup.GOLD_SILVER
    CRYSTAL = auto(), GameGroup.CRYSTAL
    RUBY = auto(), GameGroup.RUBY_SAPPHIRE
    SAPPHIRE = auto(), GameGroup.RUBY_SAPPHIRE
    FIRE_RED = auto(), GameGroup.FIRE_RED_LEAF_GREEN
    LEAF_GREEN = auto(), GameGroup.FIRE_RED_LEAF_GREEN
    EMERALD = auto(), GameGroup.EMERALD
    DIAMOND = auto(), GameGroup.DIAMOND_PEARL
    PEARL = auto(), GameGroup.DIAMOND_PEARL
    PLATINUM = auto(), GameGroup.PLATINUM
    HEART_GOLD = auto(), GameGroup.HEART_GOLD_SOUL_SILVER
    SOUL_SILVER = auto(), GameGroup.HEART_GOLD_SOUL_SILVER
    BLACK = auto(), GameGroup.BLACK_WHITE
    WHITE = auto(), GameGroup.BLACK_WHITE
    BLACK_2 = auto(), GameGroup.BLACK_2_WHITE_2
    WHITE_2 = auto(), GameGroup.BLACK_2_WHITE_2
    X = auto(), GameGroup.X_Y
    Y = auto(), GameGroup.X_Y
    OMEGA_RUBY = auto(), GameGroup.OMEGA_RUBY_ALPHA_SAPPHIRE
    ALPHA_SAPPHIRE = auto(), GameGroup.OMEGA_RUBY_ALPHA_SAPPHIRE
    SUN = auto(), GameGroup.SUN_MOON
    MOON = auto(), GameGroup.SUN_MOON
    ULTRA_SUN = auto(), GameGroup.ULTRA_SUN_ULTRA_MOON
    ULTRA_MOON = auto(), GameGroup.ULTRA_SUN_ULTRA_MOON
    LETS_GO_PIKACHU = auto(), GameGroup.LETS_GO_PIKACHU_EEVEE
    LETS_GO_EEVEE = auto(), GameGroup.LETS_GO_PIKACHU_EEVEE
    SWORD = auto(), GameGroup.SWORD_SHIELD
    SHIELD = auto(), GameGroup.SWORD_SHIELD
    BRILLIANT_DIAMOND = auto(), GameGroup.BRILLIANT_DIAMOND_SHINING_PEARL
    SHINING_PEARL = auto(), GameGroup.BRILLIANT_DIAMOND_SHINING_PEARL
    LEGENDS_ARCEUS = auto(), GameGroup.LEGENDS_ARCEUS
    SCARLET = auto(), GameGroup.SCARLET_VIOLET
    VIOLET = auto(), GameGroup.SCARLET_VIOLET
    LEGENDS_ZA = auto(), GameGroup.LEGENDS_ZA

    game_group: GameGroup

    def __new__(cls, value: str, game_group: "GameGroup") -> "Game":
        obj = object.__new__(cls)
        obj._value_ = value
        obj.game_group = game_group
        return obj


@unique
class HeldItemSlot(OrderedEnum):
    COMMON = auto()
    RARE = auto()
    RARER_DARK_GRASS = auto()


@unique
class Language(OrderedEnum):
    JAPANESE_KANA = "jp_kana"
    JAPANESE_KANJI = "jp_kanji"
    ENGLISH = "en"
    FRENCH = "fr"
    ITALIAN = "it"
    GERMAN = "de"
    SPANISH = "es"
    KOREAN = "ko"
    CHINESE_SIMPLIFIED = "zh_simp"
    CHINESE_TRADITIONAL = "zh_trad"
    SPANISH_LATAM = "es_latam"

    @classmethod
    def get_default(cls) -> "Language":
        return cls.ENGLISH


@unique
class Stat(OrderedEnum):
    HP = auto()
    ATTACK = auto()
    DEFENSE = auto()
    SPECIAL_ATTACK = auto()
    SPECIAL_DEFENSE = auto()
    SPEED = auto()
    SPECIAL = auto()
