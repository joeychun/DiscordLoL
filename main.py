############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

# Import your models for use in your script
from db.models import *

############################################################################
## START OF APPLICATION
############################################################################

# Work with Python 3.6

# https://discord.com/api/oauth2/authorize?client_id=739069897606299648&permissions=1073883200&scope=bot

import requests
import json

import random
from random import choice

import time, datetime

import discord, asyncio
from discord.ext import commands, tasks
from discord import Colour
from discord import Embed
from asyncio import sleep

import sqlite3

from asgiref.sync import sync_to_async

from django.core.exceptions import ObjectDoesNotExist

from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

APIKey = 'RGAPI-0b8aa233-aeda-4680-853e-0e21c1402668'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

slash = SlashCommand(bot, sync_commands=True)

### EXCEPTIONS
class InvalidRegion(Exception):
    pass

class InvalidSummonerName(Exception):
    pass

class InvalidSummonerId(Exception):
    pass

class InvalidMatch(Exception):
    pass

class InvalidCircle(Exception):
    pass

class NotCircled(Exception):
    pass

class LoadingScreen(Exception):
    pass

class AlreadyLinkedAccount(Exception):
    pass

class IconAlreadySuggested(Exception):
    pass

class UserAnotherAuth(Exception):
    pass

class OtherUserAuth(Exception):
    pass

"""
TODO LIST

1. Authorize LoL account
2. Region Pictures
3. Account Link


"""


### RIOT API

maps = { # Outdated maps were excluded
  11: {
    "mapId": 11,
    "mapName": "Summoner's Rift",
    "notes": "SR"
  },
  12: {
    "mapId": 12,
    "mapName": "Howling Abyss",
    "notes": "ARAM"
  },
  20: {
    "mapId": 20,
    "mapName": "Convergence",
    "notes": "TFT"
  },
  21: {
    "mapId": 21,
    "mapName": "Nexus Blitz",
    "notes": "NexBlitz"
  }
}

types = {
    "CUSTOM_GAME": "Custom",
    "TUTORIAL_GAME": "Tutorial",
    "MATCHED_GAME": "Matched"
}

queues = {
    0: {
        "map": "Custom games", 
        "description": "Custom"
    },
    78: {
        "map": "Howling Abyss",
        "description": "1FA (Mirror)"
    },
    83: {
        "map": "Summoner's Rift",
        "description": "Co-op vs AI Ultra Rapid Fire games"
    },
    325: {
        "map": "Summoner's Rift", 
        "description": "All Random"
    },
    400: {
        "map": "Summoner's Rift",
        "description": "Draft Pick"
    },
    420: {
        "map": "Summoner's Rift",
        "description": "Ranked Solo"
    },
    430: {
        "map": "Summoner's Rift",
        "description": "Blind Pick"
    },
    440: {
        "map": "Summoner's Rift",
        "description": "Ranked Flex"
    },
    450: {
        "map": "Howling Abyss", 
        "description": "ARAM"
    },
    830: {
        "map": "Summoner's Rift",
        "description": "AI Bot"
    },
    840: {
        "map": "Summoner's Rift",
        "description": "AI Bot"
    },
    850: {
        "map": "Summoner's Rift",
        "description": "AI Bot"
    },
    900: {
        "map": "Summoner's Rift", 
        "description": "URF"
    },
    1010: {
        "map": "Summoner's Rift", 
        "description": "ARURF"
    },
    1020: {
        "map": "Summoner's Rift", 
        "description": "1FA"
    },
    1090: {
        "map": "Convergence",
        "description": "TFT"
    },
    1100: {
        "map": "Convergence",
        "description": "Ranked TFT"
    },
    1110: {
        "map": "Convergence",
        "description": "TFT"
    },
    1111: {
        "map": "Convergence",
        "description": "TFT"
    },
    1300: {
        "map": "Nexus Blitz", 
        "description": "Nexus Blitz"
    },
    2000: {
        "map": "Summoner's Rift", 
        "description": "Tutorial"
    },
    2010: {
        "map": "Summoner's Rift", 
        "description": "Tutorial"
    },
    2020: {
        "map": "Summoner's Rift", 
        "description": "Tutorial"
    },
}

spells = {
  1: "Cleanse",
  3: "Exhaust",
  4: "Flash",
  6: "Ghost",
  7: "Heal",
  11: "Smite",
  12: "Teleport",
  13: "Clarity",
  14: "Ignite",
  21: "Barrier",
  32: "Snowball",
  54: "Placeholder"
}

champIds = {
    1: "Annie",
    2: "Olaf",
    3: "Galio",
    4: "Twisted Fate",
    5: "Xin Zhao",
    6: "Urgot",
    7: "Leblanc",
    8: "Vladimir",
    9: "Fiddlesticks",
    10: "Kayle",
    11: "Master Yi",
    12: "Alistar",
    13: "Ryze",
    14: "Sion",
    15: "Sivir",
    16: "Soraka",
    17: "Teemo",
    18: "Tristana",
    19: "Warwick",
    20: "Nunu",
    21: "Miss Fortune",
    22: "Ashe",
    23: "Tryndamere",
    24: "Jax",
    25: "Morgana",
    26: "Zilean",
    27: "Singed",
    28: "Evelynn",
    29: "Twitch",
    30: "Karthus",
    31: "Cho'gath",
    32: "Amumu",
    33: "Rammus",
    34: "Anivia",
    35: "Shaco",
    36: "Dr Mundo",
    37: "Sona",
    38: "Kassadin",
    39: "Irelia",
    40: "Janna",
    41: "Gangplank",
    42: "Corki",
    43: "Karma",
    44: "Taric",
    45: "Veigar",
    48: "Trundle",
    50: "Swain",
    51: "Caitlyn",
    53: "Blitzcrank",
    54: "Malphite",
    55: "Katarina",
    56: "Nocturne",
    57: "Maokai",
    58: "Renekton",
    59: "Jarvan IV",
    60: "Elise",
    61: "Orianna",
    62: "Wukong",
    63: "Brand",
    64: "Lee'Sin",
    67: "Vayne",
    68: "Rumble",
    69: "Cassiopeia",
    72: "Skarner",
    74: "Heimerdinger",
    75: "Nasus",
    76: "Nidalee",
    77: "Udyr",
    78: "Poppy",
    79: "Gragas",
    80: "Pantheon",
    81: "Ezreal",
    82: "Mordekaiser",
    83: "Yorick",
    84: "Akali",
    85: "Kennen",
    86: "Garen",
    89: "Leona",
    90: "Malzahar",
    91: "Talon",
    92: "Riven",
    96: "Kog'Maw",
    98: "Shen",
    99: "Lux",
    101: "Xerath",
    102: "Shyvana",
    103: "Ahri",
    104: "Graves",
    105: "Fizz",
    106: "Volibear",
    107: "Rengar",
    110: "Varus",
    111: "Nautilus",
    112: "Viktor",
    113: "Sejuani",
    114: "Fiora",
    115: "Ziggs",
    117: "Lulu",
    119: "Draven",
    120: "Hecarim",
    121: "Kha'Zix",
    122: "Darius",
    126: "Jayce",
    127: "Lissandra",
    131: "Diana",
    133: "Quinn",
    134: "Syndra",
    136: "Aurelion Sol",
    141: "Kayn",
    142: "Zoe",
    143: "Zyra",
    145: "Kaisa",
    147: "Seraphine",
    150: "Gnar",
    154: "Zac",
    157: "Yasuo",
    161: "Vel'Koz",
    163: "Taliyah",
    164: "Camille",
    166: "Akshan",
    201: "Braum",
    202: "Jhin",
    203: "Kindred",
    222: "Jinx",
    223: "Tahm Kench",
    234: "Viego",
    235: "Senna",
    236: "Lucian",
    238: "Zed",
    240: "Kled",
    245: "Ekko",
    246: "Qiyana",
    254: "Vi",
    266: "Aatrox",
    267: "Nami",
    268: "Azir",
    350: "Yuumi",
    360: "Samira",
    412: "Thresh",
    420: "Illaoi",
    421: "Rek'Sai",
    427: "Ivern",
    429: "Kalista",
    432: "Bard",
    497: "Rakan",
    498: "Xayah",
    516: "Ornn",
    517: "Sylas",
    518: "Neeko",
    523: "Aphelios",
    526: "Rell",
    555: "Pyke",
    777: "Yone",
    875: "Sett",
    876: "Lillia",
    887: "Gwen",
}

champIdsReversed = {
    "Aatrox": 266,
    "Ahri": 103,
    "Akali": 84,
    "Akshan": 166,
    "Alistar": 12,
    "Amumu": 32,
    "Anivia": 34,
    "Annie": 1,
    "Aphelios": 523,
    "Ashe": 22,
    "Aurelion Sol": 136,
    "Azir": 268,
    "Bard": 432,
    "Blitzcrank": 53,
    "Brand": 63,
    "Braum": 201,
    "Caitlyn": 51,
    "Camille": 164,
    "Cassiopeia": 69,
    "Cho'gath": 31,
    "Corki": 42,
    "Darius": 122,
    "Diana": 131,
    "Draven": 119,
    "Dr Mundo": 36,
    "Ekko": 245,
    "Elise": 60,
    "Evelynn": 28,
    "Ezreal": 81,
    "Fiddlesticks": 9,
    "Fiora": 114,
    "Fizz": 105,
    "Galio": 3,
    "Gangplank": 41,
    "Garen": 86,
    "Gnar": 150,
    "Gragas": 79,
    "Graves": 104,
    "Gwen": 887,
    "Hecarim": 120,
    "Heimerdinger": 74,
    "Illaoi": 420,
    "Irelia": 39,
    "Ivern": 427,
    "Janna": 40,
    "Jarvan IV": 59,
    "Jax": 24,
    "Jayce": 126,
    "Jhin": 202,
    "Jinx": 222,
    "Kaisa": 145,
    "Kalista": 429,
    "Karma": 43,
    "Karthus": 30,
    "Kassadin": 38,
    "Katarina": 55,
    "Kayle": 10,
    "Kayn": 141,
    "Kennen": 85,
    "Kha'Zix": 121,
    "Kindred": 203,
    "Kled": 240,
    "Kog'Maw": 96,
    "Leblanc": 7,
    "Lee'Sin": 64,
    "Leona": 89,
    "Lillia": 876,
    "Lissandra": 127,
    "Lucian": 236,
    "Lulu": 117,
    "Lux": 99,
    "Malphite": 54,
    "Malzahar": 90,
    "Maokai": 57,
    "Master Yi": 11,
    "Miss Fortune": 21,
    "Wukong": 62,
    "Mordekaiser": 82,
    "Morgana": 25,
    "Nami": 267,
    "Nasus": 75,
    "Nautilus": 111,
    "Neeko": 518,
    "Nidalee": 76,
    "Nocturne": 56,
    "Nunu": 20,
    "Olaf": 2,
    "Orianna": 61,
    "Ornn": 516,
    "Pantheon": 80,
    "Poppy": 78,
    "Pyke": 555,
    "Qiyana": 246,
    "Quinn": 133,
    "Rakan": 497,
    "Rammus": 33,
    "Rek'Sai": 421,
    "Rell": 526,
    "Renekton": 58,
    "Rengar": 107,
    "Riven": 92,
    "Rumble": 68,
    "Ryze": 13,
    "Samira": 360,
    "Sejuani": 113,
    "Senna": 235,
    "Seraphine": 147,
    "Sett": 875,
    "Shaco": 35,
    "Shen": 98,
    "Shyvana": 102,
    "Singed": 27,
    "Sion": 14,
    "Sivir": 15,
    "Skarner": 72,
    "Sona": 37,
    "Soraka": 16,
    "Swain": 50,
    "Sylas": 517,
    "Syndra": 134,
    "Tahm Kench": 223,
    "Taliyah": 163,
    "Talon": 91,
    "Taric": 44,
    "Teemo": 17,
    "Thresh": 412,
    "Tristana": 18,
    "Trundle": 48,
    "Tryndamere": 23,
    "Twisted Fate": 4,
    "Twitch": 29,
    "Udyr": 77,
    "Urgot": 6,
    "Varus": 110,
    "Vayne": 67,
    "Veigar": 45,
    "Vel'Koz": 161,
    "Vi": 254,
    "Viego": 234,
    "Viktor": 112,
    "Vladimir": 8,
    "Volibear": 106,
    "Warwick": 19,
    "Xayah": 498,
    "Xerath": 101,
    "Xin Zhao": 5,
    "Yasuo": 157,
    "Yone": 777,
    "Yorick": 83,
    "Yuumi": 350,
    "Zac": 154,
    "Zed": 238,
    "Ziggs": 115,
    "Zilean": 26,
    "Zoe": 142,
    "Zyra": 143,
}

champEmojis = {
    "Akshan": "<:Akshan:871462616382468216>",
    "Akali": "<:Akali:813197313782579200>",
    "Alistar": "<:Alistar:813197313874067477>",
    "Amumu": "<:Amumu:813197314410676304>",
    "Aatrox": "<:Aatrox:813197314419064912>",
    "Annie": "<:Annie:813197314465988609>",
    "Ahri": "<:Ahri:813197314519728169>",
    "Azir": "<:Azir:813197314528378881>",
    "Aurelion Sol": "<:AurelionSol:813197314570584074>",
    "Aphelios": "<:Aphelios:813197314578841630>",
    "Braum": "<:Braum:813197315027894293>",
    "Bard": "<:Bard:813197315136684032>",
    "Camille": "<:Camille:813197315673161808>",
    "Cassiopeia": "<:Cassiopeia:813197315682074645>",
    "Ashe": "<:Ashe:813197315682598942>",
    "Anivia": "<:Anivia:813197315912892426>",
    "Blitzcrank": "<:Blitzcrank:813197316026138634>",
    "Dr Mundo": "<:DrMundo:813197316378853386>",
    "Ekko": "<:Ekko:813197316436918332>",
    "Jax": "<:Jax:813197316470734879>",
    "Illaoi": "<:Illaoi:813197316499832873>",
    "Jhin": "<:Jhin:815233434788167750>",
    "Kha'Zix": "<:KhaZix:815233359260942376>",
    "Qiyana": "<:Qiyana:815233454001750037>",
    "Vel'Koz": "<:VelKoz:815233494732767272>",
    "Rek'Sai": "<:RekSai:815233471416762388>",
    "Brand": "<:Brand:813197316503634020>",
    "Draven": "<:Draven:813197316516478986>",
    "Ivern": "<:Ivern:813197316553965578>",
    "Gnar": "<:Gnar:813197316601151488>",
    "Graves": "<:Graves:813197316604559390>",
    "Fiora": "<:Fiora:813197316625530981>",
    "Galio": "<:Galio:813197316626186261>",
    "Elise": "<:Elise:813197316651089930>",
    "Caitlyn": "<:Caitlyn:813197316655153186>",
    "Fiddlesticks": "<:Fiddlesticks:813197316899078146>",
    "Kaisa": "<:Kaisa:813197316923588618>",
    "Irelia": "<:Irelia:813197316953604167>",
    "Jarvan IV": "<:JarvanIV:813197317003149382>",
    "Jinx": "<:Jinx:813197317066457118>",
    "Janna": "<:Janna:813197317137235968>",
    "Evelynn": "<:Evelynn:813197317142347786>",
    "Jayce": "<:Jayce:813197317146542092>",
    "Gragas": "<:Gragas:813197317154930688>",
    "Fizz": "<:Fizz:813197317175246850>",
    "Diana": "<:Diana:813197317322440715>",
    "Heimerdinger": "<:Heimerdinger:813197317402394665>",
    "Corki": "<:Corki:813197317477105704>",
    "Gangplank": "<:Gangplank:813197317511446528>",
    "Gwen": "<:Gwen:832985160945106974>",
    "Garen": "<:Garen:813197317544476702>",
    "Ezreal": "<:Ezreal:813197317565579336>",
    "Darius": "<:Darius:813197317569511454>",
    "Kalista": "<:Kalista:813197317599526932>",
    "Hecarim": "<:Hecarim:813197317633081394>",
    "Cho'gath": "<:Chogath:813197317792202784>",
    "Karma": "<:Karma:813197397957935125>",
    "Kayle": "<:Kayle:813197896769994774>",
    "Kindred": "<:Kindred:813197897013264405>",
    "Kayn": "<:Kayn:813197897054683168>",
    "Leblanc": "<:Leblanc:813197897100427266>",
    "Kled": "<:Kled:813197897104883753>",
    "Karthus": "<:Karthus:813197897117597757>",
    "Lee'Sin": "<:LeeSin:813197897247227914>",
    "KhaZix": "<:KhaZix:813197897268199454>",
    "Morgana": "<:Morgana:813197897302147093>",
    "Kog'Maw": "<:KogMaw:813197897398222858>",
    "Mordekaiser": "<:Mordekaiser:813197897410543667>",
    "Kennen": "<:Kennen:813197897410805780>",
    "Leona": "<:Leona:813197897420111893>",
    "Kassadin": "<:Kassadin:813197897436364861>",
    "Lissandra": "<:Lissandra:813197897528115210>",
    "Lucian": "<:Lucian:813197897545941012>",
    "Quinn": "<:Quinn:813197897558523905>",
    "Orianna": "<:Orianna:813197897641492480>",
    "Master Yi": "<:MasterYi:813197897670721556>",
    "Malphite": "<:Malphite:813197897704276049>",
    "Pantheon": "<:Pantheon:813197897717776444>",
    "Poppy": "<:Poppy:813197897754476594>",
    "RekSai": "<:RekSai:813197897813590037>",
    "Ornn": "<:Ornn:813197897922248734>",
    "Nocturne": "<:Nocturne:813197897939943435>",
    "Nautilus": "<:Nautilus:813197897990537246>",
    "Maokai": "<:Maokai:813197898036543500>",
    "Nunu": "<:Nunu:813197898090283068>",
    "Nami": "<:Nami:813197898132881450>",
    "Rengar": "<:Rengar:813197898162372638>",
    "Lulu": "<:Lulu:813197898182688788>",
    "Ryze": "<:Ryze:813197898190684221>",
    "Riven": "<:Riven:813197898228695080>",
    "Rakan": "<:Rakan:813197898384277524>",
    "Malzahar": "<:Malzahar:813197898396860436>",
    "Rell": "<:Rell:813197898397122560>",
    "Katarina": "<:Katarina:813197898485465139>",
    "Rumble": "<:Rumble:813197898492674108>",
    "Olaf": "<:Olaf:813197898510630922>",
    "Lillia": "<:Lillia:813197898568302592>",
    "Samira": "<:Samira:871460516525113354>",
    "Pyke": "<:Pyke:813197898657169438>",
    "Nasus": "<:Nasus:813197898660577280>",
    "Lux": "<:Lux:813197898669621258>",
    "Neeko": "<:Neeko:813197898715365376>",
    "Nidalee": "<:Nidalee:813197898724409344>",
    "Renekton": "<:Renekton:813197898841718825>",
    "Rammus": "<:Rammus:813197898887331840>",
    "Miss Fortune": "<:MissFortune:813197899148165150>",
    "Sejuani": "<:Sejuani:813197990876413952>",
    "Senna": "<:Senna:813198360240193606>",
    "Tahm Kench": "<:TahmKench:813198360394727445>",
    "Sett": "<:Sett:813198360437719041>",
    "Swain": "<:Swain:813198360705368084>",
    "Warwick": "<:Warwick:813198360784928820>",
    "Zac": "<:Zac:813198360794234891>",
    "Twitch": "<:Twitch:813198360848760883>",
    "Sona": "<:Sona:813198360869470228>",
    "Zed": "<:Zed:813198360948637717>",
    "Shen": "<:Shen:813198360965414912>",
    "Taric": "<:Taric:813198361011552316>",
    "Seraphine": "<:Seraphine:813198361066340354>",
    "Soraka": "<:Soraka:813198361095307334>",
    "Syndra": "<:Syndra:813198361099632640>",
    "Sylas": "<:Sylas:813198361141313557>",
    "Taliyah": "<:Taliyah:813198361149964308>",
    "Wukong": "<:Wukong:813198361208946718>",
    "Viktor": "<:Viktor:813198361246695484>",
    "Sivir": "<:Sivir:813198361275400222>",
    "Xayah": "<:Xayah:813198361288507412>",
    "Trundle": "<:Trundle:813198361288900619>",
    "Urgot": "<:Urgot:813198361305940038>",
    "Yasuo": "<:Yasuo:813198361380651018>",
    "Ziggs": "<:Ziggs:813198361393627148>",
    "VelKoz": "<:VelKoz:813198361394020362>",
    "Tryndamere": "<:Tryndamere:813198361431113779>",
    "Skarner": "<:Skarner:813198361464537138>",
    "Yorick": "<:Yorick:813198361490489354>",
    "Varus": "<:Varus:813198361506349096>",
    "Veigar": "<:Veigar:813198361518931988>",
    "Twisted Fate": "<:TwistedFate:813198361544097832>",
    "Vi": "<:Vi:813198361544359936>",
    "Volibear": "<:Volibear:815221503602851850>",
    "Udyr": "<:Udyr:813198361565593641>",
    "Sion": "<:Sion:813198361598623766>",
    "Zilean": "<:Zilean:813198361724190750>",
    "Tristana": "<:Tristana:813198361750405120>",
    "Singed": "<:Singed:813198361795493888>",
    "Shaco": "<:Shaco:813198361799819294>",
    "Vladimir": "<:Vladimir:813198361817514055>",
    "Yuumi": "<:Yuumi:813198361851199488>",
    "Shyvana": "<:Shyvana:813198361858539531>",
    "Thresh": "<:Thresh:813198361905594422>",
    "Yone": "<:Yone:813198361967591464>",
    "Xin Zhao": "<:XinZhao:813198362009665567>",
    "Teemo": "<:Teemo:813198362085163008>",
    "Vayne": "<:Vayne:813198362131038218>",
    "Xerath": "<:Xerath:813198362160529428>",
    "Viego": "<:Viego:813198362169835560>",
    "Talon": "<:Talon:813198362308116500>",
    "Zoe": "<:Zoe:813198534052413490>",
    "Zyra": "<:Zyra:813198664432091137>",
}

spellEmojis = {
  "Cleanse": "<:Cleanse:813606194425102366>",
  "Exhaust": "<:Exhaust:813606194291146752>",
  "Flash": "<:Flash:813606194278825984>",
  "Ghost": "<:Ghost:813606194382897152>",
  "Heal": "<:Heal:813606194388140093>",
  "Smite": "<:Smite:813606194685018120>",
  "Teleport": "<:Teleport:813606194702450708>",
  "Clarity": "<:Clarity:813606194248810526>",
  "Ignite": "<:Ignite:813606194471370762>",
  "Barrier": "<:Barrier:813606194354454568>",
  "Snowball": "<:Snowball:813606194743738418>",
  "Placeholder": "⬜"
}

regionEmojis = {
    "br1": "<:BR:872883833555521588>",
    "eun1": "<:EUNE:872883833782034482>",
    "euw1": "<:EUW:872883833756868649>",
    "jp1": "<:JP:872883833719128124>",
    "kr": "<:KR:872883833735892992>",
    "la1": "<:LAN:872883833773649960>",
    "la2": "<:LAS:872883833505206293>",
    "na1": "<:NA:872883833731690506>",
    "oc1": "<:OCE:872883833794592818>",
    "ru": "<:RU:872883833878503494>",
    "tr1": "<:TR:872883833752662046>"
}

diamonds = {
    "blue": "<:blue_diamond:815170368574324756>",
    "red": "<:red_diamond:815169433785335808>"
}

hexcolors = {
    "🔴": Colour.red(),
    "🟠": Colour.orange(),
    "🟡": Colour.gold(),
    "🟢": Colour.green(),
    "🔵": Colour.blue(),
    "🟣": Colour.purple(),
    "🟤": Colour.dark_orange(),
    "⚫": 0x000000,
    "⚪": 0xfefefe
}

regionList = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "ru", "tr1"]

regionsAbbrev = {
    "BR": "br1",
    "EUNE": "eun1",
    "EUW": "euw1",
    "JP": "jp1",
    "KR": "kr",
    "LAN": "la1",
    "LAS": "la2",
    "NA": "na1",
    "OCE": "oc1",
    "RU": "ru",
    "TR": "tr1",
}

regionsIntro = {
    "br1": "**BR** (Brazil)",
    "eun1": "**EUNE** (Europe Nordic & East)",
    "euw1": "**EUW** (Europe West)",
    "jp1": "**JP** (Japan)",
    "kr": "**KR** (Korea)",
    "la1": "**LAN** (Latin America North)",
    "la2": "**LAS** (Latin America South)",
    "na1": "**NA** (North America)",
    "oc1": "**OCE** (Oceania)",
    "ru": "**RU** (Russia)",
    "tr1": "**TR** (Turkey)"
}

invalidRegionMsg = """
**BR** (Brazil)
**EUNE** (Europe Nordic & East)
**EUW** (Europe West)
**JP** (Japan)
**KR** (Korea)
**LAN** (Latin America North)
**LAS** (Latin America South)
**NA** (North America)
**OCE** (Oceania)
**RU** (Russia)
**TR** (Turkey)
"""

### FUNCTIONS
def checkValidRegion(region):
    """
    Checks if the region is valid.
    If not valid, returns False.
    If valid, returns the region string.
    --------------------
    region: The region to check
    """
    
    availRegions = regionList
    # https://leagueoflegends.fandom.com/wiki/Servers
    if region.lower() in availRegions:
        return region.lower()
    if region.upper() in regionsAbbrev.keys():
        return regionsAbbrev[region.upper()]
    else:
        return False

def discordManagerFinder(discordServer):
    """
    When given a discordServer ID,
    Returns a discordManager object that is connected to that discord server
    --------------------
    discordServer: The ID of the discord server
    """
    for discordManager in discordManagerList:
        if discordManager.discordServer == discordServer:
            return discordManager

    return False

def matchDictReader(matchDict):
    """
    Goes through the match information, and converts "IDs" into knowable LoL langauage.
    --------------------
    matchDict: The match dictionary to read through
    """
    returnDict = {}

    returnDict["gameId"] = matchDict["gameId"]
    returnDict["map"] = maps[matchDict["mapId"]]
    returnDict["gameType"] = types[matchDict["gameType"]]
    try:
        returnDict["gameQueue"] = queues[matchDict["gameQueueConfigId"]]
    except KeyError:
        returnDict["gameQueue"] = {
            "description": "Custom",
            "map": returnDict["map"]["mapName"]
        }

    participants = []
    team1 = []
    team2 = []

    for player in matchDict["participants"]:
        temp = {}
        temp["spell1"] = spells[player["spell1Id"]]
        temp["spell2"] = spells[player["spell2Id"]]
        temp["champion"] = champIds[player["championId"]]
        temp["summonerName"] = player["summonerName"]
        temp["summonerId"] = player["summonerId"]
        temp["isBot"] = player["bot"]
        if player["teamId"] == 100:
            team1.append(temp)
        else:
            team2.append(temp)
    
    participants.append(team1)
    participants.append(team2)
    
    returnDict["participants"] = participants
    returnDict["gameStartTime"] = matchDict["gameStartTime"]

    return returnDict

def timeChanger(gameStartTime):
    """
    Converts gameStartTime into the current game length. Returns (min, sec) tuple
    --------------------
    gameStartTime: The game start time
    """
    start = datetime.datetime.fromtimestamp(gameStartTime/1000)
    cur = datetime.datetime.now()
    timeDelta = cur - start
    seconds_in_day = 24 * 60 * 60

    minsec = divmod(timeDelta.days * seconds_in_day + timeDelta.seconds, 60)
    minute = str(minsec[0])
    second = str(minsec[1])
    if len(minute) == 1:
        minute = "0" + minute
    if len(second) == 1:
        second = "0" + second
    
    return (minute, second)

async def executePeriodically(time, func):
    """
    The given function will be executed every time
    --------------------
    time: How often the function will be executed
    func: Function that will be periodically executed
    """
    while True:
        await asyncio.sleep(time)
        await func()



### DATABASE FUNCTIONS

# Store Summoner without Discord User into DataBase
def _storeSummoner(summoner, serverId):
    new_DBUser = DBUser(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        summonerLevel = summoner.summonerLevel, region = summoner.region)
    new_DBUser.save()

storeSummoner = sync_to_async(_storeSummoner, thread_sensitive=True)

# Store Summoner with Discord User into DataBase
def _storeSummonerUser(summoner, serverId, discordUser):
    new_DBUser = DBUser(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        summonerLevel = summoner.summonerLevel, region = summoner.region, discordUser = discordUser)
    new_DBUser.save()

storeSummonerUser = sync_to_async(_storeSummonerUser, thread_sensitive=True)

# Store Summoner with Discord User into DataBase
def _giveSummonerUser(summoner, serverId, discordUser):
    player = DBUser.objects.get(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        region = summoner.region)
    if player.discordUesr == -1:
        player.discordUser = discordUser
        player.save()
    else:
        raise AlreadyLinkedAccount

giveSummonerUser = sync_to_async(_giveSummonerUser, thread_sensitive=True)

# Get from DataBase to Summoner (disregards Discord User data)
def _getSummoner(summoner, serverId):
    player = DBUser.objects.get(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        region = summoner.region)
    summoner = Summoner(player.returnSummonerInfo())
    return summoner

getSummoner = sync_to_async(_getSummoner, thread_sensitive=True)

# Get from DataBase to Summoner (regards Discord User data)
def _getSummonerUser(summoner, serverId, discordUser):
    player = DBUser.objects.get(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        region = summoner.region, discordUser=discordUser)
    summoner = Summoner(player.returnSummonerInfo())
    return summoner

getSummonerUser = sync_to_async(_getSummonerUser, thread_sensitive=True)

# Check if Summoner is owned by a user
def _isOwnedSummoner(summoner, serverId):
    player = DBUser.objects.get(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        region = summoner.region)
    return player.discordUser != -1

isOwnedSummoner = sync_to_async(_isOwnedSummoner, thread_sensitive=True)

# Delete Summoner from DataBase (disregards Discord User data)
def _deleteSummoner(summoner, serverId):
    player = DBUser.objects.get(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        region = summoner.region)
    player.delete()

deleteSummoner = sync_to_async(_deleteSummoner, thread_sensitive=True)

# Delete Summoner from DataBase (regards Discord User data)
def _deleteSummonerUser(summoner, serverId, discordUser):
    player = DBUser.objects.get(discordServer=serverId, summonerName = summoner.summonerName, summonerId = summoner.summonerId, \
        region = summoner.region, discordUser=discordUser)
    player.delete()

deleteSummonerUser = sync_to_async(_deleteSummonerUser, thread_sensitive=True)

# Get Summoners of one discord server
def _discordServerSummoners(serverId):
    summoners = []
    for region in regionList:
        players = DBUser.objects.filter(discordServer=serverId, region=region)
        for player in players:
            summoner = Summoner(player.returnSummonerInfo())
            summoners.append((summoner, player.discordUser))
    return summoners

discordServerSummoners = sync_to_async(_discordServerSummoners, thread_sensitive=True)

# Get Summoners of one discord server and discord user
def _discordServerUserSummoners(serverId, discordUser):
    summoners = []
    for region in regionList:
        players = DBUser.objects.filter(discordServer=serverId, discordUser=discordUser, region=region)
        for player in players:
            summoner = Summoner(player.returnSummonerInfo())
            summoners.append(summoner)
    return summoners

discordServerUserSummoners = sync_to_async(_discordServerUserSummoners, thread_sensitive=True)

# Get Summoners of one discord server and many discord user
def _discordServerUsersSummoners(serverId, discordUsers):
    regionSummoners = {}
    for region in regionList:
        regionSummoners[region] = []

    players = DBUser.objects.filter(discordServer=serverId)
    for player in players:
        if player.discordUser in discordUsers:
            summoner = Summoner(player.returnSummonerInfo())
            regionSummoners[player.region].append((summoner, player.discordUser))

    summoners = []
    for region in regionList:
        summoners += regionSummoners[region]

    return summoners

discordServerUsersSummoners = sync_to_async(_discordServerUsersSummoners, thread_sensitive=True)


### CLASSES
class Summoner:
    """
    Manages Summoner Info
    --------------------
    __init__ METHODS

    1. Get Information from Riot API
    unofficialSummonerName: A summoner name that is not the official name, due to difference in case or spaces
    unofficialRegion: An unofficial region of the summoner

    2. Get Information from pre-stored Data Base
    summonerName: models.CharField() official summoner name
    summonerId: models.CharField() summoner ID
    summonerLevel: models.IntegerField() summoner level
    region: models.CharField() official region
    (WARNING: This method does not check if there is an existing summoner with these attributes)
    """

    def __init__(self, *args):
        if len(args) == 2: # METHOD 1
            unofficialSummonerName = args[0]
            unofficialRegion = args[1]
            region = checkValidRegion(unofficialRegion)
            if region is False:
                raise InvalidRegion

            URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + unofficialSummonerName + "?api_key=" + APIKey
            response = requests.get(URL)
            
            if response.status_code == 200:
                infoDict = json.loads(response.text)
                
                self.summonerName = infoDict['name']
                self.summonerId = infoDict['id']
                self.summonerLevel = infoDict['summonerLevel']
                self.region = region
                print(infoDict)
            else:
                raise InvalidSummonerName
        
        else: # METHOD 2
            if len(args) == 1: # When the information is put in a list of list ( args = [[name, id, lv, region]] )
                self.summonerName = args[0][0]
                self.summonerId = args[0][1]
                self.summonerLevel = args[0][2]
                self.region = args[0][3]
            else: # When the information is put in one list ( args = [name, id, lv, regions] )
                self.summonerName = args[0]
                self.summonerId = args[1]
                self.summonerLevel = args[2]
                self.region = args[3]
    
    def __eq__(self, other):
        return self.summonerName == other.summonerName and self.summonerId == other.summonerId and self.region == other.region

    def getProfileIcon(self):
        # Need to make new object (because user could have changed profile icon)\
        URL = "https://" + self.region + ".api.riotgames.com/lol/summoner/v4/summoners/" + self.summonerId + "?api_key=" + APIKey
        response = requests.get(URL)
        
        if response.status_code == 200:
            infoDict = json.loads(response.text)
            return infoDict['profileIconId']
        else:
            raise InvalidSummonerId

    def getMatchInfo(self, matchManager, circleManager=None, store=False):
        """
        Gets Match Info of what summoner is currently playing.
        Also, makes a new Match object if there isn't one yet, if wanting to store.
        Returns Game ID of the summoner's match, and raises InvalidMatch if not in live match
        --------------------
        matchManager: MatchManager object that is used for creating new Match object
        store: Boolean that decides whether the Match object will be stored in matchManager.matches or not
        """
        URL = "https://" + self.region + ".api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + self.summonerId + "?api_key=" + APIKey
        response = requests.get(URL)

        if response.status_code == 200:
            infoDict = json.loads(response.text)
            # print(infoDict)
            infoDict = matchDictReader(infoDict)
            # print(infoDict)
            if store:
                # Check if match already stored
                # if matchManager.matchExists(gameId=infoDict["gameId"])
                try:
                    matchManager.append(gameId=infoDict["gameId"], infoDict=infoDict, region=self.region, isCircled=True, circleManager=circleManager, circle=None)
                except LoadingScreen:
                    raise InvalidMatch
            else:
                matchManager.create(gameId=infoDict["gameId"], infoDict=infoDict, region=self.region)

            return infoDict["gameId"]
        else:
            raise InvalidMatch
    
    def presentSummoner(self, matchManager, gameId, requestedTime):
        """
        Presents information of the summoner's live match.
        WARNING: Will not check if the summoner is in a live game or not; will automatically assume the summoner is
        --------------------
        matchManager: MatchManager object that is used for creating new Match object
        gameId: ID of the LoL match
        requestedTime: (min, sec) tuple of the current game length
        """

        matchDict = matchManager.matches[gameId]
        match = matchDict["match"]
        infoDict = match.infoDict
        if match.isCircled:
            returnStr = "{0}: {1} | Playing: ** {2} ** | In Game: {3} | {4}:{5}".format(infoDict["gameQueue"]["description"], \
            infoDict["gameQueue"]["map"], match.summonerChamp(self.summonerName), match.circle.emoji, \
            requestedTime[0], requestedTime[1])
        else:
            returnStr = "{0}: {1} | Playing: ** {2} ** | {4}:{5}".format(infoDict["gameQueue"]["description"], \
            infoDict["gameQueue"]["map"], match.summonerChamp(self.summonerName), \
            requestedTime[0], requestedTime[1])
        
        return returnStr

class Circle:
    """
    Circle (🔴) that will be attributed to stored live matches
    --------------------
    emoji: The string emoji (🔴) that will be used
    hexcolor: The hexcolor of the circle that will be used for Embed
    available: Boolean that decides whether the circle is available or is used by another match
    """

    def __init__(self, emoji, hexcolor=0xb09e99):
        self.emoji = emoji
        self.hexcolor = hexcolor
        self.available = True
    
    def __eq__(self, other):
        return self.emoji == other.emoji

    def matchesEmoji(self, emoji):
        return self.emoji == emoji
    
class CircleManager:
    """
    Manages Circle Objects in one discord server
    --------------------
    discordServer: The ID of the discord server
    allCircles: List of Circle objects that could be used
    """

    def __init__(self, discordServer):
        # Emoji Circles that will be used: 🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪
        self.discordServer = discordServer
        self.allCircles = [
            Circle("🔴", Colour.red()),
            Circle("🟠", Colour.orange()),
            Circle("🟡", Colour.gold()),
            Circle("🟢", Colour.green()),
            Circle("🔵", Colour.blue()),
            Circle("🟣", Colour.purple()),
            Circle("🟤", Colour.dark_orange()),
            Circle("⚫", 0x000000),
            Circle("⚪", 0xfefefe)
        ]
    
    def getAvailableEmojis(self):
        return [circle for circle in self.allCircles if circle.available]

    def distribEmoji(self):
        availEmojis = self.getAvailableEmojis()
        choosedCircle = random.choice(availEmojis)

        for index in range(len(self.allCircles)): # Need to disable availibility
            circle = self.allCircles[index]
            # if circle.matchesEmoji(choosedCircle.emoji):
            if circle == choosedCircle:
                circle.available = False
        
        return choosedCircle

class Match:
    """
    Manages Match Info
    --------------------
    gameId: ID of LoL Game
    infoDict: A dictionary that has all of the match information
    region: Region of the match
    isCircled: Boolean that decides if the match is attributed to a circle
    circle: If isCircled is True, the Circle object that the match is attributed to
    """
    
    def __init__(self, gameId, infoDict, region, isCircled=False, circle=None):
        self.gameId = gameId
        self.infoDict = infoDict
        self.region = region
        self.isCircled = isCircled
        self.circle = circle
    
    def summonerChamp(self, summonerName):
        """
        Presents champion information of the summoner's live match
        Returns False if the summoner is not in that match
        --------------------
        summonerName: Summoner name that will be investigated to return champion
        """
        # print(self.infoDict["participants"])
        for team in self.infoDict["participants"]:
            for player in team:
                if player["summonerName"] == summonerName:
                    return player["champion"]
        
        return False
    
    def firstParticipant(self):
        """
        Finds the first non-bot first participant of the match
        Returns SummonerDict
        """
        for team in self.infoDict["participants"]:
            for player in team:
                if player["isBot"] is False:
                    return player
    
    def presentMatch(self):
        """
        Presents information of the live match, including the use of emojis
        """
        if not self.isCircled:
            raise NotCircled
        
        infoDict = self.infoDict

        timeTuple = timeChanger(infoDict["gameStartTime"])
        returnDict = {
            "Color": self.circle.hexcolor,
            "Circle": self.circle.emoji,
            "MatchType": infoDict["gameQueue"]["description"] + " : " + infoDict["gameQueue"]["map"],
            "Time": timeTuple[0] + ":" + timeTuple[1]
        }

        participants = infoDict["participants"]
        # Add Blue Team Info
        blueTeam = participants[0]
        returnDict["BlueTeam"] = participants[0]

        # Add Red Team Info
        returnDict["RedTeam"] = participants[1]

        return returnDict

class MatchManager:
    """
    Manages Match Objects in one discord server.
    --------------------
    discordServer: The ID of the discord server
    matches: Dictionary that maps gameId to a dictionary containing 
        Match object,
        game time when the information was last requested,
        counter in which how many times the match was requested <-- MIGHT NOT USE
    """

    def __init__(self, discordServer):
        self.discordServer = discordServer

        self.matches = {}

    def matchExists(self, gameId):
        """
        Returns if the gameId of a match is from a match in self.matches
        --------------------
        gameId: ID of the LoL match
        """
        return gameId in self.matches.keys()

    def circleMatch(self, circle):
        """
        Returns matchDict of the match that contains the circle "circle"
        --------------------
        circle: Circle object of the match that is being found
        """
        for gameId, matchDict in self.matches.items():
            # if circle.matchesEmoji(matchDict["match"].circle.emoji):
            if circle == matchDict["match"].circle:
                return matchDict
        return False
    
    def circleEmojiMatch(self, circleEmoji):
        """
        Returns matchDict of the match that contains the circle with circleEmoji
        --------------------
        circleEmoji: Circle emoji of the match that is being found
        """
        for gameId, matchDict in self.matches.items():
            # if circle.matchesEmoji(matchDict["match"].circle.emoji):
            if circleEmoji == matchDict["match"].circle.emoji:
                return matchDict
        return False
    
    def updateTime(self, gameId):
        """
        Updates the current game length of the game with gameId
        Returns the updated time
        WARNING: Will not check if gameId is a valid key for self.matches
        --------------------
        gameId: ID of the LoL match that will get its game length updated
        """
        match = self.matches[gameId]["match"]
        self.matches[gameId]["matchTime"] = timeChanger(match.infoDict["gameStartTime"])
        return self.matches[gameId]["matchTime"]

    def create(self, gameId, infoDict, region, isCircled=False, circle=None):
        """
        Creates a Match object and returns it
        """
        match = Match(gameId=gameId, infoDict=infoDict, region=region, isCircled=isCircled, circle=circle)
        return match
    
    def append(self, gameId, infoDict, region, isCircled=False, circleManager=None, circle=None):
        """
        Creates a Match object and stores it in self.matches
        """

        if self.matchExists(gameId): # Does not store if already existing
            return False
        else:
            # Creates a circle for the Match
            if isCircled and circle is None:
                circle = circleManager.distribEmoji()

            match = self.create(gameId=gameId, infoDict=infoDict, region=region, isCircled=isCircled, circle=circle)

            if int(match.infoDict["gameStartTime"]) == 0: # Game is still in loading screen
                raise LoadingScreen

            temp = {}
            temp["match"] = match
            temp["updateRequest"] = True
            self.matches[gameId] = temp
            self.updateTime(gameId)
            return temp

    def getAll(self, circleManager, summonersRegionList):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns dictionary with gameId as key and List of summonerName, presentSummoner dictionary as value
        --------------------
        circleManager: Manager of the circles; used to distribute 
        summonersRegionList: Dictionary of region as key and List of Summoners as value
        """
        gameIdList = set()  # Will be used to initialize match's updateRequest to True
        sortedByGame = {}
        for region, players in summonersRegionList.items():
            for summoner in players:
                try:
                    gameId = summoner.getMatchInfo(self, circleManager, store=True)
                    matchInfo = self.matches[gameId]

                    gameIdList.add(gameId)
                    
                    # Getting the current game length of the match
                    requestedTime = None
                    if matchInfo["updateRequest"]:
                        # Update the time
                        requestedTime = self.updateTime(gameId)
                        matchInfo["updateRequest"] = False
                    else:
                        # Use the orignial matchtime
                        requestedTime = matchInfo["matchTime"]
                    
                    if gameId not in sortedByGame.keys():
                        sortedByGame[gameId] = []
                    
                    temp = {
                        "summonerName": summoner.summonerName,
                        "presentSummoner": summoner.presentSummoner(self, gameId, requestedTime)
                    }
                    sortedByGame[gameId].append(temp)
                except InvalidRegion:
                    print("REGION INVALID")
                except InvalidSummonerName:
                    print("SUMMONER NAME INVALID")
                except InvalidMatch:
                    print("MATCH INVALID")
        
        for gameId in gameIdList:
            self.matches[gameId]["updateRequest"] = True
        
        return sortedByGame

    async def getAll2(self, circleManager, discordServer):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns dictionary with gameId as key and List of summonerName, presentSummoner dictionary as value
        --------------------
        circleManager: Manager of the circles; used to distribute 
        discordServer: The ID of the discord server
        """
        gameIdList = set()  # Will be used to initialize match's updateRequest to True
        sortedByGame = {}

        players = await discordServerSummoners(discordServer)

        for summoner, discordUser in players:
            try:
                gameId = summoner.getMatchInfo(self, circleManager, store=True)
                matchInfo = self.matches[gameId]

                gameIdList.add(gameId)
                
                # Getting the current game length of the match
                requestedTime = None
                if matchInfo["updateRequest"]:
                    # Update the time
                    requestedTime = self.updateTime(gameId)
                    matchInfo["updateRequest"] = False
                else:
                    # Use the orignial matchtime
                    requestedTime = matchInfo["matchTime"]
                
                if gameId not in sortedByGame.keys():
                    sortedByGame[gameId] = []
                
                temp = {
                    "summonerName": summoner.summonerName,
                    "presentSummoner": summoner.presentSummoner(self, gameId, requestedTime),
                    "discordUser": discordUser
                }
                sortedByGame[gameId].append(temp)
            except InvalidRegion:
                print("REGION INVALID")
            except InvalidSummonerName:
                print("SUMMONER NAME INVALID")
            except InvalidMatch:
                print("MATCH INVALID")
        
        for gameId in gameIdList:
            self.matches[gameId]["updateRequest"] = True
        
        return sortedByGame
    
    async def getSome(self, circleManager, discordServer, querySet):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns dictionary with gameId as key and List of summonerName, presentSummoner dictionary as value
        --------------------
        circleManager: Manager of the circles; used to distribute 
        discordServer: The ID of the discord server
        """
        gameIdList = set()  # Will be used to initialize match's updateRequest to True
        sortedByGame = {}

        players = querySet

        for summoner, discordUser in players:
            try:
                gameId = summoner.getMatchInfo(self, circleManager, store=True)
                matchInfo = self.matches[gameId]

                gameIdList.add(gameId)
                
                # Getting the current game length of the match
                requestedTime = None
                if matchInfo["updateRequest"]:
                    # Update the time
                    requestedTime = self.updateTime(gameId)
                    matchInfo["updateRequest"] = False
                else:
                    # Use the orignial matchtime
                    requestedTime = matchInfo["matchTime"]
                
                if gameId not in sortedByGame.keys():
                    sortedByGame[gameId] = []
                
                temp = {
                    "summonerName": summoner.summonerName,
                    "presentSummoner": summoner.presentSummoner(self, gameId, requestedTime),
                    "discordUser": discordUser
                }
                sortedByGame[gameId].append(temp)
            except InvalidRegion:
                print("REGION INVALID")
            except InvalidSummonerName:
                print("SUMMONER NAME INVALID")
            except InvalidMatch:
                print("MATCH INVALID")
        
        for gameId in gameIdList:
            self.matches[gameId]["updateRequest"] = True
        
        return sortedByGame

    def presentAll(self, circleManager, summonersRegionList):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns string of summoner and summoner live match information for each summoner
        --------------------
        circleManager: Manager of the circles; used to distribute 
        summonersRegionList: Dictionary of region as key and List of Summoners as value
        """
        returnStr = ""
        gamesDict = self.getAll(circleManager, summonersRegionList)
        for gameId, summonerDictList in gamesDict.items():
            for summonerDict in summonerDictList:
                returnStr += summonerDict["summonerName"]
                returnStr += "\n"
                returnStr += summonerDict["presentSummoner"]
                returnStr += "\n\n"

        return returnStr
    
    def testPrintMatch(self):
        """
        Test usage of how the template of !opgg match would look like
        """
        returnStr = ""
        returnStr += "**In Game: 🔴** \n"
        returnStr += "_Ranked Solo: Summoner's Rift_                  14:59\n"
        returnStr += "\n🟦 **Blue Team**\n"
        returnStr += "🟦 <:Aatrox:813197314419064912> FireKnight25         <:Flash:813606194278825984> <:Snowball:813606194743738418>\n"
        returnStr += "🟦 <:Aatrox:813197314419064912> FireKnight25         <:Flash:813606194278825984> <:Snowball:813606194743738418>\n"
        returnStr += "🟦 <:Aatrox:813197314419064912> FireKnight25         <:Flash:813606194278825984> <:Snowball:813606194743738418>\n"
        returnStr += "\n🟥 **Red Team**\n"
        returnStr += "🟥 <:Gnar:813197316601151488> FireKnight          <:Ignite:813606194471370762> <:Flash:813606194278825984>\n"
        returnStr += "🟥 <:Gnar:813197316601151488> FireKnight          <:Ignite:813606194471370762> <:Flash:813606194278825984>\n"
        returnStr += "🟥 <:Gnar:813197316601151488> FireKnight          <:Ignite:813606194471370762> <:Flash:813606194278825984>\n"
        return returnStr
   
    async def presentMatch(self, circleEmoji, discordServer):
        """
        Gives Live Match Information of a match associated to do circle
        Will be used for !opgg match command
        Returns Discord Embed object that will be sent
        --------------------
        circleEmoji: Circle emoji of the match that will be presented
        discordServer: The ID of the discord server
        """
        matchDict = self.circleEmojiMatch(circleEmoji)
        if matchDict is False:
            raise InvalidCircle
        matchInfo = matchDict["match"].presentMatch()
        region = matchDict["match"].region
        embed = discord.Embed(title="In Game: {0}".format(matchInfo["Circle"]), description=matchInfo["MatchType"] + "　|　　" + matchInfo["Time"], color=matchInfo["Color"])

        # Check if summoner in the game is in the summonerList
        registeredAccounts = await discordServerSummoners(discordServer)
        inList = lambda name : len([summoner for summoner, discordUser in registeredAccounts if summoner.summonerName == name]) != 0

        # Create Embed Value Strings for Blue Team
        blueTeam = matchInfo["BlueTeam"]
        blueFirstStr = ""
        blueSecondStr = ""
        for player in blueTeam:
            if inList(player["summonerName"]):
                blueFirstStr += "‎\n{0} {1} __{2}__ \n".format(diamonds["blue"], champEmojis[player["champion"]], player["summonerName"])
            else:
                blueFirstStr += "‎\n{0} {1} {2} \n".format(diamonds["blue"], champEmojis[player["champion"]], player["summonerName"])
            blueSecondStr += "‎\n{0} {1} \n".format(spellEmojis[player["spell1"]], spellEmojis[player["spell2"]])

        embed.add_field(name="** 🟦 Blue Team**", value=blueFirstStr + "‎", inline=True)
        embed.add_field(name="‎", value="‎", inline=True)
        embed.add_field(name="‎", value=blueSecondStr + "‎", inline=True)

        redTeam = matchInfo["RedTeam"]
        redFirstStr = ""
        redSecondStr = ""
        for player in redTeam:
            if inList(player["summonerName"]):
                redFirstStr += "‎\n{0} {1} __{2}__ \n".format(diamonds["red"], champEmojis[player["champion"]], player["summonerName"])
            else:
                redFirstStr += "‎\n{0} {1} {2} \n".format(diamonds["red"], champEmojis[player["champion"]], player["summonerName"])
            redSecondStr += "‎\n{0} {1} \n".format(spellEmojis[player["spell1"]], spellEmojis[player["spell2"]])

        embed.add_field(name="** 🟥 Red Team **", value=redFirstStr + "‎", inline=True)
        embed.add_field(name="‎", value="‎", inline=True)
        embed.add_field(name="‎", value=redSecondStr + "‎", inline=True)

        return embed

    def alarm(self, circleEmoji):
        """
        Returns Embed for alarm message, raises InvalidCircle if the circle is not in matches
        --------------------
        circleEmoji: Circle emoji of the match that will be presented
        """
        matchDict = self.circleEmojiMatch(circleEmoji)
        if matchDict is False:
            raise InvalidCircle
        
        embed = discord.Embed(title="Alarm", description="I will alarm you when the match {0} ends".format(matchDict["match"].circle.emoji), color=matchDict["match"].circle.hexcolor)
        return embed

    async def deleteOutdated(self): # Will get called every 20 seconds
        """
        Will check for outdated (already ended) matches in self.matches, and will erase their information
        """
        temp = self.matches.copy()
        deletedEmojis = []
        for gameId, matchDict in self.matches.items():
            match = matchDict["match"]
            participants = match.infoDict["participants"]
            
            firstParticipant = match.firstParticipant()
            firstSummoner = Summoner(firstParticipant["summonerName"], match.region)
            try:
                firstSummoner.getMatchInfo(self)
                continue
            except InvalidMatch:
                # Match is Invalid; should get deleted
                match.circle.available = True # The circle used for this ended match is now avail for use
                
                deletedEmojis.append(match.circle.emoji)
                del temp[gameId]
        
        self.matches = temp.copy()

        return deletedEmojis

class AccountsManager:
    """
    Will Manage the LoL accounts that are being profile-authenticated
    ---------------------
    pendingAccounts: Dictionary of Discord Users with Summoners that are pending for profile authentication
    authAccounts: Dictionary of Discord Users with Authenticated Summoners that will be temporarily stored
                    before being moved in DB with !lol link
    authStartTimes: Dictionary of Discord Users with DateTimes of when the authorization was first called
    authStartUsers: Dictionary of Discord Users with ctx.author info (for later DM sending)
    icons: Dictionary of Discord Users with Their Icons
    discordServer: The ID of the discord server
    """
    #TODO: Account authentication to add it (profile icon id 1~27)
    # Pictures can be gotten from https://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/27.png

    def __init__(self, discordServer):
        self.pendingAccounts = {}
        self.authAccounts = {}
        self.authStartTimes = {}
        self.authStartUsers = {}
        self.icons = {}
        self.discordServer = discordServer
    
    def setStartTime(self, discordUser, author):
        self.authStartTimes[discordUser] = datetime.datetime.now()
        self.authStartUsers[discordUser] = author

    def removeUser(self, discordUser):
        del self.pendingAccounts[discordUser]
        del self.icons[discordUser]
        del self.authStartTimes[discordUser]
        del self.authStartUsers[discordUser]
    
    def removeAuthedUser(self, discordUser):
        del self.authAccounts[discordUser]
    
    def pendingCheck(self, summoner):
        """
        Checks and Returns if the summoner is in the stage of pending for if the profile icon is checked
        Returns Boolean
        --------------------
        summoner: Summoner being checked
        """
        return summoner in self.pendingAccounts.values()
    
    def authedCheck(self, summoner):
        """
        Checks and Returns if the summoner is authenticated 
        Returns Boolean
        --------------------
        summoner: Summoner being checked
        """
        return summoner in self.authAccounts.values()
    
    def pendingCheckUser(self, summoner, discordUser):
        """
        Checks and Returns if the summoner is in the stage of pending for if the profile icon is checked
        Returns Boolean
        --------------------
        summoner: Summoner being checked
        discordUser: Discord User being checked
        """
        return discordUser in self.pendingAccounts.keys() and self.pendingAccounts[discordUser] == summoner

    def suggestNewProfile(self, summoner, discordUser):
        """
        Suggests a New Profile to the summoner, one that is different from the currenty used profile
        Returns a dictionary of 
            {
                id: (New Profile Icon ID)
                picture: (Link for the Picture for New Profile)
            }
        --------------------
        summoner: Summoner being suggested a new profile
        discordUser: Discord User being suggested a new profile
        """
        if self.pendingCheckUser(summoner, discordUser): # Already in Auth
            raise IconAlreadySuggested
        elif self.pendingCheck(summoner): # Other person doing Auth
            raise OtherUserAuth
        elif discordUser in self.pendingAccounts.keys(): # User already doing another authentication process
            raise UserAnotherAuth
        else:
            self.pendingAccounts[discordUser] = summoner
            profileIcons = list(range(1, 28))
            currentIcon = summoner.getProfileIcon()

            if 1 <= currentIcon and currentIcon <= 27:
                profileIcons.remove(currentIcon)

            randomId = random.choice(profileIcons)
            self.icons[discordUser] = randomId
            return {"id": randomId, "picture": "https://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/{0}.png".format(randomId)}

    def checkProfile(self, discordUser):
        """
        Checks if the Discord User's auth-aspiring Summoner's icon is equal to that of the bot's suggestion
        If the two are equal, Discord User is no longer a pending account; it becomes an authorized account
        Returns a Boolean of whether Discord User's Summoner's icon is the auth-suggested icon
        """
        iconId = self.icons[discordUser]
        currentIcon = self.pendingAccounts[discordUser].getProfileIcon()
        if currentIcon == iconId:
            self.authAccounts[discordUser] = self.pendingAccounts[discordUser]
            del self.pendingAccounts[discordUser]
        return currentIcon == iconId

class DiscordManager:
    """
    Will Manage all the Managers for one discord server, including
    MatchManager, CircleManager, AccountsManager and the serverId for the DB
    --------------------
    discordServer: The ID of the discord server
    """

    def __init__(self, discordServer):
        self.discordServer = discordServer
        self.matchManager = MatchManager(discordServer = discordServer)
        self.circleManager = CircleManager(discordServer = discordServer)
        self.accountsManager = AccountsManager(discordServer = discordServer)
        self.alarmRequests = []  # Will contain {"author": __(discord User), "circleStr": __(str)}

    def __eq__(self, other):
        return self.discordServer == other.discordServer
    
    async def periodicCheck(self):
        """
        Will check for outdated (already ended) matches in self.matches, and will erase their information
        In addition, will check for alarmRequested matches and if they have ended
        Also, will check if some authentication processes need to expire due to passing 5 minutes
        """
        # Update Outdated matches & Check for Alarms
        deletedEmojis = await self.matchManager.deleteOutdated()
        alarmRequests = self.alarmRequests.copy()

        toDeleteIndex = []

        idx = 0
        for request in alarmRequests:
            if request["circleStr"] in deletedEmojis:
                embed = discord.Embed(title="Alarm", description="{0} has ended!".format(request["circleStr"]), color=hexcolors[request["circleStr"]])
                toDeleteIndex.append(idx)
                await request["author"].send(embed=embed)
            idx += 1

        shiftAccum = 0
        for idx in toDeleteIndex:
            self.alarmRequests.pop(idx - shiftAccum)
            shiftAccum += 1
        
        # Check for expired Auth Attempts (expire if more than 5 minutes passed)
        curTime = datetime.datetime.now()
        for discordUser, startTime in self.accountsManager.authStartTimes.copy().items():
            if (curTime - startTime) >= datetime.timedelta(seconds=300): # NEED TO CHANGE TO 300 SECONDS LATER
                # Auto unauth the discordUser
                embed = discord.Embed(title="Authentication Expiration", description="Your authentication for __{0}__ has expired because 5 minutes have passed".format(self.accountsManager.pendingAccounts[discordUser].summonerName), color=0xff0033)
                await self.accountsManager.authStartUsers[discordUser].send(embed=embed)
                self.accountsManager.removeUser(discordUser)
    


### SETUP
"""
koreans = [
    Summoner("소년가장1", "kr"),
    Summoner("Fireknight25", "kr"),
    Summoner("Fireknight", "kr"),
    Summoner("EviliotoJeffrey", "kr"),
    Summoner("점멸혐오자", "kr"),
    Summoner("poochi", "kr"),
    Summoner("joshuah22", "kr"),
    Summoner("kinddd", "kr"),
    Summoner("swaggwad", "kr"),
    Summoner("SKT 롤", "kr"),
    Summoner("JEEEEFFFFF", "kr"),
    Summoner("Hangry05", "kr"),
    Summoner("yeonwooc24", "kr"),
    Summoner("yummykhan05", "kr"),
    Summoner("BONZI BUDDY", "kr"),
    Summoner("GP아아아", "kr"),
    Summoner("그냥 제이스장인", "kr"),
    Summoner("M0dern times", "kr"),
    Summoner("nan shen", "kr"),
]
americans = [
    Summoner("Anda", "na1")
]
testSummoners = {"kr": koreans, "na1": americans}"""

## Discord Manager List Setup
discordManagerList = []

## Help Command Embed Setup
helpsInfo = {}

helpEmbeds = {}
    
# Page 1
embed=Embed(title="Commands", description="\u200b", color=0xb09e99)
embed.add_field(name="__Live Match Commands__", value="\u200b", inline=False)
embed.add_field(name="!lol rn", value="Presents all summoners saved in the sever summoner list that are currently in a match", inline=False)
embed.add_field(name="!lol match (circle)", value="Presents information of the match attributed to the circle", inline=False)
embed.add_field(name="!lol alarm (circle)", value="Alarms user via DM when the match attributed to the circle ends", inline=False)
embed.add_field(name="!lol (mention)", value="Presents all summoners linked to the mentioned user that are currently in a match", inline=False)
embed.add_field(name="!lol (role)", value="Presents all summoners linked to users with the role that are currently in a match", inline=False)
embed.set_footer(text="Page 1 / 4")
helpEmbeds[1] = embed

# Page 2
embed=Embed(title="Commands", description="\u200b", color=0xb09e99)
embed.add_field(name="__Get Server's Summoners Commands__", value="\u200b", inline=False)
embed.add_field(name="!lol list", value="Gives all LoL accounts saved in the server summoner list", inline=False)
embed.add_field(name="!lol accounts", value="Gives all LoL accounts linked to __you__ in this server", inline=False)
embed.add_field(name="!lol accounts (mention)", value="Gives all LoL accounts linked to the __mentioned user__ in this server", inline=False)
embed.set_footer(text="Page 2 / 4")
helpEmbeds[2] = embed

# Page 3
embed=Embed(title="Commands", description="\u200b", color=0xb09e99)
embed.add_field(name="__Linking Summoner to User Commands__", value="\u200b", inline=False)
embed.add_field(name="!lol link (region) (summoner)", value="Links the summoner in the region to the user (authentication required)", inline=False)
embed.add_field(name="!lol unlink (region) (summoner)", value="Unlinks the summoner in the region from the user", inline=False)
embed.add_field(name="!lol auth", value="Checks if the authentication for summoner linking is successful for the user", inline=False)
embed.add_field(name="!lol unauth", value="Stops the summoner linking authentication process for the user", inline=False)
embed.set_footer(text="Page 3 / 4")
helpEmbeds[3] = embed

# Page 4
embed=Embed(title="Commands", description="\u200b", color=0xb09e99)
embed.add_field(name="__Manage Server's Accounts Commands (For Mod & lolmanager roles)__", value="\u200b", inline=False)
embed.add_field(name="!lol add (region) (summoner)", value="Adds the summoner in the region to the server summoner list", inline=False)
embed.add_field(name="!lol del (region) (summoner)", value="Deletes the summoner in the region to the server summoner list", inline=False)
embed.set_footer(text="Page 4 / 4")
helpEmbeds[4] = embed



### BOT COMMANDS

@bot.command(pass_context=True, aliases=['opgg','OPGG', 'league', 'LEAGUE', 'LoL', 'LOL'])
async def lol(ctx, *args):
    """
    Command that will give information about a live match of a summoner, or will execute actions regarding that information
    """
    if ctx.author == bot.user:
        return

    if (args[0].lower() == "rn" or args[0].lower() == "@everyone") and len(args) == 1:
        """
        Command: !lol rn
        Function: Gives a list of summoners that are currently in a game, also giving
                their live match information
        """
        embed = discord.Embed(title="Who is in a game of League of Legends?", description="People In This Server:", color=0xb09e99)
        discordManager = discordManagerFinder(ctx.guild.id)
        gamesDict = await discordManager.matchManager.getAll2(discordManager.circleManager, discordManager.discordServer)

        for gameId, summonerDictList in gamesDict.items():
            for summonerDict in summonerDictList:
                embed.add_field(name="✅  " + summonerDict["summonerName"], value=summonerDict["presentSummoner"], inline=False)
        
        await ctx.send(embed=embed)
    
    if (args[0].lower() == "match" or args[0].lower() == "game") and len(args) == 2:
        """
        Command: !lol match (circle)
        Function: Gives data of the live match, including time, summoner names, champions
        Exception: If a match with (circle) does not exist, reacts with a question mark
        """
        discordManager = discordManagerFinder(ctx.guild.id)
        try:
            embed = await discordManager.matchManager.presentMatch(args[1], discordManager.discordServer)
            embed.set_footer(text = "Requested by: " + ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
        except InvalidCircle:
            await ctx.message.add_reaction("❓")
    
    if args[0].lower() == "alarm" and len(args) == 2:
        """
        Command: !lol alarm (circle)
        Function: Gives a DM to the requested user when the match (circle) ends
        Exception: If a match with (circle) does not exist, reacts with a question mark
        """
        discordManager = discordManagerFinder(ctx.guild.id)
        try:
            embed = discordManager.matchManager.alarm(args[1])
            discordManager.alarmRequests.append({"author": ctx.author, "circleStr": args[1]})
            await ctx.author.send(embed=embed)
        except InvalidCircle:
            await ctx.message.add_reaction("❓")
    
    if args[0].lower() == "list" and len(args) == 1:
        """
        Command: !lol list
        Function: Gives a catalog of the server Summoners
        """
        embed = Embed(title="Server Accounts", description = "\u200b", color=0xb09e99)
        summoners = await discordServerSummoners(ctx.guild.id)
        
        for summoner, discordUser in summoners:
            if discordUser == -1:
                embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="⠀\n⠀", inline=False)
            else:
                mention = ctx.guild.get_member(discordUser).mention
                embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="⠀⠀⠀(" + mention + ")\n⠀", inline=False)

        await ctx.send(embed=embed)

    if args[0].lower() == "add":
        """
        Command: !lol add (region) (LoL Account)
        Function: Adds the following LoL Account to the Data Base
        Exception: If the region or LoL account is invalid, says so
        """
        has_role = lambda role_name: role_name in [r.name.lower() for r in ctx.author.roles]
        if not (ctx.author.guild_permissions.administrator or has_role("lolmanager") or has_role("lol manager")): # Does not have permission to do this command
            embed = Embed(title="Needs Permission", description="Sorry, you must either be administrator or have \"LoLManager\" role", color=0xff0033)
            await ctx.send(embed=embed)
            return

        if len(args) < 3:
            embed = Embed(title="Proper Command Usage", description="!lol add (region) (account name)", color=0xff0033)
            await ctx.send(embed=embed)
            return

        unofficialRegion = args[1]
        unofficialName = ""
        for a in args[2:]:
            unofficialName += a
            unofficialName += " "
        unofficialName = unofficialName[0:-1]
        
        try:
            summoner = Summoner(unofficialName, unofficialRegion)
            try:
                await getSummoner(summoner, ctx.guild.id)
                # Account already exists in database
                embed = Embed(title="Account already Saved", description="The summoner __{0}__ is already saved into this server account list".format(summoner.summonerName), color=0xff0033)
                await ctx.send(embed=embed)
            
            except ObjectDoesNotExist: # Account that is not already in the database 
                await storeSummoner(summoner, ctx.guild.id)
                embed = Embed(title="Summoner __{0}__ successfully added to the server accounts list".format(summoner.summonerName), description="{0} will now be tracked from !lol commands".format(summoner.summonerName), color=0x50c878)
                await ctx.send(embed=embed)

        except InvalidRegion:
            embed = Embed(title="Invalid Region", description="!lol add (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
            await ctx.send(embed=embed)
        except InvalidSummonerName:
            embed = Embed(title="Invalid Summoner", description="!lol add (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
            await ctx.send(embed=embed)
        
            

    if args[0].lower() == "del" or args[0].lower() == "delete" or args[0].lower() == "remove":
        """
        Command: !lol del (region) (LoL Account)
        Function: Deletes the following LoL Account from the Data Base
        Exception: If the region or LoL account is invalid, says so
                    If the account is not in the server data base, says so
        """
        has_role = lambda role_name: role_name in [r.name.lower() for r in ctx.author.roles]
        if not (ctx.author.guild_permissions.administrator or has_role("lolmanager") or has_role("lol manager")): # Does not have permission to do this command
            embed = Embed(title="Needs Permission", description="Sorry, you must either be administrator or have \"LoLManager\" role", color=0xff0033)
            await ctx.send(embed=embed)
            return

        if len(args) < 3:
            embed = Embed(title="Proper Command Usage", description="!lol del (region) (account name)", color=0xff0033)
            await ctx.send(embed=embed)
            return

        unofficialRegion = args[1]
        unofficialName = ""
        for a in args[2:]:
            unofficialName += a
            unofficialName += " "
        unofficialName = unofficialName[0:-1]
        
        try:
            summoner = Summoner(unofficialName, unofficialRegion)
            await deleteSummoner(summoner, ctx.guild.id)
            embed = Embed(title="Summoner __{0}__ successfully deleted from server DataBase".format(summoner.summonerName), description="{0} will now not be tracked from !lol commands".format(summoner.summonerName), color=0x50c878)
            await ctx.send(embed=embed)
        except InvalidRegion:
            embed = Embed(title="Invalid Region", description="!lol add (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
            await ctx.send(embed=embed)
        except InvalidSummonerName:
            embed = Embed(title="Invalid Summoner", description="!lol add (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
            await ctx.send(embed=embed)
        except ObjectDoesNotExist:
            embed = Embed(title="Summoner Not In List", description="!lol add (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="The summoner __{0}__ is not in the server list from the beginning".format(unofficialName), value="\u200b", inline=False)
            await ctx.send(embed=embed)

    if (args[0].lower() == "account" or args[0].lower() == "accounts" or args[0].lower() == "acc" or args[0].lower() == "accs") and len(args) == 1:
        """
        Command: !lol accounts
        Function: Gives all of the accounts linked by the user
        """
        embed = Embed(title="Linked Accounts", description = "(For {0})".format(ctx.author.mention), color=0xb09e99)
        summoners = await discordServerUserSummoners(ctx.guild.id, ctx.author.id)

        embed.add_field(name="\u200b", value="\u200b", inline=False)
        
        for summoner in summoners:
            embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="\u200b", inline=False)

        await ctx.send(embed=embed)
    
    if (args[0].lower() == "account" or args[0].lower() == "accounts" or args[0].lower() == "acc" or args[0].lower() == "accs") and len(args) == 2:
        """
        Command: !lol accounts (mention)
        Function: Gives all of the accounts linked by the mentioned user
        """
        # Retrieve Info of the mentioned one
        mention = args[1]
        temp_id = None
        if '0' <= mention[2] and mention[2] <= '9':
            temp_id = int(mention[2:-1])
        else:
            temp_id = int(mention[3:-1])

        user = ctx.guild.get_member(temp_id)

        embed = Embed(title="Linked Accounts", description = "(For {0})".format(user.mention), color=0xb09e99)
        summoners = await discordServerUserSummoners(ctx.guild.id, user.id)

        embed.add_field(name="\u200b", value="\u200b", inline=False)
        
        for summoner in summoners:
            embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="\u200b", inline=False)

        await ctx.send(embed=embed)

    if (args[0].lower() == "auth" or args[0].lower() == "authenticate") and len(args) == 1:
        """
        Command: !lol auth
        Function: Chekcs if the profile authentication process worked validly
        """
        discordManager = discordManagerFinder(ctx.guild.id)
        try:
            if discordManager.accountsManager.checkProfile(ctx.author.id):
                # New profile checked, authentication successful
                summoner = discordManager.accountsManager.authAccounts[ctx.author.id]
                embed = Embed(title="Summoner __{0}__ successfully authenticated!".format(summoner.summonerName), description="{0} is now an authenticated account for {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
                await ctx.send(embed=embed)
            else:
                # Profile did not match, authentication unsuccessful, suggest that user retry
                embed = Embed(title="Profile Icons do not Match", description="Make sure your profile icon matches the one the bot gave, and retry !lol auth", color=0xff0033)
                await ctx.send(embed=embed)
        except KeyError: # Nothing to auth from the first place
            embed = Embed(title="You have nothing to authenticate check from the first place", description="\u200b", color=0xff0033)
            await ctx.send(embed=embed)

    if args[0].lower() == "unauth" or args[0].lower() == "unauthenticate":
        """
        Command: !lol unauth
        Function: Stops the summoner linking authentication process for the user
        """
        discordManager = discordManagerFinder(ctx.guild.id)
        try:
            discordManager.accountsManager.removeUser(ctx.author.id)
            embed=Embed(title="You have stopped your authentication process", description="\u200b", color=0x50c878)
            await ctx.send(embed=embed)
        except KeyError: # Author has not requested authentication for anything
            embed=Embed(title="You have not authenticated any account from the beginning", description="(Authentication Process automatically expires after 5 minutes)", color=0xff0033)
            await ctx.send(embed=embed)
        

    if args[0].lower() == "link":
        """
        Command: !lol link (region) (LoL Account)
        Function: Links the following LoL Account to the Discord User
        Exception: If the region or LoL account is invalid, says so
                   If the account is already linked, says so
        """
        if len(args) < 3:
            embed = Embed(title="Proper Command Usage", description="!lol link (region) (account name)", color=0xff0033)
            await ctx.send(embed=embed)
            return

        unofficialRegion = args[1]
        unofficialName = ""
        for a in args[2:]:
            unofficialName += a
            unofficialName += " "
        unofficialName = unofficialName[0:-1]
        
        # Check if summoner is valid
        summoner = None
        try:
            summoner = Summoner(unofficialName, unofficialRegion)
        except InvalidRegion:
            embed = Embed(title="Invalid Region", description="!lol link (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
            await ctx.send(embed=embed)
            return
        except InvalidSummonerName:
            embed = Embed(title="Invalid Summoner", description="!lol link (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
            await ctx.send(embed=embed)
            return

        # Do different actions based on if account is in database (with/without discord user linked)
        try:
            DBsummoner = await getSummonerUser(summoner, ctx.guild.id, ctx.author.id)
            # Already Linked
            embed = Embed(title="Summoner __{0}__ already linked to you!".format(summoner.summonerName), description="{0} is already and will continue to be linked to {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
            await ctx.send(embed=embed)
        except ObjectDoesNotExist: # Not already linked
            # First need to authenticate the account (profile authentication)
            discordManager = discordManagerFinder(ctx.guild.id)
            if discordManager.accountsManager.authedCheck(summoner):
                discordManager.accountsManager.removeAuthedUser(ctx.author.id)
                try: 
                    await giveSummonerUser(summoner, ctx.guild.id, ctx.author.id)
                    # Account inside Server Database already, without owner
                    embed = Embed(title="Summoner __{0}__ successfully linked to you!".format(summoner.summonerName), description="{0} will now be linked to {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
                    await ctx.send(embed=embed)
                except AlreadyLinkedAccount: # Account already linked to another person.
                    embed = Embed(title="Sorry, Summoner __{0}__ is already linked to another user".format(summoner.summonerName), description="\u200b", color=0xff0033)
                    await ctx.send(embed=embed)
                except ObjectDoesNotExist: # Account not in database, need to add newly
                    await storeSummonerUser(summoner, ctx.guild.id, ctx.author.id)
                    embed = Embed(title="Summoner __{0}__ successfully linked to you!".format(summoner.summonerName), description="{0} will now be linked to {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
                    await ctx.send(embed=embed)
            else:
                embed = Embed(title="Before linking, you must authenticate that Summoner __{0}__ is your account!".format(summoner.summonerName), description="\u200b", color=0x50c878)
                embed.add_field(name="Preparing Authentication Process...", value="\u200b", inline=False)
                await ctx.send(embed=embed)

                # Need Authentication
                # Check if Owned Account
                try:
                    isOwned = await isOwnedSummoner(summoner, ctx.guild.id)
                    if isOwned:
                        embed = Embed(title="Summoner __{0}__ is already linked to a user, so authentication is unavailable".format(summoner.summonerName), description="\u200b", color=0xff0033)
                        await ctx.send(embed=embed)
                        return
                except Exception:
                    pass

                try:
                    profileDict = discordManager.accountsManager.suggestNewProfile(summoner, ctx.author.id)
                    
                    embed=Embed(title="Change Account Profile Icon to the picture sent in DM", description="\u200b", color=0x50c878)
                    embed.add_field(name="Then do !lol auth", value="(Authentication Process automatically expires after 5 minutes)", inline=False)
                    await ctx.send(embed=embed)
                    
                    embed=Embed(title="Change Account Profile for __{0}__ to this:".format(summoner.summonerName), description="(Authentication Process automatically expires after 5 minutes)", color=0x50c878)
                    embed.set_image(url=profileDict['picture'])
                    await ctx.author.send(embed=embed)

                    discordManager.accountsManager.setStartTime(ctx.author.id, ctx.author)
                except OtherUserAuth:
                    embed=Embed(title="An other user is authenticating this account already", description="\u200b", color=0xff0033)
                    await ctx.send(embed=embed)
                except IconAlreadySuggested:
                    embed=Embed(title="You already did this command!", description="\u200b", color=0xff0033)
                    await ctx.send(embed=embed)
                except UserAnotherAuth:
                    embed=Embed(title="You are already authorizing another account. Do !lol unauth first to authorize this account", description="\u200b", color=0xff0033)
                    await ctx.send(embed=embed)
    
    if args[0].lower() == "unlink":
        """
        Command: !lol unlink (region) (LoL Account)
        Function: Unlinks the following LoL Account to the Discord User (including deletion of the account from server database)
        Exception: If the region or LoL account is invalid, says so
                   If the account is not linked by the user, says so
        """
        # TODO: Authority? Authenticate Account? Idk
        if len(args) < 3:
            embed = Embed(title="Proper Command Usage", description="!lol unlink (region) (account name)", color=0xff0033)
            await ctx.send(embed=embed)
            return

        unofficialRegion = args[1]
        unofficialName = ""
        for a in args[2:]:
            unofficialName += a
            unofficialName += " "
        unofficialName = unofficialName[0:-1]
        
        # Check if summoner is valid
        summoner = None
        try:
            summoner = Summoner(unofficialName, unofficialRegion)
        except InvalidRegion:
            embed = Embed(title="Invalid Region", description="!lol link (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
            await ctx.send(embed=embed)
            return
        except InvalidSummonerName:
            embed = Embed(title="Invalid Summoner", description="!lol link (region) (account name)", color=0xff0033)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
            await ctx.send(embed=embed)
            return
        
        try: # Try deleting
            await deleteSummonerUser(summoner, ctx.guild.id, ctx.author.id)
            # Already Linked
            embed = Embed(title="Summoner __{0}__ successfully unlinked and deleted!".format(summoner.summonerName), description="{0} is now unlinked from {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
            await ctx.send(embed=embed)
        except ObjectDoesNotExist: # Not an account linked
            embed = Embed(title="Summoner __{0}__ was not linked to you from the beginning.".format(summoner.summonerName), description="\u200b", color=0xff0033)
            await ctx.send(embed=embed)

    elif args[0][0] == "<" and args[0][-1] == ">" and args[0][2] != "&" and len(args) == 1:
        """
        Command: !lol (mention)
        Function: Gives a list of summoners that are currently in a game for the mentioned user, also giving
                their live match information
        """
        # Retrieve Info of the mentioned one
        mention = args[0]
        temp_id = None
        if '0' <= mention[2] and mention[2] <= '9':
            temp_id = int(mention[2:-1])
        else:
            temp_id = int(mention[3:-1])

        user = ctx.guild.get_member(temp_id)
        if user is None:
            return
        

        embed = discord.Embed(title="Who is in a game of League of Legends?", description="Accounts for {0}:".format(user.mention), color=0xb09e99)
        discordManager = discordManagerFinder(ctx.guild.id)
        querySet = await discordServerUsersSummoners(ctx.guild.id, [user.id])

        gamesDict = await discordManager.matchManager.getSome(discordManager.circleManager, discordManager.discordServer, querySet)

        for gameId, summonerDictList in gamesDict.items():
            for summonerDict in summonerDictList:
                embed.add_field(name="✅  " + summonerDict["summonerName"], value=summonerDict["presentSummoner"], inline=False)
        
        await ctx.send(embed=embed)

    elif args[0][0] == "<" and args[0][-1] == ">" and args[0][2] == "&" and len(args) == 1:
        """
        Command: !lol (role)
        Function: Gives a list of summoners that are currently in a game for the users with the role, also giving
                their live match information
        """
        # Retrieve Info of the mentioned role
        role = ctx.guild.get_role(int(args[0][3:-1]))
        if role is None:
            return
        
        usersIds = []
        for user in ctx.guild.members:
            if role in user.roles:
                usersIds.append(user.id)

        embed = discord.Embed(title="Who is in a game of League of Legends?", description="People with role {0}:".format(role.mention), color=0xb09e99)
        discordManager = discordManagerFinder(ctx.guild.id)
        querySet = await discordServerUsersSummoners(ctx.guild.id, usersIds)

        gamesDict = await discordManager.matchManager.getSome(discordManager.circleManager, discordManager.discordServer, querySet)

        for gameId, summonerDictList in gamesDict.items():
            for summonerDict in summonerDictList:
                embed.add_field(name="✅  " + summonerDict["summonerName"], value=summonerDict["presentSummoner"], inline=False)
        
        await ctx.send(embed=embed)

    elif (args[0].lower() == "help" or args[0].lower() == "commands") and len(args) == 1:
        """
        Command: !lol help
        Function: Gets all "!lol" commands
        """
        embed=Embed(title="Commands", description="\u200b", color=0xb09e99)
    
        # Page 1
        embed.add_field(name="__Live Match Commands__", value="\u200b", inline=False)
        embed.add_field(name="!lol rn", value="Presents all summoners saved in the sever summoner list that are currently in a match", inline=False)
        embed.add_field(name="!lol match (circle)", value="Presents information of the match attributed to the circle", inline=False)
        embed.add_field(name="!lol alarm (circle)", value="Alarms user via DM when the match attributed to the circle ends", inline=False)
        embed.add_field(name="!lol (mention)", value="Presents all summoners linked to the mentioned user that are currently in a match", inline=False)
        embed.add_field(name="!lol (role)", value="Presents all summoners linked to users with the role that are currently in a match", inline=False)
        embed.set_footer(text="Page 1 / 4")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

        helpsInfo[msg.id] = {"page": 1, "msg": msg}

@bot.command(aliases=['HELP', 'commands', 'COMMANDS'])
async def help(ctx):
    embed=Embed(title="Commands", description="\u200b", color=0xb09e99)
    
    # Page 1
    embed.add_field(name="__Live Match Commands__", value="\u200b", inline=False)
    embed.add_field(name="!lol rn", value="Presents all summoners saved in the sever summoner list that are currently in a match", inline=False)
    embed.add_field(name="!lol match (circle)", value="Presents information of the match attributed to the circle", inline=False)
    embed.add_field(name="!lol alarm (circle)", value="Alarms user via DM when the match attributed to the circle ends", inline=False)
    embed.add_field(name="!lol (mention)", value="Presents all summoners linked to the mentioned user that are currently in a match", inline=False)
    embed.add_field(name="!lol (role)", value="Presents all summoners linked to users with the role that are currently in a match", inline=False)
    embed.set_footer(text="Page 1 / 4")
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("◀️")
    await msg.add_reaction("▶️")

    helpsInfo[msg.id] = {"page": 1, "msg": msg}

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    msg = reaction.message
    channel = msg.channel

    if msg.id in helpsInfo.keys(): # Added reaction to a help command embed
        if reaction.emoji == "◀️":
            if helpsInfo[msg.id]["page"] != 1:
                helpsInfo[msg.id]["page"] -= 1
                await helpsInfo[msg.id]["msg"].edit(embed=helpEmbeds[helpsInfo[msg.id]["page"]])
            await msg.remove_reaction("◀️", user)
        elif reaction.emoji == "▶️":
            if helpsInfo[msg.id]["page"] != 4:
                helpsInfo[msg.id]["page"] += 1
                await helpsInfo[msg.id]["msg"].edit(embed=helpEmbeds[helpsInfo[msg.id]["page"]])
            await msg.remove_reaction("▶️", user)
        else:
            pass
    


### SLASH COMMANDS

regionChoices=[
    create_choice(
        name="BR",
        value="BR"
    ),
    create_choice(
        name="EUNE",
        value="EUNE"
    ),
    create_choice(
        name="EUW",
        value="EUW"
    ),
    create_choice(
        name="JP",
        value="JP"
    ),
    create_choice(
        name="KR",
        value="KR"
    ),
    create_choice(
        name="LAN",
        value="LAS"
    ),
    create_choice(
        name="NA",
        value="NA"
    ),
    create_choice(
        name="OCE",
        value="OCE"
    ),
    create_choice(
        name="RU",
        value="RU"
    ),
    create_choice(
        name="TR",
        value="TR"
    ),
]

@slash.subcommand(base="lol", name="rn", description="Presents all summoners saved in the sever summoner list that are currently in a match")
async def _lolRn(ctx: SlashContext):
    """
    Command: !lol rn
    Function: Gives a list of summoners that are currently in a game, also giving
            their live match information
    """
    await ctx.defer()
    embed = discord.Embed(title="Who is in a game of League of Legends?", description="People In This Server:", color=0xb09e99)
    discordManager = discordManagerFinder(ctx.guild.id)
    gamesDict = await discordManager.matchManager.getAll2(discordManager.circleManager, discordManager.discordServer)

    for gameId, summonerDictList in gamesDict.items():
        for summonerDict in summonerDictList:
            embed.add_field(name="✅  " + summonerDict["summonerName"], value=summonerDict["presentSummoner"], inline=False)
    
    await ctx.send(embed=embed)



@slash.subcommand(base="lol", name="match", description="Presents information of the match attributed to the circle",
        options=[
            create_option(
                name="circle",
                description="Circle attributed to a live match (ex: 🔴)",
                option_type=3,
                required=True
            )
        ])
async def _lolmatch(ctx: SlashContext, circle):
    """
    Command: !lol match (circle)
    Function: Gives data of the live match, including time, summoner names, champions
    Exception: If a match with (circle) does not exist, says that match has already ended or does not exist
    """
    discordManager = discordManagerFinder(ctx.guild.id)
    try:
        embed = await discordManager.matchManager.presentMatch(circle, discordManager.discordServer)
        embed.set_footer(text = "Requested by: " + ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except InvalidCircle:
        embed=Embed(title="You have either given a wrong input, or the match does not exist or has already ended", description="\u200b", color=0xff0033)
        await ctx.send(embed=embed)



@slash.subcommand(base="lol", name="game", description="Presents information of the match attributed to the circle",
        options=[
            create_option(
                name="circle",
                description="Circle attributed to a live match (ex: 🔴)",
                option_type=3,
                required=True
            )
        ])
async def _lolgame(ctx: SlashContext, circle):
    """
    Command: !lol game (circle)
    Function: Gives data of the live match, including time, summoner names, champions
    Exception: If a match with (circle) does not exist, says that match has already ended or does not exist
    """
    discordManager = discordManagerFinder(ctx.guild.id)
    try:
        embed = await discordManager.matchManager.presentMatch(circle, discordManager.discordServer)
        embed.set_footer(text = "Requested by: " + ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except InvalidCircle:
        embed=Embed(title="You have either given a wrong input, or the match does not exist or has already ended", description="\u200b", color=0xff0033)
        await ctx.send(embed=embed)




@slash.subcommand(base="lol", name="alarm", description="Alarms user via DM when the match attributed to the circle ends",
        options=[
            create_option(
                name="circle",
                description="Circle attributed to a live match (ex: 🔴)",
                option_type=3,
                required=True
            )
        ])
async def _lolalarm(ctx: SlashContext, circle):
    """
    Command: !lol alarm (circle)
    Function: Gives a DM to the requested user when the match (circle) ends
    Exception: If a match with (circle) does not exist, reacts with a question mark
    """
    discordManager = discordManagerFinder(ctx.guild.id)
    try:
        embed = discordManager.matchManager.alarm(circle)
        discordManager.alarmRequests.append({"author": ctx.author, "circleStr": circle})
        await ctx.author.send(embed=embed)
    except InvalidCircle:
        embed=Embed(title="You have either given a wrong input, or the match does not exist or has already ended", description="\u200b", color=0xff0033)
        await ctx.send(embed=embed)



@slash.subcommand(base="lol", name="list", description="Gives all LoL accounts saved in the server summoner list")
async def _lollist(ctx: SlashContext):
    """
    Command: !lol list
    Function: Gives a catalog of the server Summoners
    """
    embed = Embed(title="Server Accounts", description = "\u200b", color=0xb09e99)
    summoners = await discordServerSummoners(ctx.guild.id)
    
    for summoner, discordUser in summoners:
        if discordUser == -1:
            embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="⠀\n⠀", inline=False)
        else:
            mention = ctx.guild.get_member(discordUser).mention
            embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="⠀⠀⠀(" + mention + ")\n⠀", inline=False)

    await ctx.send(embed=embed)


@slash.subcommand(base="lol", name="add", description="Adds the summoner in the region to the server summoner list",
        options=[
            create_option(
                name="region",
                description="Summoner's Region",
                option_type=3,
                required=True,
                choices=regionChoices
            ),
            create_option(
                name="summoner",
                description="Summoner Name",
                option_type=3,
                required=True
            )
        ])
async def _loladd(ctx: SlashContext, region, summoner):
    """
    Command: !lol add (region) (LoL Account)
    Function: Adds the following LoL Account to the Data Base
    Exception: If the region or LoL account is invalid, says so
    """
    unofficialRegion = region
    unofficialName = summoner

    has_role = lambda role_name: role_name in [r.name.lower() for r in ctx.author.roles]
    if not (ctx.author.guild_permissions.administrator or has_role("lolmanager") or has_role("lol manager")): # Does not have permission to do this command
        embed = Embed(title="Needs Permission", description="Sorry, you must either be administrator or have \"LoLManager\" role", color=0xff0033)
        await ctx.send(embed=embed)
        return
    
    try:
        summoner = Summoner(unofficialName, unofficialRegion)
        try:
            await getSummoner(summoner, ctx.guild.id)
            # Account already exists in database
            embed = Embed(title="Account already Saved", description="The summoner __{0}__ is already saved into this server account list".format(summoner.summonerName), color=0xff0033)
            await ctx.send(embed=embed)
        
        except ObjectDoesNotExist: # Account that is not already in the database 
            await storeSummoner(summoner, ctx.guild.id)
            embed = Embed(title="Summoner __{0}__ successfully added to the server accounts list".format(summoner.summonerName), description="{0} will now be tracked from !lol commands".format(summoner.summonerName), color=0x50c878)
            await ctx.send(embed=embed)

    except InvalidRegion:
        embed = Embed(title="Invalid Region", description="!lol add (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
        await ctx.send(embed=embed)
    except InvalidSummonerName:
        embed = Embed(title="Invalid Summoner", description="!lol add (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
        await ctx.send(embed=embed)




@slash.subcommand(base="lol", name="del", description="Deletes the summoner in the region to the server summoner list",
        options=[
            create_option(
                name="region",
                description="Summoner's Region",
                option_type=3,
                required=True,
                choices=regionChoices
            ),
            create_option(
                name="summoner",
                description="Summoner Name",
                option_type=3,
                required=True
            )
        ])
async def _loldel(ctx: SlashContext, region, summoner):
    """
    Command: !lol del (region) (LoL Account)
    Function: Deletes the following LoL Account from the Data Base
    Exception: If the region or LoL account is invalid, says so
                If the account is not in the server data base, says so
    """
    unofficialRegion = region
    unofficialName = summoner

    has_role = lambda role_name: role_name in [r.name.lower() for r in ctx.author.roles]
    if not (ctx.author.guild_permissions.administrator or has_role("lolmanager") or has_role("lol manager")): # Does not have permission to do this command
        embed = Embed(title="Needs Permission", description="Sorry, you must either be administrator or have \"LoLManager\" role", color=0xff0033)
        await ctx.send(embed=embed)
        return
    
    try:
        summoner = Summoner(unofficialName, unofficialRegion)
        await deleteSummoner(summoner, ctx.guild.id)
        embed = Embed(title="Summoner __{0}__ successfully deleted from server DataBase".format(summoner.summonerName), description="{0} will now not be tracked from !lol commands".format(summoner.summonerName), color=0x50c878)
        await ctx.send(embed=embed)
    except InvalidRegion:
        embed = Embed(title="Invalid Region", description="!lol add (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
        await ctx.send(embed=embed)
    except InvalidSummonerName:
        embed = Embed(title="Invalid Summoner", description="!lol add (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
        await ctx.send(embed=embed)
    except ObjectDoesNotExist:
        embed = Embed(title="Summoner Not In List", description="!lol add (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="The summoner __{0}__ is not in the server list from the beginning".format(unofficialName), value="\u200b", inline=False)
        await ctx.send(embed=embed)



@slash.subcommand(base="lol", name="accounts", description="Gives all LoL accounts linked to you in this server",
            options=[
                create_option(
                    name="user",
                    description="Discord User (Mention)",
                    option_type=6,
                    required=False
                )
            ])
async def _lolaccs(ctx: SlashContext, user=None):
    """
    Command: !lol accounts
    Function: Gives all of the accounts linked by the user
    """
    discordUser = user
    if discordUser is None:
        discordUser = ctx.author
    embed = Embed(title="Linked Accounts", description = "(For {0})".format(discordUser.mention), color=0xb09e99)
    summoners = await discordServerUserSummoners(ctx.guild.id, discordUser.id)

    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    for summoner in summoners:
        embed.add_field(name=regionEmojis[summoner.region] + "    " + summoner.summonerName, value="\u200b", inline=False)

    await ctx.send(embed=embed)
 


@slash.subcommand(base="lol", name="auth", description="Checks if the authentication for summoner linking is successful for the user")
async def _lolauthcheck(ctx: SlashContext):
    """
    Command: !lol auth
    Function: Chekcs if the profile authentication process worked validly
    """
    discordManager = discordManagerFinder(ctx.guild.id)
    try:
        if discordManager.accountsManager.checkProfile(ctx.author.id):
            # New profile checked, authentication successful
            summoner = discordManager.accountsManager.authAccounts[ctx.author.id]
            embed = Embed(title="Summoner __{0}__ successfully authenticated!".format(summoner.summonerName), description="{0} is now an authenticated account for {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
            await ctx.send(embed=embed)
        else:
            # Profile did not match, authentication unsuccessful, suggest that user retry
            embed = Embed(title="Profile Icons do not Match", description="Make sure your profile icon matches the one the bot gave, and retry !lol auth", color=0xff0033)
            await ctx.send(embed=embed)
    except KeyError: # Nothing to auth from the first place
        embed = Embed(title="You have nothing to authenticate check from the first place", description="\u200b", color=0xff0033)
        await ctx.send(embed=embed)



@slash.subcommand(base="lol", name="unauth", description="Stops the summoner linking authentication process for the user")
async def _lolunauth(ctx: SlashContext):
    """
    Command: !lol unauth
    Function: Stops the summoner linking authentication process for the user
    """
    discordManager = discordManagerFinder(ctx.guild.id)
    try:
        discordManager.accountsManager.removeUser(ctx.author.id)
        embed=Embed(title="You have stopped your authentication process", description="\u200b", color=0x50c878)
        await ctx.send(embed=embed)
    except KeyError: # Author has not requested authentication for anything
        embed=Embed(title="You have not authenticated any account from the beginning", description="(Authentication Process automatically expires after 5 minutes)", color=0xff0033)
        await ctx.send(embed=embed)



@slash.subcommand(base="lol", name="link", description="Links the summoner in the region to the user (authentication required)",
        options=[
            create_option(
                name="region",
                description="Summoner's Region",
                option_type=3,
                required=True,
                choices=regionChoices
            ),
            create_option(
                name="summoner",
                description="Summoner Name",
                option_type=3,
                required=True
            )
        ])
async def _lollink(ctx: SlashContext, region, summoner):
    """
    Command: !lol link (region) (LoL Account)
    Function: Links the following LoL Account to the Discord User
    Exception: If the region or LoL account is invalid, says so
                If the account is already linked, says so
    """
    unofficialRegion = region
    unofficialName = summoner
    
    # Check if summoner is valid
    summoner = None
    try:
        summoner = Summoner(unofficialName, unofficialRegion)
    except InvalidRegion:
        embed = Embed(title="Invalid Region", description="!lol link (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
        await ctx.send(embed=embed)
        return
    except InvalidSummonerName:
        embed = Embed(title="Invalid Summoner", description="!lol link (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
        await ctx.send(embed=embed)
        return

    # Do different actions based on if account is in database (with/without discord user linked)
    try:
        DBsummoner = await getSummonerUser(summoner, ctx.guild.id, ctx.author.id)
        # Already Linked
        embed = Embed(title="Summoner __{0}__ already linked to you!".format(summoner.summonerName), description="{0} is already and will continue to be linked to {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
        await ctx.send(embed=embed)
    except ObjectDoesNotExist: # Not already linked
        # First need to authenticate the account (profile authentication)
        discordManager = discordManagerFinder(ctx.guild.id)
        if discordManager.accountsManager.authedCheck(summoner):
            discordManager.accountsManager.removeAuthedUser(ctx.author.id)
            try: 
                await giveSummonerUser(summoner, ctx.guild.id, ctx.author.id)
                # Account inside Server Database already, without owner
                embed = Embed(title="Summoner __{0}__ successfully linked to you!".format(summoner.summonerName), description="{0} will now be linked to {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
                await ctx.send(embed=embed)
            except AlreadyLinkedAccount: # Account already linked to another person.
                embed = Embed(title="Sorry, Summoner __{0}__ is already linked to another user".format(summoner.summonerName), description="\u200b", color=0xff0033)
                await ctx.send(embed=embed)
            except ObjectDoesNotExist: # Account not in database, need to add newly
                await storeSummonerUser(summoner, ctx.guild.id, ctx.author.id)
                embed = Embed(title="Summoner __{0}__ successfully linked to you!".format(summoner.summonerName), description="{0} will now be linked to {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
                await ctx.send(embed=embed)
        else:
            embed = Embed(title="Before linking, you must authenticate that Summoner __{0}__ is your account!".format(summoner.summonerName), description="\u200b", color=0x50c878)
            embed.add_field(name="Preparing Authentication Process...", value="\u200b", inline=False)
            await ctx.send(embed=embed)

            # Need Authentication
            # Check if Owned Account
            try:
                isOwned = await isOwnedSummoner(summoner, ctx.guild.id)
                if isOwned:
                    embed = Embed(title="Summoner __{0}__ is already linked to a user, so authentication is unavailable".format(summoner.summonerName), description="\u200b", color=0xff0033)
                    await ctx.send(embed=embed)
                    return
            except Exception:
                pass

            try:
                profileDict = discordManager.accountsManager.suggestNewProfile(summoner, ctx.author.id)
                
                embed=Embed(title="Change Account Profile Icon to the picture sent in DM", description="\u200b", color=0x50c878)
                embed.add_field(name="Then do !lol auth", value="(Authentication Process automatically expires after 5 minutes)", inline=False)
                await ctx.send(embed=embed)
                
                embed=Embed(title="Change Account Profile for __{0}__ to this:".format(summoner.summonerName), description="(Authentication Process automatically expires after 5 minutes)", color=0x50c878)
                embed.set_image(url=profileDict['picture'])
                await ctx.author.send(embed=embed)

                discordManager.accountsManager.setStartTime(ctx.author.id, ctx.author)
            except OtherUserAuth:
                embed=Embed(title="An other user is authenticating this account already", description="\u200b", color=0xff0033)
                await ctx.send(embed=embed)
            except IconAlreadySuggested:
                embed=Embed(title="You already did this command!", description="\u200b", color=0xff0033)
                await ctx.send(embed=embed)
            except UserAnotherAuth:
                embed=Embed(title="You are already authorizing another account. Do !lol unauth first to authorize this account", description="\u200b", color=0xff0033)
                await ctx.send(embed=embed)




@slash.subcommand(base="lol", name="unlink", description="Unlinks the summoner in the region from the user",
        options=[
            create_option(
                name="region",
                description="Summoner's Region",
                option_type=3,
                required=True,
                choices=regionChoices
            ),
            create_option(
                name="summoner",
                description="Summoner Name",
                option_type=3,
                required=True
            )
        ])
async def _lolunlink(ctx: SlashContext, region, summoner):
    """
    Command: !lol unlink (region) (LoL Account)
    Function: Unlinks the following LoL Account to the Discord User (including deletion of the account from server database)
    Exception: If the region or LoL account is invalid, says so
                If the account is not linked by the user, says so
    """
    unofficialRegion = region
    unofficialName = summoner
    
    # Check if summoner is valid
    summoner = None
    try:
        summoner = Summoner(unofficialName, unofficialRegion)
    except InvalidRegion:
        embed = Embed(title="Invalid Region", description="!lol link (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Region should be within the following:", value=invalidRegionMsg, inline=False)
        await ctx.send(embed=embed)
        return
    except InvalidSummonerName:
        embed = Embed(title="Invalid Summoner", description="!lol link (region) (account name)", color=0xff0033)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="The summoner __{0}__ is not found, at least in the selected region".format(unofficialName), value="\u200b", inline=False)
        await ctx.send(embed=embed)
        return
    
    try: # Try deleting
        await deleteSummonerUser(summoner, ctx.guild.id, ctx.author.id)
        # Already Linked
        embed = Embed(title="Summoner __{0}__ successfully unlinked and deleted!".format(summoner.summonerName), description="{0} is now unlinked from {1}".format(summoner.summonerName, ctx.author.mention), color=0x50c878)
        await ctx.send(embed=embed)
    except ObjectDoesNotExist: # Not an account linked
        embed = Embed(title="Summoner __{0}__ was not linked to you from the beginning.".format(summoner.summonerName), description="\u200b", color=0xff0033)
        await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for guild in bot.guilds:
        discordManagerList.append(DiscordManager(discordServer = guild.id))
    # Remove the Servers Bot is in for Emojis
    discordManagerList.remove(DiscordManager(discordServer = 813197122962587649))
    discordManagerList.remove(DiscordManager(discordServer = 813197673124331522))
    discordManagerList.remove(DiscordManager(discordServer = 813198200319377450))
    discordManagerList.remove(DiscordManager(discordServer = 813198617245909003))
    discordManagerList.remove(DiscordManager(discordServer = 813605793601159198))
    print(discordManagerList)
    for discordManager in discordManagerList:
        matchManager = discordManager.matchManager
        # task = asyncio.create_task(executePeriodically(20, matchManager.deleteOutdated))
        task = asyncio.create_task(executePeriodically(20, discordManager.periodicCheck))
    
TOKEN = 'private info'
bot.run(TOKEN)