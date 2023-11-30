import re
from bs4 import BeautifulSoup


def find_header(input_text: str) -> str:
    return input_text


def find_summary(input_text: str) -> str:
    return input_text


def find_content(input_text: str) -> str:
    return input_text


def find_tags(input_text: str) -> list:
    return input_text


def find_types(input_text: str) -> list:
    return input_text


def find_timestamp(input_text: str) -> str:
    return input_text


def clean_html(input_html: str) -> str:
    soup = BeautifulSoup(input_html, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    for tag in soup():
        if "src" in tag.attrs:
            del tag["src"]

    for media_tag in soup(["img", "audio", "video"]):
        media_tag.decompose()

    for svg_tag in soup("svg"):
        svg_tag.decompose()

    cleaned_html = str(soup)
    cleanr = re.compile("<.*?>")
    cleaned_html = re.sub(cleanr, "", cleaned_html)

    return cleaned_html
