"""Utilities for loading pages.

Functions:
    get_browser: Get a chromium browser instance.
    get_page: Get a page instance.
"""

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


async def get_page(browser: Browser, url: str, locators_to_await: list[str]) -> Page:
    """Get a page instance.

    Args:
        browser (Browser): a browser instance
        url (str): url to load
        locators_to_await (list): list of locators to wait

    Returns:
        Page: a loaded page instance
    """
    page: Page = await browser.new_page()
    await page.goto(url)
    for locator in locators_to_await:
        await page.wait_for_selector(locator)
    return page
