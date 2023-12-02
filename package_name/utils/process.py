import re
from package_name.utils.clean import clean_html, convert_to_english_digits


# ! change as needed for your project
def find_title(input_text: str) -> str:
    """
    Find the title from the input text.

    Args:
        input_text (str): The input text containing HTML.

    Returns:
        str: The extracted title from the input text.

    Raises:
        IndexError: If the title cannot be found in the input text.

    Example:
        >>> input_text = '<html><head><meta itemprop="name" content="Example Title"></head></html>'
        >>> find_title(input_text)
        'Example Title'
    """
    title = re.findall(r'<meta itemprop="name" content="(.*?)">', input_text)
    return clean_html(title[0].strip()) if title else ""


def find_summary(input_text: str) -> str:
    """
    Find the summary from the input text.

    Args:
        input_text (str): The input text containing HTML.

    Returns:
        str: The summary extracted from the input text.

    Raises:
        IndexError: If the summary is not found in the input text.

    Example:
        >>> find_summary('<meta itemprop="description" content="This is a summary">')
        'This is a summary'
    """
    summary = re.findall(r'<meta itemprop="description" content="(.*?)">', input_text)
    return clean_html(summary[0].strip()) if summary else ""


def find_content(input_text: str) -> str:
    """
    Find and extract content from HTML text.

    Args:
        input_text (str): The HTML text to search for content.

    Returns:
        str: The extracted content, cleaned of HTML tags and leading/trailing whitespace.
    """
    content = re.findall(
        r'<div class="text-justify">(.*?)</div>', input_text, re.DOTALL
    )
    content += re.findall(
        r'<p style="text-align:justify;">(.*?)</p>', input_text, re.DOTALL
    )
    content += re.findall(
        r'<section class="body">(.*?)</section>', input_text, re.DOTALL
    )

    return clean_html("".join(content).strip()) if content else ""


def find_tags(input_text: str) -> list:
    """
    Find tags in the input text.

    Args:
        input_text (str): The text to search for tags.

    Returns:
        list: A list of tags found in the input text.
    """
    tags = re.findall(r'class="tag-item" target="_blank">(.*?)</a>', input_text)
    return tags if tags else []


def find_types(input_text: str) -> list:
    """
    Find and extract types from the input text.

    Args:
        input_text (str): The input text to search for types.

    Returns:
        list: A list of extracted types.

    """
    types = re.findall(r'<a class="service-name-news"(.*?)</a>', input_text)
    for i in range(len(types)):
        types[i] = types[i][types[i].find(">") + 1 :]
    return types if types else []


def find_timestamp(input_text: str) -> str:
    """
    Finds and returns the timestamp from the input text.

    Args:
        input_text (str): The input text containing the timestamp.

    Returns:
        str: The extracted timestamp.

    """
    timestamp = re.findall(r'<span class="news-pdate">(.*?)</span>', input_text)
    timestamp = timestamp[0].strip() if timestamp else ""
    timestamp = timestamp.replace("&nbsp;", " ")
    timestamp = timestamp.split(" ")
    for i in range(len(timestamp)):
        timestamp[i] = convert_to_english_digits(timestamp[i])

    return timestamp


def extract_data(input_text: str) -> dict:
    """
    Extracts data from the given input text.

    Args:
        input_text (str): The input text to extract data from.

    Returns:
        dict: A dictionary containing the extracted data with the following keys:
            - "title": The title extracted from the input text.
            - "summary": The summary extracted from the input text.
            - "content": The content extracted from the input text.
            - "tags": The tags extracted from the input text.
            - "types": The types extracted from the input text.
            - "timestamp": The timestamp extracted from the input text.
    """
    title = find_title(input_text)
    summary = find_summary(input_text)
    content = find_content(input_text)
    tags = find_tags(input_text)
    types = find_types(input_text)
    timestamp = find_timestamp(input_text)
    return {
        "title": title,
        "summary": summary,
        "content": content,
        "tags": tags,
        "types": types,
        "timestamp": timestamp,
    }
