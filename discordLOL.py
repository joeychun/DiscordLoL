# Work with Python 3.6

# https://discord.com/api/oauth2/authorize?client_id=739069897606299648&permissions=1073883200&scope=bot

import requests
import json

import random

import time, datetime

import discord, asyncio
from discord.ext import commands, tasks
from discord import Embed
from asyncio import sleep


APIKey = 'RGAPI-cf8029e9-3170-4e31-a5f0-547104beb46e'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

### EXCEPTIONS
class InvalidRegion(Exception):
    pass

class InvalidSummonerName(Exception):
    pass

class InvalidMatch(Exception):
    pass

class NotCircled(Exception):
    pass


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
  32: "Snowball"
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
}

champIdsReversed = {
    "Aatrox": 266,
    "Ahri": 103,
    "Akali": 84,
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
    "Samira": "<:Samira:813197898610114580>",
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
  "Snowball": "<:Snowball:813606194743738418>"
}

### FUNCTIONS
def checkValidRegion(region):
    """
    Checks if the region is valid.
    If not valid, returns False.
    If valid, returns the region string.
    --------------------
    region: The region to check
    """
    
    availRegions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "ru", "tr1"]
    if region.lower() in availRegions:
        return region.lower()
    else:
        return False

def discordManagerFinder(discordServer):
    """
    When given a discordServer ID,
    Returns a discordManager object that is connected to that discord server
    --------------------
    discordServer: Discord server ID
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
    print(type(func))
    while True:
        await asyncio.sleep(time)
        await func()



### CLASSES
class Summoner:
    """
    Manages Summoner Info
    --------------------
    unofficialSummonerName: A summoner name that is not the official name, due to difference in case or spaces
    unofficialRegion: An unofficial region of the summoner
    """

    def __init__(self, unofficialSummonerName, unofficialRegion):
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
            print(infoDict)
            infoDict = matchDictReader(infoDict)
            print(infoDict)
            if store:
                # Check if match already stored
                # if matchManager.matchExists(gameId=infoDict["gameId"])
                matchManager.append(gameId=infoDict["gameId"], infoDict=infoDict, region=self.region, isCircled=True, circleManager=circleManager, circle=None)
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

    def __init__(self, emoji, hexcolor=0x00ff00):
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
    discordServer: ID of the discord server
    allCircles: List of Circle objects that could be used
    """

    def __init__(self, discordServer):
        # Emoji Circles that will be used: 🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪
        self.discordServer = discordServer
        self.allCircles = [
            Circle("🔴", 0xff0000),
            Circle("🟠", 0xffa500),
            Circle("🟡", 0xffff00),
            Circle("🟢", 0x00ff00),
            Circle("🔵", 0x0000ff),
            Circle("🟣", 0xb19cd9),
            Circle("🟤", 0xb5651d),
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
        print(self.infoDict["participants"])
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

        returnDict = {
            "Circle": self.circle.emoji,
            "MatchType": infoDict["gameQueue"]["description"] + " : " + infoDict["gameQueue"]["map"],
            "Time": timeChanger(infoDict["gameStartTime"])
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
    discordServer: ID of the discord server
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
        # Creates a circle for the Match
        if isCircled and circle is None:
            circle = circleManager.distribEmoji()


        match = self.create(gameId=gameId, infoDict=infoDict, region=region, isCircled=isCircled, circle=circle)
        if self.matchExists(gameId): # Does not store if already existing
            return False
        else:
            temp = {}
            temp["match"] = match
            temp["updateRequest"] = True
            self.matches[gameId] = temp
            self.updateTime(gameId)
            return temp

    def getAll(self, circleManager, playersList):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns dictionary with gameId as key and List of summonerName, presentSummoner dictionary as value
        --------------------
        circleManager: Manager of the circles; used to distribute 
        playersList: Dictionary of region as key and List of Summoners as value
        """
        gameIdList = set()  # Will be used to initialize match's updateRequest to True
        sortedByGame = {}
        for region, players in playersList.items():
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
    
    def presentAll(self, circleManager, playersList):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns string of summoner and summoner live match information for each summoner
        --------------------
        circleManager: Manager of the circles; used to distribute 
        playersList: Dictionary of region as key and List of Summoners as value
        """
        returnStr = ""
        gamesDict = self.getAll(circleManager, playersList)
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
        returnStr += "\n🟥 **Red Team**\n"
        returnStr += "🟥 <:Gnar:813197316601151488> FireKnight          <:Ignite:813606194471370762> <:Flash:813606194278825984>\n"
        return returnStr

    def matchInfo(self, circle):
        """
        Presents Live Match Information of a match associated to do circle
        Will be used for !opgg match command
        Returns.... TODO
        """
        matchDict = self.circleMatch(circle)
        match = matchDict["match"]
        # TODO: PRESNT MATCH

        firstParticipant = match.firstParticipant()
        firstSummoner = Summoner(firstParticipant["summonerName"], match.region)
        k = firstSummoner.getMatchInfo(self)


    async def deleteOutdated(self): # Will get called every 20 seconds
        """
        Will check for outdated (already ended) matches in self.matches, and will erase their information
        """
        temp = self.matches.copy()
        for gameId, matchDict in self.matches.items():
            match = matchDict["match"]
            participants = match.infoDict["participants"]
            
            firstParticipant = match.firstParticipant()
            firstSummoner = Summoner(firstParticipant["summonerName"], match.region)
            # participants[0][0]["summonerId"]
            try:
                firstSummoner.getMatchInfo(self)
                continue
            except InvalidMatch:
                # Match is Invalid; should get deleted
                match.circle.available = True # The circle used for this ended match is now avail for use
                del temp[gameId]
        
        self.matches = temp.copy()

class DiscordManager:
    """
    Will Manage all the Managers for one discord server, including
    MatchManager, CircleManager, and SQLite (maybe in the future, TODO)
    --------------------
    discordServer: The ID of the discord server
    summonersList: List of summoners in the server
    """

    def __init__(self, discordServer, summonersList=[]):
        self.discordServer = discordServer
        self.matchManager = MatchManager(discordServer = discordServer)
        self.circleManager = CircleManager(discordServer = discordServer)
        self.summonersList = playersList


### PLAYERS LIST
koreans = [
    Summoner("sahngwonL12", "kr"),
    Summoner("Fireknight25", "kr"),
    Summoner("Fireknight", "kr"),
    Summoner("EviliotoJeffrey", "kr"),
    Summoner("점멸혐오자", "kr"),
    Summoner("joshuah22", "kr"),
    Summoner("돼지야작작먹어", "kr"),
    Summoner("JEEEEFFFFF", "kr"),
    Summoner("Hangry05", "kr"),
    Summoner("yeonwooc24", "kr"),
    Summoner("yummykhan05", "kr"),
    Summoner("ryanrb", "kr"),
    Summoner("인절미 스낵", "kr"),
    Summoner("크레이지캣66", "kr"),
    Summoner("GP아아아", "kr"),
    Summoner("그냥 제이스장인", "kr"),
]
americans = [
    Summoner("Anda", "na1")
]
playersList = {"kr": koreans, "na1": "Anda"}

# MY TWO BOT TEST DISCORD SERVERS
discordManager1 = DiscordManager(discordServer = 511516851289849856, summonersList = playersList)
discordManager2 = DiscordManager(discordServer = 457485526606544897, summonersList = playersList)
discordManagerList = [ # WILL EVENTUALLY BECOME A DATABASE WITH SQLite
    discordManager1,
    discordManager2
]


### BOT COMMANDS

@bot.command(pass_context=True, aliases=['OPGG'])
async def opgg(ctx, *args):
    """
    Command that will give information about a live match of a summoner, or will execute actions regarding that information
    """
    if ctx.author == bot.user:
        return

    if args[0].lower() == "rn" and len(args) == 1:
        """
        Command: !opgg rn
        Function: Gives a list of summoners that are currently in a game, also giving
                their live match information
        """
        embed = discord.Embed(title="Who is in a game of League of Legends?", description="People In This Server:", color=0x00ff00)
        discordManager = discordManagerFinder(ctx.guild.id)
        gamesDict = discordManager.matchManager.getAll(discordManager.circleManager, playersList)

        for gameId, summonerDictList in gamesDict.items():
            for summonerDict in summonerDictList:
                embed.add_field(name="✅  " + summonerDict["summonerName"], value=summonerDict["presentSummoner"], inline=False)
        
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def champimgs(ctx, *args):
    """
    Testing global emoji usage of bot; will be deleted in the future
    """
    name = ""
    for a in args:
        name += a
        name += " "
    name = name[0:-1]

    await ctx.send(champEmojis[name])

@bot.command(pass_context=True)
async def spellimgs(ctx, name):
    """
    Testing global emoji usage of bot; will be deleted in the future
    """

    await ctx.send(spellEmojis[name])

@bot.command(pass_context=True)
async def test(ctx, *args):
    """
    Test of how !opgg match would be templated
    """
    await ctx.send(matchManager.testPrintMatch())

@bot.command(pass_context=True)
async def testembed(ctx, *args):
    """
    Test of how !opgg match would be templated (including Embed)
    """
    embed = discord.Embed(title="In Game: (O)", description=".", color=0x00ff00)
    # USE OF BLANK CHARACTER
    embed.add_field(name="Just a test             <:Flash:813606194278825984>", value="Just a test     <:Flash:813606194278825984>\nJust a test", inline=False)
    # JUST
    embed.add_field(name="Just a test", value="Just a test", inline=False)
    
    # TODO, maybe: SHOULD HAVE GOOD USE OF THIS " " CHARACTER blank character.
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for discordManager in discordManagerList:
        matchManager = discordManager.matchManager
        print(type(matchManager))
        print(type(matchManager.deleteOutdated))
        task = asyncio.create_task(executePeriodically(20, matchManager.deleteOutdated))
    

TOKEN = 'private info"
bot.run(TOKEN)