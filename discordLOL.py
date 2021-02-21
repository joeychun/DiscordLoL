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


APIKey = 'RGAPI-7559e246-26f3-4437-9034-c5c9ca80161f'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

### EXCEPTIONS
class InvalidRegion(Exception):
    pass

class InvalidSummonerName(Exception):
    pass

class InvalidMatch(Exception):
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

### FUNCTIONS REGARDING RIOT API
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
    
    if team1 != []:
        participants.append(team1)
    if team2 != []:
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


def circleSorter(summonerPresentingList): # MIGHT NOT BE USED, TODO
    """
    Sorts the list of summoner present info by In Game.
    --------------------
    summonerPresentingList: List of string of presentSummoner information
    """
    pass

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

    def __init__(self, emoji, hexcolor):
        self.emoji = emoji
        self.hexcolor = hexcolor
        self.available = True
    
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
        # HEXCOLOR IS TODO
        # 🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪
        self.discordServer = discordServer
        self.allCircles = [
            Circle("🔴", 0x000000),
            Circle("🟠", 0x000000),
            Circle("🟡", 0x000000),
            Circle("🟢", 0x000000),
            Circle("🔵", 0x000000),
            Circle("🟣", 0x000000),
            Circle("🟤", 0x000000),
            Circle("⚫", 0x000000),
            Circle("⚪", 0x000000)
        ]
    
    def getAvailableEmojis(self):
        return [circle for circle in self.allCircles if circle.available]

    def distribEmoji(self):
        availEmojis = self.getAvailableEmojis()
        choosedCircle = random.choice(availEmojis)

        for index in range(len(self.allCircles)): # Need to disable availibility
            circle = self.allCircles[index]
            if circle.matchesEmoji(choosedCircle.emoji):
                circle.available = False
        
        return choosedCircle
    
    def freeOutdated(self): # MIGHT NOT USE: TODO
        """
        Frees circles that are no longer in use due to the match ending.
        Freed circles will be able to be used for attributing other matches
        """
        pass
                

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
        for team in self.infoDict["participants"]:
            for player in team:
                if player["summonerName"] == summonerName:
                    return player["champion"]
        
        return False

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
            self.updateTime(gameId) # MIGHT NOT USE: TODO
            return temp

    def getAll(self, playersList):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns dictionary with gameId as key and List of summonerName, presentSummoner dictionary as value
        --------------------
        playersList: Dictionary of region as key and List of Summoners as value
        """
        gameIdList = set()  # Will be used to initialize match's updateRequest to True
        sortedByGame = {}
        for region, players in playersList.items():
            for summoner in players:
                try:
                    gameId = summoner.getMatchInfo(matchManager, circleManager, store=True)
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
                    # print(summoner.presentSummoner(matchManager, gameId, requestedTime))
                    
                    if gameId not in sortedByGame.keys():
                        sortedByGame[gameId] = []
                    
                    temp = {
                        "summonerName": summoner.summonerName,
                        "presentSummoner": summoner.presentSummoner(matchManager, gameId, requestedTime)
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
    
    def presentAll(self, playersList):
        """
        Goes through every player from the list, stores or updates time info, and returns it
        Returns string of summoner and summoner live match information for each summoner
        --------------------
        playersList: Dictionary of region as key and List of Summoners as value
        """
        returnStr = ""
        gamesDict = self.getAll(playersList)
        for gameId, summonerDictList in gamesDict.items():
            for summonerDict in summonerDictList:
                returnStr += summonerDict["summonerName"]
                returnStr += "\n"
                returnStr += summonerDict["presentSummoner"]
                returnStr += "\n\n"

        return returnStr



    def deleteOutdated(self): # Will get called every 20 seconds
        """
        Will check for outdated (already ended) matches in self.matches, and will erase their information
        """
        temp = self.matches.copy()
        for gameId, matchDict in self.matches.items():
            match = matchDict["match"]
            participants = match.infoDict["participants"]
            
            firstParticipant = None
            for team in participants:
                for player in team:
                    if player["isBot"] is False:
                        firstParticipant = player
                        break
            firstPlayer = Summoner(firstParticipant["summonerName"], match.region)
            # participants[0][0]["summonerId"]
            try:
                firstPlayer.getMatchInfo(self)
                continue
            except InvalidMatch:
                # Match is Invalid; should get deleted
                match.circle.available = True # The circle used for this ended match is now avail for use
                del temp[gameId]
        
        self.matches = temp.copy()



matchManager = MatchManager(discordServer = 1)
circleManager = CircleManager(discordServer = 1)

matchManagerList = [
    matchManager
]

# print(timeChanger(1613827905777))

### PLAYERS LIST
koreans = [
    Summoner("sahngwonL12", "kr"),
    Summoner("Fireknight25", "kr"),
    Summoner("Fireknight", "kr"),
    Summoner("EviliotoJeffrey", "kr"),
    Summoner("JEEEEFFFFF", "kr"),
    Summoner("yeonwooc24", "kr"),
    Summoner("yummykhan05", "kr"),
    Summoner("ryanrb", "kr"),
    Summoner("인절미 스낵", "kr"),
    Summoner("크레이지캣66", "kr")
]
playersList = {"kr": koreans}

"""
print(matchManager.presentAll(playersList))

updateRequestGlobal = 1
for region, players in playersList.items():
    for summoner in players:
        try:
            gameId = summoner.getMatchInfo(matchManager, circleManager, store=True)
            print(summoner.presentSummoner(matchManager, gameId))
        except InvalidMatch:
            print("MATCH INVALID")"""


### BOT COMMANDS

@bot.command(pass_context=True, aliases=['OPGG'])
async def opgg(ctx, *args):
    """
    Command that will give information about a live match of a summoner, or will execute actions regarding that information
    """
    if ctx.author == bot.user:
        return

    if args[0].lower() == "rn" and len(args) == 1:
        await ctx.send(matchManager.presentAll(playersList))

@bot.command(pass_context=True)
async def hanpoo(ctx): 
    """
    Testing global emoji usage of bot; will be deleted in the future
    """
    if ctx.author == bot.user:
        return
    
    await ctx.send("<:hanpoo:800567372834406470>")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for matchManager in matchManagerList:
        task = asyncio.create_task(executePeriodically(20, matchManager.deleteOutdated))
    

TOKEN = 'PRIVATE INFO'
bot.run(TOKEN)