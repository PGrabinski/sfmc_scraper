"""Crawling functionalities.

Functions:
    extend_website_map: Extend the website map with the navlinks.
    process_page: Process the page.
    save_website_map: Save the website map to a file.
    crawl_website_map: Crawl the website map.
"""

from pathlib import Path
from typing import Any

from playwright.async_api import Browser, Page, TimeoutError

from .page_loading import get_page
from .parsing import (
    filter_urls_based_on_base_url,
    get_all_urls,
    get_main_content,
    trim_url,
)
from .utils import logger, save_to_file


def get_next_empty_url(website_map: dict[str, str | None]) -> str | None:
    """Get the next empty URL.

    Args:
        website_map (dict): website map

    Returns:
        str: the next empty URL
    """
    for url, content in website_map.items():
        if content is None:
            return url
    return None


async def extend_website_map(
    website_map: dict[str, str | None], navlinks: list[str], config: dict[str, Any]
) -> dict[str, str | None]:
    """Extend the website map with the navlinks.

    Args:
        website_map (dict): website map
        navlinks (list): list of navlinks
        config (dict): configuration

    Returns:
        dict: the extended website map
    """
    new_map = website_map.copy()
    for navlink in navlinks:
        trimmed_navlink = trim_url(navlink, config["base-url"])
        if trimmed_navlink not in new_map:
            new_map[trimmed_navlink] = None
    non_empty_entries = {
        key: value for key, value in new_map.items() if value is not None
    }
    logger.debug(
        f"Number of non-empty entries after extension in website map: {len(non_empty_entries)} out of {len(website_map)}"
    )
    logger.debug(f"Non-empty entries after extension: {list(non_empty_entries.keys())}")
    return new_map


async def process_page(
    page: Page,
    current_navlink: str,
    website_map: dict[str, str | None],
    config: dict[str, Any],
) -> dict[str, str | None]:
    """Process the page."""
    navlinks: list[str] = await get_all_urls(page)
    navlinks = filter_urls_based_on_base_url(navlinks, config["base-url"])
    new_map = await extend_website_map(website_map, navlinks, config)
    new_content = await get_main_content(page)
    logger.debug(f"Assigning content {new_content[:100]} to {current_navlink}")
    new_map[current_navlink] = new_content
    return new_map


def save_website_map(website_map: dict[str, str | None], path: Path) -> None:
    """Save the website map to a file."""
    for navlink, content in website_map.items():
        if content:
            save_to_file(
                content,
                path / f"{navlink.replace("/", "_")}.html",
            )


async def crawl_website_map(
    website_map: dict[str, str | None],
    browser: Browser,
    current_step: int,
    config: dict[str, Any],
) -> dict[str, str | None]:
    """Crawl the website map."""
    potential_url: str = get_next_empty_url(website_map)
    if not potential_url or current_step >= config["max-steps"]:
        return website_map
    current_url: str = trim_url(potential_url, config["base-url"])
    logger.info(f"Crawling {current_url}")
    new_map = website_map.copy()
    full_url: str = config["salesforce-url"] + current_url
    try:
        page: Page = await get_page(browser, full_url)
    except TimeoutError:
        logger.error(f"Failed to load the page {full_url}")
        new_map[current_url] = "Failed to load the page"
        return await crawl_website_map(new_map, browser, current_step + 1, config)

    new_map = await process_page(page, current_url, new_map, config)
    await page.close()
    return await crawl_website_map(new_map, browser, current_step + 1, config)
