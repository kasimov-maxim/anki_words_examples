import os
from random import shuffle


def clear_terminal():
    # Очищення термінала для Linux, macOS, і Windows
    os.system("cls" if os.name == "nt" else "clear")


def lowercase(x: str):
    return " ".join(x.lower().rstrip(".").split())


def practice_phrases(phrases):
    print('Натисніть Enter, щоб почати. "q" щоб вийти')
    key = input()  # Очікує натискання Enter
    if key.strip().lower() in ("q", "й"):
        return

    total_phrases = len(phrases)
    step = 0
    for _, _, english_sentence, ukrainian_sentence in phrases:
        step += 1
        try:
            clear_terminal()
            print("=" * 100)
            print(f"\n (step {step}/{total_phrases}). Речення українською:")
            print(f"\033[92m{ukrainian_sentence}\033[0m")  # Зелений текст

            print(
                "\nНатисніть Enter, щоб побачити англійське речення."
                ' "q" щоб вийти',
            )
            your_answer = input()  # Очікує натискання Enter

            if your_answer.strip().lower() in ("q", "й"):
                break

            print(f"\033[97m{'='*100}\033[0m")
            if lowercase(your_answer) == lowercase(english_sentence):
                your_answer_color = "\033[92m"  # green
            else:
                your_answer_color = "\033[91m"  # red

            print(
                f"{'Ваша відповідь:':>21} "
                f"{your_answer_color}{your_answer}\033[0m",
            )

            print(
                f"{'Контрольна відповідь:':>20} "
                f"\033[93m{english_sentence}\033[0m",  # yellow
            )

            print(f"\033[97m{'^'*100}\033[0m")

            print(
                "\nНатисніть Enter, щоб перейти до наступної вправи."
                ' "q" щоб вийти',
            )
            key = input()  # Очікує натискання Enter
            if key.strip().lower() in ("q", "й"):
                break

        except KeyboardInterrupt:
            pass

    print("\nВсі вправи завершено. Добра робота!")


if __name__ == "__main__":
    from learning_material_3_1 import phrases

    shuffle(phrases)
    practice_phrases(phrases)
