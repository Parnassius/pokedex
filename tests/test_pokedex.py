import re

import pytest

from pokedex import (
    Ability,
    EggGroup,
    GameGroup,
    HeldItemSlot,
    Item,
    Language,
    Move,
    Nature,
    Pokemon,
    Type,
    cache,
    set_context,
)
from pokedex.entities.base import BaseEntity, EntityRef


@pytest.mark.parametrize(
    ("entity", "identifier"),
    [
        (Ability, "run_away"),
        (EggGroup, "field"),
        (Item, "nugget"),
        (Move, "splash"),
        (Nature, "timid"),
        (Type, "normal"),
    ],
)
def test_get(entity: type[BaseEntity], identifier: str) -> None:
    entry = entity.get(identifier)
    assert entry is not None
    assert entry.identifier == identifier


@pytest.mark.parametrize(
    ("entity", "name", "entries"),
    [
        (
            Pokemon,
            "Papinox",
            {(Language.FRENCH, "dustox")},
        ),
        (
            Nature,
            "Timida",
            {(Language.ITALIAN, "timid"), (Language.SPANISH, "bashful")},
        ),
        (
            Move,
            "Mach Punch",
            {(Language.ENGLISH, "mach_punch"), (Language.FRENCH, "mach_punch")},
        ),
        (
            Item,
            "4호실열쇠",
            {(Language.KOREAN, "key_to_room_4")},
        ),
        (
            Ability,
            "プラス",
            {(Language.JAPANESE_KANA, "plus"), (Language.JAPANESE_KANJI, "plus")},
        ),
        (
            Item,
            "Ｚ手環",
            {(Language.CHINESE_TRADITIONAL, "z_ring")},
        ),
    ],
)
def test_search(
    entity: type[BaseEntity], name: str, entries: set[tuple[Language, str]]
) -> None:
    assert {
        (language, ref.identifier) for language, ref in entity.search(name)
    } == entries


def test_pokemon() -> None:
    pikachu = Pokemon.get("pikachu")
    assert pikachu is not None
    assert pikachu.identifier == "pikachu"

    assert pikachu.species_id.single() == 25
    assert pikachu.forms["pikachu_original_cap"].form_id.single() == 1
    assert pikachu.gmax_forms["pikachu_gigantamax"].form_id.single() == 999

    assert [x.get() for x in pikachu.forms["pikachu"].types.single()] == [
        Type.get("electric")
    ]
    assert [x.get() for x in pikachu.forms["pikachu"].egg_groups.single()] == [
        EggGroup.get("field"),
        EggGroup.get("fairy"),
    ]
    assert [x.get() for x in pikachu.forms["pikachu"].abilities.single()] == [
        Ability.get("static")
    ]
    assert pikachu.forms["pikachu"].hidden_ability.single().get() == Ability.get(
        "lightning_rod"
    )

    items_xy = pikachu.forms["pikachu"].held_items[GameGroup.X_Y]
    assert HeldItemSlot.COMMON not in items_xy
    item_xy_rare = items_xy[HeldItemSlot.RARE]
    assert isinstance(item_xy_rare, EntityRef)
    assert item_xy_rare.get() == Item.get("light_ball")


@pytest.mark.parametrize("entity", BaseEntity.__subclasses__())
def test_indices(entity: type[BaseEntity]) -> None:
    normalized_value_re = (
        r"["
        r"a-z0-9"
        r"\u3040-\u309F"  # hiragana
        r"\u30A0-\u30FF"  # katakana
        r"\u4E00-\u9FFF"  # cjk unified ideographs
        r"\uAC00-\uD7AF"  # hangul syllables
        r"]*"
    )
    for key in cache.get(entity).index:
        assert re.fullmatch(normalized_value_re, key)


def test_context() -> None:
    articuno = Pokemon.get("articuno")
    articuno_names = articuno.names
    assert articuno_names.get() == "Articuno"

    ctx = set_context(GameGroup.RED_BLUE)
    assert articuno_names.get() == "ARTICUNO"
    ctx.reset()

    ctx = set_context(Language.KOREAN)
    assert articuno_names.get() == "프리져"
    ctx.reset()

    ctx = set_context(GameGroup.EMERALD, Language.GERMAN)
    assert articuno_names.get() == "ARKTOS"
    ctx.reset()

    assert articuno_names.get() == "Articuno"

    with set_context(GameGroup.GOLD_SILVER):
        assert articuno_names.get() == "ARTICUNO"

    with set_context(Language.JAPANESE_KANA):
        assert articuno_names.get() == "フリーザー"

    with set_context(GameGroup.CRYSTAL, Language.FRENCH):
        assert articuno_names.get() == "ARTIKODIN"

    assert articuno_names.get() == "Articuno"

    with set_context(GameGroup.LEGENDS_ARCEUS):
        assert articuno_names.get() == "Articuno"
        assert articuno.species_id.get() == 144
        assert articuno_names.get(Language.CHINESE_SIMPLIFIED) == "急冻鸟"
