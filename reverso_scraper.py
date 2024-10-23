from enum import Enum

import requests
from bs4 import BeautifulSoup


class Language(str, Enum):
    """
    Supported languages
    """

    ARABIC = "arabic"
    GERMAN = "german"
    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"
    HEBREW = "hebrew"
    ITALIAN = "italian"
    JAPANESE = "japanese"
    KOREAN = "korean"
    DUTCH = "dutch"
    POLISH = "polish"
    PORTUGUESE = "portuguese"
    ROMANIAN = "romanian"
    SWEDISH = "swedish"
    TURKISH = "turkish"
    UKRAINIAN = "ukrainian"
    CHINESE = "chinese"


def extract_translation_examples(contents: str) -> list[tuple[str, str]]:
    """
    Extracts English and Ukrainian translation examples
        from the given HTML content.

    :param contents: The HTML content to parse.
    :return: A list of tuples where each tuple contains
        an English example and its Ukrainian translation.
    """
    soup = BeautifulSoup(contents, "html.parser")
    results = []

    # Find all blocks with translation examples
    for example in soup.find_all("div", class_="example"):
        # Extract English and Ukrainian text
        en_text = example.find("div", class_="src ltr").find(
            "span",
            class_="text",
        )
        uk_text = example.find("div", class_="trg ltr").find(
            "span",
            class_="text",
        )

        for text in (en_text, uk_text):
            # Update <em> tags style to blue
            for em_tag in text.find_all("em"):
                em_tag["style"] = "color:blue"

            # Remove <a> tags but keep their content
            for a_tag in text.find_all("a"):
                a_tag.unwrap()

        results.append((en_text, uk_text))

    return results


def format_examples(parsed_data: list[tuple[str, str]]) -> str:
    """
    Formats parsed translation examples into an HTML string.

    :param parsed_data: A list of tuples where each tuple contains
        an English example and its Ukrainian translation.
    :return: A string of HTML-formatted translation examples.
    """
    return "".join(
        f"<p>{example[0]}<br>{example[1]}</p>" for example in parsed_data
    )


def fetch_reverso_content(
    word: str,
    source_language: Language,
    target_language: Language,
) -> str:
    """
    Fetches the HTML content of the translation page for
        the given word from Reverso.

    :param word: The word for which the translation examples are fetched.
    :return: The HTML content of the page.
    :raises HTTPError: If the HTTP request fails.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        ),
    }
    url = (
        "https://context.reverso.net/translation"
        f"/{source_language}-{target_language}/{word}"
    )

    # Send GET request
    response = requests.get(url, headers=headers, timeout=15)

    # Check for successful response
    response.raise_for_status()

    return response.text


def fetch_reverso_examples(
    word: str,
    source_language: Language,
    target_language: Language,
) -> str:
    """
    Fetches translation examples for a given word from Reverso Context,
    based on the source and target languages, and formats them into a string.

    :param word: The word for which to fetch translation examples.
    :param source_language: The language from which the word
        is being translated (source).
    :param target_language: The language into which the word
        is being translated (target).
    :return: A string containing formatted translation examples
        from the source to target language.

    This function works by first fetching the HTML content
        from Reverso Context based on the word and specified languages.
        It then extracts translation examples
    from the content and formats them into a readable string.

    The formatted examples are returned as an HTML string, where each example
    contains the source and target translation pair.

    :raises HTTPError: If there is a problem fetching the content from Reverso.
    """
    contents: str = fetch_reverso_content(
        word=word,
        source_language=source_language,
        target_language=target_language,
    )
    parsed_data: list[dict[str, str]] = extract_translation_examples(
        contents,
    )
    return format_examples(parsed_data)


if __name__ == "__main__":

    import sys

    search_word = sys.argv[1].strip()

    # with open("./data/html.html", "r", encoding="utf-8") as file:
    #     reverso_contents = file.read()
    reverso_contents = fetch_reverso_content(
        word=search_word,
        source_language=Language.ENGLISH,
        target_language=Language.UKRAINIAN,
    )

    # Process and print the results
    parsed_examples = extract_translation_examples(reverso_contents)
    print(format_examples(parsed_examples))
