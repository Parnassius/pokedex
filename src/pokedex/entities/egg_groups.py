from dataclasses import dataclass

from pokedex.entities.base import BaseEntity, SimpleLocalized


@dataclass
class EggGroup(BaseEntity):
    yaml_name = "egg_groups"

    names: SimpleLocalized[str]
