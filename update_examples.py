from typing import Any

from anki_connect import send_anki_request
from reverso_scraper import Language, fetch_reverso_examples


def update_anki_notes_with_examples(
    deck_id: str,
    source_language: Language,
    target_language: Language,
    word_field: str = "Front",
    example_field: str = "Examples",
) -> None:
    """
    Updates Anki notes in the specified deck
    with usage examples for the given word.

    This function fetches all notes in the specified Anki deck,
    retrieves the word from the designated field (default: 'Front'),
    and if the card doesn't already have examples,
    fetches and parses example sentences for the word,
    then updates the card's 'Examples' field with the results.

    :param deck_id: The ID of the Anki deck to search for notes.
    :param word_field: The name of the field containing the word
        to search for examples (default: 'Front').
    :param example_field: The name of the field where examples
        will be stored (default: 'Examples').
    :raises Exception: If an error occurs during
        the fetching or updating process.
    """
    # Find all notes in the specified deck
    notes_list: list[int] = send_anki_request(
        "findNotes",
        query=f"deck:{deck_id}",
    )

    for note_id in notes_list:
        # Retrieve card information
        notes: list[dict[str, Any]] = send_anki_request(
            "notesInfo",
            notes=(note_id,),
        )

        # Get the word from the specified field
        note = notes[-1]
        word: str = note["fields"][word_field]["value"]

        # If the word contains a slash, take the last part
        if "/" in word:
            word = word.split("/")[-1]

        # Check if the card already has examples
        examples: str = note["fields"][example_field]["value"]
        if examples.strip():
            print(f'The word "{word}" already has examples.')
            continue

        try:
            examples: str = fetch_reverso_examples(
                word=word,
                source_language=source_language,
                target_language=target_language,
            )

            # Update the Anki note with the fetched examples
            send_anki_request(
                "updateNote",
                note={
                    "id": note_id,
                    "fields": {
                        example_field: examples,
                    },
                },
            )
        except Exception as exc:
            print(f'An exception occurred while processing the word "{word}".')
            print(exc)
        else:
            print(f'The word "{word}" was processed successfully.')


if __name__ == "__main__":
    update_anki_notes_with_examples(
        deck_id="459",
        source_language=Language.ENGLISH,
        target_language=Language.UKRAINIAN,
        word_field="Front",
        example_field="examples",
    )
