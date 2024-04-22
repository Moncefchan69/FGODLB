import os
import requests
import time
import json
from datetime import datetime
import user
import coloredlogs
import logging

# Enviroments Variables
userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
fate_region = os.environ['fateRegion']
webhook_discord_url = os.environ['webhookDiscord']

UA = os.environ['UserAgent']

if UA:
    # Assuming fgourl is not used for UserAgent configuration
    pass

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def check_blue_apple_cron(instance):
    # Remove code related to bluebroncefruit
    pass


def get_latest_verCode():
    endpoint = ""

    if fate_region == "NA":
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/NA/VerCode.json"
    else:
        endpoint += "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"

    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        logger.info('Getting Latest Assets Info')

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                logger.info('Logging in!')
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                try:
                    time.sleep(2)
                    logger.info('Starting Friend Point summoning!!')
                    for _ in range(1):  # You can define how many times to automatically draw FP summon each login (default is 1 time)
                        instance.drawFP()
                        time.sleep(4)
                except Exception as ex:
                    logger.error(ex)

            except Exception as ex:
                logger.error(ex)


if __name__ == "__main__":
    main()
