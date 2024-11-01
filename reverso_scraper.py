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


def get_language_code(language: Language) -> str:
    """
    Converts a Language enum value into its
        corresponding two-letter ISO 639-1 language code.

    :param language: A value from the Language enum.
    :return: A two-letter language code corresponding to the input language.
    """
    language_map = {
        Language.ARABIC: "ar",
        Language.GERMAN: "de",
        Language.ENGLISH: "en",
        Language.SPANISH: "es",
        Language.FRENCH: "fr",
        Language.HEBREW: "he",
        Language.ITALIAN: "it",
        Language.JAPANESE: "ja",
        Language.KOREAN: "ko",
        Language.DUTCH: "nl",
        Language.POLISH: "pl",
        Language.PORTUGUESE: "pt",
        Language.ROMANIAN: "ro",
        Language.SWEDISH: "sv",
        Language.TURKISH: "tr",
        Language.UKRAINIAN: "uk",
        Language.CHINESE: "zh",
    }

    return language_map.get(language, "unknown")


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
    :raises Timeout: If the request takes longer
        than the specified timeout (15 seconds).
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


def extract_relevant_and_other_synonyms(
    contents: str,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """
    Extracts relevant and non-relevant synonyms from the given HTML content.

    :param contents: HTML content as a string, which contains anchor
        elements (<a>) with the classes "synonym" and optionally "relevant".
    :return: A tuple containing two tuples:
             - The first tuple includes all synonyms with the class "relevant".
             - The second tuple includes all synonyms without the class
                "relevant".

    This function parses the given HTML content, extracts all anchor tags
        with the class "synonym", and filters them into two separate groups:
        those with the class "relevant" and those without it.
    """
    # Parse the HTML content
    soup = BeautifulSoup(contents, "html.parser")

    # Find all anchor elements with the class "synonym"
    synonym_links = soup.find_all("a", class_="synonym")

    # Filter synonyms with and without the "relevant" class
    relevant_synonyms = tuple(
        link.text.strip()
        for link in synonym_links
        if "relevant" in link.get("class", [])
    )
    other_synonyms = tuple(
        link.text.strip()
        for link in synonym_links
        if "relevant" not in link.get("class", [])
    )

    return relevant_synonyms, other_synonyms


def extract_antonyms(html_content: str) -> list[str]:
    """
    Extracts a list of antonyms from the provided HTML content.

    :param html_content: A string containing the HTML content.
    :return: A list of antonym words.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <li> elements containing antonyms inside the class "word-box"
    antonym_elements = soup.select("div.antonyms-wrapper ul.word-box li a")

    # Extract the text of each antonym
    return [
        antonym
        for antonym in filter(
            lambda x: x,
            map(lambda x: x.text.strip(), antonym_elements),
        )
    ]


def wrap_youglish(word: str) -> str:
    """
    Wraps the given word in an HTML anchor tag that links to its
        pronunciation on YouGlish.

    :param word: The word to be wrapped in the YouGlish pronunciation link.
    :return: A string containing an HTML anchor tag that links to YouGlish for
        the pronunciation of the word.
        The link points to YouGlish's US English pronunciation page.
    """
    return (
        f'<a href="https://youglish.com/pronounce/{word}/english/us" '
        f'target="_blank">{word}</a>'
    )


def format_synonyms(
    relevant_synonyms: list[str],
    other_synonyms: list[str],
    add_youglish: bool = False,
) -> str:
    """
    Formats relevant and other synonyms into an HTML string.
        Relevant synonyms are bolded.

    :param relevant_synonyms: A list of relevant synonyms.
    :param other_synonyms: A list of other synonyms.
    :param add_youglish: If True, wraps each word with a link
        to YouGlish for pronunciation.
    :return: An HTML-formatted string of synonyms.
    """

    def format_word(word: str, is_bold: bool = False) -> str:
        # Wrap word in a YouGlish link if add_youglish is True
        if add_youglish:
            word = wrap_youglish(word)

        # Make word bold if it's a relevant synonym
        return f"<strong>{word}</strong>" if is_bold else word

    # Format relevant synonyms (bolded)
    formatted_relevant = [
        format_word(word, is_bold=True) for word in relevant_synonyms
    ]

    # Format other synonyms (not bolded)
    formatted_others = [format_word(word) for word in other_synonyms]

    # Join both lists with commas and return as a single HTML string
    return ", ".join(formatted_relevant + formatted_others)


def format_antonyms(antonyms: list[str], add_youglish: bool = False) -> str:
    """
    Formats antonyms into an HTML string. If add_youglish is True,
        each word is wrapped with a link to YouGlish.

    :param antonyms: A list of antonyms.
    :param add_youglish: If True, wraps each word with a link
        to YouGlish for pronunciation.
    :return: An HTML-formatted string of antonyms.
    """

    def format_word(word: str) -> str:
        # Wrap word in a YouGlish link if add_youglish is True
        if add_youglish:
            word = wrap_youglish(word)
        return word

    # Format antonyms and join them with commas
    formatted_antonyms = [format_word(word) for word in antonyms]

    return ", ".join(formatted_antonyms)


def fetch_reverso_synonym_content(
    word: str,
    language: Language,
) -> str:
    """
    Fetches the HTML content for synonyms of a given word from
        Reverso Synonym for the specified language.

    :param word: The word for which to fetch synonym content.
    :param language: The language in which to search for synonyms.
        This should be a value from the `Language` enum.
    :return: A string containing the HTML content of the synonyms page.

    :raises HTTPError: If the HTTP request fails.
    :raises Timeout: If the request takes longer
        than the specified timeout (15 seconds).
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        ),
    }
    lang = get_language_code(language)
    url = f"https://synonyms.reverso.net/synonym/{lang}/{word}"

    # Send GET request
    response = requests.get(url, headers=headers, timeout=15)

    # Check for successful response
    response.raise_for_status()

    return response.text


def fetch_reverso_synonyms_and_antonyms(
    word: str,
    language: Language,
) -> tuple[str, str]:
    """
    Fetches the HTML content from Reverso Synonym
        for the given word and language,
        extracts relevant and other synonyms, antonyms
        and formats them into an HTML string.

    :param word: The word for which to fetch synonyms and antonyms.
    :param language: The language in which to fetch synonyms and antonyms.
        This should be a value from the `Language` enum.
    :return: A formatted HTML string containing the synonyms and antonyms.
    """

    # Fetch the HTML content for the word and language
    contents: str = fetch_reverso_synonym_content(word=word, language=language)

    # Determine if YouGlish links should be added (only for English)
    add_youglish: bool = language == Language.ENGLISH

    # Extract relevant and other synonyms
    relevant_synonyms, other_synonyms = extract_relevant_and_other_synonyms(
        contents,
    )

    # Extract antonyms
    antonyms = extract_antonyms(contents)

    # Return the formatted HTML result
    return (
        format_synonyms(
            relevant_synonyms,
            other_synonyms,
            add_youglish=add_youglish,
        ),
        format_antonyms(antonyms, add_youglish=add_youglish),
    )


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
    print("\n\n")
    print(
        fetch_reverso_synonyms_and_antonyms(
            word=search_word,
            language=Language.ENGLISH,
        ),
    )
