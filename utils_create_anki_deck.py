from collections import defaultdict
from typing import Sequence

from anki_connect import ServerError, send_anki_request
from reverso_scraper import (
    Language,
    extract_ipa_pronunciation,
    extract_suggestions,
    extract_translation_examples,
    extract_translations,
    fetch_reverso_content,
    fetch_reverso_synonyms_and_antonyms,
    format_examples,
    format_suggestions,
    format_translations,
)
from utils import split_words_into_list


def create_phrase_card(
    deck_id: str,
    model_name: str,
    word: str,
    word_translates: list[str] = None,
    examples: list[str] = None,
):

    def ipa_pronunciations_str(ipa_pronunciations: dict) -> str:
        return (
            str(ipa_pronunciations).strip("{}") if ipa_pronunciations else ""
        )

    # ^--

    ipa_pronunciations = {}
    synonyms = ""
    antonyms = ""

    try:
        # pass
        reverso_contents = fetch_reverso_content(
            word=word,
            source_language=Language.ENGLISH,
            target_language=Language.UKRAINIAN,
        )
        ipa_pronunciations = extract_ipa_pronunciation(reverso_contents)
        if not ipa_pronunciations:
            print(f"\tThere is no ipa-pronunciation for word: {word}")
        reverso_examples = format_examples(
            extract_translation_examples(reverso_contents),
        )
        if examples:
            phrase_examples = "\n<br/><br/>".join(examples)
            card_examples = f"{phrase_examples}\n<br/><br/>{reverso_examples}"
        else:
            card_examples = reverso_examples

        alttranslations = format_translations(
            extract_translations(
                reverso_contents,
                web_url_base="https://context.reverso.net/",
            ),
        )

        suggestions = format_suggestions(
            extract_suggestions(
                reverso_contents,
                web_url_base="https://context.reverso.net/",
            ),
        )

        synonyms, antonyms = fetch_reverso_synonyms_and_antonyms(
            word=word,
            language=Language.ENGLISH,
        )
    except Exception as exc:
        print(f"An error occured for the word: {word}")
        print(exc)

    send_anki_request(
        "addNote",
        note={
            "deckName": deck_id,
            "modelName": model_name,
            "fields": {
                "Front": word,
                "transcription": ipa_pronunciations_str(ipa_pronunciations),
                "translation": (
                    ", ".join(word_translates) if word_translates else ""
                ),
                "examples": card_examples if card_examples else "",
                "synonyms": synonyms if synonyms else "",
                "antonyms": antonyms if antonyms else "",
                "alttranslations": alttranslations,
                "suggestions": suggestions,
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": f"{deck_id}",
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
            "tags": [],
        },
    )

    # ^--


def create_deck_from_filelist(
    deck_id: str,
    model_name: str,
    filename: str,
):
    send_anki_request("createDeck", deck=deck_id)
    num = 1
    with open(filename, "r", encoding="utf-8") as words_f:
        words = map(lambda x: x.strip(), words_f.readlines())
        for word in words:
            try:
                create_phrase_card(
                    deck_id=deck_id,
                    model_name=model_name,
                    word=word,
                )
                print(f"{num}: Created card for {word}")
            except ServerError as err:
                print(f"{num}: Error for {word}: {err}")
            num += 1


def create_phrases_deck(
    deck_id: str,
    model_name: str,
    phrases: Sequence[tuple[str, str, str, str]],
    create_new_deck: bool = True,
):
    deck_id = deck_id.strip()
    model_name = model_name.strip()

    words_dict, examples_dict = create_phrases_dicts(phrases=phrases)

    if create_new_deck:
        send_anki_request("createDeck", deck=deck_id)
    num = 1
    for word, translates in words_dict.items():
        print(f"{num}: Create card for: {word}")
        examples = examples_dict.get(word)
        create_phrase_card(
            deck_id=deck_id,
            model_name=model_name,
            word=word,
            word_translates=translates,
            examples=examples,
        )
        num += 1
    # ^--


def create_phrases_dicts(
    phrases: Sequence[tuple[str, str, str, str]],
) -> tuple[dict, dict]:
    words_dict = defaultdict(set)
    examples_dict = defaultdict(list)
    for phrase in phrases:
        print(f"Proccess phrase: {phrase}")
        words, words_translate, sentence, _ = phrase
        for uk_word, en_word in zip(
            split_words_into_list(words_translate),
            split_words_into_list(words),
            strict=True,
        ):
            words_dict[en_word].add(uk_word)
            examples_dict[en_word].append(sentence)

    return words_dict, examples_dict


if __name__ == "__main__":

    # import sys

    # filename = sys.argv[1]
    # deck_id = sys.argv[2]
    # model_name = sys.argv[3]
    # print(
    #     "Paramters: "
    #     f"filename: {filename}; "
    #     f"deck_id: {deck_id}; "
    #     f"model_name: {model_name};"
    # )
    # create_deck_from_filelist(
    #     deck_id=deck_id,
    #     model_name=model_name,
    #     filename=filename,
    # )

    from learning_material_7 import phrases

    create_phrases_deck(
        deck_id="learning_material_7",
        model_name="459",
        phrases=phrases,
    )
