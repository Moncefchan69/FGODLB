import requests
import json

from mytime import GetTimeStamp

# Get Friend Summon Gacha Sub Id
def GetGachaSubIdFP(region):
    response = requests.get(f"https://git.atlasacademy.io/atlasacademy/fgo-game-data/raw/branch/{region}/master/mstGachaSub.json");
    gachaList = json.loads(response.text)
    timeNow = GetTimeStamp()
    priority = 0
    goodGacha = {}
    for gacha in gachaList:
        openedAt = gacha["openedAt"]
        closedAt = gacha["closedAt"]

        if openedAt <= timeNow & timeNow <= closedAt:
            p = int(gacha["priority"])
            if(p > priority):
                priority = p
                goodGacha = gacha
    return str(goodGacha["id"])
