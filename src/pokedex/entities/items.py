from dataclasses import dataclass

from pokedex.entities.base import BaseEntity, Localized


@dataclass
class Item(BaseEntity):
    yaml_name = "items"

    names: Localized[str]
    descriptions: Localized[str] | None = None
