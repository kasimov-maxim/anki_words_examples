# flake8: noqa: E501

from collections import defaultdict

from utils import get_words_list, make_words_set

SKIP_WORDS = set(
    map(
        lambda x: x.strip(),
        (
            "it she he they and a the of"
            " to in was her his for is on"
            " with from we by i an you their"
            " are that this at your as my but"
            " our have had into can has over"
            " them were what be "
            # " I you he she it we they me him her us them "  # особисті
            # " my your his her its our their mine yours his hers ours theirs "  # присвійні
            # " this that these those "  # вказівні
            # " myself yourself himself herself itself ourselves yourselves themselves "  # зворотні
            # " some any no every someone anyone nobody everybody something anything nothing everything "  # неозначені
            # " who whom whose which that "  # відносні
            # " who whom whose which what where when why how "  # питальні
            # " now then today yesterday tomorrow soon later early late always usually often sometimes rarely never "  # часу
            # " here there everywhere nowhere inside outside above below near far "  # місця
            # " quickly slowly carefully carelessly loudly quietly well badly "  # дії
            # " very quite too enough so as more most less least "  # ступеня
            # " yes no not maybe perhaps indeed really "  # заперечення
            # " and but or nor for so yet "  # сурядні
            # " after although as as if as long as as soon as because before even if even though if in order that since so that than though till unless until when whenever where whereas while    "  # підрядні
            # " can could may might must shall should will would "  # Модальні
            # " oh ah ouch wow oops hello goodbye "  # Вигуки
            # " one two three ten hundred thousand first second third "  # числівники
            # " Monday Tuesday Wednesday Thursday Friday Saturday Sunday "  # дні
            # " January February March April May June July August September October November December "  # місяці
        )
        .lower()
        .split(),
    ),
)


# Функція для підрахунку кількості входжень слова
def count_word_occurrences(phrases, include_sentences: bool = True):
    words_counter = defaultdict(int)

    for phrase in phrases:
        words, _, sentence, _ = phrase
        words_set = make_words_set(words)

        if include_sentences:
            sentence_set = make_words_set(sentence)

            for w in sentence_set:
                if w in words_set:
                    continue
                if w in SKIP_WORDS:
                    continue
                words_counter[w] += 1

        for w in words_set:
            if w in SKIP_WORDS:
                continue
            words_counter[w] += 1

    return words_counter


def print_alphabetical(word_count, lookup_words: set = None, file=None):
    # Сортуємо словник за ключами (словами) у алфавітному порядку
    sorted_words = sorted(word_count.items(), key=lambda x: x[0])

    # Виводимо результат
    for word, count in sorted_words:
        is_in_dict = "*\t" if lookup_words and word in lookup_words else "\t"
        print(f"{is_in_dict}{word}\t{count}", file=file)


def print_descending(word_count, lookup_words: set = None, file=None):
    # Сортуємо словник за значеннями (кількістю входжень) у спадаючому порядку
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # Виводимо результат
    for word, count in sorted_words:
        is_in_dict = "*\t" if lookup_words and word in lookup_words else "\t"
        print(f"{is_in_dict}{count}\t{word}", file=file)


if __name__ == "__main__":
    from learning_materials.all_materials import phrases

    learning_dictionary = get_words_list("459_words.txt")

    occurrences = count_word_occurrences(phrases, include_sentences=False)
    with open("print_descending.txt", "w", encoding="utf-8") as f:
        print_descending(occurrences, lookup_words=learning_dictionary, file=f)
    # print("="*100)
    with open("print_alphabetical.txt", "w", encoding="utf-8") as f:
        print_alphabetical(
            occurrences,
            lookup_words=learning_dictionary,
            file=f,
        )

    learned_words = set(occurrences.keys())
    print(f"Not studied: {learning_dictionary.difference(learned_words)}")
