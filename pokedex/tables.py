from __future__ import annotations

from collections.abc import Collection
from typing import Annotated, ClassVar

from sqlalchemy import CheckConstraint, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    attribute_keyed_dict,
    mapped_column,
    relationship,
)

from pokedex import enums, mixins

intpk = Annotated[int, mapped_column(primary_key=True)]
strpk = Annotated[str, mapped_column(primary_key=True)]


# Note: some annotations ignore UP037 (quotes in type annotation) because sqlalchemy
# doesn't handle forward references in `Mapped` if the annotation contains a nested
# generic (for example `dict[tuple[enums.Language, enums.Game], "PokemonFlavorText"]`).
# https://github.com/sqlalchemy/sqlalchemy/blob/b304ef2808ba30ce9f7f250830a670be7f3058f5/lib/sqlalchemy/orm/util.py#L2282-L2307


class Base(DeclarativeBase):
    type_annotation_map: ClassVar = {
        enums.OrderedEnum: Enum(
            enums.OrderedEnum, values_callable=lambda x: [i.sql_value for i in x]
        ),
    }


class Ability(Base):
    __tablename__ = "abilities"

    identifier: Mapped[strpk]

    name_associations: Mapped[dict[enums.Language, AbilityName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )

    pokemon: Mapped[list[Pokemon]] = relationship(
        secondary="pokemon_abilities", viewonly=True
    )


class AbilityName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "ability_names"

    ability_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("abilities.identifier")
    )

    ability: Mapped[Ability] = relationship(viewonly=True)


class AbilityNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "ability_name_changes"

    ability_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("abilities.identifier")
    )

    ability: Mapped[Ability] = relationship(viewonly=True)


class EggGroup(Base):
    __tablename__ = "egg_groups"

    identifier: Mapped[strpk]

    name_associations: Mapped[dict[enums.Language, EggGroupName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )

    pokemon: Mapped[list[Pokemon]] = relationship(
        secondary="pokemon_egg_groups", viewonly=True
    )


class EggGroupName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "egg_group_names"

    egg_group_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("egg_groups.identifier")
    )

    egg_group: Mapped[EggGroup] = relationship(viewonly=True)


class Item(Base):
    __tablename__ = "items"

    identifier: Mapped[strpk]

    name_associations: Mapped[dict[enums.Language, ItemName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )

    pokemon_wild_held_game_group: Mapped[list[Pokemon]] = relationship(
        secondary="pokemon_wild_held_items_game", viewonly=True
    )
    pokemon_wild_held_game: Mapped[list[Pokemon]] = relationship(
        secondary="pokemon_wild_held_items_game", viewonly=True
    )

    @property
    def pokemon_wild_held(self) -> Collection[Pokemon]:
        return {*self.pokemon_wild_held_game_group, *self.pokemon_wild_held_game}


class ItemName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "item_names"

    item_identifier: Mapped[strpk] = mapped_column(ForeignKey("items.identifier"))

    item: Mapped[Item] = relationship(viewonly=True)


class ItemNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "item_name_changes"

    item_identifier: Mapped[strpk] = mapped_column(ForeignKey("items.identifier"))

    item: Mapped[Item] = relationship(viewonly=True)


class Move(Base):
    __tablename__ = "moves"

    identifier: Mapped[strpk]

    name_associations: Mapped[dict[enums.Language, MoveName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )


class MoveName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "move_names"

    move_identifier: Mapped[strpk] = mapped_column(ForeignKey("moves.identifier"))

    move: Mapped[Move] = relationship(viewonly=True)


class MoveNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "move_name_changes"

    move_identifier: Mapped[strpk] = mapped_column(ForeignKey("moves.identifier"))

    move: Mapped[Move] = relationship(viewonly=True)


class Nature(Base):
    __tablename__ = "natures"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    name_associations: Mapped[dict[enums.Language, NatureName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )


class NatureName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "nature_names"

    nature_identifier: Mapped[strpk] = mapped_column(ForeignKey("natures.identifier"))

    nature: Mapped[Nature] = relationship(viewonly=True)


class NatureNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "nature_name_changes"

    nature_identifier: Mapped[strpk] = mapped_column(ForeignKey("natures.identifier"))

    nature: Mapped[Nature] = relationship(viewonly=True)


class Pokemon(Base):
    __tablename__ = "pokemon"

    identifier: Mapped[strpk]
    pokemon_species_identifier: Mapped[str] = mapped_column(
        ForeignKey("pokemon_species.identifier")
    )
    form_order: Mapped[int]

    pokemon_species: Mapped[PokemonSpecies] = relationship(viewonly=True)

    form_name_associations: Mapped[dict[enums.Language, PokemonFormName]] = (
        relationship(collection_class=attribute_keyed_dict("language"), viewonly=True)
    )
    form_names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "form_name_associations", "name"
    )

    flavor_text_associations: Mapped[
        dict[tuple[enums.Language, enums.Game], "PokemonFlavorText"]  # noqa: UP037
    ] = relationship(
        collection_class=attribute_keyed_dict("key_identifier"), viewonly=True
    )
    flavor_text: AssociationProxy[dict[tuple[enums.Language, enums.Game], str]] = (
        association_proxy("flavor_text_associations", "flavor_text")
    )

    ability_associations: Mapped[dict[enums.AbilitySlot, PokemonAbility]] = (
        relationship(collection_class=attribute_keyed_dict("slot"), viewonly=True)
    )
    abilities: AssociationProxy[dict[enums.AbilitySlot, Ability]] = association_proxy(
        "ability_associations", "ability"
    )

    egg_groups: Mapped[list[EggGroup]] = relationship(
        secondary="pokemon_egg_groups", order_by="PokemonEggGroup.slot", viewonly=True
    )

    ev_yield_associations: Mapped[dict[Stat, PokemonEvYield]] = relationship(
        collection_class=attribute_keyed_dict("stat"), viewonly=True
    )
    evs_yield: AssociationProxy[dict[Stat, int]] = association_proxy(
        "ev_yield_associations", "value"
    )

    stat_associations: Mapped[dict[Stat, PokemonStat]] = relationship(
        collection_class=attribute_keyed_dict("stat"), viewonly=True
    )
    stats: AssociationProxy[dict[Stat, int]] = association_proxy(
        "stat_associations", "value"
    )

    types: Mapped[list[Type]] = relationship(
        secondary="pokemon_types", order_by="PokemonType.slot", viewonly=True
    )

    wild_held_item_game_group_associations: Mapped[
        dict[
            tuple[enums.GameGroup, enums.HeldItemSlot],
            "PokemonWildHeldItemGameGroup",  # noqa: UP037
        ]
    ] = relationship(
        collection_class=attribute_keyed_dict("key_identifier"), viewonly=True
    )
    wild_held_items_game_group: AssociationProxy[
        dict[tuple[enums.GameGroup, enums.HeldItemSlot], Item]
    ] = association_proxy("wild_held_item_game_group_associations", "item")

    wild_held_item_game_associations: Mapped[
        dict[
            tuple[enums.Game, enums.HeldItemSlot],
            "PokemonWildHeldItemGame",  # noqa: UP037
        ]
    ] = relationship(
        collection_class=attribute_keyed_dict("key_identifier"), viewonly=True
    )
    wild_held_items_game: AssociationProxy[
        dict[tuple[enums.Game, enums.HeldItemSlot], Item]
    ] = association_proxy("wild_held_item_game_associations", "item")

    __table_args__ = (
        UniqueConstraint("pokemon_species_identifier", "form_order", name="order"),
    )


class PokemonAbility(Base):
    __tablename__ = "pokemon_abilities"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[enums.AbilitySlot] = mapped_column(primary_key=True)
    ability_identifier: Mapped[str] = mapped_column(ForeignKey("abilities.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    ability: Mapped[Ability] = relationship(viewonly=True)


class PokemonAbilityChange(mixins.ChangesTable, Base):
    __tablename__ = "pokemon_ability_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[enums.AbilitySlot] = mapped_column(primary_key=True)
    ability_identifier: Mapped[str] = mapped_column(ForeignKey("abilities.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
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


class PokemonFlavorText(mixins.GameCollectionTable, mixins.TranslationsTable, Base):
    __tablename__ = "pokemon_flavor_text"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    flavor_text: Mapped[str]

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)

    @property
    def key_identifier(self) -> tuple[enums.Language, enums.Game]:
        return self.language, self.game


class PokemonFlavorTextChange(
    mixins.GameCollectionTable, mixins.TranslationsTable, Base
):
    __tablename__ = "pokemon_flavor_text_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    game_revision_from: Mapped[strpk]
    game_revision_to: Mapped[strpk]
    flavor_text: Mapped[str]

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonFormName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "pokemon_form_names"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonFormNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "pokemon_form_name_changes"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)


class PokemonSpecies(Base):
    __tablename__ = "pokemon_species"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    pokemon: Mapped[list[Pokemon]] = relationship(
        order_by="Pokemon.form_order", viewonly=True
    )

    name_associations: Mapped[dict[enums.Language, PokemonSpeciesName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )


class PokemonSpeciesName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "pokemon_species_names"

    pokemon_species_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("pokemon_species.identifier")
    )

    pokemon_species: Mapped[PokemonSpecies] = relationship(viewonly=True)


class PokemonSpeciesNameChange(
    mixins.ChangesTable, mixins.NamesTranslationsTable, Base
):
    __tablename__ = "pokemon_species_name_changes"

    pokemon_species_identifier: Mapped[strpk] = mapped_column(
        ForeignKey("pokemon_species.identifier")
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


class PokemonWildHeldItemGame(mixins.GameCollectionTable, Base):
    __tablename__ = "pokemon_wild_held_items_game"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[enums.HeldItemSlot] = mapped_column(primary_key=True)
    item_identifier: Mapped[str] = mapped_column(ForeignKey("items.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    item: Mapped[Item] = relationship(viewonly=True)

    @property
    def key_identifier(self) -> tuple[enums.Game, enums.HeldItemSlot]:
        return self.game, self.slot


class PokemonWildHeldItemGameGroup(mixins.GameGroupCollectionTable, Base):
    __tablename__ = "pokemon_wild_held_items_game_group"

    pokemon_identifier: Mapped[strpk] = mapped_column(ForeignKey("pokemon.identifier"))
    slot: Mapped[enums.HeldItemSlot] = mapped_column(primary_key=True)
    item_identifier: Mapped[str] = mapped_column(ForeignKey("items.identifier"))

    pokemon: Mapped[Pokemon] = relationship(viewonly=True)
    item: Mapped[Item] = relationship(viewonly=True)

    @property
    def key_identifier(self) -> tuple[enums.GameGroup, enums.HeldItemSlot]:
        return self.game_group, self.slot


class Stat(Base):
    __tablename__ = "stats"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    name_associations: Mapped[dict[enums.Language, StatName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )


class StatName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "stat_names"

    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))

    stat: Mapped[Stat] = relationship(viewonly=True)


class StatNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "stat_name_changes"

    stat_identifier: Mapped[strpk] = mapped_column(ForeignKey("stats.identifier"))

    stat: Mapped[Stat] = relationship(viewonly=True)


class Type(Base):
    __tablename__ = "types"

    identifier: Mapped[strpk]
    order: Mapped[int] = mapped_column(index=True, unique=True)

    name_associations: Mapped[dict[enums.Language, TypeName]] = relationship(
        collection_class=attribute_keyed_dict("language"), viewonly=True
    )
    names: AssociationProxy[dict[enums.Language, str]] = association_proxy(
        "name_associations", "name"
    )

    pokemon: Mapped[list[Pokemon]] = relationship(
        secondary="pokemon_types", viewonly=True
    )


class TypeName(mixins.NamesTranslationsTable, Base):
    __tablename__ = "type_names"

    type_identifier: Mapped[strpk] = mapped_column(ForeignKey("types.identifier"))

    type: Mapped[Type] = relationship(viewonly=True)


class TypeNameChange(mixins.ChangesTable, mixins.NamesTranslationsTable, Base):
    __tablename__ = "type_name_changes"

    type_identifier: Mapped[strpk] = mapped_column(ForeignKey("types.identifier"))

    type: Mapped[Type] = relationship(viewonly=True)
