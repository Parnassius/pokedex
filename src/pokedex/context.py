from contextvars import ContextVar
from types import TracebackType
from typing import overload

from pokedex.enums import GameGroup, Language

context_game_group = ContextVar("context_game_group", default=GameGroup.get_default())
context_language = ContextVar("context_language", default=Language.get_default())


class _Context:
    def __init__(self, *args: GameGroup | Language) -> None:
        self._game_group_token = None
        if game_group := next((x for x in args if isinstance(x, GameGroup)), None):
            self._game_group_token = context_game_group.set(game_group)

        self._language_token = None
        if language := next((x for x in args if isinstance(x, Language)), None):
            self._language_token = context_language.set(language)

    def reset(self) -> None:
        if self._game_group_token:
            context_game_group.reset(self._game_group_token)
        if self._language_token:
            context_language.reset(self._language_token)

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.reset()


@overload
def set_context(game_group: GameGroup, /) -> _Context: ...


@overload
def set_context(language: Language, /) -> _Context: ...


@overload
def set_context(game_group: GameGroup, language: Language, /) -> _Context: ...


def set_context(*args: GameGroup | Language) -> _Context:
    return _Context(*args)
