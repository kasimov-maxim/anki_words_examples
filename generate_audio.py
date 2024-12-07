import hashlib
import os
import random
import subprocess
from datetime import date
from typing import Sequence

from gtts import gTTS

TEMP_DIR = "temp_audio"
OUTPUT_DIR = "audio"
CONCAT_LIST = "concat_list.txt"


def get_text_hash(text: str) -> str:
    """
    Генерує хеш для заданого тексту.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def make_audio_file(
    text: str,
    lang: str = "en",
    slow: bool = False,
) -> None:
    """
    Generates an audio file for a given phrase
    and optionally appends it to an existing audio file.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)

    output_path = os.path.join(TEMP_DIR, f"{get_text_hash(text)}.mp3")
    if os.path.exists(output_path):
        print(f'Audio file already exists for text: "{text}"')
        return output_path

    tmp_output_path = f"{output_path}.gtts"

    # Generate TTS audio
    tts = gTTS(text, lang=lang, slow=slow)
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


def make_words_list(words_string: str):
    return map(
        lambda x: x.strip().strip("."),
        words_string.strip().split(","),
    )


def generate_audio(
    phrases: Sequence[tuple[str, str]],
    shuffle_phrases: bool,
    native_first: bool,
    pause_after_first: bool,
    spell_foreign: bool,
    include_sentences_summary: bool,
    output_filename: str = None,
    foreign_repetition_count: int = 2,
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
        if output_filename:
            return output_filename

        options = []

        if native_first:
            options.append("uk_en")
        else:
            options.append("en_uk")

        if spell_foreign:
            options.append("spell")

        if pause_after_first:
            options.append("pause")

        if include_sentences_summary:
            options.append("summary")

        options.append(date.today().strftime("%d-%m"))

        return f"{'_'.join(options)}.mp3"

    # ^--

    audio_files_list = []
    copy_audio_files_list = []

    # Create a temporary directory for storing individual audio files
    os.makedirs(TEMP_DIR, exist_ok=True)

    silence_2 = generate_silence(2, "silence_2.mp3")
    silence_4 = generate_silence(4, "silence_4.mp3")

    if shuffle_phrases:
        random.shuffle(phrases)

    # Save each phrase as a separate audio file
    for words, words_translate, sentence, sentence_translate in phrases:
        print(f"Generating audio for: {words}")

        for uk_word, en_word in zip(
            make_words_list(words_translate),
            make_words_list(words),
        ):
            en_word_audio = make_audio_file(
                text=en_word,
                lang="en",
                slow=True,
            )

            ua_word_audio = make_audio_file(
                text=uk_word,
                lang="uk",
            )

            # Add words exersize
            if native_first:
                audio_files_list.append(ua_word_audio)

                if pause_after_first:
                    audio_files_list.append(silence_2)

                if spell_foreign:
                    audio_files_list.extend(
                        (
                            # english word + repeat the word by letters
                            en_word_audio,
                            make_audio_file(
                                text=" ".join(en_word),
                                lang="en",
                            ),
                        ),
                    )
                audio_files_list.extend(
                    # repeat english word
                    [en_word_audio]
                    * foreign_repetition_count,
                )

            else:
                audio_files_list.append(en_word_audio)
                if spell_foreign:
                    audio_files_list.append(
                        make_audio_file(
                            text=" ".join(en_word),
                            lang="en",
                        ),
                    )

                if pause_after_first:
                    audio_files_list.append(silence_4)

                audio_files_list.append(ua_word_audio)
            # ^--

        # Add sentence exersize:
        # ukrainian -> pause -> (english -> pause) * 2
        audio_files_list.extend(
            (
                make_audio_file(
                    text=sentence_translate,
                    lang="uk",
                ),
                silence_4,
            ),
        )

        sentence_audio = make_audio_file(
            text=sentence,
            lang="en",
            slow=True,
        )
        audio_files_list.extend(
            [sentence_audio, silence_4] * 2,
        )
        # ^--

        # Read all foreign sentences withous pauses
        if include_sentences_summary:
            # repeat all english sentences at the end of summary file
            copy_audio_files_list.extend(
                [sentence_audio] * 2,
            )
        # ^--

    if include_sentences_summary:
        # randomly compose sences all sentances without translation
        random.shuffle(copy_audio_files_list)
        audio_files_list.extend(copy_audio_files_list)

    # Create a concatenation file for ffmpeg
    create_concat_file(audio_files_list)
    combine_audio(output_filename=get_output_filename())

    # Clean up temporary files and directories
    # clean_up(
    #     audio_files_list + [concat_list, silence_2, silence_4],
    #     directories=[TEMP_DIR],
    # )


def combine_audio(output_filename: str) -> None:
    """
    Combines multiple audio files listed in a concatenation file into
        a single output file.

    This function uses FFmpeg to merge audio files listed in
        a text file (`CONCAT_LIST`) and saves the resulting combined audio
        in the specified output directory (`OUTPUT_DIR`) with
        the given `output_filename`.

    Parameters:
        output_filename (str): The name of the output audio file to be created.

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

    # Prepare output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

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
        ],
        check=True,
    )


def generate_silence(duration: float, output_filename: str) -> str:
    """
    Generates a silence audio file of the given duration using ffmpeg.

    :param duration: Duration of the silence in seconds.
    :output_filename (str): The name of the output audio file to be created.

    Returns:
    :output_path: Path to save the silence audio file.
    """
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
        ],
        check=True,
    )

    return output_path


def get_phrases_words(phrases):
    res = set()
    for phrase in phrases:
        words, _, _, _ = phrase

        for word in map(lambda x: x.strip(), words.strip(".").split(",")):
            res.add(word)

    return res


def get_words_list(filename: str) -> set:
    with open(filename, encoding="utf-8") as f:
        return (
            word for word in map(lambda x: x.strip(), f.readlines()) if word
        )


def store_words_list(filename: str, words: set):
    with open(filename, "w", encoding="utf-8") as f:
        for w in words:
            f.write(f"{w}\n")


def lookup_words(phrases_words, words_list) -> tuple[set, set]:
    not_found, found = set(), set()
    for word in phrases_words:
        if word not in words_list:
            not_found.add(word)
        else:
            found.add(word)

    return not_found, found


def find_exercizes_with_word(
    lookup_word: str,
    phrases: Sequence[tuple[str, str]],
):
    for words, words_translate, sentence, sentence_translate in phrases:
        words_list = make_words_list(words)
        if lookup_word in words_list:
            print("(")
            for i in (words, words_translate, sentence, sentence_translate):
                print("\t", i)
            print(")")


def count_words(phrases: Sequence[tuple[str, str]], print_list: bool = True):
    from collections import defaultdict

    counter = defaultdict(int)
    for words, _, _, _ in phrases:
        words_list = make_words_list(words)
        for word in words_list:
            counter[word] += 1

    counter_list = list(counter.items())
    counter_list_s = sorted(counter_list, key=lambda x: x[1])

    for k, v in counter_list_s:
        if print_list:
            print(k, "\t\t->\t", v)

    return k  # the most frequent


if __name__ == "__main__":

    from learning_material_2 import phrases

    phrases_words = get_phrases_words(phrases=phrases)
    print(f"Learning of {len(phrases_words)} words")
    print(phrases_words)

    print("\n")

    _459_words = set(get_words_list("459_words.txt"))

    not_found_words, found_words = lookup_words(
        phrases_words,
        _459_words,
    )
    print(f"Not found words count: {len(not_found_words)} words")
    print(not_found_words)

    print(f"Found words count: {len(found_words)} words")
    print(found_words)

    # store_words_list(
    #     "459_words_without_1.txt",
    #     _459_words.difference(found_words),
    # )

    frequent_word = count_words(phrases=phrases, print_list=True)
    # print(f"The most frequent word: {frequent_word}")
    find_exercizes_with_word(frequent_word, phrases=phrases)

    # english -> pause -> ukraine
    generate_audio(
        phrases=phrases,
        shuffle_phrases=True,
        native_first=False,
        spell_foreign=False,
        pause_after_first=True,
        include_sentences_summary=False,
    )

    # ukraine -> pause -> english
    generate_audio(
        phrases=phrases,
        shuffle_phrases=True,
        native_first=True,
        pause_after_first=True,
        spell_foreign=True,
        foreign_repetition_count=2,
        include_sentences_summary=False,
    )
