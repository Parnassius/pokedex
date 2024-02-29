from __future__ import annotations

import csv
from pathlib import Path
from zlib import crc32

from sqlalchemy import Enum, create_engine, insert, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from pokedex.tables import Base


class Pokedex:
    csv_dir = Path(__file__).parent / "data"

    def __init__(self) -> None:
        self._path: Path | None = None
        self._session: sessionmaker[Session] | None = None
        self._async_session: async_sessionmaker[AsyncSession] | None = None

    def _database_uri(self, *, ro: bool = False, aiosqlite: bool = False) -> str:
        engine = "sqlite"
        if aiosqlite:
            engine += "+aiosqlite"
        uri = f"{engine}:///file:{self._path}?uri=true"
        if ro:
            uri += "&mode=ro"
        return uri

    @property
    def session(self) -> sessionmaker[Session]:
        if self._session is None:
            if self._path is None:
                msg = "Call setup_database before using the session"
                raise TypeError(msg)
            engine = create_engine(self._database_uri(ro=True))
            self._session = sessionmaker(engine)
        return self._session

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        if self._async_session is None:
            if self._path is None:
                msg = "Call setup_database before using the session"
                raise TypeError(msg)
            engine = create_async_engine(self._database_uri(ro=True, aiosqlite=True))
            self._async_session = async_sessionmaker(engine)
        return self._async_session

    def setup_database(self, path: Path, *, skip_build: bool = False) -> None:
        self._path = path

        if not skip_build:
            engine_rw = create_engine(self._database_uri())

            new_crc = crc32(b"")
            for file in sorted(self.csv_dir.glob("*.csv")):
                new_crc = crc32(file.read_bytes(), new_crc)

            new_crc -= 2**31  # user_version is a 32-bit signed integer

            try:
                with engine_rw.begin() as conn:
                    old_crc: int = conn.scalar(text("PRAGMA user_version"))
                    if old_crc == new_crc:
                        return  # Database is already up-to-date, skip build
            except OperationalError:  # Table does not exist
                pass

            path.write_bytes(b"")  # Truncate file

            Base.metadata.create_all(engine_rw)
            with engine_rw.begin() as conn:
                for table in Base.metadata.sorted_tables:
                    file = self.csv_dir / f"{table.key}.csv"
                    if file.is_file():
                        with file.open(encoding="utf-8") as f:
                            csv_data = csv.DictReader(f)
                            if csv_data.fieldnames is not None:
                                mappings = []
                                for csv_row in csv_data:
                                    row = {}
                                    for column, value in csv_row.items():
                                        column_type = table.columns[column].type
                                        if isinstance(column_type, Enum):
                                            value = next(
                                                x
                                                for x in column_type.python_type
                                                if x.value == value
                                            )
                                        elif (
                                            table.columns[column].nullable
                                            and value == ""
                                        ):
                                            value = None
                                        row[column] = value
                                    mappings.append(row)
                                conn.execute(insert(table), mappings)

                conn.execute(text(f"PRAGMA user_version = {new_crc}"))


pokedex = Pokedex()
