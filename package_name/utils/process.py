import re
from bs4 import BeautifulSoup


def find_title(input_text: str) -> str:
    title = re.findall(r'<meta itemprop="name" content="(.*?)">', input_text)
    return title[0].strip() if title else ""


def find_summary(input_text: str) -> str:
    summary = re.findall(r'<meta itemprop="description" content="(.*?)">', input_text)
    return summary[0].strip() if summary else ""


def find_content(input_text: str) -> str:
    content = re.findall(
        r'<div class="text-justify">(.*?)</div>', input_text, re.DOTALL
    )
    content += re.findall(
        r'<p style="text-align:justify;">(.*?)</p>', input_text, re.DOTALL
    )
    content += re.findall(
        r'<section class="body">(.*?)</section>', input_text, re.DOTALL
    )

    return "".join(content).strip() if content else ""


def find_tags(input_text: str) -> list:
    tags = re.findall(r'class="tag-item" target="_blank">(.*?)</a>', input_text)
    return tags if tags else []


def find_types(input_text: str) -> list:
    types = re.findall(r'<a class="service-name-news"(.*?)</a>', input_text)
    for i in range(len(types)):
        types[i] = types[i][types[i].find(">") + 1 :]
    return types if types else []


def convert_to_english_digits(input_text: str) -> str:
    input_text = input_text.strip()
    month = {
        "فروردین": "01",
        "اردیبهشت": "02",
        "خرداد": "03",
        "تیر": "04",
        "مرداد": "05",
        "شهریور": "06",
        "مهر": "07",
        "آبان": "08",
        "آذر": "09",
        "دی": "10",
        "بهمن": "11",
        "اسفند": "12",
    }
    if input_text in month:
        return month[input_text]
    input_text = list(input_text)
    dates = {
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "۰": "0",
    }
    for i in range(len(input_text)):
        if input_text[i] in dates.keys():
            input_text[i] = dates[input_text[i]]
    return "".join(input_text).strip()


def find_timestamp(input_text: str) -> str:
    timestamp = re.findall(r'<span class="news-pdate">(.*?)</span>', input_text)
    timestamp = timestamp[0].strip() if timestamp else ""
    timestamp = timestamp.replace("&nbsp;", " ")
    timestamp = timestamp.split(" ")
    for i in range(len(timestamp)):
        timestamp[i] = convert_to_english_digits(timestamp[i])

    return timestamp


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
    for svg_tag in soup("path"):
        svg_tag.decompose()

    cleaned_html = str(soup)
    cleanr = re.compile("<.*?>")
    cleaned_html = re.sub(cleanr, "", cleaned_html)

    return cleaned_html.strip()


def extract_data(input_text: str) -> dict:
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
