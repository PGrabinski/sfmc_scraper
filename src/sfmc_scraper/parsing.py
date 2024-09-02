"""Utils for parsing html to markdown."""

from unstructured.documents.elements import Element


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
