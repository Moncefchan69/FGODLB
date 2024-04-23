import main
import requests
import user


def topLogin(data: list) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]

    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name is not None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Login System - " + main.fate_region,
                "description": f"Login successful. Listing character information.\n\n{messageBonus}",
                "color": 563455,
                "fields": [
                    {
                        "name": "Level",
                        "value": f"{rewards.level}",
                        "inline": True
                    },
                    {
                        "name": "Summon Tickets",
                        "value": f"{rewards.ticket}",
                        "inline": True
                    },
                    {
                        "name": "Saint Quartz",
                        "value": f"{rewards.stone}",
                        "inline": True
                    },
                    {
                        "name": "Saint Quartz Fragments",
                        "value": f"{rewards.sqf01}",
                        "inline": True
                    },
                    {
                        "name": "Golden Apples",
                        "value": f"{rewards.goldenfruit}",
                        "inline": True
                    },
                    {
                        "name": "Silver Apples",
                        "value": f"{rewards.silverfruit}",
                        "inline": True
                    },
                    {
                        "name": "Bronze Apples",
                        "value": f"{rewards.bronzefruit}",
                        "inline": True
                    },
                    {
                        "name": "Blue Apples",
                        "value": f"{rewards.bluebronzefruit}",
                        "inline": True
                    },
                    {
                        "name": "Blue Apple Saplings",
                        "value": f"{rewards.bluebronzesapling}",
                        "inline": True
                    },
                    {
                        "name": "Login Streak",
                        "value": f"{login.login_days}",
                        "inline": True
                    },
                    {
                        "name": "Total Login Days",
                        "value": f"{login.total_days}",
                        "inline": True
                    },
                    {
                        "name": "White Cubes",
                        "value": f"{rewards.pureprism}",
                        "inline": True
                    },
                    {
                        "name": "Friendship Points",
                        "value": f"{login.total_fp}",
                        "inline": True
                    },
                    {
                        "name": "Friendship Points Gained Today",
                        "value": f"+{login.add_fp}",
                        "inline": True
                    },
                    {
                        "name": "Current Maximum AP",
                        "value": f"{login.act_max}",
                        "inline": True
                    },
                    {
                        "name": "Holy Grail",
                        "value": f"{rewards.holygrail}",
                        "inline": True
                    },
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara01.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def shop(item: str, quantity: str) -> None:
    endpoint = main.webhook_discord_url

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Automatic Shopping System - " + main.fate_region,
                "description": f"Purchase successful.",
                "color": 5814783,
                "fields": [
                    {
                        "name": f"Shop",
                        "value": f"Spent {40 * quantity} AP to buy {quantity}x {item}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo2/images/commnet_chara10.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def drawFP(servants, missions) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""

    if len(servants) > 0:
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt_lang_en.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            svt = svt_dict[servant.objectId]
            message_servant += f"`{svt['name']}` "

    if len(missions) > 0:
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Automatic Summoning System - " + main.fate_region,
                "description": f"Complete free friend summon for the day. Listing summon results.\n\n{message_mission}",
                "color": 5750876,
                "fields": [
                    {
                        "name": "Friend Point Pool",
                        "value": f"{message_servant}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara02_rv.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)
