import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

def configure_logging():
    logging.basicConfig(level=logging.DEBUG)

def retrieve_environment_variables():
    global userIds, authKeys, secretKeys, userNums, authKeyNums, secretKeyNums, UA
    userIds = os.environ['userIds'].split(',')
    authKeys = os.environ['authKeys'].split(',')
    secretKeys = os.environ['secretKeys'].split(',')
    userNums = len(userIds)
    authKeyNums = len(authKeys)
    secretKeyNums = len(secretKeys)
    fgourl.ver_code_ = os.environ['verCode']
    fate_region = os.environ['fateRegion']
    webhook_discord_url = os.environ['webhookDiscord']
    blue_apple_cron = os.environ.get("MAKE_BLUE_APPLE")
    
    UA = os.environ['UserAgent']
    if UA:
        fgourl.user_agent_ = UA

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def check_blue_apple_cron(instance):
    if blue_apple_cron:
        cron = croniter(blue_apple_cron)
        next_date = cron.get_next(datetime)
        current_date = datetime.now()

        if current_date >= next_date:
            logger.info('Exchanging Blue Fruit!')
            instance.buyBlueApple(1)
            time.sleep(2)


def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/xdeadboy666x/FGO-VerCode-extractor/JP/VerCode.json"

    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    configure_logging()
    retrieve_environment_variables()
    if userNums == authKeyNums and userNums == secretKeyNums:
        logger.info('Fetching Game Data')
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                logger.info('Login in...')
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                instance.lq001()
                instance.lq002()
                time.sleep(2)

                check_blue_apple_cron(instance)
                logger.info('Exchanging Blue Fruit!')
                try:
                    instance.buyBlueApple(1)
                    time.sleep(2)
                    for _ in range(3):
                        instance.buyBlueApple(1)
                        time.sleep(2)
                except Exception as ex:
                    logger.error(ex)

            except Exception as ex:
                logger.error(ex)


if __name__ == "__main__":
    main()
