# flake8: noqa: E501

import csv

# from utils_generate_audio import print_exercizes
from utils import (  # split_words_into_list,; count_words,; store_words_list,; lookup_words
    get_phrases_words,
    get_words_list,
    get_words_list_from_csv,
)

# Dictionary with words that contains new words to learn
# among those I have already know
NEW_DICTIONARY = (
    "./words_lists/ameriacan_oxford_3000_words_by_hands_with_ukraine.txt"
)
# Dictionary format is like this (4 tab-delimeted columns):
#   1	abandon	v. B2	відмовитися
#   2	ability	n. A2	здатність
#   3	able	adj. A2	здатний
# ^--

# Words that I have already learnt
OLD_DICTIONARY = "./words_lists/3000_oxford_words.txt"
# Dictionary format is like this (1 column):
#   able
#   about
#   above
# ^--

# Dictionary with words that are not included in OLD_DICTIONARY
NEED_TO_LEARN_DICTIONARY = "./words_lists/next_words_to_learn.txt"
# Use this dictionary for further selection with
# python ./utils_select_words_to_learn.py
# ^--


if __name__ == "__main__":
    from learning_materials.all_materials import phrases

    _new_words = set(get_words_list_from_csv(NEW_DICTIONARY))

    # select all words that I've already learnt
    _learned_words = set(get_words_list(OLD_DICTIONARY))

    _learned_phrases_words = get_phrases_words(
        phrases=phrases,
        include_sentences=True,
    )
    print(f"Learned words count: {len(_learned_phrases_words)}")

    _all_learnead_words = _learned_phrases_words.union(_learned_words)
    print(f"Summary count of known words: {len(_all_learnead_words)}")
    # ^--

    _need_to_learn_words = _new_words.difference(_all_learnead_words)
    print(f"Need to learn words count: {len(_need_to_learn_words)}")

    # # Save words that I need to learn word by word in new line
    # store_words_list(
    #     "./words_lists/next_words_to_learn.txt",
    #     _need_to_learn_words,
    # )
    # # ^--

    # Save not just english words (as above), but their translations
    # and other information as well
    result = []
    with open(NEW_DICTIONARY, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if len(row) < 4:
                continue  # Пропускаємо некоректні рядки

            english_word = row[1]

            if english_word in _need_to_learn_words:
                result.append(row)

    if result:
        with open(
            NEED_TO_LEARN_DICTIONARY,
            "a",
            encoding="utf-8",
            newline="",
        ) as file:
            writer = csv.writer(file, delimiter="\t")
            writer.writerows(result)
    # ^--
