import atexit
import importlib.metadata
import os
import shelve
import shutil
import tempfile
import unicodedata
from collections import defaultdict
from collections.abc import Collection, Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import cast

import yaml

from pokedex.cache.converter import converter
from pokedex.entities.base import BaseEntity, EntityMap, EntityRef
from pokedex.enums import Language


def _normalize_value(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = unicodedata.normalize("NFC", text)
    text = text.casefold().replace("♀", "f").replace("♂", "m").replace("œ", "oe")
    return "".join(c for c in text if unicodedata.category(c)[0] in ("L", "N"))


@dataclass
class CacheData[T: BaseEntity]:
    entity: type[T]
    shelf: shelve.Shelf[T]

    @cached_property
    def index(self) -> Mapping[str, Collection[tuple[Language, str]]]:
        return self.shelf["_index"]  # type: ignore[return-value]

    def __getitem__(self, key: str) -> T:
        return self.shelf[key]

    def search(self, name: str) -> Sequence[tuple[Language, EntityRef[T]]]:
        return [
            (language, EntityRef(self.entity, identifier))
            for language, identifier in self.index[_normalize_value(name)]
        ]

    def list_identifiers(self) -> Sequence[str]:
        return [x for x in self.shelf if not x.startswith("_")]


data: dict[type[BaseEntity], CacheData[BaseEntity]] = {}


def _build_shelf_index(
    structured_data: EntityMap[BaseEntity],
) -> Mapping[str, Collection[tuple[Language, str]]]:
    index = defaultdict(set)
    for identifier, entry in structured_data.items():
        assert hasattr(entry, "names")
        for language, name in entry.names.items():
            if isinstance(language, tuple):
                language = language[0]
            index[_normalize_value(name)].add((language, identifier))

    return index


def _build_shelf_if_required(entity: type["BaseEntity"], shelf_path: Path) -> None:
    version = importlib.metadata.version("pokedex")

    with suppress(Exception), shelve.open(shelf_path, "r") as db:
        if db["_version"] == version:
            return

    data = {}
    for file in BaseEntity.yaml_dir.glob(f"*/{entity.yaml_name}.yaml"):
        with file.open("r", encoding="utf-8") as f:
            data[file.parent.name] = yaml.safe_load(f)

    with shelve.open(shelf_path, "n") as db:
        structured_data = converter.structure(data, EntityMap[entity])  # type: ignore[valid-type]
        db.update(structured_data)
        index = _build_shelf_index(structured_data)
        db["_index"] = index
        db["_version"] = version


def load_all(cache_path: Path | None = None) -> None:
    if cache_path is None:
        if env_path := os.getenv("POKEDEX_DEFAULT_CACHE_PATH"):
            cache_path = Path(env_path)
        else:
            temp_dir = tempfile.mkdtemp()
            atexit.register(shutil.rmtree, temp_dir)
            cache_path = Path(temp_dir)

    for entity in BaseEntity.__subclasses__():
        shelf_path = cache_path / entity.yaml_name
        _build_shelf_if_required(entity, shelf_path)
        shelf = shelve.open(shelf_path, "r")  # noqa: SIM115
        atexit.register(shelf.close)
        data[entity] = CacheData(entity, shelf)


def get[T: BaseEntity](entity: type[T]) -> CacheData[T]:
    if entity not in data:
        load_all()
    return cast("CacheData[T]", data[entity])
