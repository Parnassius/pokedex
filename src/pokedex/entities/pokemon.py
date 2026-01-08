from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from pokedex.entities.abilities import Ability
from pokedex.entities.base import (
    BaseEntity,
    EntityMap,
    EntityRef,
    GameLocalized,
    Localized,
    MaybeGameMapping,
    Multi,
    SubEntity,
)
from pokedex.entities.egg_groups import EggGroup
from pokedex.entities.items import Item
from pokedex.entities.types import Type
from pokedex.enums import HeldItemSlot, Stat


@dataclass
class PokemonForm(SubEntity):
    form_id: Multi[int]
    names: Localized[str]

    base_stats: Multi[Mapping[Stat, int]]
    evs_yield: Multi[Mapping[Stat, int]]

    types: Multi[Sequence[EntityRef[Type]]]
    egg_groups: Multi[Sequence[EntityRef[EggGroup]]]
    abilities: Multi[Sequence[EntityRef[Ability]]]
    hidden_ability: Multi[EntityRef[Ability]]

    held_items: Multi[Mapping[HeldItemSlot, MaybeGameMapping[EntityRef[Item]]]]

    descriptions: GameLocalized[str]


@dataclass
class PokemonGmaxForm(SubEntity):
    form_id: Multi[int]
    names: Localized[str]
    descriptions: GameLocalized[str]


@dataclass
class Pokemon(BaseEntity):
    yaml_name = "pokemon"

    species_id: Multi[int]
    names: Localized[str]
    forms: EntityMap[PokemonForm]
    gmax_forms: EntityMap[PokemonGmaxForm] = field(default_factory=EntityMap)
