from dataclasses import dataclass

from pokedex.entities.base import BaseEntity, Localized


@dataclass
class Type(BaseEntity):
    yaml_name = "types"

    names: Localized[str]
