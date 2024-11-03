"""Utils for parsing html to markdown.

Functions:
    element_to_text: Convert a html_partial element to text.
    get_all_navlinks_available: Get all available navlinks on the page.
    get_main_content: Get the main content of the page.
    filter_missing_navlinks: Get the missing navlinks.
    get_empty_navlinks_locators: Get the empty navlinks urls.
    get_all_urls: Retrieve all the URLs from the given page.
    click_all_locators: Click all locators.
"""

from playwright.async_api import Locator, Page, TimeoutError
from unstructured.documents.elements import Element

from .utils import logger


def element_to_text(element: Element) -> str:
    """Convert a html_partial element to text.

    Args:
        element (Element): a html_partial element

    Returns:
        str: the text representation of the element
    """
    element_text: str = element.text
    if element.metadata.link_urls:
        element_text += f"\n{element.metadata.link_urls}"
    return element_text + "\n\n"


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
    # markdown_body: str = await page.locator("div.markdown-body").inner_html()
    # content_body: str = await page.locator("div.content-body").inner_html()

    # if markdown_body:
    #     print(f"Markdown body: {markdown_body}")
    #     return markdown_body
    # elif content_body:
    #     print(f"Content body: {content_body}")
    #     return content_body

    markdown_body: Locator = page.locator("div.markdown-body")
    try:
        return await markdown_body.inner_html(timeout=5000)
    except TimeoutError:
        logger.error("Failed to load the content.")
        return "Failed to load the content."


def filter_missing_navlinks(navlinks: list[str]) -> list[str]:
    """Get the missing navlinks.

    Args:
        navlinks (list[str]): list of navlinks

    Returns:
        list[str]: list of missing navlinks
    """
    return [
        navlink
        for navlink in navlinks
        if "docs/marketing/marketing-cloud/" not in navlink
    ]


async def get_empty_navlinks_locators(
    page: Page, navlinks: list[str]
) -> list[list[Locator]]:
    """Get the empty navlinks urls.

    Args:
        page (Page): a loaded page instance
        navlinks (list): list of navlinks

    Returns:
        list: list of empty navlinks urls
    """
    empty_navlinks: list[str] = [
        navlink.split("](")[0][1:] for navlink in filter_missing_navlinks(navlinks)
    ]

    empty_locators: list[list[Locator]] = [
        await page.locator(f'a.sidebar-item:has-text("{navlink}")').all()
        for navlink in empty_navlinks
    ]

    return empty_locators


async def get_all_urls(page: Page) -> list[str | None]:
    """Retrieve all the URLs from the given page.

    Args:
        page (Page): The page to scrape URLs from.
        prefix (str): The prefix to filter the URLs with.

    Returns:
        list[str | None]: A list of URLs found on the page.
    """
    all_as: list[Locator] = await page.locator("a").all()

    urls = [await a.get_attribute("href") for a in all_as]

    return [url for url in urls if url and len(url) > 1]


def filter_urls_based_on_base_url(urls: list[str], base_url: str) -> list[str]:
    """Filter URLs based on the base URL.

    Args:
        urls (list): list of URLs
        base_url (str): base URL

    Returns:
        list: list of filtered URLs
    """
    return [url for url in urls if base_url in url]


def trim_url(url: str, redundant_part: str) -> str:
    """Trim the URL.

    Args:
        url (str): a URL
        redundant_part (str): the redundant part

    Returns:
        str: the trimmed URL
    """
    return url.replace(redundant_part, "")


async def click_all_locators(page: Page, locators: list[Locator]) -> None:
    """Click all locators.

    Args:
        page (Page): a loaded page instance
        locators (list): list of locators
    """
    for i, locator in enumerate(locators):
        await locator.click()
        print(f"Clicked locator {i}")
    await page.screenshot(path="screenshot.png")
