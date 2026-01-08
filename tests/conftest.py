from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from pokedex import pokedex


@pytest.fixture(scope="session", autouse=True)
def setup_database(tmp_path_factory: pytest.TempPathFactory) -> None:
    pokedex.setup_database(tmp_path_factory.getbasetemp() / "pokedex.sqlite")


@pytest.fixture
def session() -> Iterator[Session]:
    s = pokedex.session()
    try:
        yield s
    finally:
        s.close()


@pytest.fixture
async def async_session() -> AsyncIterator[AsyncSession]:
    s = pokedex.async_session()
    try:
        yield s
    finally:
        await s.close()
