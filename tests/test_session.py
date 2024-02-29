from __future__ import annotations

from pokedex import pokedex, tables


def test_session() -> None:
    with pokedex.session() as session:
        pikachu = session.get(tables.PokemonSpecies, "pikachu")
        assert pikachu is not None
        assert pikachu.identifier == "pikachu"
        assert pikachu.order == 25


async def test_async_session() -> None:
    async with pokedex.async_session() as session:
        pikachu = await session.get(tables.PokemonSpecies, "pikachu")
        assert pikachu is not None
        assert pikachu.identifier == "pikachu"
        assert pikachu.order == 25
