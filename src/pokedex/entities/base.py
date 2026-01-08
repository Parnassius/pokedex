from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Self, overload

from pokedex import cache
from pokedex.context import context_game_group, context_language
from pokedex.enums import Game, GameGroup, Language


class _BaseMulti[K, V](Mapping[K, V]):
    def __init__(self, data: Mapping[K, V]) -> None:
        self._data = dict(data)

    def __repr__(self) -> str:
        cls = type(self)
        return f"{cls.__module__}.{cls.__qualname__}({self._data!r})"

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    @property
    def _default_keys(self) -> Iterable[K]:
        raise NotImplementedError

    @overload
    def get(self, key: K | None = None, /) -> V | None: ...

    @overload
    def get(self, key: K | None, default: V, /) -> V: ...

    @overload
    def get[T](self, key: K | None, default: T, /) -> V | T: ...

    def get[T](
        self, key: K | None = None, default: V | T | None = None, /
    ) -> V | T | None:
        if key is not None:
            return self._data.get(key, default)

        for key in self._default_keys:
            with suppress(KeyError):
                return self._data[key]

        return default

    def single(self) -> V:
        if not self:
            msg = "The mapping is empty."
            raise ValueError(msg)

        values = iter(self.values())
        first = next(values)
        if all(x == first for x in values):
            return first

        msg = "Not all values are the same."
        raise ValueError(msg)

    def group(self) -> list[tuple[set[K], V]]:
        groups: list[tuple[set[K], V]] = []
        for key, val in self.items():
            group_key = next((k for k, v in groups if v == val), None)
            if group_key:
                group_key.add(key)
            else:
                groups.append(({key}, val))
        return groups


class Multi[V](_BaseMulti[GameGroup, V]):
    @property
    def _default_keys(self) -> Iterable[GameGroup]:
        yield from context_game_group.get().sorted_with_default


class SimpleLocalized[V](_BaseMulti[Language, V]):
    @property
    def _default_keys(self) -> Iterable[Language]:
        yield context_language.get()


class Localized[V](_BaseMulti[tuple[Language, GameGroup], V]):
    @property
    def _default_keys(self) -> Iterable[tuple[Language, GameGroup]]:
        language = context_language.get()
        game_group = context_game_group.get()
        yield from ((language, x) for x in game_group.sorted_with_default)

    @overload
    def get(
        self, key: tuple[Language, GameGroup] | Language | GameGroup | None = None, /
    ) -> V | None: ...

    @overload
    def get(
        self,
        key: tuple[Language, GameGroup] | Language | GameGroup | None,
        default: V,
        /,
    ) -> V: ...

    @overload
    def get[T](
        self,
        key: tuple[Language, GameGroup] | Language | GameGroup | None,
        default: T,
        /,
    ) -> V | T: ...

    def get[T](
        self,
        key: tuple[Language, GameGroup] | Language | GameGroup | None = None,
        default: V | T | None = None,
        /,
    ) -> V | T | None:
        keys: Iterable[tuple[Language, GameGroup]]
        if isinstance(key, tuple):
            keys = [key]
        elif isinstance(key, Language):
            keys = [(key, x) for x in context_game_group.get().sorted_with_default]
        elif isinstance(key, GameGroup):
            keys = [(context_language.get(), key)]
        else:
            keys = self._default_keys

        for key in keys:
            with suppress(KeyError):
                return self._data[key]

        return default

    def with_language(self, key: Language | None = None) -> Multi[V]:
        if key is None:
            key = context_language.get()
        return Multi(
            {
                game_group: value
                for (language, game_group), value in self._data.items()
                if language is key
            }
        )

    def with_game_group(self, key: GameGroup | None = None) -> SimpleLocalized[V]:
        if key is None:
            key = context_game_group.get()
        return SimpleLocalized(
            {
                language: value
                for (language, game_group), value in self._data.items()
                if game_group is key
            }
        )


type GameLocalized[V] = Localized[Mapping[Game, V]]


type MaybeGameMapping[T] = T | Mapping[Game, T]


class EntityRef[T: "BaseEntity"]:
    def __init__(self, entity: type[T], identifier: str) -> None:
        self.entity = entity
        self.identifier = identifier

    def __repr__(self) -> str:
        cls = type(self)
        ent = self.entity
        return (
            f"{cls.__module__}.{cls.__qualname__}"
            f"({ent.__module__}.{ent.__qualname__}, {self.identifier!r})"
        )

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, EntityRef):
            return (self.entity, self.identifier) == (other.entity, other.identifier)
        return NotImplemented

    def get(self) -> T:
        return self.entity.get(self.identifier)


@dataclass
class BaseEntity:
    identifier: str

    yaml_dir: ClassVar = Path(__file__).parent.parent / "data"
    yaml_name: ClassVar[str]

    @classmethod
    def get(cls, identifier: str) -> Self:
        return cache.get(cls)[identifier]

    @classmethod
    def search(cls, name: str) -> Sequence[tuple[Language, EntityRef[Self]]]:
        return cache.get(cls).search(name)

    @classmethod
    def list_identifiers(cls) -> Sequence[str]:
        return cache.get(cls).list_identifiers()


@dataclass
class SubEntity:
    identifier: str


class EntityMap[T: "BaseEntity | SubEntity"](Mapping[str, T]):
    def __init__(self, data: Mapping[str, T] | None = None) -> None:
        self._data = dict(data or {})

    def __getitem__(self, key: str) -> T:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)
