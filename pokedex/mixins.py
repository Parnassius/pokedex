from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from pokedex import enums

if TYPE_CHECKING:
    from pokedex import tables


NORMALIZED_VALUE_RE = (
    r"["
    r"a-z0-9"
    r"\u3040-\u309F"  # hiragana
    r"\u30A0-\u30FF"  # katakana
    r"\u4E00-\u9FFF"  # cjk unified ideographs
    r"\uAC00-\uD7AF"  # hangul syllables
    r"]*"
)
OTHER_NORMALIZED_CHARACTERS = {
    "œ": "oe",
}


def _normalize_value(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = unicodedata.normalize("NFC", text)
    text = text.replace("♀", "f").replace("♂", "m")
    text = "".join(c for c in text if unicodedata.category(c)[0] in ("L", "N"))
    text = text.casefold()
    return "".join(OTHER_NORMALIZED_CHARACTERS.get(c, c) for c in text)


def _normalized_value(field: str) -> Callable[[DefaultExecutionContext], str]:
    def inner(context: DefaultExecutionContext) -> str:
        text = context.get_current_parameters()[field]  # type: ignore[no-untyped-call]
        assert isinstance(text, str)
        text = _normalize_value(text)
        assert re.fullmatch(NORMALIZED_VALUE_RE, text), text
        return text

    return inner


# Common collection classes


class GameGroupCollectionTable:
    game_group_identifier: Mapped[enums.GameGroup] = mapped_column(
        ForeignKey("game_groups.identifier"), primary_key=True
    )

    @declared_attr
    @classmethod
    def game_group(cls) -> Mapped[tables.GameGroup]:
        return relationship(viewonly=True)


class GameCollectionTable:
    game_identifier: Mapped[enums.Game] = mapped_column(
        ForeignKey("games.identifier"), primary_key=True
    )

    @declared_attr
    @classmethod
    def game(cls) -> Mapped[tables.Game]:
        return relationship(viewonly=True)


# Changes


class ChangesTable:
    game_group_identifier_from: Mapped[enums.GameGroup] = mapped_column(
        ForeignKey("game_groups.identifier"), primary_key=True
    )
    game_revision_from: Mapped[str] = mapped_column(primary_key=True)
    game_group_identifier_to: Mapped[enums.GameGroup] = mapped_column(
        ForeignKey("game_groups.identifier"), primary_key=True
    )
    game_revision_to: Mapped[str] = mapped_column(primary_key=True)

    @declared_attr
    @classmethod
    def game_group_from(cls) -> Mapped[tables.GameGroup]:
        return relationship(foreign_keys=cls.game_group_identifier_from, viewonly=True)

    @declared_attr
    @classmethod
    def game_group_to(cls) -> Mapped[tables.GameGroup]:
        return relationship(foreign_keys=cls.game_group_identifier_to, viewonly=True)


# Translations


class TranslationsTable:
    language_identifier: Mapped[enums.Language] = mapped_column(
        ForeignKey("languages.identifier"), primary_key=True
    )

    @declared_attr
    @classmethod
    def language(cls) -> Mapped[tables.Language]:
        return relationship(viewonly=True)


class NamesTranslationsTable(TranslationsTable):
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )
