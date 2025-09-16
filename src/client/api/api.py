import json
import logging

import requests

from ..config import settings

logger = logging.getLogger("hijacker.app")


def fetch_target_process_name():
    logger.info("Fetching target's process name...")
    try:
        response = requests.get(settings.server_url + "/api/target/")
        target_process = response.json().get("target")
        logger.info(f"Target's process name acquired: {target_process}")
        return target_process
    except json.JSONDecodeError:
        logger.error("Failed to fetch target's process name.")
