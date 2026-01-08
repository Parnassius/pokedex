from dataclasses import dataclass

from pokedex.entities.base import BaseEntity, Localized


@dataclass
class Move(BaseEntity):
    yaml_name = "moves"

    names: Localized[str]
    descriptions: Localized[str]
