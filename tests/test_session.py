from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from pokedex import tables


def test_session(session: Session) -> None:
    pikachu = session.get(tables.PokemonSpecies, "pikachu")
    assert pikachu is not None
    assert pikachu.identifier == "pikachu"
    assert pikachu.order == 25


async def test_async_session(async_session: AsyncSession) -> None:
    pikachu = await async_session.get(tables.PokemonSpecies, "pikachu")
    assert pikachu is not None
    assert pikachu.identifier == "pikachu"
    assert pikachu.order == 25
