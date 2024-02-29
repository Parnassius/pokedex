from __future__ import annotations

from typing import Any

import pytest
from sqlalchemy import ColumnElement, String, cast, func, select

from pokedex import pokedex, tables
from pokedex.enums import AbilitySlot, GameGroup

ChangesDict = dict[  # type: ignore[misc]
    GameGroup, dict[str, tuple[dict[Any, str], dict[Any, str]]]
]

ability_changes: ChangesDict = {
    GameGroup.DP: {
        "pidgey": (
            {AbilitySlot.SLOT_1: "keen-eye"},
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.SLOT_2: "tangled-feet"},
        ),
        "pidgeotto": (
            {AbilitySlot.SLOT_1: "keen-eye"},
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.SLOT_2: "tangled-feet"},
        ),
        "pidgeot": (
            {AbilitySlot.SLOT_1: "keen-eye"},
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.SLOT_2: "tangled-feet"},
        ),
        "nidoran-f": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "rivalry"},
        ),
        "nidorina": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "rivalry"},
        ),
        "nidoqueen": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "rivalry"},
        ),
        "nidoran-m": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "rivalry"},
        ),
        "nidorino": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "rivalry"},
        ),
        "nidoking": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "rivalry"},
        ),
        "clefairy": (
            {AbilitySlot.SLOT_1: "cute-charm"},
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.SLOT_2: "magic-guard"},
        ),
        "clefable": (
            {AbilitySlot.SLOT_1: "cute-charm"},
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.SLOT_2: "magic-guard"},
        ),
        "paras": (
            {AbilitySlot.SLOT_1: "effect-spore"},
            {AbilitySlot.SLOT_1: "effect-spore", AbilitySlot.SLOT_2: "dry-skin"},
        ),
        "parasect": (
            {AbilitySlot.SLOT_1: "effect-spore"},
            {AbilitySlot.SLOT_1: "effect-spore", AbilitySlot.SLOT_2: "dry-skin"},
        ),
        "venonat": (
            {AbilitySlot.SLOT_1: "compound-eyes"},
            {AbilitySlot.SLOT_1: "compound-eyes", AbilitySlot.SLOT_2: "tinted-lens"},
        ),
        "venomoth": (
            {AbilitySlot.SLOT_1: "shield-dust"},
            {AbilitySlot.SLOT_1: "shield-dust", AbilitySlot.SLOT_2: "tinted-lens"},
        ),
        "meowth": (
            {AbilitySlot.SLOT_1: "pickup"},
            {AbilitySlot.SLOT_1: "pickup", AbilitySlot.SLOT_2: "technician"},
        ),
        "persian": (
            {AbilitySlot.SLOT_1: "limber"},
            {AbilitySlot.SLOT_1: "limber", AbilitySlot.SLOT_2: "technician"},
        ),
        "mankey": (
            {AbilitySlot.SLOT_1: "vital-spirit"},
            {AbilitySlot.SLOT_1: "vital-spirit", AbilitySlot.SLOT_2: "anger-point"},
        ),
        "primeape": (
            {AbilitySlot.SLOT_1: "vital-spirit"},
            {AbilitySlot.SLOT_1: "vital-spirit", AbilitySlot.SLOT_2: "anger-point"},
        ),
        "machop": (
            {AbilitySlot.SLOT_1: "guts"},
            {AbilitySlot.SLOT_1: "guts", AbilitySlot.SLOT_2: "no-guard"},
        ),
        "machoke": (
            {AbilitySlot.SLOT_1: "guts"},
            {AbilitySlot.SLOT_1: "guts", AbilitySlot.SLOT_2: "no-guard"},
        ),
        "machamp": (
            {AbilitySlot.SLOT_1: "guts"},
            {AbilitySlot.SLOT_1: "guts", AbilitySlot.SLOT_2: "no-guard"},
        ),
        "seel": (
            {AbilitySlot.SLOT_1: "thick-fat"},
            {AbilitySlot.SLOT_1: "thick-fat", AbilitySlot.SLOT_2: "hydration"},
        ),
        "dewgong": (
            {AbilitySlot.SLOT_1: "thick-fat"},
            {AbilitySlot.SLOT_1: "thick-fat", AbilitySlot.SLOT_2: "hydration"},
        ),
        "shellder": (
            {AbilitySlot.SLOT_1: "shell-armor"},
            {AbilitySlot.SLOT_1: "shell-armor", AbilitySlot.SLOT_2: "skill-link"},
        ),
        "cloyster": (
            {AbilitySlot.SLOT_1: "shell-armor"},
            {AbilitySlot.SLOT_1: "shell-armor", AbilitySlot.SLOT_2: "skill-link"},
        ),
        "drowzee": (
            {AbilitySlot.SLOT_1: "insomnia"},
            {AbilitySlot.SLOT_1: "insomnia", AbilitySlot.SLOT_2: "forewarn"},
        ),
        "hypno": (
            {AbilitySlot.SLOT_1: "insomnia"},
            {AbilitySlot.SLOT_1: "insomnia", AbilitySlot.SLOT_2: "forewarn"},
        ),
        "hitmonlee": (
            {AbilitySlot.SLOT_1: "limber"},
            {AbilitySlot.SLOT_1: "limber", AbilitySlot.SLOT_2: "reckless"},
        ),
        "hitmonchan": (
            {AbilitySlot.SLOT_1: "keen-eye"},
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.SLOT_2: "iron-fist"},
        ),
        "tangela": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "leaf-guard"},
        ),
        "kangaskhan": (
            {AbilitySlot.SLOT_1: "early-bird"},
            {AbilitySlot.SLOT_1: "early-bird", AbilitySlot.SLOT_2: "scrappy"},
        ),
        "horsea": (
            {AbilitySlot.SLOT_1: "swift-swim"},
            {AbilitySlot.SLOT_1: "swift-swim", AbilitySlot.SLOT_2: "sniper"},
        ),
        "seadra": (
            {AbilitySlot.SLOT_1: "poison-point"},
            {AbilitySlot.SLOT_1: "poison-point", AbilitySlot.SLOT_2: "sniper"},
        ),
        "mr-mime": (
            {AbilitySlot.SLOT_1: "soundproof"},
            {AbilitySlot.SLOT_1: "soundproof", AbilitySlot.SLOT_2: "filter"},
        ),
        "scyther": (
            {AbilitySlot.SLOT_1: "swarm"},
            {AbilitySlot.SLOT_1: "swarm", AbilitySlot.SLOT_2: "technician"},
        ),
        "jynx": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "forewarn"},
        ),
        "pinsir": (
            {AbilitySlot.SLOT_1: "hyper-cutter"},
            {AbilitySlot.SLOT_1: "hyper-cutter", AbilitySlot.SLOT_2: "mold-breaker"},
        ),
        "tauros": (
            {AbilitySlot.SLOT_1: "intimidate"},
            {AbilitySlot.SLOT_1: "intimidate", AbilitySlot.SLOT_2: "anger-point"},
        ),
        "eevee": (
            {AbilitySlot.SLOT_1: "run-away"},
            {AbilitySlot.SLOT_1: "run-away", AbilitySlot.SLOT_2: "adaptability"},
        ),
        "porygon": (
            {AbilitySlot.SLOT_1: "trace"},
            {AbilitySlot.SLOT_1: "trace", AbilitySlot.SLOT_2: "download"},
        ),
        "cleffa": (
            {AbilitySlot.SLOT_1: "cute-charm"},
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.SLOT_2: "magic-guard"},
        ),
        "hoppip": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "leaf-guard"},
        ),
        "skiploom": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "leaf-guard"},
        ),
        "jumpluff": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "leaf-guard"},
        ),
        "sunkern": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "solar-power"},
        ),
        "sunflora": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "solar-power"},
        ),
        "murkrow": (
            {AbilitySlot.SLOT_1: "insomnia"},
            {AbilitySlot.SLOT_1: "insomnia", AbilitySlot.SLOT_2: "super-luck"},
        ),
        "granbull": (
            {AbilitySlot.SLOT_1: "intimidate"},
            {AbilitySlot.SLOT_1: "intimidate", AbilitySlot.SLOT_2: "quick-feet"},
        ),
        "scizor": (
            {AbilitySlot.SLOT_1: "swarm"},
            {AbilitySlot.SLOT_1: "swarm", AbilitySlot.SLOT_2: "technician"},
        ),
        "shuckle": (
            {AbilitySlot.SLOT_1: "sturdy"},
            {AbilitySlot.SLOT_1: "sturdy", AbilitySlot.SLOT_2: "gluttony"},
        ),
        "teddiursa": (
            {AbilitySlot.SLOT_1: "pickup"},
            {AbilitySlot.SLOT_1: "pickup", AbilitySlot.SLOT_2: "quick-feet"},
        ),
        "ursaring": (
            {AbilitySlot.SLOT_1: "guts"},
            {AbilitySlot.SLOT_1: "guts", AbilitySlot.SLOT_2: "quick-feet"},
        ),
        "swinub": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "snow-cloak"},
        ),
        "piloswine": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "snow-cloak"},
        ),
        "remoraid": (
            {AbilitySlot.SLOT_1: "hustle"},
            {AbilitySlot.SLOT_1: "hustle", AbilitySlot.SLOT_2: "sniper"},
        ),
        "octillery": (
            {AbilitySlot.SLOT_1: "suction-cups"},
            {AbilitySlot.SLOT_1: "suction-cups", AbilitySlot.SLOT_2: "sniper"},
        ),
        "kingdra": (
            {AbilitySlot.SLOT_1: "swift-swim"},
            {AbilitySlot.SLOT_1: "swift-swim", AbilitySlot.SLOT_2: "sniper"},
        ),
        "porygon2": (
            {AbilitySlot.SLOT_1: "trace"},
            {AbilitySlot.SLOT_1: "trace", AbilitySlot.SLOT_2: "download"},
        ),
        "stantler": (
            {AbilitySlot.SLOT_1: "intimidate"},
            {AbilitySlot.SLOT_1: "intimidate", AbilitySlot.SLOT_2: "frisk"},
        ),
        "smeargle": (
            {AbilitySlot.SLOT_1: "own-tempo"},
            {AbilitySlot.SLOT_1: "own-tempo", AbilitySlot.SLOT_2: "technician"},
        ),
        "tyrogue": (
            {AbilitySlot.SLOT_1: "guts"},
            {AbilitySlot.SLOT_1: "guts", AbilitySlot.SLOT_2: "steadfast"},
        ),
        "hitmontop": (
            {AbilitySlot.SLOT_1: "intimidate"},
            {AbilitySlot.SLOT_1: "intimidate", AbilitySlot.SLOT_2: "technician"},
        ),
        "smoochum": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "forewarn"},
        ),
        "miltank": (
            {AbilitySlot.SLOT_1: "thick-fat"},
            {AbilitySlot.SLOT_1: "thick-fat", AbilitySlot.SLOT_2: "scrappy"},
        ),
        "poochyena": (
            {AbilitySlot.SLOT_1: "run-away"},
            {AbilitySlot.SLOT_1: "run-away", AbilitySlot.SLOT_2: "quick-feet"},
        ),
        "mightyena": (
            {AbilitySlot.SLOT_1: "intimidate"},
            {AbilitySlot.SLOT_1: "intimidate", AbilitySlot.SLOT_2: "quick-feet"},
        ),
        "zigzagoon": (
            {AbilitySlot.SLOT_1: "pickup"},
            {AbilitySlot.SLOT_1: "pickup", AbilitySlot.SLOT_2: "gluttony"},
        ),
        "linoone": (
            {AbilitySlot.SLOT_1: "pickup"},
            {AbilitySlot.SLOT_1: "pickup", AbilitySlot.SLOT_2: "gluttony"},
        ),
        "shroomish": (
            {AbilitySlot.SLOT_1: "effect-spore"},
            {AbilitySlot.SLOT_1: "effect-spore", AbilitySlot.SLOT_2: "poison-heal"},
        ),
        "breloom": (
            {AbilitySlot.SLOT_1: "effect-spore"},
            {AbilitySlot.SLOT_1: "effect-spore", AbilitySlot.SLOT_2: "poison-heal"},
        ),
        "skitty": (
            {AbilitySlot.SLOT_1: "cute-charm"},
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.SLOT_2: "normalize"},
        ),
        "delcatty": (
            {AbilitySlot.SLOT_1: "cute-charm"},
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.SLOT_2: "normalize"},
        ),
        "sableye": (
            {AbilitySlot.SLOT_1: "keen-eye"},
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.SLOT_2: "stall"},
        ),
        "illumise": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "tinted-lens"},
        ),
        "numel": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "simple"},
        ),
        "camerupt": (
            {AbilitySlot.SLOT_1: "magma-armor"},
            {AbilitySlot.SLOT_1: "magma-armor", AbilitySlot.SLOT_2: "solid-rock"},
        ),
        "spinda": (
            {AbilitySlot.SLOT_1: "own-tempo"},
            {AbilitySlot.SLOT_1: "own-tempo", AbilitySlot.SLOT_2: "tangled-feet"},
        ),
        "barboach": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "anticipation"},
        ),
        "whiscash": (
            {AbilitySlot.SLOT_1: "oblivious"},
            {AbilitySlot.SLOT_1: "oblivious", AbilitySlot.SLOT_2: "anticipation"},
        ),
        "shuppet": (
            {AbilitySlot.SLOT_1: "insomnia"},
            {AbilitySlot.SLOT_1: "insomnia", AbilitySlot.SLOT_2: "frisk"},
        ),
        "banette": (
            {AbilitySlot.SLOT_1: "insomnia"},
            {AbilitySlot.SLOT_1: "insomnia", AbilitySlot.SLOT_2: "frisk"},
        ),
        "tropius": (
            {AbilitySlot.SLOT_1: "chlorophyll"},
            {AbilitySlot.SLOT_1: "chlorophyll", AbilitySlot.SLOT_2: "solar-power"},
        ),
        "absol": (
            {AbilitySlot.SLOT_1: "pressure"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.SLOT_2: "super-luck"},
        ),
        "snorunt": (
            {AbilitySlot.SLOT_1: "inner-focus"},
            {AbilitySlot.SLOT_1: "inner-focus", AbilitySlot.SLOT_2: "ice-body"},
        ),
        "glalie": (
            {AbilitySlot.SLOT_1: "inner-focus"},
            {AbilitySlot.SLOT_1: "inner-focus", AbilitySlot.SLOT_2: "ice-body"},
        ),
        "spheal": (
            {AbilitySlot.SLOT_1: "thick-fat"},
            {AbilitySlot.SLOT_1: "thick-fat", AbilitySlot.SLOT_2: "ice-body"},
        ),
        "sealeo": (
            {AbilitySlot.SLOT_1: "thick-fat"},
            {AbilitySlot.SLOT_1: "thick-fat", AbilitySlot.SLOT_2: "ice-body"},
        ),
        "walrein": (
            {AbilitySlot.SLOT_1: "thick-fat"},
            {AbilitySlot.SLOT_1: "thick-fat", AbilitySlot.SLOT_2: "ice-body"},
        ),
    },
    GameGroup.XY: {
        "jigglypuff": (
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.HIDDEN: "friend-guard"},
            {
                AbilitySlot.SLOT_1: "cute-charm",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "friend-guard",
            },
        ),
        "wigglytuff": (
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.HIDDEN: "frisk"},
            {
                AbilitySlot.SLOT_1: "cute-charm",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "frisk",
            },
        ),
        "zapdos": (
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "lightning-rod"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "static"},
        ),
        "igglybuff": (
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.HIDDEN: "friend-guard"},
            {
                AbilitySlot.SLOT_1: "cute-charm",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "friend-guard",
            },
        ),
        "plusle": (
            {AbilitySlot.SLOT_1: "plus"},
            {AbilitySlot.SLOT_1: "plus", AbilitySlot.HIDDEN: "lightning-rod"},
        ),
        "minun": (
            {AbilitySlot.SLOT_1: "minus"},
            {AbilitySlot.SLOT_1: "minus", AbilitySlot.HIDDEN: "volt-absorb"},
        ),
        "feebas": (
            {AbilitySlot.SLOT_1: "swift-swim", AbilitySlot.HIDDEN: "adaptability"},
            {
                AbilitySlot.SLOT_1: "swift-swim",
                AbilitySlot.SLOT_2: "oblivious",
                AbilitySlot.HIDDEN: "adaptability",
            },
        ),
        "milotic": (
            {AbilitySlot.SLOT_1: "marvel-scale", AbilitySlot.HIDDEN: "cute-charm"},
            {
                AbilitySlot.SLOT_1: "marvel-scale",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "cute-charm",
            },
        ),
        "kecleon": (
            {AbilitySlot.SLOT_1: "color-change"},
            {AbilitySlot.SLOT_1: "color-change", AbilitySlot.HIDDEN: "protean"},
        ),
        "duskull": (
            {AbilitySlot.SLOT_1: "levitate"},
            {AbilitySlot.SLOT_1: "levitate", AbilitySlot.HIDDEN: "frisk"},
        ),
        "dusclops": (
            {AbilitySlot.SLOT_1: "pressure"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "frisk"},
        ),
        "starly": (
            {AbilitySlot.SLOT_1: "keen-eye"},
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.HIDDEN: "reckless"},
        ),
        "dusknoir": (
            {AbilitySlot.SLOT_1: "pressure"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "frisk"},
        ),
        "venipede": (
            {
                AbilitySlot.SLOT_1: "poison-point",
                AbilitySlot.SLOT_2: "swarm",
                AbilitySlot.HIDDEN: "quick-feet",
            },
            {
                AbilitySlot.SLOT_1: "poison-point",
                AbilitySlot.SLOT_2: "swarm",
                AbilitySlot.HIDDEN: "speed-boost",
            },
        ),
        "whirlipede": (
            {
                AbilitySlot.SLOT_1: "poison-point",
                AbilitySlot.SLOT_2: "swarm",
                AbilitySlot.HIDDEN: "quick-feet",
            },
            {
                AbilitySlot.SLOT_1: "poison-point",
                AbilitySlot.SLOT_2: "swarm",
                AbilitySlot.HIDDEN: "speed-boost",
            },
        ),
        "scolipede": (
            {
                AbilitySlot.SLOT_1: "poison-point",
                AbilitySlot.SLOT_2: "swarm",
                AbilitySlot.HIDDEN: "quick-feet",
            },
            {
                AbilitySlot.SLOT_1: "poison-point",
                AbilitySlot.SLOT_2: "swarm",
                AbilitySlot.HIDDEN: "speed-boost",
            },
        ),
        "gothita": (
            {AbilitySlot.SLOT_1: "frisk", AbilitySlot.HIDDEN: "shadow-tag"},
            {
                AbilitySlot.SLOT_1: "frisk",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "shadow-tag",
            },
        ),
        "gothorita": (
            {AbilitySlot.SLOT_1: "frisk", AbilitySlot.HIDDEN: "shadow-tag"},
            {
                AbilitySlot.SLOT_1: "frisk",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "shadow-tag",
            },
        ),
        "gothitelle": (
            {AbilitySlot.SLOT_1: "frisk", AbilitySlot.HIDDEN: "shadow-tag"},
            {
                AbilitySlot.SLOT_1: "frisk",
                AbilitySlot.SLOT_2: "competitive",
                AbilitySlot.HIDDEN: "shadow-tag",
            },
        ),
        "ferrothorn": (
            {AbilitySlot.SLOT_1: "iron-barbs"},
            {AbilitySlot.SLOT_1: "iron-barbs", AbilitySlot.HIDDEN: "anticipation"},
        ),
        "litwick": (
            {
                AbilitySlot.SLOT_1: "flash-fire",
                AbilitySlot.SLOT_2: "flame-body",
                AbilitySlot.HIDDEN: "shadow-tag",
            },
            {
                AbilitySlot.SLOT_1: "flash-fire",
                AbilitySlot.SLOT_2: "flame-body",
                AbilitySlot.HIDDEN: "infiltrator",
            },
        ),
        "lampent": (
            {
                AbilitySlot.SLOT_1: "flash-fire",
                AbilitySlot.SLOT_2: "flame-body",
                AbilitySlot.HIDDEN: "shadow-tag",
            },
            {
                AbilitySlot.SLOT_1: "flash-fire",
                AbilitySlot.SLOT_2: "flame-body",
                AbilitySlot.HIDDEN: "infiltrator",
            },
        ),
        "chandelure": (
            {
                AbilitySlot.SLOT_1: "flash-fire",
                AbilitySlot.SLOT_2: "flame-body",
                AbilitySlot.HIDDEN: "shadow-tag",
            },
            {
                AbilitySlot.SLOT_1: "flash-fire",
                AbilitySlot.SLOT_2: "flame-body",
                AbilitySlot.HIDDEN: "infiltrator",
            },
        ),
    },
    GameGroup.SM: {
        "gengar": (
            {AbilitySlot.SLOT_1: "levitate"},
            {AbilitySlot.SLOT_1: "cursed-body"},
        ),
        "raikou": (
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "volt-absorb"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "inner-focus"},
        ),
        "entei": (
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "flash-fire"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "inner-focus"},
        ),
        "suicune": (
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "water-absorb"},
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "inner-focus"},
        ),
        "wingull": (
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.HIDDEN: "rain-dish"},
            {
                AbilitySlot.SLOT_1: "keen-eye",
                AbilitySlot.SLOT_2: "hydration",
                AbilitySlot.HIDDEN: "rain-dish",
            },
        ),
        "pelipper": (
            {AbilitySlot.SLOT_1: "keen-eye", AbilitySlot.HIDDEN: "rain-dish"},
            {
                AbilitySlot.SLOT_1: "keen-eye",
                AbilitySlot.SLOT_2: "drizzle",
                AbilitySlot.HIDDEN: "rain-dish",
            },
        ),
        "torkoal": (
            {AbilitySlot.SLOT_1: "white-smoke", AbilitySlot.HIDDEN: "shell-armor"},
            {
                AbilitySlot.SLOT_1: "white-smoke",
                AbilitySlot.SLOT_2: "drought",
                AbilitySlot.HIDDEN: "shell-armor",
            },
        ),
        "roggenrola": (
            {AbilitySlot.SLOT_1: "sturdy", AbilitySlot.HIDDEN: "sand-force"},
            {
                AbilitySlot.SLOT_1: "sturdy",
                AbilitySlot.SLOT_2: "weak-armor",
                AbilitySlot.HIDDEN: "sand-force",
            },
        ),
        "boldore": (
            {AbilitySlot.SLOT_1: "sturdy", AbilitySlot.HIDDEN: "sand-force"},
            {
                AbilitySlot.SLOT_1: "sturdy",
                AbilitySlot.SLOT_2: "weak-armor",
                AbilitySlot.HIDDEN: "sand-force",
            },
        ),
        "gigalith": (
            {AbilitySlot.SLOT_1: "sturdy", AbilitySlot.HIDDEN: "sand-force"},
            {
                AbilitySlot.SLOT_1: "sturdy",
                AbilitySlot.SLOT_2: "sand-stream",
                AbilitySlot.HIDDEN: "sand-force",
            },
        ),
        "vanillite": (
            {AbilitySlot.SLOT_1: "ice-body", AbilitySlot.HIDDEN: "weak-armor"},
            {
                AbilitySlot.SLOT_1: "ice-body",
                AbilitySlot.SLOT_2: "snow-cloak",
                AbilitySlot.HIDDEN: "weak-armor",
            },
        ),
        "vanillish": (
            {AbilitySlot.SLOT_1: "ice-body", AbilitySlot.HIDDEN: "weak-armor"},
            {
                AbilitySlot.SLOT_1: "ice-body",
                AbilitySlot.SLOT_2: "snow-cloak",
                AbilitySlot.HIDDEN: "weak-armor",
            },
        ),
        "vanilluxe": (
            {AbilitySlot.SLOT_1: "ice-body", AbilitySlot.HIDDEN: "weak-armor"},
            {
                AbilitySlot.SLOT_1: "ice-body",
                AbilitySlot.SLOT_2: "snow-warning",
                AbilitySlot.HIDDEN: "weak-armor",
            },
        ),
        "cubchoo": (
            {AbilitySlot.SLOT_1: "snow-cloak", AbilitySlot.HIDDEN: "rattled"},
            {
                AbilitySlot.SLOT_1: "snow-cloak",
                AbilitySlot.SLOT_2: "slush-rush",
                AbilitySlot.HIDDEN: "rattled",
            },
        ),
        "beartic": (
            {AbilitySlot.SLOT_1: "snow-cloak", AbilitySlot.HIDDEN: "swift-swim"},
            {
                AbilitySlot.SLOT_1: "snow-cloak",
                AbilitySlot.SLOT_2: "slush-rush",
                AbilitySlot.HIDDEN: "swift-swim",
            },
        ),
    },
    GameGroup.SS: {
        "koffing": (
            {AbilitySlot.SLOT_1: "levitate"},
            {
                AbilitySlot.SLOT_1: "levitate",
                AbilitySlot.SLOT_2: "neutralizing-gas",
                AbilitySlot.HIDDEN: "stench",
            },
        ),
        "weezing": (
            {AbilitySlot.SLOT_1: "levitate"},
            {
                AbilitySlot.SLOT_1: "levitate",
                AbilitySlot.SLOT_2: "neutralizing-gas",
                AbilitySlot.HIDDEN: "stench",
            },
        ),
    },
    GameGroup.SV: {
        "growlithe-hisuian-form": (
            {
                AbilitySlot.SLOT_1: "intimidate",
                AbilitySlot.SLOT_2: "flash-fire",
                AbilitySlot.HIDDEN: "justified",
            },
            {
                AbilitySlot.SLOT_1: "intimidate",
                AbilitySlot.SLOT_2: "flash-fire",
                AbilitySlot.HIDDEN: "rock-head",
            },
        ),
        "arcanine-hisuian-form": (
            {
                AbilitySlot.SLOT_1: "intimidate",
                AbilitySlot.SLOT_2: "flash-fire",
                AbilitySlot.HIDDEN: "justified",
            },
            {
                AbilitySlot.SLOT_1: "intimidate",
                AbilitySlot.SLOT_2: "flash-fire",
                AbilitySlot.HIDDEN: "rock-head",
            },
        ),
        "typhlosion-hisuian-form": (
            {AbilitySlot.SLOT_1: "blaze", AbilitySlot.HIDDEN: "flash-fire"},
            {AbilitySlot.SLOT_1: "blaze", AbilitySlot.HIDDEN: "frisk"},
        ),
        "sneasel-hisuian-form": (
            {
                AbilitySlot.SLOT_1: "inner-focus",
                AbilitySlot.SLOT_2: "keen-eye",
                AbilitySlot.HIDDEN: "poison-touch",
            },
            {
                AbilitySlot.SLOT_1: "inner-focus",
                AbilitySlot.SLOT_2: "keen-eye",
                AbilitySlot.HIDDEN: "pickpocket",
            },
        ),
        "shiftry": (
            {
                AbilitySlot.SLOT_1: "chlorophyll",
                AbilitySlot.SLOT_2: "early-bird",
                AbilitySlot.HIDDEN: "pickpocket",
            },
            {
                AbilitySlot.SLOT_1: "chlorophyll",
                AbilitySlot.SLOT_2: "wind-rider",
                AbilitySlot.HIDDEN: "pickpocket",
            },
        ),
        "piplup": (
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "defiant"},
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "competitive"},
        ),
        "prinplup": (
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "defiant"},
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "competitive"},
        ),
        "empoleon": (
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "defiant"},
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "competitive"},
        ),
        "gallade": (
            {AbilitySlot.SLOT_1: "steadfast", AbilitySlot.HIDDEN: "justified"},
            {
                AbilitySlot.SLOT_1: "steadfast",
                AbilitySlot.SLOT_2: "sharpness",
                AbilitySlot.HIDDEN: "justified",
            },
        ),
        "samurott-hisuian-form": (
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "shell-armor"},
            {AbilitySlot.SLOT_1: "torrent", AbilitySlot.HIDDEN: "sharpness"},
        ),
        "braviary-hisuian-form": (
            {
                AbilitySlot.SLOT_1: "keen-eye",
                AbilitySlot.SLOT_2: "sheer-force",
                AbilitySlot.HIDDEN: "defiant",
            },
            {
                AbilitySlot.SLOT_1: "keen-eye",
                AbilitySlot.SLOT_2: "sheer-force",
                AbilitySlot.HIDDEN: "tinted-lens",
            },
        ),
        "decidueye-hisuian-form": (
            {AbilitySlot.SLOT_1: "overgrow", AbilitySlot.HIDDEN: "long-reach"},
            {AbilitySlot.SLOT_1: "overgrow", AbilitySlot.HIDDEN: "scrappy"},
        ),
        "sliggoo-hisuian-form": (
            {
                AbilitySlot.SLOT_1: "sap-sipper",
                AbilitySlot.SLOT_2: "overcoat",
                AbilitySlot.HIDDEN: "gooey",
            },
            {
                AbilitySlot.SLOT_1: "sap-sipper",
                AbilitySlot.SLOT_2: "shell-armor",
                AbilitySlot.HIDDEN: "gooey",
            },
        ),
        "goodra-hisuian-form": (
            {
                AbilitySlot.SLOT_1: "sap-sipper",
                AbilitySlot.SLOT_2: "overcoat",
                AbilitySlot.HIDDEN: "gooey",
            },
            {
                AbilitySlot.SLOT_1: "sap-sipper",
                AbilitySlot.SLOT_2: "shell-armor",
                AbilitySlot.HIDDEN: "gooey",
            },
        ),
        "kleavor": (
            {
                AbilitySlot.SLOT_1: "swarm",
                AbilitySlot.SLOT_2: "sheer-force",
                AbilitySlot.HIDDEN: "steadfast",
            },
            {
                AbilitySlot.SLOT_1: "swarm",
                AbilitySlot.SLOT_2: "sheer-force",
                AbilitySlot.HIDDEN: "sharpness",
            },
        ),
        "basculegion-male": (
            {
                AbilitySlot.SLOT_1: "rattled",
                AbilitySlot.SLOT_2: "adaptability",
                AbilitySlot.HIDDEN: "mold-breaker",
            },
            {
                AbilitySlot.SLOT_1: "swift-swim",
                AbilitySlot.SLOT_2: "adaptability",
                AbilitySlot.HIDDEN: "mold-breaker",
            },
        ),
        "basculegion-female": (
            {
                AbilitySlot.SLOT_1: "rattled",
                AbilitySlot.SLOT_2: "adaptability",
                AbilitySlot.HIDDEN: "mold-breaker",
            },
            {
                AbilitySlot.SLOT_1: "swift-swim",
                AbilitySlot.SLOT_2: "adaptability",
                AbilitySlot.HIDDEN: "mold-breaker",
            },
        ),
        "sneasler": (
            {AbilitySlot.SLOT_1: "pressure", AbilitySlot.HIDDEN: "poison-touch"},
            {
                AbilitySlot.SLOT_1: "pressure",
                AbilitySlot.SLOT_2: "unburden",
                AbilitySlot.HIDDEN: "poison-touch",
            },
        ),
        "enamorus-incarnate-forme": (
            {AbilitySlot.SLOT_1: "healer", AbilitySlot.HIDDEN: "contrary"},
            {AbilitySlot.SLOT_1: "cute-charm", AbilitySlot.HIDDEN: "contrary"},
        ),
    },
}
egg_group_changes: ChangesDict = {
    GameGroup.SS: {
        "trapinch": (
            {"1": "bug"},
            {"1": "bug", "2": "dragon"},
        ),
        "vibrava": (
            {"1": "bug"},
            {"1": "bug", "2": "dragon"},
        ),
        "flygon": (
            {"1": "bug"},
            {"1": "bug", "2": "dragon"},
        ),
        "ralts": (
            {"1": "amorphous"},
            {"1": "human-like", "2": "amorphous"},
        ),
        "kirlia": (
            {"1": "amorphous"},
            {"1": "human-like", "2": "amorphous"},
        ),
        "gardevoir": (
            {"1": "amorphous"},
            {"1": "human-like", "2": "amorphous"},
        ),
        "gallade": (
            {"1": "amorphous"},
            {"1": "human-like", "2": "amorphous"},
        ),
        "hawlucha": (
            {"1": "human-like"},
            {"1": "flying", "2": "human-like"},
        ),
        "bergmite": (
            {"1": "monster"},
            {"1": "monster", "2": "mineral"},
        ),
        "avalugg": (
            {"1": "monster"},
            {"1": "monster", "2": "mineral"},
        ),
        "noibat": (
            {"1": "flying"},
            {"1": "flying", "2": "dragon"},
        ),
        "noivern": (
            {"1": "flying"},
            {"1": "flying", "2": "dragon"},
        ),
    },
}
types_changes: ChangesDict = {
    GameGroup.GS: {
        "magnemite": (
            {"1": "electric"},
            {"1": "electric", "2": "steel"},
        ),
        "magneton": (
            {"1": "electric"},
            {"1": "electric", "2": "steel"},
        ),
    },
    GameGroup.BW: {
        "rotom-heat": (
            {"1": "electric", "2": "ghost"},
            {"1": "electric", "2": "fire"},
        ),
        "rotom-wash": (
            {"1": "electric", "2": "ghost"},
            {"1": "electric", "2": "water"},
        ),
        "rotom-frost": (
            {"1": "electric", "2": "ghost"},
            {"1": "electric", "2": "ice"},
        ),
        "rotom-fan": (
            {"1": "electric", "2": "ghost"},
            {"1": "electric", "2": "flying"},
        ),
        "rotom-mow": (
            {"1": "electric", "2": "ghost"},
            {"1": "electric", "2": "grass"},
        ),
    },
    GameGroup.XY: {
        "clefairy": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
        "clefable": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
        "jigglypuff": (
            {"1": "normal"},
            {"1": "normal", "2": "fairy"},
        ),
        "wigglytuff": (
            {"1": "normal"},
            {"1": "normal", "2": "fairy"},
        ),
        "mr-mime": (
            {"1": "psychic"},
            {"1": "psychic", "2": "fairy"},
        ),
        "cleffa": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
        "igglybuff": (
            {"1": "normal"},
            {"1": "normal", "2": "fairy"},
        ),
        "togepi": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
        "togetic": (
            {"1": "normal", "2": "flying"},
            {"1": "fairy", "2": "flying"},
        ),
        "marill": (
            {"1": "water"},
            {"1": "water", "2": "fairy"},
        ),
        "azumarill": (
            {"1": "water"},
            {"1": "water", "2": "fairy"},
        ),
        "snubbull": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
        "granbull": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
        "ralts": (
            {"1": "psychic"},
            {"1": "psychic", "2": "fairy"},
        ),
        "kirlia": (
            {"1": "psychic"},
            {"1": "psychic", "2": "fairy"},
        ),
        "gardevoir": (
            {"1": "psychic"},
            {"1": "psychic", "2": "fairy"},
        ),
        "azurill": (
            {"1": "normal"},
            {"1": "normal", "2": "fairy"},
        ),
        "mawile": (
            {"1": "steel"},
            {"1": "steel", "2": "fairy"},
        ),
        "mime-jr": (
            {"1": "psychic"},
            {"1": "psychic", "2": "fairy"},
        ),
        "togekiss": (
            {"1": "normal", "2": "flying"},
            {"1": "fairy", "2": "flying"},
        ),
        "cottonee": (
            {"1": "grass"},
            {"1": "grass", "2": "fairy"},
        ),
        "whimsicott": (
            {"1": "grass"},
            {"1": "grass", "2": "fairy"},
        ),
    },
    GameGroup.SS: {
        "silvally-type-fighting": (  # TODO: maybe hardcode these?
            {"1": "normal"},
            {"1": "fighting"},
        ),
        "silvally-type-flying": (
            {"1": "normal"},
            {"1": "flying"},
        ),
        "silvally-type-poison": (
            {"1": "normal"},
            {"1": "poison"},
        ),
        "silvally-type-ground": (
            {"1": "normal"},
            {"1": "ground"},
        ),
        "silvally-type-rock": (
            {"1": "normal"},
            {"1": "rock"},
        ),
        "silvally-type-bug": (
            {"1": "normal"},
            {"1": "bug"},
        ),
        "silvally-type-ghost": (
            {"1": "normal"},
            {"1": "ghost"},
        ),
        "silvally-type-steel": (
            {"1": "normal"},
            {"1": "steel"},
        ),
        "silvally-type-fire": (
            {"1": "normal"},
            {"1": "fire"},
        ),
        "silvally-type-water": (
            {"1": "normal"},
            {"1": "water"},
        ),
        "silvally-type-grass": (
            {"1": "normal"},
            {"1": "grass"},
        ),
        "silvally-type-electric": (
            {"1": "normal"},
            {"1": "electric"},
        ),
        "silvally-type-psychic": (
            {"1": "normal"},
            {"1": "psychic"},
        ),
        "silvally-type-ice": (
            {"1": "normal"},
            {"1": "ice"},
        ),
        "silvally-type-dragon": (
            {"1": "normal"},
            {"1": "dragon"},
        ),
        "silvally-type-dark": (
            {"1": "normal"},
            {"1": "dark"},
        ),
        "silvally-type-fairy": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
    },
    GameGroup.BDSP: {
        "arceus-fighting-type": (  # TODO: maybe hardcode these?
            {"1": "normal"},
            {"1": "fighting"},
        ),
        "arceus-flying-type": (
            {"1": "normal"},
            {"1": "flying"},
        ),
        "arceus-poison-type": (
            {"1": "normal"},
            {"1": "poison"},
        ),
        "arceus-ground-type": (
            {"1": "normal"},
            {"1": "ground"},
        ),
        "arceus-rock-type": (
            {"1": "normal"},
            {"1": "rock"},
        ),
        "arceus-bug-type": (
            {"1": "normal"},
            {"1": "bug"},
        ),
        "arceus-ghost-type": (
            {"1": "normal"},
            {"1": "ghost"},
        ),
        "arceus-steel-type": (
            {"1": "normal"},
            {"1": "steel"},
        ),
        "arceus-fire-type": (
            {"1": "normal"},
            {"1": "fire"},
        ),
        "arceus-water-type": (
            {"1": "normal"},
            {"1": "water"},
        ),
        "arceus-grass-type": (
            {"1": "normal"},
            {"1": "grass"},
        ),
        "arceus-electric-type": (
            {"1": "normal"},
            {"1": "electric"},
        ),
        "arceus-psychic-type": (
            {"1": "normal"},
            {"1": "psychic"},
        ),
        "arceus-ice-type": (
            {"1": "normal"},
            {"1": "ice"},
        ),
        "arceus-dragon-type": (
            {"1": "normal"},
            {"1": "dragon"},
        ),
        "arceus-dark-type": (
            {"1": "normal"},
            {"1": "dark"},
        ),
        "arceus-fairy-type": (
            {"1": "normal"},
            {"1": "fairy"},
        ),
    },
}


@pytest.mark.parametrize(
    "table, entry_column, changes",
    [
        (
            tables.PokemonAbility,
            func.group_concat(
                tables.PokemonAbility.slot_identifier
                + ":"
                + tables.PokemonAbility.ability_identifier
            ),
            ability_changes,
        ),
        (
            tables.PokemonEggGroup,
            func.group_concat(
                cast(tables.PokemonEggGroup.slot, String)
                + ":"
                + tables.PokemonEggGroup.egg_group_identifier
            ),
            egg_group_changes,
        ),
        (
            tables.PokemonType,
            func.group_concat(
                cast(tables.PokemonType.slot, String)
                + ":"
                + tables.PokemonType.type_identifier
            ),
            types_changes,
        ),
    ],
)
def test_pokemon_attribute_changes(
    table: type[tables.Base],
    entry_column: ColumnElement[str],
    changes: ChangesDict,
) -> None:
    with pokedex.session() as session:
        stmt = (
            select(
                table.pokemon_identifier,  # type: ignore[attr-defined]
                table.game_group_identifier,  # type: ignore[attr-defined]
                entry_column.label("entry"),
            )
            .select_from(table)
            .join(tables.GameGroup)
            .group_by(
                table.pokemon_identifier,  # type: ignore[attr-defined]
                table.game_group_identifier,  # type: ignore[attr-defined]
            )
            .order_by(
                table.pokemon_identifier,  # type: ignore[attr-defined]
                tables.GameGroup.order,
            )
        )
        result = session.execute(stmt)

        identifier = ""
        entry: dict[Any, str]  # type: ignore[misc]
        for row in result:
            row_entry = dict(x.split(":") for x in row.entry.split(","))
            if table is tables.PokemonAbility:
                row_entry = {AbilitySlot[k]: v for k, v in row_entry.items()}
            if row.pokemon_identifier != identifier:
                identifier = row.pokemon_identifier
                entry = row_entry
            elif (
                row.game_group_identifier == GameGroup.BW
                and table is tables.PokemonAbility
                and AbilitySlot.HIDDEN in row_entry
            ):
                entry[AbilitySlot.HIDDEN] = row_entry[AbilitySlot.HIDDEN]

            change = changes.get(row.game_group_identifier, {}).get(identifier, None)
            if row_entry == entry:
                assert change is None, (
                    identifier,
                    row.game_group_identifier,
                )
            else:
                assert change == (entry, row_entry), (
                    identifier,
                    row.game_group_identifier,
                )
            entry = row_entry


def test_pokemon_stat_changes() -> None:
    base_stat_changes: ChangesDict = {
        GameGroup.XY: {
            "butterfree": (
                {"sp-atk": "80"},
                {"sp-atk": "90"},
            ),
            "beedrill": (
                {"attack": "80"},
                {"attack": "90"},
            ),
            "pidgeot": (
                {"speed": "91"},
                {"speed": "101"},
            ),
            "pikachu": (
                {"defense": "30", "sp-def": "40"},
                {"defense": "40", "sp-def": "50"},
            ),
            "raichu": (
                {"speed": "100"},
                {"speed": "110"},
            ),
            "nidoqueen": (
                {"attack": "82"},
                {"attack": "92"},
            ),
            "nidoking": (
                {"attack": "92"},
                {"attack": "102"},
            ),
            "clefable": (
                {"sp-atk": "85"},
                {"sp-atk": "95"},
            ),
            "wigglytuff": (
                {"sp-atk": "75"},
                {"sp-atk": "85"},
            ),
            "vileplume": (
                {"sp-atk": "100"},
                {"sp-atk": "110"},
            ),
            "poliwrath": (
                {"attack": "85"},
                {"attack": "95"},
            ),
            "alakazam": (
                {"sp-def": "85"},
                {"sp-def": "95"},
            ),
            "victreebel": (
                {"sp-def": "60"},
                {"sp-def": "70"},
            ),
            "golem": (
                {"attack": "110"},
                {"attack": "120"},
            ),
            "ampharos": (
                {"defense": "75"},
                {"defense": "85"},
            ),
            "bellossom": (
                {"defense": "85"},
                {"defense": "95"},
            ),
            "azumarill": (
                {"sp-atk": "50"},
                {"sp-atk": "60"},
            ),
            "jumpluff": (
                {"sp-def": "85"},
                {"sp-def": "95"},
            ),
            "beautifly": (
                {"sp-atk": "90"},
                {"sp-atk": "100"},
            ),
            "exploud": (
                {"sp-def": "63"},
                {"sp-def": "73"},
            ),
            "staraptor": (
                {"sp-def": "50"},
                {"sp-def": "60"},
            ),
            "roserade": (
                {"defense": "55"},
                {"defense": "65"},
            ),
            "stoutland": (
                {"attack": "100"},
                {"attack": "110"},
            ),
            "unfezant": (
                {"attack": "105"},
                {"attack": "115"},
            ),
            "gigalith": (
                {"sp-def": "70"},
                {"sp-def": "80"},
            ),
            "seismitoad": (
                {"attack": "85"},
                {"attack": "95"},
            ),
            "leavanny": (
                {"sp-def": "70"},
                {"sp-def": "80"},
            ),
            "scolipede": (
                {"attack": "90"},
                {"attack": "100"},
            ),
            "krookodile": (
                {"defense": "70"},
                {"defense": "80"},
            ),
        },
        GameGroup.SM: {
            "arbok": (
                {"attack": "85"},
                {"attack": "95"},
            ),
            "dugtrio": (
                {"attack": "80"},
                {"attack": "100"},
            ),
            "alakazam-mega": (
                {"sp-def": "95"},
                {"sp-def": "105"},
            ),
            "farfetchd": (
                {"attack": "65"},
                {"attack": "90"},
            ),
            "dodrio": (
                {"speed": "100"},
                {"speed": "110"},
            ),
            "electrode": (
                {"speed": "140"},
                {"speed": "150"},
            ),
            "exeggutor": (
                {"sp-def": "65"},
                {"sp-def": "75"},
            ),
            "noctowl": (
                {"sp-atk": "76"},
                {"sp-atk": "86"},
            ),
            "ariados": (
                {"sp-def": "60"},
                {"sp-def": "70"},
            ),
            "qwilfish": (
                {"defense": "75"},
                {"defense": "85"},
            ),
            "magcargo": (
                {"hp": "50", "sp-atk": "80"},
                {"hp": "60", "sp-atk": "90"},
            ),
            "corsola": (
                {"hp": "55", "defense": "85", "sp-def": "85"},
                {"hp": "65", "defense": "95", "sp-def": "95"},
            ),
            "mantine": (
                {"hp": "65"},
                {"hp": "85"},
            ),
            "swellow": (
                {"sp-atk": "50"},
                {"sp-atk": "75"},
            ),
            "pelipper": (
                {"sp-atk": "85"},
                {"sp-atk": "95"},
            ),
            "masquerain": (
                {"sp-atk": "80", "speed": "60"},
                {"sp-atk": "100", "speed": "80"},
            ),
            "delcatty": (
                {"speed": "70"},
                {"speed": "90"},
            ),
            "volbeat": (
                {"defense": "55", "sp-def": "75"},
                {"defense": "75", "sp-def": "85"},
            ),
            "illumise": (
                {"defense": "55", "sp-def": "75"},
                {"defense": "75", "sp-def": "85"},
            ),
            "lunatone": (
                {"hp": "70"},
                {"hp": "90"},
            ),
            "solrock": (
                {"hp": "70"},
                {"hp": "90"},
            ),
            "chimecho": (
                {"hp": "65", "defense": "70", "sp-def": "80"},
                {"hp": "75", "defense": "80", "sp-def": "90"},
            ),
            "woobat": (
                {"hp": "55"},
                {"hp": "65"},
            ),
            "crustle": (
                {"attack": "95"},
                {"attack": "105"},
            ),
            "beartic": (
                {"attack": "110"},
                {"attack": "130"},
            ),
            "cryogonal": (
                {"hp": "70", "defense": "30"},
                {"hp": "80", "defense": "50"},
            ),
        },
        GameGroup.SS: {
            "aegislash-shield-forme": (
                {"defense": "150", "sp-def": "150"},
                {"defense": "140", "sp-def": "140"},
            ),
            "aegislash-blade-forme": (
                {"attack": "150", "sp-atk": "150"},
                {"attack": "140", "sp-atk": "140"},
            ),
        },
        GameGroup.LA: {
            "cherrim-sunshine-form": (
                {"attack": "60", "sp-def": "78"},
                {"attack": "90", "sp-def": "117"},
            ),
        },
        GameGroup.SV: {
            "cresselia": (
                {"defense": "120", "sp-def": "130"},
                {"defense": "110", "sp-def": "120"},
            ),
            "zacian-hero-of-many-battles": (
                {"attack": "130"},
                {"attack": "120"},
            ),
            "zacian-crowned-sword": (
                {"attack": "170"},
                {"attack": "150"},
            ),
            "zamazenta-hero-of-many-battles": (
                {"attack": "130"},
                {"attack": "120"},
            ),
            "zamazenta-crowned-shield": (
                {"attack": "130", "defense": "145", "sp-def": "145"},
                {"attack": "120", "defense": "140", "sp-def": "140"},
            ),
        },
    }
    ev_yield_changes: ChangesDict = {
        GameGroup.DP: {
            "yanma": (
                {"speed": "2"},
                {"speed": "1"},
            ),
            "misdreavus": (
                {"sp-atk": "1", "sp-def": "1"},
                {"sp-atk": "0", "sp-def": "1"},
            ),
            "blissey": (
                {"hp": "2"},
                {"hp": "3"},
            ),
            "roselia": (
                {"sp-atk": "1"},
                {"sp-atk": "2"},
            ),
            "duskull": (
                {"defense": "1", "sp-def": "1"},
                {"defense": "0", "sp-def": "1"},
            ),
            "dusclops": (
                {"defense": "1", "sp-def": "2"},
                {"defense": "1", "sp-def": "1"},
            ),
            "deoxys-attack-forme": (
                {"attack": "0", "sp-atk": "0"},
                {"attack": "2", "sp-atk": "1"},
            ),
            "deoxys-defense-forme": (
                {"defense": "0", "sp-def": "0"},
                {"defense": "2", "sp-def": "1"},
            ),
            "deoxys-speed-forme": (
                {"speed": "0"},
                {"speed": "3"},
            ),
        },
        GameGroup.B2W2: {
            "watchog": (
                {"attack": "1"},
                {"attack": "2"},
            ),
        },
        GameGroup.SS: {
            "slowking": (
                {"sp-def": "3"},
                {"sp-def": "2"},
            ),
        },
        GameGroup.SV: {
            "basculin-white-striped-form": (
                {"speed": "1"},
                {"speed": "2"},
            ),
            "wyrdeer": (
                {"attack": "1", "sp-atk": "0"},
                {"attack": "1", "sp-atk": "1"},
            ),
            "kleavor": (
                {"attack": "2"},
                {"attack": "3"},
            ),
            "basculegion-male": (
                {"hp": "2"},
                {"hp": "3"},
            ),
            "basculegion-female": (
                {"hp": "2"},
                {"hp": "3"},
            ),
            "sneasler": (
                {"attack": "1", "speed": "1"},
                {"attack": "2", "speed": "0"},
            ),
            "overqwil": (
                {"attack": "1"},
                {"attack": "2"},
            ),
            "enamorus-therian-forme": (
                {"attack": "3", "sp-atk": "0"},
                {"attack": "0", "sp-atk": "3"},
            ),
        },
    }

    with pokedex.session() as session:
        stmt = (
            select(
                tables.PokemonStat.pokemon_identifier,
                tables.PokemonStat.game_group_identifier,
                func.group_concat(
                    tables.PokemonStat.stat_identifier
                    + ":"
                    + cast(tables.PokemonStat.base_value, String)
                    + ";"
                    + cast(tables.PokemonStat.ev_yield, String)
                ).label("entry"),
            )
            .select_from(tables.PokemonStat)
            .join(tables.GameGroup)
            .group_by(
                tables.PokemonStat.pokemon_identifier,
                tables.PokemonStat.game_group_identifier,
            )
            .order_by(
                tables.PokemonStat.pokemon_identifier,
                tables.GameGroup.order,
            )
        )
        result = session.execute(stmt)

        identifier = ""
        for row in result:
            row_entry = [x.split(":") for x in row.entry.split(",")]
            row_base_stats = {k: v.split(";")[0] for k, v in row_entry}
            row_evs_yield = {k: v.split(";")[1] for k, v in row_entry}
            if row.pokemon_identifier != identifier:
                identifier = row.pokemon_identifier
                base_stats = row_base_stats
                evs_yield = row_evs_yield
            elif row.game_group_identifier == GameGroup.GS:
                del base_stats["special"]
                base_stats["sp-atk"] = row_base_stats["sp-atk"]
                base_stats["sp-def"] = row_base_stats["sp-def"]

            base_stat_change = base_stat_changes.get(row.game_group_identifier, {}).get(
                identifier, None
            )
            if row_base_stats == base_stats:
                assert base_stat_change is None, (
                    identifier,
                    row.game_group_identifier,
                )
            else:
                assert (
                    row_base_stats | base_stat_change[0],  # type: ignore[index]
                    base_stats | base_stat_change[1],  # type: ignore[index]
                ) == (base_stats, row_base_stats), (
                    identifier,
                    row.game_group_identifier,
                )

            if row.game_group_identifier > GameGroup.RS:
                ev_yield_change = ev_yield_changes.get(
                    row.game_group_identifier, {}
                ).get(identifier, None)
                if row_evs_yield == evs_yield:
                    assert ev_yield_change is None, (
                        identifier,
                        row.game_group_identifier,
                    )
                else:
                    assert (
                        row_evs_yield | ev_yield_change[0],  # type: ignore[index]
                        evs_yield | ev_yield_change[1],  # type: ignore[index]
                    ) == (evs_yield, row_evs_yield), (
                        identifier,
                        row.game_group_identifier,
                    )

            base_stats = row_base_stats
            evs_yield = row_evs_yield
