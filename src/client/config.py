import logging
from pathlib import Path
from time import sleep

from pydantic_settings import BaseSettings

logger = logging.getLogger("hijacker.app")


class Settings(BaseSettings):
    server_url: str

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        env_path = Path(self.Config.env_file)
        if not env_path.exists():
            logger.info("No .env file found, initiating setup...")
            sleep(0.1)
            server_url = input("Enter the server URL: ")
            env_path.write_text(
                f"SERVER_URL={server_url}\n"
            )
            logger.info(".env file created successfully.")

        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name in self.model_fields:
            env_path = Path(self.Config.env_file)
            new_settings = [f"{k}={v}" if k != name else f"{name}={value}" for k, v in self.model_fields.items()]
            env_path.write_text("\n".join(new_settings))
            logger.info(f"Updated {name} in .env file.")

settings = Settings()
