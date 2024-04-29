import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging
from datetime import datetime
from croniter import croniter

# Environment Variables
userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
fate_region = os.environ['fateRegion']
webhook_discord_url = os.environ['webhookDiscord']
blue_apple_cron = os.environ.get("MAKE_BLUE_APPLE")

UA = os.environ.get('UserAgent')  # Use get() to avoid KeyError if 'UserAgent' is not set

if UA:
    fgourl.user_agent_ = UA
    
userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

# Configure logging
logger = logging.getLogger("FGO Daily Login")
logger.setLevel(logging.DEBUG)  # Set the root logger level to DEBUG

# Console handler for printing logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the console handler level to DEBUG

# Formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

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
    if userNums == authKeyNums and userNums == secretKeyNums:
        logger.info('Fetching Game Data')
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                
                # Retry login if initial login fails due to server error
                retry_count = 3
                while retry_count > 0:
                    logger.info('Logging in...')
                    try:
                        instance.topLogin()
                        break  # Login successful, exit retry loop
                    except Exception as ex:
                        logger.error(f'Login attempt failed: {ex}')
                        logger.info(f'Retrying login ({retry_count} attempts left)')
                        retry_count -= 1
                        time.sleep(2)
                
                if retry_count == 0:
                    logger.error('Login failed after multiple attempts')
                    continue  # Skip to the next user if login fails

                logger.info('Login successful')
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
                    logger.debug("Exception occurred during blue apple exchange")

            except Exception as ex:
                logger.error(ex)
                logger.debug("Exception occurred during main loop iteration")

if __name__ == "__main__":
    main()
