import csv
from collections import defaultdict
from typing import Sequence


def split_words_into_list(words_string: str):
    """
    Split words strings in phrase exercizes into a list

    >>> for i in split_words_into_list("blanket, eerie, glow"):
    ...     print(i)
    ...
    blanket
    eerie
    glow
    >>>

    Args:
        words_string (str): comma separated string

    Returns:
        map object
    """
    return map(
        lambda x: x.strip().strip(".").lower(),
        words_string.strip().replace(".", ",").split(","),
    )


def make_words_set(words: str) -> map:
    """
    Split sentences for comma-separated strings into a set of words

    >>> make_words_set("He tried to persuade her to pursue her dreams")
    {'pursue', 'to', 'her', 'persuade', 'dreams', 'he', 'tried'}
    >>> make_words_set("reached, curtain, reveal, pouring")
    {'curtain', 'reveal', 'pouring', 'reached'}
    >>>

    Args:
        words (str): _description_

    Returns:
        map: _description_
    """
    return set(
        map(
            lambda x: x.strip().strip("\"'()?-1234567890."),
            words.lower().replace(",", "").replace(".", "").split(),
        ),
    )


def get_words_list(filename: str) -> set:
    with open(filename, encoding="utf-8") as f:
        return set(
            word for word in map(lambda x: x.strip(), f.readlines()) if word
        )


def get_words_list_from_csv(
    filename: str,
    delimeter: str = "\t",
    column_number: int = 1,
    encoding="utf-8",
) -> set:
    """
    get words list from csv file like this below:
        1	abandon	v. B2	відмовитися
        2	ability	n. A2	здатність
        3	able	adj. A2	здатний
        ...
        1547	live1	v. A1	live1
        ...

    Args:
        filename (str): name of a csv formated file.
        delimeter (str, optional): columns delimeter.
            Defaults to "\t".
        column_number (int, optional): english word column number.
            Defaults to 1.
        encoding (str, optional): file's encoding.

    Returns:
        set: distinct set of words
    """
    with open(filename, encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimeter)
        return set(
            row[column_number].strip("1234567890 ")
            for row in reader
            if len(row) >= column_number
        )


# def get_phrases_words(phrases):
#     res = set()
#     for phrase in phrases:
#         words, _, _, _ = phrase

#         for word in map(lambda x: x.strip(), words.strip(".").split(",")):
#             res.add(word)

#     return res


def get_phrases_words(phrases, include_sentences: bool = False):

    result = set()

    for phrase in phrases:
        words, _, sentence, _ = phrase
        result.update(make_words_set(words))

        if include_sentences:
            result.update(make_words_set(sentence))

    return result


def lookup_words(phrases_words, words_list) -> tuple[set, set]:
    not_found, found = set(), set()
    for word in phrases_words:
        if word not in words_list:
            not_found.add(word)
        else:
            found.add(word)

    return not_found, found


def store_words_list(filename: str, words: set):
    with open(filename, "w", encoding="utf-8") as f:
        for w in words:
            f.write(f"{w}\n")


def count_words(phrases: Sequence[tuple[str, str]], print_list: bool = True):

    counter = defaultdict(int)
    for words, _, _, _ in phrases:
        words_list = split_words_into_list(words)
        for word in words_list:
            counter[word] += 1

    counter_list = list(counter.items())
    counter_list_s = sorted(counter_list, key=lambda x: x[1])

    for k, v in counter_list_s:
        if print_list:
            print(k, "\t\t->\t", v)

    return k  # the most frequent
