from dataclasses import dataclass

from pokedex.entities.base import BaseEntity, Localized


@dataclass
class Nature(BaseEntity):
    yaml_name = "natures"

    names: Localized[str]
