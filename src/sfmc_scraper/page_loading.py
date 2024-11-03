"""Utilities for loading pages.

Functions:
    get_browser: Get a chromium browser instance.
    get_page: Get a page instance.
"""

import logging

from playwright.async_api import Browser, Page, Playwright


async def get_browser(playwright: Playwright) -> Browser:
    """Get a chromium browser instance.

    Args:
        playwright (PlaywrightContextManager): Playwright context manager

    Returns:
        browser: chromium browser instance
    """
    browser: Browser = await playwright.chromium.launch()
    return browser


async def get_page(browser: Browser, url: str) -> Page:
    """Get a page instance.

    Args:
        browser (Browser): a browser instance
        url (str): url to load

    Returns:
        Page: a loaded page instance
    """
    page: Page = await browser.new_page()
    logging.info(f"Loading {url}")
    await page.goto(url)
    return page
