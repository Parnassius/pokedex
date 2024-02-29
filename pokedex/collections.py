from __future__ import annotations

from collections.abc import Hashable
from typing import Generic, TypeVar, cast

from pokedex import enums, mixins

HashableT = TypeVar("HashableT", bound=Hashable)


class BaseCollection(list[mixins.BaseCollectionTableT]):
    def _get(
        self, game_group: enums.GameGroup | str | None
    ) -> list[mixins.BaseCollectionTableT]:
        if game_group is None:
            game_group = max(x.game_group_enum for x in self)
        else:
            game_group = enums.GameGroup(game_group)

        return [x for x in self if x.game_group_enum == game_group]


class GameGroupSequenceCollection(BaseCollection[mixins.GameGroupSequenceTableT]):
    def get(
        self, game_group: enums.GameGroup | str | None = None
    ) -> list[mixins.GameGroupSequenceTableT]:
        return self._get(game_group)


class GameGroupMappingCollection(
    BaseCollection[mixins.GameGroupMappingTableT],
    Generic[mixins.GameGroupMappingTableT, HashableT],
):
    def get(
        self, game_group: enums.GameGroup | str | None = None
    ) -> dict[HashableT, mixins.GameGroupMappingTableT]:
        return {x.mapping_key: x for x in self._get(game_group)}  # type: ignore[misc]


class GameMappingCollection(
    BaseCollection[mixins.GameMappingTableT],
    Generic[mixins.GameMappingTableT, HashableT],
):
    def get(
        self, game_group: enums.GameGroup | str | None = None
    ) -> dict[HashableT, dict[enums.Game, mixins.GameMappingTableT]]:
        entries: dict[HashableT, dict[enums.Game, mixins.GameMappingTableT]] = {}
        for entry in self._get(game_group):
            key = cast(HashableT, entry.mapping_key)
            if key not in entries:
                entries[key] = {}
            entries[key][entry.game_identifier] = entry
        return entries


class GameGroupOrGameMappingCollection(
    Generic[mixins.GameGroupMappingTableT, mixins.GameMappingTableT, HashableT]
):
    def __init__(
        self,
        game_group_table: GameGroupMappingCollection[
            mixins.GameGroupMappingTableT, HashableT
        ],
        game_table: GameMappingCollection[mixins.GameMappingTableT, HashableT],
    ) -> None:
        self._game_group_table = game_group_table
        self._game_table = game_table

    def get(self, game_group: enums.GameGroup | str | None = None) -> dict[
        HashableT,
        mixins.GameGroupMappingTableT | dict[enums.Game, mixins.GameMappingTableT],
    ]:
        return {
            **self._game_group_table.get(game_group),
            **self._game_table.get(game_group),
        }


class BaseTranslationsCollection(BaseCollection[mixins.TranslationsTableT]):
    def all(
        self,
        *,
        game_group: enums.GameGroup | str | None = None,
        language: enums.Language | str | None = None,
    ) -> list[mixins.TranslationsTableT]:
        game_group = enums.GameGroup(game_group) if game_group else None
        language = enums.Language(language) if language else None

        entries = []
        for entry in self:
            if game_group and game_group != entry.game_group_enum:
                continue
            if language and language != entry.language_identifier:
                continue
            entries.append(entry)
        return entries


class TranslationsCollection(BaseTranslationsCollection[mixins.TranslationsTableT]):
    def get(
        self, *, language: enums.Language | str = enums.Language.get_default()
    ) -> mixins.TranslationsTableT:
        language_ = enums.Language(language)

        return max(self, key=lambda x: x.sort_key(language_))


class GameGroupTranslationsCollection(
    BaseTranslationsCollection[mixins.GameGroupTranslationsTableT]
):
    def get(
        self,
        game_group: enums.GameGroup | str = enums.GameGroup.get_default(),
        *,
        language: enums.Language | str = enums.Language.get_default(),
    ) -> mixins.GameGroupTranslationsTableT:
        game_group_ = enums.GameGroup(game_group)
        language_ = enums.Language(language)

        return max(self, key=lambda x: x.sort_key(language_, game_group_))


class GameTranslationsCollection(
    BaseTranslationsCollection[mixins.GameTranslationsTableT]
):
    def get(
        self,
        game_group: enums.GameGroup | str = enums.GameGroup.get_default(),
        *,
        language: enums.Language | str = enums.Language.get_default(),
    ) -> dict[enums.Game, mixins.GameTranslationsTableT]:
        game_group = enums.GameGroup(game_group)
        language = enums.Language(language)

        sort_key = max(x.sort_key(language, game_group) for x in self)
        return {
            x.game.identifier: x
            for x in self
            if x.sort_key(language, game_group) == sort_key
        }
