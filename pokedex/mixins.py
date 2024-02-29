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
    def game_group(self) -> Mapped[tables.GameGroup]:
        return relationship(viewonly=True)

    @property
    def game_group_enum(self) -> enums.GameGroup:
        return self.game_group_identifier


class GameCollectionTable(BaseCollectionTable):
    game_identifier: Mapped[enums.Game] = mapped_column(
        ForeignKey("games.identifier"), primary_key=True
    )

    @declared_attr
    def game(self) -> Mapped[tables.Game]:
        return relationship(viewonly=True)

    @property
    def game_group_enum(self) -> enums.GameGroup:
        return self.game.game_group_identifier


class GameGroupRevisionCollectionTable(GameGroupCollectionTable):
    game_revision: Mapped[str] = mapped_column(primary_key=True)


class GameRevisionCollectionTable(GameCollectionTable):
    game_revision: Mapped[str] = mapped_column(primary_key=True)


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
    def language(self) -> Mapped[tables.Language]:
        return relationship(viewonly=True)

    @property
    def game_group_enum(self) -> enums.GameGroup:
        return enums.GameGroup.get_default()

    def sort_key(
        self,
        language: enums.Language,
        game_group: enums.GameGroup = enums.GameGroup.get_default(),
    ) -> tuple[int, int]:
        language_key = 0
        if self.language_identifier == enums.Language.get_default():
            language_key = 1
        elif self.language_identifier == language:
            language_key = 2

        game_group_key = 0
        entry_game_group = self.game_group_enum
        game_group_key = entry_game_group.order
        if entry_game_group > game_group:
            game_group_key = -game_group_key

        return (language_key, game_group_key)


TranslationsTableT = TypeVar("TranslationsTableT", bound=TranslationsTable)


class GameGroupTranslationsTable(GameGroupCollectionTable, TranslationsTable):
    pass


GameGroupTranslationsTableT = TypeVar(
    "GameGroupTranslationsTableT", bound=GameGroupTranslationsTable
)


class GameTranslationsTable(GameCollectionTable, TranslationsTable):
    pass


GameTranslationsTableT = TypeVar("GameTranslationsTableT", bound=GameTranslationsTable)


class GameGroupRevisionTranslationsTable(
    GameGroupRevisionCollectionTable, TranslationsTable
):
    pass


GameGroupRevisionTranslationsTableT = TypeVar(
    "GameGroupRevisionTranslationsTableT", bound=GameGroupRevisionTranslationsTable
)


class GameRevisionTranslationsTable(GameRevisionCollectionTable, TranslationsTable):
    pass


GameRevisionTranslationsTableT = TypeVar(
    "GameRevisionTranslationsTableT", bound=GameRevisionTranslationsTable
)
