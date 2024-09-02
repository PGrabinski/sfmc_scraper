"""Functions to scrape the Salesforce Marketing Cloud documentation.

Functions:
    get_all_navlinks_available: Get all available navlinks on the page.
    get_main_content: Get the main content of the page.
"""

import asyncio
from pathlib import Path
from typing import Any

from playwright.async_api import Browser, Locator, Page, async_playwright
from ruamel.yaml import YAML

from .page_loading import get_browser, get_page  # type: ignore

scraped_data = Path("scraped/")


def load_config() -> dict[str, Any]:
    """Load the config file."""
    yaml = YAML()
    with open("config.yaml", "r") as file:
        config: dict[str, Any] = yaml.load(file)
    return config


async def get_all_navlinks_available(page: Page) -> list[str]:
    """Get all available navlinks on the page.

    Args:
        page (Page): a loaded page instance

    Returns:
        list[str]: list of navlinks urls
    """
    link_elements: list[Locator] = await page.locator("a.sidebar-item").all()
    return [
        f"[{await link.inner_text()}]({await link.get_attribute("href")})"
        for link in link_elements
    ]


async def get_main_content(page: Page) -> str:
    """Get the main content of the page.

    Args:
        page (Page): a loaded page instance

    Returns:
        str: the main content of the page
    """
    html: str = await page.inner_html("div.markdown-body")
    return html


def save_to_file(content: str, filename: Path) -> None:
    """Save the content to a file.

    Args:
        content (str): the content to save
        filename (Path): the filename to save to
    """
    with open(filename, "w") as file:
        file.write(content)


async def _run(config: dict[str, Any]) -> None:
    """Run the main async function."""
    async with async_playwright() as playwright:
        browser: Browser = await get_browser(playwright)
        page: Page = await get_page(
            browser, config["salesforce-url"], config["locators-to-await"]
        )
        navlinks: list[str] = await get_all_navlinks_available(page)
        save_to_file("\n".join(navlinks), scraped_data / "navlinks.html")

        main_content: str = await get_main_content(page)
        save_to_file(main_content, scraped_data / "main_content.html")

        await browser.close()


def run() -> None:
    """Call the main function."""
    config: dict[str, Any] = load_config()
    asyncio.run(_run(config))
