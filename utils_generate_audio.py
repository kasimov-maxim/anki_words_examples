import hashlib
import os
import random
import re
import subprocess
import urllib.parse
from collections import defaultdict
from datetime import date
from typing import Sequence

from gtts import gTTS

from utils import get_words_exercises_from_csv, split_words_into_list

TEMP_DIR = "temp_audio"
OUTPUT_DIR = "audio"
CONCAT_LIST = "concat_list.txt"


def get_text_hash(text: str) -> str:
    """
    Генерує хеш для заданого тексту.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def generate_filename(text, tld):

    is_latin = bool(re.fullmatch(r"[a-zA-Z]+", text))

    if " " in text:  # Якщо це речення, створити хеш
        filename = f"__s_{get_text_hash(text)}__{tld}"
    elif is_latin:  # Якщо це слово з латинськими символами
        filename = f"{urllib.parse.quote(text.encode('utf-8'))}__{tld}"
    else:
        filename = f"__w_{get_text_hash(text)}__{tld}"

    return filename


def make_audio_file(
    text: str,
    lang: str = "en",
    tld: str = "com",
    slow: bool = False,
) -> None:
    """
    Generates an audio file for a given phrase
    and optionally appends it to an existing audio file.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)

    filename = generate_filename(text=text, tld=tld)
    output_path = os.path.join(TEMP_DIR, f"{filename}.mp3")
    if os.path.exists(output_path):
        print(f'Audio file already exists for text: "{text}"')
        return output_path

    tmp_output_path = f"{output_path}.gtts"

    # Generate TTS audio
    tts = gTTS(text, lang=lang, slow=slow, tld=tld)
    tts.save(tmp_output_path)

    try:
        # Convert TTS output to compatible format
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                tmp_output_path,
                "-ar",
                "44100",
                "-ac",
                "1",
                "-q:a",
                "9",
                output_path,
                "-y",
            ],
            check=True,
        )
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_output_path):
            os.remove(tmp_output_path)

    return output_path


def create_concat_file(input_files: Sequence[str]) -> None:
    """
    Creates a file listing input audio files for concatenation using ffmpeg.
    """
    with open(CONCAT_LIST, "w", encoding="utf-8") as f:
        for file in input_files:
            f.write(f"file '{file}'\n")


def clean_up(files: Sequence[str], directories: Sequence[str] = ()) -> None:
    """Deletes specified files and removes empty directories."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    for directory in directories:
        if os.path.exists(directory):
            os.rmdir(directory)


def generate_audio(
    phrases: Sequence[tuple[str, str]],
    shuffle_phrases: bool,
    native_first: bool,
    spell_foreign: bool,
    include_sentences_summary: bool,
    include_sentences: bool = True,
    output_filename: str = None,
    first_pause_duration_after_native_word: int = 2,
    first_pause_duration_after_foreign_word: int = 4,
    pause_duration_after_native_sentence: int = 12,
    first_pause_duration_after_foreign_sentence: int = 5,
    second_pause_duration_after_foreign_sentence: int = 4,
    foreign_repetition_count: int = 2,
    foreign_tld: str = "com",
    native_tld: str = "com",
    shoud_print_exercizes: bool = False,
    initial_silince_duration: int = 30,
) -> None:
    """
    Generates a single audio file by combining multiple phrases.

    :param phrases: A sequence of phrases to be converted to audio.
    :param shuffle_phrases: Shuffle the order of phrases.
    :param pause_after_first: Make a pause after learning word pronounced.
    :param spell_words: Whether to spell foreign words letter by letter.
    :param word_repetition_count: Number of repetitions for foreign words.
    :param include_sentences_summary: Add a summary of all sentences
        at the end.
    :param output_filename: The name of the output audio file.
    :param native_first: Determines the order of native and foreign words.
    """

    def get_output_filename():
        # Prepare output dir
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        if output_filename:
            _output_filename = output_filename
        else:
            options = []

            if native_first:
                options.append(f"uk_en.{foreign_tld}")
            else:
                options.append(f"en.{foreign_tld}_uk")

            if spell_foreign:
                options.append("spell")

            if (
                first_pause_duration_after_native_word
                or first_pause_duration_after_foreign_word
            ):
                options.append("pause")

            if include_sentences_summary:
                options.append("summary")

            if include_sentences:
                options.append("with_sentences")
            else:
                options.append("words_only")

            options.append(date.today().strftime("%d-%m"))

            _output_filename = f"{'_'.join(options)}"

        return os.path.join(OUTPUT_DIR, _output_filename)

    # ^--

    audio_files_list = []
    copy_audio_files_list = []

    # Create a temporary directory for storing individual audio files
    os.makedirs(TEMP_DIR, exist_ok=True)

    if initial_silince_duration:
        initial_silince = generate_silence(initial_silince_duration)
        audio_files_list.append(initial_silince)

    first_pause_after_native_word = generate_silence(
        first_pause_duration_after_native_word,
    )
    first_pause_after_foreign_word = generate_silence(
        first_pause_duration_after_foreign_word,
    )
    pause_after_native_sentence = generate_silence(
        pause_duration_after_native_sentence,
    )

    first_pause_after_foreign_sentence = generate_silence(
        first_pause_duration_after_foreign_sentence,
    )
    second_pause_after_foreign_sentence = generate_silence(
        second_pause_duration_after_foreign_sentence,
    )

    if shuffle_phrases:
        random.shuffle(phrases)

    # Save each phrase as a separate audio file
    for phrase in phrases:
        print(f"!!!!!!!!!!!!!! Generating audio for: {phrase}")
        (
            audio_words,
            audio_words_translate,
            audio_sentence,
            audio_sentence_translate,
            audio_spelled_words,
        ) = make_phrase_audio(
            phrase,
            spell_foreign=spell_foreign,
            foreign_tld=foreign_tld,
            native_tld=native_tld,
        )

        # audio_spelled_words.reverse()
        for ua_word_audio, en_word_audio, spelled in zip(
            audio_words_translate,
            audio_words,
            audio_spelled_words,
            strict=True,
        ):
            # Add words exersize
            if native_first:
                audio_files_list.append(ua_word_audio)

                if first_pause_duration_after_native_word:
                    audio_files_list.append(first_pause_after_native_word)

                if spelled:
                    audio_files_list.extend(
                        (
                            # english word + repeat the word by letters
                            en_word_audio,
                            spelled,
                        ),
                    )
                audio_files_list.extend(
                    # repeat english word
                    [en_word_audio]
                    * foreign_repetition_count,
                )

            else:
                audio_files_list.append(en_word_audio)
                if spelled:
                    audio_files_list.append(spelled)

                if first_pause_duration_after_foreign_word:
                    audio_files_list.append(first_pause_after_foreign_word)

                audio_files_list.append(ua_word_audio)
            # ^--

        # Add sentence exersize:
        if include_sentences:
            # ukrainian -> pause -> (english -> pause) * 2
            audio_files_list.extend(
                (
                    audio_sentence_translate,
                    pause_after_native_sentence,
                ),
            )

            audio_files_list.extend(
                # [sentence_audio, silence_4] * 2,
                [
                    audio_sentence,
                    first_pause_after_foreign_sentence,
                    audio_sentence,
                    second_pause_after_foreign_sentence,
                ],
            )
        # ^--

        # Read all foreign sentences withous pauses
        if include_sentences_summary:
            # repeat all english sentences at the end of summary file
            copy_audio_files_list.extend(
                [audio_sentence] * 2,
            )
        # ^--

    if include_sentences_summary:
        # randomly compose sences all sentances without translation
        random.shuffle(copy_audio_files_list)
        audio_files_list.extend(copy_audio_files_list)

    # Create a concatenation file for ffmpeg
    create_concat_file(audio_files_list)

    filename = get_output_filename()
    combine_audio(output_path=f"{filename}.mp3")

    if shoud_print_exercizes:
        with open(f"{filename}.txt", "w", encoding="utf-8") as f:
            print_exercizes(phrases=phrases, output_file=f)

    # Clean up temporary files and directories
    # clean_up(
    #     audio_files_list + [concat_list, silence_2, silence_4],
    #     directories=[TEMP_DIR],
    # )


def make_phrase_audio(
    phrase: tuple[str, str],
    spell_foreign: bool,
    foreign_tld: str = "com",
    native_tld: str = "com",
) -> tuple[list[str], list[str], str, str, list[str]]:

    def spell(text) -> str | None:
        # do not spell words with the "-" sign
        if "-" in text:
            return None

        return " ".join(text)

    # ^--

    words, words_translate, sentence, sentence_translate = phrase
    audio_words: list[str] = []
    audio_spelled_words: list[str] = []
    audio_words_translate: list[str] = []
    audio_sentence: str = make_audio_file(
        text=sentence,
        lang="en",
        slow=True,
        tld=foreign_tld,
    )

    audio_sentence_translate: str = make_audio_file(
        text=sentence_translate,
        lang="uk",
        tld=native_tld,
    )

    for uk_word, en_word in zip(
        split_words_into_list(words_translate),
        split_words_into_list(words),
        strict=True,
    ):
        en_word_audio = make_audio_file(
            text=en_word,
            lang="en",
            # slow=True,
            tld=foreign_tld,
        )

        uk_word_audio = make_audio_file(
            text=uk_word,
            lang="uk",
            tld=native_tld,
        )

        audio_words.append(en_word_audio)
        audio_words_translate.append(uk_word_audio)

        if spell_foreign:
            spelled = spell(en_word)
            if spelled:
                audio_spelled_words.append(
                    make_audio_file(
                        text=spelled,
                        lang="en",
                        tld=foreign_tld,
                    ),
                )
            else:
                audio_spelled_words.append(None)
        else:
            audio_spelled_words.append(None)

    return (
        audio_words,
        audio_words_translate,
        audio_sentence,
        audio_sentence_translate,
        audio_spelled_words,
    )


def combine_audio(output_path: str) -> None:
    """
    Combines multiple audio files listed in a concatenation file into
        a single output file.

    This function uses FFmpeg to merge audio files listed in
        a text file (`CONCAT_LIST`) and saves the resulting combined audio
        in the specified output directory (`OUTPUT_DIR`) with
        the given `output_path`.

    Parameters:
        output_path (str): The name of the output audio file to be created.

    Raises:
        subprocess.CalledProcessError: If the FFmpeg command fails
        during execution.

    Notes:
        - The `CONCAT_LIST` file should contain the paths of the audio files
          to be combined, listed line by line in the following format:
              file '/path/to/audio1.mp3'
              file '/path/to/audio2.mp3'
        - The `OUTPUT_DIR` constant should define the directory where
          the output file will be saved.
        - Ensure FFmpeg is installed and accessible from the system's PATH.
    """

    # Combine individual audio files into a single file
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            CONCAT_LIST,
            "-c",
            "copy",
            output_path,
            "-y",
        ],
        check=True,
    )


def generate_silence(duration: float) -> str:
    """
    Generates a silence audio file of the given duration using ffmpeg.

    :param duration: Duration of the silence in seconds.
    :output_filename (str): The name of the output audio file to be created.

    Returns:
    :output_path: Path to save the silence audio file.
    """
    output_filename = f"silence_{duration}.mp3"
    output_path = os.path.join(TEMP_DIR, output_filename)

    if os.path.exists(output_path):
        return output_path

    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=mono:sample_rate=44100",
            "-t",
            str(duration),
            "-q:a",
            "9",
            output_path,
            "-y",
        ],
        check=True,
    )

    return output_path


def print_exercizes(
    phrases: Sequence[tuple[str, str]],
    lookup_word: str = None,
    output_file=None,
    dictionary: set = None,
    print_words: bool = True,
    print_words_translate: bool = True,
    print_sentence: bool = True,
    print_sentence_translate: bool = True,
):
    for words, words_translate, sentence, sentence_translate in phrases:
        words_list = split_words_into_list(words)
        if lookup_word and lookup_word not in words_list:
            continue

        if dictionary:
            marked_words_list = []
            for word in words_list:
                if word in dictionary:
                    marked_word = f"*{word}"
                else:
                    marked_word = word
                marked_words_list.append(marked_word)
            words = ", ".join(marked_words_list)

        print("(", file=output_file)
        what_to_print = []
        if print_words:
            what_to_print.append(words)
        if print_words_translate:
            what_to_print.append(words_translate)
        if print_sentence:
            what_to_print.append(sentence)
        if print_sentence_translate:
            what_to_print.append(sentence_translate)

        for i in what_to_print:
            print("\t", i, file=output_file)
        print(")", file=output_file)


def get_unique_words_as_phrases(phrases):
    """
    Processes a list of phrase pairs and extracts unique word associations
    between a foreign language (e.g., English) and a native language
    (e.g., Ukrainian).
    The function builds a mapping between these words and returns
    a structured list of unique word associations.

    Args:
        phrases (list of tuples): A list where each tuple contains:
            - words (str): The phrase in the native language.
            - words_translate (str): The translated phrase
                in the foreign language.
            - Unused value (any): Placeholder, ignored in processing.
            - Unused value (any): Placeholder, ignored in processing.

    Returns:
        list of tuples: A list of word associations, where each tuple contains:
            - A string of foreign words joined by " / ".
            - A string of native words joined by " / ".
            - The string "u" (constant placeholder).
            - The string "и" (constant placeholder).

    Processing Steps:
        1. Parses words and their translations into separate word mappings.
        2. Handles words containing "/" or "-" by splitting them and storing
           each variant separately.
        3. Constructs two dictionaries:
            - `foreign_native__words_dict`: Maps foreign words to native words.
            - `native_foreign__words_dict`: Maps native words to foreign words.
        4. Merges both mappings to form bidirectional word associations.
        5. Formats the result into a list of tuples with joined word sets.
    """

    foreign_native__words_dict = defaultdict(set)
    native_foreign__words_dict = defaultdict(set)

    for phrase in phrases:
        words, words_translate, _, _ = phrase

        for uk_word, en_word in zip(
            split_words_into_list(words_translate),
            split_words_into_list(words),
            strict=True,
        ):
            # foreign_native__words_dict[en_word].add(uk_word)
            for i in map(lambda x: x.strip(), re.split("[/]", uk_word)):
                foreign_native__words_dict[en_word].add(i)
            # ^--

            # native_foreign__words_dict[uk_word].add(en_word)
            for i in map(lambda x: x.strip(), re.split("[/]", en_word)):
                for j in map(lambda x: x.strip(), re.split("[/]", uk_word)):
                    native_foreign__words_dict[j].add(i)
            # ^--

    # combine both of the dicts above
    combined_list = []
    for _, uk_words_set in foreign_native__words_dict.items():
        # en_words_set = {"тест", }
        en_words_set = set()

        for uk_word in uk_words_set:
            for i in native_foreign__words_dict[uk_word]:
                en_words_set.add(i)

        combined_list.append(
            (tuple(en_words_set), tuple(uk_words_set)),
        )

    # pprint.pprint(combined_list)
    return [
        (
            " / ".join(en_words_tuple),
            " / ".join(uk_words_tuple),
            "u",
            "и",
        )
        for en_words_tuple, uk_words_tuple in dict(combined_list).items()
    ]


if __name__ == "__main__":

    from learning_materials.all_materials import phrases

    # english -> pause -> ukraine
    # without spell
    generate_audio(
        phrases=phrases,
        shuffle_phrases=True,
        native_first=False,
        spell_foreign=False,
        first_pause_duration_after_native_word=2,
        include_sentences_summary=False,
        foreign_tld="us",
    )

    # ukraine -> pause -> english
    # without spell
    generate_audio(
        phrases=get_unique_words_as_phrases(phrases),
        shuffle_phrases=True,
        native_first=True,
        spell_foreign=False,
        foreign_repetition_count=2,
        include_sentences=False,
        include_sentences_summary=False,
        foreign_tld="us",
    )
    # words only practice: ukraine -> pause -> english
    generate_audio(
        # phrases=get_unique_words_as_phrases(phrases),
        phrases=get_unique_words_as_phrases(
            get_words_exercises_from_csv(
                "./words_lists/ameriacan_oxford_3000_words_with_ukraine_selected_to_learn.txt",  # noqa: E501
                delimeter="\t",
                foreign_column_number=1,
                native_column_number=3,
            ),
        ),
        shuffle_phrases=True,
        native_first=True,
        first_pause_duration_after_native_word=2,
        spell_foreign=False,
        foreign_repetition_count=2,
        include_sentences=False,
        include_sentences_summary=False,
        foreign_tld="us",
        shoud_print_exercizes=False,
    )
    # with spell
    generate_audio(
        phrases=phrases,
        shuffle_phrases=True,
        native_first=True,
        first_pause_duration_after_native_word=2,
        spell_foreign=True,
        foreign_repetition_count=2,
        include_sentences_summary=False,
        foreign_tld="us",
    )
