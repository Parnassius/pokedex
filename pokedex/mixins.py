from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from pokedex import enums

if TYPE_CHECKING:
    from pokedex import tables


# Common collection classes


class BaseCollectionTable:
    @property
    def game_group_enum(self) -> enums.GameGroup:
        raise NotImplementedError


BaseCollectionTableT = TypeVar("BaseCollectionTableT", bound=BaseCollectionTable)


class GameGroupCollectionTable(BaseCollectionTable):
    game_group_identifier: Mapped[enums.GameGroup] = mapped_column(
        ForeignKey("game_groups.identifier"), primary_key=True
    )

    @declared_attr
    @classmethod
    def game_group(cls) -> Mapped[tables.GameGroup]:
        return relationship(viewonly=True)

    @property
    def game_group_enum(self) -> enums.GameGroup:
        return self.game_group_identifier


class GameCollectionTable(BaseCollectionTable):
    game_identifier: Mapped[enums.Game] = mapped_column(
        ForeignKey("games.identifier"), primary_key=True
    )

    @declared_attr
    @classmethod
    def game(cls) -> Mapped[tables.Game]:
        return relationship(viewonly=True)

    @property
    def game_group_enum(self) -> enums.GameGroup:
        return self.game.game_group_identifier


# Sequences (pokemon egg groups, pokemon types, ...)


class GameGroupSequenceTable(GameGroupCollectionTable):
    pass


GameGroupSequenceTableT = TypeVar(
    "GameGroupSequenceTableT", bound=GameGroupSequenceTable
)


# Mappings (pokemon abilities, pokemon stats, ...)


class BaseMappingTable(BaseCollectionTable):
    @property
    def mapping_key(self) -> Hashable:
        raise NotImplementedError


class GameGroupMappingTable(GameGroupCollectionTable, BaseMappingTable):
    pass


GameGroupMappingTableT = TypeVar("GameGroupMappingTableT", bound=GameGroupMappingTable)


class GameMappingTable(GameCollectionTable, BaseMappingTable):
    pass


GameMappingTableT = TypeVar("GameMappingTableT", bound=GameMappingTable)


# Translations


class TranslationsTable(BaseCollectionTable):
    language_identifier: Mapped[enums.Language] = mapped_column(
        ForeignKey("languages.identifier"), primary_key=True
    )

    @declared_attr
    @classmethod
    def language(cls) -> Mapped[tables.Language]:
        return relationship(viewonly=True)


TranslationsTableT = TypeVar("TranslationsTableT", bound=TranslationsTable)


class TranslationChangesTable(TranslationsTable):
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
        return relationship(viewonly=True, foreign_keys=cls.game_group_identifier_from)

    @declared_attr
    @classmethod
    def game_group_to(cls) -> Mapped[tables.GameGroup]:
        return relationship(viewonly=True, foreign_keys=cls.game_group_identifier_to)


class GameTranslationsTable(GameCollectionTable, TranslationsTable):
    pass


GameTranslationsTableT = TypeVar("GameTranslationsTableT", bound=GameTranslationsTable)


class GameTranslationChangesTable(GameTranslationsTable):
    game_revision_from: Mapped[str] = mapped_column(primary_key=True)
    game_revision_to: Mapped[str] = mapped_column(primary_key=True)
