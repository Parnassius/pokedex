from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from typing import Any, get_args, get_origin

from cattrs import BaseValidationError, Converter

from pokedex.entities.base import (
    BaseEntity,
    EntityMap,
    EntityRef,
    Localized,
    MaybeGameMapping,
    Multi,
    SimpleLocalized,
    SubEntity,
)
from pokedex.enums import Game, GameGroup, Language

converter = Converter()


@converter.register_structure_hook_factory(lambda tp: get_origin(tp) is Multi)  # type: ignore[comparison-overlap]
def _multi_hook_factory[T](
    tp: type[Multi[T]], conv: Converter
) -> Callable[[Any, type[Multi[T]]], Multi[T]]:
    key_arg = GameGroup
    value_arg = get_args(tp)[0]
    key_handler = conv.get_structure_hook(key_arg)
    value_handler = conv.get_structure_hook(value_arg)

    def hook(data: Any, tp: type[Multi[T]]) -> Multi[T]:
        return Multi(
            {
                key_handler(k, key_arg): value_handler(v, value_arg)
                for k, v in data.items()
            }
        )

    return hook


@converter.register_structure_hook_factory(
    lambda tp: get_origin(tp) is SimpleLocalized  # type: ignore[comparison-overlap]
)
def _simple_localized_hook_factory[T](
    tp: type[SimpleLocalized[T]], conv: Converter
) -> Callable[[Any, type[SimpleLocalized[T]]], SimpleLocalized[T]]:
    key_arg = Language
    value_arg = get_args(tp)[0]
    key_handler = conv.get_structure_hook(key_arg)
    value_handler = conv.get_structure_hook(value_arg)

    def hook(data: Any, tp: type[SimpleLocalized[T]]) -> SimpleLocalized[T]:
        out = {}
        for game_group, subdata in data.items():
            if game_group != "common":
                msg = f"Unexpected value '{game_group}'"
                raise ValueError(msg)
            out.update(subdata)

        return SimpleLocalized(
            {
                key_handler(k, key_arg): value_handler(v, value_arg)
                for k, v in out.items()
            }
        )

    return hook


@converter.register_structure_hook_factory(
    lambda tp: get_origin(tp) is Localized  # type: ignore[comparison-overlap]
)
def _localized_hook_factory[T](
    tp: type[Localized[T]], conv: Converter
) -> Callable[[Any, type[Localized[T]]], Localized[T]]:
    key_arg = tuple[Language, GameGroup]
    value_arg = get_args(tp)[0]
    key_handler = conv.get_structure_hook(key_arg)
    value_handler = conv.get_structure_hook(value_arg)

    def hook(data: Any, tp: type[Localized[T]]) -> Localized[T]:
        out = {
            (language, game_group): value
            for game_group, subdata in data.items()
            for language, value in subdata.items()
        }

        return Localized(
            {
                key_handler(k, key_arg): value_handler(v, value_arg)
                for k, v in out.items()
            }
        )

    return hook


@converter.register_structure_hook_factory(
    lambda tp: get_origin(tp) is MaybeGameMapping  # type: ignore[comparison-overlap]
)
def _maybe_game_mapping_hook_factory[T](
    tp: type[MaybeGameMapping[T]], conv: Converter
) -> Callable[[Any, type[MaybeGameMapping[T]]], MaybeGameMapping[T]]:
    key_arg = Game
    value_arg = get_args(tp)[0]
    key_handler = conv.get_structure_hook(key_arg)
    value_handler = conv.get_structure_hook(value_arg)

    def hook(data: Any, tp: type[MaybeGameMapping[T]]) -> MaybeGameMapping[T]:
        if isinstance(data, dict):
            with suppress(BaseValidationError):
                return {
                    key_handler(k, key_arg): value_handler(v, value_arg)
                    for k, v in data.items()
                }

        return value_handler(data, value_arg)  # type: ignore[no-any-return]

    return hook


@converter.register_structure_hook_factory(lambda tp: get_origin(tp) is EntityRef)  # type: ignore[comparison-overlap]
def _entity_ref_hook_factory[T: BaseEntity](
    tp: type[EntityRef[T]], conv: Converter
) -> Callable[[Any, type[EntityRef[T]]], EntityRef[T]]:
    entity = get_args(tp)[0]
    handler = conv.get_structure_hook(str)

    def hook(data: Any, tp: type[EntityRef[T]]) -> EntityRef[T]:
        return EntityRef(entity, handler(data, str))

    return hook


@converter.register_structure_hook_factory(lambda tp: get_origin(tp) is EntityMap)  # type: ignore[comparison-overlap]
def _entity_map_hook_factory[T: BaseEntity | SubEntity](
    tp: type[EntityMap[T]], conv: Converter
) -> Callable[[Any, type[EntityMap[T]]], EntityMap[T]]:
    key_arg = str
    value_arg = get_args(tp)[0]
    key_handler = conv.get_structure_hook(key_arg)
    value_handler = conv.get_structure_hook(value_arg)

    def hook(data: Any, tp: type[EntityMap[T]]) -> EntityMap[T]:
        raw_data = defaultdict[str, dict[str, dict[str, Any]]](
            lambda: defaultdict(dict)
        )
        for game, game_data in data.items():
            for identifier, entity_data in game_data.items():
                raw_data[identifier]["identifier"] = identifier
                for key, value in entity_data.items():
                    raw_data[identifier][key][game] = value

        return EntityMap(
            {
                key_handler(k, key_arg): value_handler(v, value_arg)
                for k, v in raw_data.items()
            }
        )

    return hook
