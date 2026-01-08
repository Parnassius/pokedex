from dataclasses import dataclass

from pokedex.entities.base import BaseEntity, Localized


@dataclass
class Ability(BaseEntity):
    yaml_name = "abilities"

    names: Localized[str]
    descriptions: Localized[str]
