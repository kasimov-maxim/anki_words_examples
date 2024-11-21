import os
from typing import Sequence

from gtts import gTTS


def save_phrase_as_audio(phrase: str, output_path: str) -> None:
    """Generates an audio file for a given phrase."""
    tts = gTTS(phrase, lang="en")
    tts.save(output_path)


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
        os.remove(file)
    for directory in directories:
        os.rmdir(directory)


def generate_audio(phrases: Sequence[str], output_filename: str) -> None:
    """
    Generates a single audio file by combining multiple phrases.

    :param phrases: A sequence of phrases to be converted to audio.
    :param output_filename: The name of the output audio file.
    """
    temp_dir = "temp_audio"
    concat_list = "concat_list.txt"

    # Create a temporary directory for storing individual audio files
    os.makedirs(temp_dir, exist_ok=True)

    # Save each phrase as a separate audio file
    temp_files = []
    for idx, phrase in enumerate(phrases):
        temp_file = os.path.join(temp_dir, f"phrase_{idx}.mp3")
        print(f"Generating audio for: {phrase}")
        save_phrase_as_audio(phrase, temp_file)
        temp_files.append(temp_file)

    # Create a concatenation file for ffmpeg
    create_concat_file(temp_files, concat_list)

    # Combine individual audio files into a single file
    os.system(
        f"ffmpeg -f concat -safe 0 -i {concat_list} -c copy {output_filename}",
    )

    # Clean up temporary files and directories
    clean_up(temp_files + [concat_list], directories=[temp_dir])


if __name__ == "__main__":
    generate_audio(
        phrases=[
            "Hello, how are you?",
            "Good morning!",
            "What is your name?",
            "Have a nice day!",
            "See you later!",
        ],
        output_filename="output_audio.mp3",
    )
