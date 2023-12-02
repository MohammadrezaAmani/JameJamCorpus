import re
from bs4 import BeautifulSoup


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
    clean_html = re.compile("&.*?;")
    cleaned_html = re.sub(clean_html, "", cleaned_html)
    # cleaned_html = (
    #     cleaned_html.encode("ascii", "ignore").decode("utf-8", "ignore").strip()
    # )
    return cleaned_html.strip()
