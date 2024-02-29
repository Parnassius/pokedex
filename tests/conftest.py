from __future__ import annotations

import os
from pathlib import Path

import pytest

from pokedex import pokedex


@pytest.fixture(scope="session", autouse=True)
def setup_database(tmp_path_factory: pytest.TempPathFactory) -> None:
    if env_id := os.environ.get("HATCH_ENV_ACTIVE"):
        cache = Path(__file__).parent / "database_cache"
        if not cache.exists():
            cache.mkdir()
            (cache / ".gitignore").write_text("*")
        database_path = cache / f"{env_id}.sqlite"
    else:
        database_path = tmp_path_factory.mktemp("data") / "pokedex.sqlite"
    pokedex.setup_database(database_path)
