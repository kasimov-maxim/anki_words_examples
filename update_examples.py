import time
from typing import Any

from anki_connect import send_anki_request
from reverso_scraper import (
    Language,
    fetch_reverso_examples,
    fetch_reverso_synonyms_and_antonyms,
)

# Interval in seconds to wait between consecutive Anki note updates
# to avoid server overload
THROTTLING_INTERVAL: int = 3


def get_field_value(note: dict[str, Any], field_name: str) -> str | None:
    """
    Retrieves the value of a specified field in a note.

    :param note: A dictionary representing the Anki note.
    :param field_name: The name of the field whose value to retrieve.
    :return: The field value as a string if it exists, otherwise None.
    """
    return note["fields"].get(field_name, {}).get("value", None)


def get_examples(
    word: str,
    note: dict[str, Any],
    example_field: str,
    source_language: Language,
    target_language: Language,
) -> str | None:
    """
    Fetches examples for a word if not present in the note.

    :param word: The word to fetch examples for.
    :param note: A dictionary representing the Anki note.
    :param example_field: The name of the field where examples are stored.
    :param source_language: The source language of the word.
    :param target_language: The target language for example translation.
    :return: A string containing examples if fetched, otherwise None.
    """
    examples: str | None = get_field_value(note, example_field)
    if examples is None:
        print(
            f'Skip examples for word "{word}": '
            f'"{example_field}" field not found.',
        )
        return None

    if examples.strip():
        print(
            f'Skip examples for word "{word}": examples already exist.',
        )
        return None

    try:
        examples = fetch_reverso_examples(
            word,
            source_language,
            target_language,
        )
        print(f'Examples for "{word}" were successfully fetched.')

    except Exception as exc:
        print(
            f'An exception occurred while fetching examples for "{word}": '
            f"{exc}",
        )

    return examples


def get_synonyms_and_antonyms(
    word: str,
    note: dict[str, Any],
    synonym_field: str,
    antonym_field: str,
    source_language: Language,
) -> tuple[str | None, str | None]:
    """
    Fetches synonyms and antonyms for a word if not present in the note.

    :param word: The word to fetch synonyms and antonyms for.
    :param note: A dictionary representing the Anki note.
    :param synonym_field: The name of the field where synonyms are stored.
    :param antonym_field: The name of the field where antonyms are stored.
    :param source_language: The source language of the word.
    :return: A tuple containing synonyms and antonyms strings, if available.
    """
    synonyms: str | None = get_field_value(note, synonym_field)
    antonyms: str | None = get_field_value(note, antonym_field)

    if synonyms is None and antonyms is None:
        print(
            f'Skip synonyms and antonyms for word "{word}": '
            "fields not found.",
        )
        return None, None

    if synonyms.strip() and antonyms.strip():
        print(
            f'Skip synonyms and antonyms for word "{word}": '
            "data already exists.",
        )
        return None, None

    try:
        synonyms, antonyms = fetch_reverso_synonyms_and_antonyms(
            word,
            source_language,
        )
        print(
            f'Synonyms and antonyms for "{word}" were successfully fetched.',
        )
    except Exception as exc:
        print(
            "An exception occurred while"
            f'fetching synonyms and antonyms for "{word}": {exc}',
        )

    return synonyms, antonyms


def update_anki_notes_with_examples(
    deck_id: str,
    source_language: Language,
    target_language: Language,
    word_field: str = "Front",
    example_field: str = "Examples",
    synonym_field: str = "Synonyms",
    antonym_field: str = "Antonyms",
    lookup_word: str = None,
) -> None:
    """
    Updates Anki notes in the specified deck
    with usage examples, synonyms, and antonyms for the given word.

    This function fetches all notes in the specified Anki deck,
    retrieves the word from the designated field (default: 'Front'),
    and if the card doesn't already have examples, synonyms, or antonyms,
    it fetches and parses this data and updates the note fields accordingly.

    :param deck_id: The ID of the Anki deck to search for notes.
    :param source_language: The source language of the word for which
        examples are fetched.
    :param target_language: The target language for example translation.
    :param word_field: The name of the field containing the word
        (default: 'Front').
    :param example_field: The field where examples are stored
        (default: 'Examples').
    :param synonym_field: The field where synonyms are stored
        (default: 'Synonyms').
    :param antonym_field: The field where antonyms are stored
        (default: 'Antonyms').
    :raises Exception: If an error occurs during fetching or updating.
    """

    def clean_word(word: str) -> str:
        """
        Cleans the word by taking the last part if it contains a slash
        and trimming any extra whitespace.

        :param word: The word to clean.
        :return: The cleaned word.
        """
        return word.split("/")[-1].strip() if "/" in word else word.strip()

    if lookup_word:
        lookup_word = lookup_word.split()[-1].strip()

    # Find all notes in the specified deck
    notes_list: list[int] = send_anki_request(
        "findNotes",
        query=f"deck:{deck_id}",
    )

    for note_id in notes_list:
        # Retrieve card information
        note: dict[str, Any] = send_anki_request(
            "notesInfo",
            notes=(note_id,),
        )[-1]
        word: str | None = get_field_value(note, word_field)

        if not word:
            print(
                f'Skip note "{note_id}": '
                f'the "{word_field}" field is empty.',
            )
            continue
        word = clean_word(word)

        if lookup_word and lookup_word != word:
            continue

        # Fetch examples, synonyms, and antonyms
        examples = get_examples(
            word,
            note,
            example_field,
            source_language,
            target_language,
        )

        synonyms, antonyms = get_synonyms_and_antonyms(
            word,
            note,
            synonym_field,
            antonym_field,
            source_language,
        )

        # Update note fields if there is new data
        fields = {
            key: value
            for key, value in (
                (example_field, examples),
                (synonym_field, synonyms),
                (antonym_field, antonyms),
            )
            if value
        }

        if fields:
            send_anki_request(
                "updateNote",
                note={"id": note_id, "fields": fields},
            )
            print(f'The word "{word}" updated successfully.')
            time.sleep(THROTTLING_INTERVAL)

        if lookup_word:
            break


if __name__ == "__main__":
    import sys

    # if len(sys.argv) > 1:
    #     lookup_word = sys.argv[-1]
    # else:
    #     lookup_word = None

    lookup_word = sys.argv[-1] if len(sys.argv) > 1 else None
    if lookup_word:
        print(f"Lookup word is {lookup_word}")

    update_anki_notes_with_examples(
        deck_id="459",
        source_language=Language.ENGLISH,
        target_language=Language.UKRAINIAN,
        word_field="Front",
        example_field="examples",
        synonym_field="synonyms",
        antonym_field="antonyms",
        # lookup_word="frighten",
    )
