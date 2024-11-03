"""Functions to scrape the Salesforce Marketing Cloud documentation.

Functions:
"""

import asyncio
from pathlib import Path
from typing import Any

from playwright.async_api import Browser, async_playwright

from . import utils
from .crawling import crawl_website_map, save_website_map
from .page_loading import get_browser


async def _run(config: dict[str, Any]) -> None:
    """Run the main async function."""
    scraped_data = Path("scraped")
    website_map: dict[str, str | None] = {config["initial-card"]: None}
    async with async_playwright() as playwright:
        utils.logger.info("Opening browser")
        browser: Browser = await get_browser(playwright)
        utils.logger.info("Starting to crawl the website")
        website_map = await crawl_website_map(website_map, browser, 0, config)
        utils.logger.info("Saving website map")
        save_website_map(website_map, scraped_data)
        await browser.close()


def run() -> None:
    """Call the main function."""
    config: dict[str, Any] = utils.load_config()
    asyncio.run(_run(config))
