"""General Utilities for the SFMC Scraper.

Functions:
    load_config: Load the config file.
"""

import logging
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def load_config() -> dict[str, Any]:
    """Load the config file."""
    yaml = YAML()
    with open("config.yaml", "r") as file:
        config: dict[str, Any] = yaml.load(file)
    config["success"] = 0
    config["failed_content"] = 0
    config["failed_page"] = 0
    logger.info("Config loaded.")
    return config


def save_to_file(content: str, filename: Path) -> None:
    """Save the content to a file.

    Args:
        content (str): the content to save
        filename (Path): the filename to save to
    """
    with open(filename, "w") as file:
        file.write(content)
    logger.info(f"Saved to {filename}")


logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("scraper.log"))
logger.info("Starting the scraper")
