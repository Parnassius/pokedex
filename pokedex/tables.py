from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable
from typing import Annotated

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from pokedex import collections, enums, mixins

NORMALIZED_VALUE_RE = (
    r"["
    r"a-z0-9"
    r"\u3040-\u309F"  # hiragana
    r"\u30A0-\u30FF"  # katakana
    r"\u4E00-\u9FFF"  # cjk unified ideographs
    r"\uAC00-\uD7AF"  # hangul syllables
    r"]*"
)
OTHER_NORMALIZED_CHARACTERS = {
    "œ": "oe",
}


def normalize_value(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = unicodedata.normalize("NFC", text)
    text = text.replace("♀", "f").replace("♂", "m")
    text = "".join(c for c in text if unicodedata.category(c)[0] in ("L", "N"))
    text = text.casefold()
    return "".join(OTHER_NORMALIZED_CHARACTERS.get(c, c) for c in text)


def _normalized_value(field: str) -> Callable[[DefaultExecutionContext], str]:
    def inner(context: DefaultExecutionContext) -> str:
        text = context.get_current_parameters()[field]  # type: ignore[no-untyped-call]
        assert isinstance(text, str)
        text = normalize_value(text)
        assert re.fullmatch(NORMALIZED_VALUE_RE, text), text
        return text

    return inner


intpk = Annotated[int, mapped_column(primary_key=True)]
strpk = Annotated[str, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class Ability(Base):
    __tablename__ = "abilities"

    identifier: Mapped[strpk]

    names: Mapped[collections.TranslationsCollection[AbilityName]] = relationship(
        viewonly=True
    )

    pokemon: Mapped[list[PokemonAbility]] = relationship(viewonly=True)


class AbilityName(mixins.TranslationsTable, Base):
    __tablename__ = "ability_names"

    ability_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("abilities.identifier")
    )
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    ability: Mapped[Ability] = relationship(viewonly=True)


class AbilityNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "ability_name_changes"

    ability_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("abilities.identifier")
    )
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    ability: Mapped[Ability] = relationship(viewonly=True)


class AbilitySlot(Base):
    __tablename__ = "ability_slots"

    identifier: Mapped[enums.AbilitySlot] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(index=True, unique=True)


class EggGroup(Base):
    __tablename__ = "egg_groups"

    identifier: Mapped[strpk]

    names: Mapped[collections.TranslationsCollection[EggGroupName]] = relationship(
        viewonly=True
    )

    pokemon: Mapped[list[PokemonEggGroup]] = relationship(viewonly=True)


class EggGroupName(mixins.TranslationsTable, Base):
    __tablename__ = "egg_group_names"

    egg_group_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("egg_groups.identifier")
    )
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    egg_group: Mapped[EggGroup] = relationship(viewonly=True)


class Game(Base):
    __tablename__ = "games"

    identifier: Mapped[enums.Game] = mapped_column(primary_key=True)
    game_group_identifier: Mapped[enums.GameGroup] = mapped_column(
        ForeignKey("game_groups.identifier")
    )
    order: Mapped[int] = mapped_column(index=True, unique=True)

    game_group: Mapped[GameGroup] = relationship(viewonly=True)


class GameGroup(Base):
    __tablename__ = "game_groups"

    identifier: Mapped[enums.GameGroup] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(index=True, unique=True)

    games: Mapped[list[Game]] = relationship(order_by="Game.order", viewonly=True)


class HeldItemSlot(Base):
    __tablename__ = "held_item_slots"

    identifier: Mapped[enums.HeldItemSlot] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(index=True, unique=True)


class Item(Base):
    __tablename__ = "items"

    identifier: Mapped[strpk]

    names: Mapped[collections.TranslationsCollection[ItemName]] = relationship(
        viewonly=True
    )

    pokemon_wild_held_game_group: Mapped[
        collections.GameGroupMappingCollection[
            PokemonWildHeldItemGameGroup, enums.HeldItemSlot
        ]
    ] = relationship(viewonly=True)
    pokemon_wild_held_game: Mapped[
        collections.GameMappingCollection[PokemonWildHeldItemGame, enums.HeldItemSlot]
    ] = relationship(viewonly=True)

    @property
    def pokemon_wild_held(
        self,
    ) -> collections.GameGroupOrGameMappingCollection[
        PokemonWildHeldItemGameGroup, PokemonWildHeldItemGame, enums.HeldItemSlot
    ]:
        return collections.GameGroupOrGameMappingCollection(
            self.pokemon_wild_held_game_group, self.pokemon_wild_held_game
        )


class ItemName(mixins.TranslationsTable, Base):
    __tablename__ = "item_names"

    item_identifier: Mapped[strpk] = mapped_column(ForeignKey("items.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    item: Mapped[Item] = relationship(viewonly=True)


class ItemNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "item_name_changes"

    item_identifier: Mapped[strpk] = mapped_column(ForeignKey("items.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    item: Mapped[Item] = relationship(viewonly=True)


class Language(Base):
    __tablename__ = "languages"

    identifier: Mapped[enums.Language] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(index=True, unique=True)


class Move(Base):
    __tablename__ = "moves"

    identifier: Mapped[strpk]

    names: Mapped[collections.TranslationsCollection[MoveName]] = relationship(
        viewonly=True
    )


class MoveName(mixins.TranslationsTable, Base):
    __tablename__ = "move_names"

    move_identifier: Mapped[strpk] = mapped_column(ForeignKey("moves.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    move: Mapped[Move] = relationship(viewonly=True)


class MoveNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "move_name_changes"

    move_identifier: Mapped[strpk] = mapped_column(ForeignKey("moves.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    move: Mapped[Move] = relationship(viewonly=True)


class Nature(Base):
    __tablename__ = "natures"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    names: Mapped[collections.TranslationsCollection[NatureName]] = relationship(
        viewonly=True
    )


class NatureName(mixins.TranslationsTable, Base):
    __tablename__ = "nature_names"

    nature_identifier: Mapped[strpk] = mapped_column(ForeignKey("natures.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    nature: Mapped[Nature] = relationship(viewonly=True)


class NatureNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "nature_name_changes"

    nature_identifier: Mapped[strpk] = mapped_column(ForeignKey("natures.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    nature: Mapped[Nature] = relationship(viewonly=True)


class Pokemon(Base):
    __tablename__ = "pokemon"

    identifier: Mapped[strpk]
    pokemon_species_identifier: Mapped[str] = mapped_column(
        ForeignKey("pokemon_species.identifier")
    )
    form_order: Mapped[int]

    pokemon_species: Mapped[PokemonSpecies] = relationship(viewonly=True)

    form_names: Mapped[collections.TranslationsCollection[PokemonFormName]] = (
        relationship(viewonly=True)
    )
    abilities: Mapped[list[PokemonAbility]] = relationship(viewonly=True)
    egg_groups: Mapped[list[PokemonEggGroup]] = relationship(
        order_by="PokemonEggGroup.slot", viewonly=True
    )
    flavor_text: Mapped[collections.GameTranslationsCollection[PokemonFlavorText]] = (
        relationship(viewonly=True)
    )
    stats: Mapped[list[PokemonStat]] = relationship(viewonly=True)
    evs_yield: Mapped[list[PokemonEvYield]] = relationship(viewonly=True)
    types: Mapped[list[PokemonType]] = relationship(
        order_by="PokemonType.slot", viewonly=True
    )
    wild_held_items_game_group: Mapped[
        collections.GameGroupMappingCollection[
            PokemonWildHeldItemGameGroup, enums.HeldItemSlot
        ]
    ] = relationship(viewonly=True)
    wild_held_items_game: Mapped[
        collections.GameMappingCollection[PokemonWildHeldItemGame, enums.HeldItemSlot]
    ] = relationship(viewonly=True)

    @property
    def wild_held_items(
        self,
    ) -> collections.GameGroupOrGameMappingCollection[
        PokemonWildHeldItemGameGroup, PokemonWildHeldItemGame, enums.HeldItemSlot
    ]:
        return collections.GameGroupOrGameMappingCollection(
            self.wild_held_items_game_group, self.wild_held_items_game
        )

    __table_args__ = (
        UniqueConstraint("pokemon_species_identifier", "form_order", name="order"),
    )


class PokemonAbility(Base):
    __tablename__ = "pokemon_abilities"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot_identifier: Mapped[enums.AbilitySlot] = mapped_column(
        ForeignKey("ability_slots.identifier"), primary_key=True
    )
    ability_identifier: Mapped[str] = mapped_column(ForeignKey("abilities.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    slot: Mapped[AbilitySlot] = relationship(viewonly=True)
    ability: Mapped[Ability] = relationship(viewonly=True)


class PokemonAbilityChange(mixins.ChangesTable, Base):
    __tablename__ = "pokemon_ability_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot_identifier: Mapped[enums.AbilitySlot] = mapped_column(
        ForeignKey("ability_slots.identifier"), primary_key=True
    )
    ability_identifier: Mapped[str] = mapped_column(ForeignKey("abilities.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    slot: Mapped[AbilitySlot] = relationship(viewonly=True)
    ability: Mapped[Ability] = relationship(viewonly=True)


class PokemonEggGroup(Base):
    __tablename__ = "pokemon_egg_groups"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[intpk] = mapped_column(CheckConstraint("slot IN (1, 2)"))
    egg_group_identifier: Mapped[str] = mapped_column(
        ForeignKey("egg_groups.identifier")
    )

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    egg_group: Mapped[EggGroup] = relationship(viewonly=True)


class PokemonEggGroupChange(mixins.ChangesTable, Base):
    __tablename__ = "pokemon_egg_group_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[intpk] = mapped_column(CheckConstraint("slot IN (1, 2)"))
    egg_group_identifier: Mapped[str] = mapped_column(
        ForeignKey("egg_groups.identifier")
    )

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    egg_group: Mapped[EggGroup] = relationship(viewonly=True)


class PokemonEvYield(Base):
    __tablename__ = "pokemon_evs_yield"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))
    value: Mapped[int] = mapped_column(CheckConstraint("value BETWEEN 0 AND 3"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    stat: Mapped[Stat] = relationship(viewonly=True)


class PokemonEvYieldChange(mixins.ChangesTable, Base):
    __tablename__ = "pokemon_ev_yield_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))
    value: Mapped[int] = mapped_column(CheckConstraint("value BETWEEN 0 AND 3"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    stat: Mapped[Stat] = relationship(viewonly=True)


class PokemonFlavorText(mixins.GameTranslationsTable, Base):
    __tablename__ = "pokemon_flavor_text"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    flavor_text: Mapped[str]

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonFlavorTextChange(mixins.GameTranslationChangesTable, Base):
    __tablename__ = "pokemon_flavor_text_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    flavor_text: Mapped[str]

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonFormName(mixins.TranslationsTable, Base):
    __tablename__ = "pokemon_form_names"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonFormNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "pokemon_form_name_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonSpecies(Base):
    __tablename__ = "pokemon_species"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    pokemon: Mapped[list[Pokemon]] = relationship(
        order_by="Pokemon.form_order", viewonly=True
    )

    names: Mapped[collections.TranslationsCollection[PokemonSpeciesName]] = (
        relationship(viewonly=True)
    )


class PokemonSpeciesName(mixins.TranslationsTable, Base):
    __tablename__ = "pokemon_species_names"

    pokemon_species_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("pokemon_species.identifier")
    )
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    pokemon_species: Mapped[PokemonSpecies] = relationship(viewonly=True)


class PokemonSpeciesNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "pokemon_species_name_changes"

    pokemon_species_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("pokemon_species.identifier")
    )
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    pokemon_species: Mapped[PokemonSpecies] = relationship(viewonly=True)


class PokemonStat(Base):
    __tablename__ = "pokemon_stats"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))
    value: Mapped[int] = mapped_column(CheckConstraint("value BETWEEN 1 AND 255"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    stat: Mapped[Stat] = relationship(viewonly=True)


class PokemonStatChange(mixins.ChangesTable, Base):
    __tablename__ = "pokemon_stat_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))
    value: Mapped[int] = mapped_column(CheckConstraint("value BETWEEN 1 AND 255"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    stat: Mapped[Stat] = relationship(viewonly=True)


class PokemonType(Base):
    __tablename__ = "pokemon_types"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[intpk] = mapped_column(CheckConstraint("slot IN (1, 2)"))
    type_identifier: Mapped[str] = mapped_column(ForeignKey("types.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    type: Mapped[Type] = relationship(viewonly=True)


class PokemonTypeChange(mixins.ChangesTable, Base):
    __tablename__ = "pokemon_type_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[intpk] = mapped_column(CheckConstraint("slot IN (1, 2)"))
    type_identifier: Mapped[str] = mapped_column(ForeignKey("types.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    type: Mapped[Type] = relationship(viewonly=True)


class PokemonWildHeldItemGame(mixins.GameMappingTable, Base):
    __tablename__ = "pokemon_wild_held_items_game"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot_identifier: Mapped[enums.HeldItemSlot] = mapped_column(
        ForeignKey("held_item_slots.identifier"), primary_key=True
    )
    item_identifier: Mapped[strpk] = mapped_column(ForeignKey("items.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    slot: Mapped[HeldItemSlot] = relationship(viewonly=True)
    item: Mapped[Item] = relationship(viewonly=True)

    @property
    def mapping_key(self) -> enums.HeldItemSlot:
        return self.slot_identifier


class PokemonWildHeldItemGameGroup(mixins.GameGroupMappingTable, Base):
    __tablename__ = "pokemon_wild_held_items_game_group"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot_identifier: Mapped[enums.HeldItemSlot] = mapped_column(
        ForeignKey("held_item_slots.identifier"), primary_key=True
    )
    item_identifier: Mapped[strpk] = mapped_column(ForeignKey("items.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    slot: Mapped[HeldItemSlot] = relationship(viewonly=True)
    item: Mapped[Item] = relationship(viewonly=True)

    @property
    def mapping_key(self) -> enums.HeldItemSlot:
        return self.slot_identifier


class Stat(Base):
    __tablename__ = "stats"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    names: Mapped[collections.TranslationsCollection[StatName]] = relationship(
        viewonly=True
    )


class StatName(mixins.TranslationsTable, Base):
    __tablename__ = "stat_names"

    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    stat: Mapped[Stat] = relationship(viewonly=True)


class StatNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "stat_name_changes"

    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    stat: Mapped[Stat] = relationship(viewonly=True)


class Type(Base):
    __tablename__ = "types"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    names: Mapped[collections.TranslationsCollection[TypeName]] = relationship(
        viewonly=True
    )

    pokemon: Mapped[list[PokemonType]] = relationship(viewonly=True)


class TypeName(mixins.TranslationsTable, Base):
    __tablename__ = "type_names"

    type_identifier: Mapped[strpk] = mapped_column(ForeignKey("types.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    type: Mapped[Type] = relationship(viewonly=True)


class TypeNameChange(mixins.TranslationChangesTable, Base):
    __tablename__ = "type_name_changes"

    type_identifier: Mapped[strpk] = mapped_column(ForeignKey("types.identifier"))
    name: Mapped[str]
    normalized_name: Mapped[str] = mapped_column(
        index=True, default=_normalized_value("name")
    )

    type: Mapped[Type] = relationship(viewonly=True)
