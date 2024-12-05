import hashlib
import os
import random
import subprocess
from typing import Sequence

from gtts import gTTS

TEMP_DIR = "temp_audio"


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


def create_concat_file(input_files: Sequence[str], concat_file: str) -> None:
    """
    Creates a file listing input audio files for concatenation using ffmpeg.
    """
    with open(concat_file, "w", encoding="utf-8") as f:
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
    output_filename: str,
    include_pause_after_native: bool,
    spell_words: bool,
    word_repetition_count: int,
    include_sentences_summary: bool,
) -> None:
    """
    Generates a single audio file by combining multiple phrases.

    :param phrases: A sequence of phrases to be converted to audio.
    :param output_filename: The name of the output audio file.
    """

    def make_words_list(words_string: str):
        return map(
            lambda x: x.strip().strip("."),
            words_string.strip().split(","),
        )

    # ^--

    concat_list = "concat_list.txt"

    audio_files_list = []
    copy_audio_files_list = []

    # Create a temporary directory for storing individual audio files
    os.makedirs(TEMP_DIR, exist_ok=True)

    silence_2 = os.path.join(TEMP_DIR, "silence_2.mp3")
    generate_silence(2, silence_2)

    silence_4 = os.path.join(TEMP_DIR, "silence_4.mp3")
    generate_silence(4, silence_4)

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

            # add native word
            audio_files_list.append(
                make_audio_file(
                    text=uk_word,
                    lang="uk",
                ),
            )

            # add pause after native
            if include_pause_after_native:
                audio_files_list.append(
                    silence_2,
                )

            if spell_words:
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
                * word_repetition_count,
            )

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

        if include_sentences_summary:
            # repeat all english sentences at the end of summary file
            copy_audio_files_list.extend(
                [sentence_audio] * 2,
            )

    if include_sentences_summary:
        # randomly compose sences all sentances without translation
        random.shuffle(copy_audio_files_list)
        audio_files_list.extend(copy_audio_files_list)

    # Create a concatenation file for ffmpeg
    create_concat_file(audio_files_list, concat_list)

    # Combine individual audio files into a single file
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_list,
            "-c",
            "copy",
            output_filename,
        ],
        check=True,
    )

    # Clean up temporary files and directories
    # clean_up(
    #     audio_files_list + [concat_list, silence_2, silence_4],
    #     directories=[TEMP_DIR],
    # )


def generate_silence(duration: float, output_path: str) -> None:
    """
    Generates a silence audio file of the given duration using ffmpeg.

    :param duration: Duration of the silence in seconds.
    :param output_path: Path to save the silence audio file.
    """
    if os.path.exists(output_path):
        return

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

    generate_audio(
        phrases=phrases,
        output_filename="output_audio.mp3",
        include_pause_after_native=False,
        spell_words=False,
        word_repetition_count=3,
        include_sentences_summary=False,
    )
