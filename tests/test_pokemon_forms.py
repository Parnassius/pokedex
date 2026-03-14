from collections import defaultdict

import pytest

from pokedex import Pokemon


@pytest.mark.parametrize(("identifier"), Pokemon.list_identifiers())
def test_pokemon_forms(identifier: str) -> None:
    pokemon = Pokemon.get(identifier)
    forms = defaultdict[int, set[str]](set)
    for key, val in pokemon.forms.items():
        forms[val.form_id.single()].add(key)

    if identifier == "pikachu":
        assert all(len(v) == 2 for k, v in forms.items() if 1 <= k <= 6)
        assert all(len(v) == 1 for k, v in forms.items() if k == 0 or k >= 7)
    else:
        assert all(len(x) == 1 for x in forms.values())
