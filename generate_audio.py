import os
from typing import Sequence

from gtts import gTTS


def save_phrase_as_audio(
    phrase: str,
    output_path: str,
    slow: bool = False,
) -> None:
    """Generates an audio file for a given phrase."""
    tts = gTTS(phrase, lang="en", slow=slow)
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


def generate_audio(
    phrases: Sequence[tuple[str, str]],
    output_filename: str,
) -> None:
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
        words, sentence = phrase
        print(f"Generating audio for: {phrase}")

        temp_file = os.path.join(temp_dir, f"phrase_{idx}_words.mp3")
        save_phrase_as_audio(
            words,
            temp_file,
            slow=True,
        )
        temp_files.append(temp_file)

        for speed in ("slow", "norm"):
            temp_file = os.path.join(temp_dir, f"phrase_{idx}_{speed}.mp3")
            save_phrase_as_audio(
                sentence,
                temp_file,
                slow=True,  # (speed == "slow"),
            )
            temp_files.append(temp_file)

    # Create a concatenation file for ffmpeg
    create_concat_file(temp_files, concat_list)

    # Combine individual audio files into a single file
    os.system(
        f"ffmpeg -f concat -safe 0 -i {concat_list} -c copy {output_filename}",
    )

    # Clean up temporary files and directories
    clean_up(temp_files + [concat_list], directories=[temp_dir])


def generate_silence(duration: float, output_path: str) -> None:
    """
    Generates a silence audio file of the given duration using ffmpeg.

    :param duration: Duration of the silence in seconds.
    :param output_path: Path to save the silence audio file.
    """
    os.system(
        "ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=44100 "
        f"-t {duration} -q:a 9 {output_path}",
    )


def get_phrases_words(phrases):
    res = set()
    for phrase in phrases:
        words, _ = phrase

        for word in map(lambda x: x.strip(), words.strip(".").split(",")):
            res.add(word)

    return res


def get_words_list(filename: str) -> set:
    with open(filename, encoding="utf-8") as f:
        return (
            word for word in map(lambda x: x.strip(), f.readlines()) if word
        )


def lookup_words(phrases_words, words_list) -> set:
    res = set()
    for word in phrases_words:
        if word not in words_list:
            res.add(word)

    return res


if __name__ == "__main__":

    phrases = [
        # (
        #     words,
        #     sentence,
        # )
        (
            "broad, valley, thin, sight",
            "The broad valley was covered in a thin layer of mist, "
            "making the sight both eerie and beautiful.",
        ),
        (
            "afterward, clever, lawyer, persuade, council",
            "Afterward, the clever lawyer managed to persuade the council "
            "to reconsider their decision.",
        ),
        (
            "wooden, fence, stood, beside, narrow, castle",
            "The wooden fence stood beside the narrow path, leading to an "
            "old castle on the hill.",
        ),
        (
            "failure, crops, faithful, harvest",
            "Despite the failure of their crops, the farmers remained "
            "faithful and hopeful for the next harvest.",
        ),
        (
            "reached, curtain, reveal, pouring",
            "She reached for the curtain to reveal the bright sunshine "
            "pouring into the room.",
        ),
        (
            "thick, mud, struggled, climb, steep, slope",
            "The thick mud stuck to his boots as he struggled to climb "
            "the steep slope.",
        ),
        (
            "frighten, fellow, beneath, cupboard.",
            "The frightened fellow hid beneath the cupboard during "
            "the thunderstorm.",
        ),
        (
            "dozen, cattle, broad, countryside.",
            "A dozen cattle wandered across the broad countryside as "
            "the sun set.",
        ),
        (
            "tied, wooden, pole, swing.",
            "She tied the rope tightly around the wooden pole to secure "
            "the swing.",
        ),
        (
            "evident, threat, sow, seeds, muddy, soil.",
            "Despite the evident threat of rain, the farmer decided "
            "to sow seeds in the muddy soil.",
        ),
        (
            "merchant, fancy, leather, gloves.",
            "The merchant sold fancy leather gloves at "
            "the bustling marketplace.",
        ),
        (
            "audience, thrilled, daring, breathtaking.",
            "The audience was thrilled by the daring acrobat's "
            "breathtaking performance.",
        ),
        (
            "folded, thick, blanket, beside.",
            "She folded the thick blanket neatly and placed it on "
            "the shelf beside the lamp.",
        ),
        (
            "modest, carpenter, chair, crafted, wood.",
            "The modest carpenter crafted a beautiful chair "
            "from fine oak wood.",
        ),
        (
            "storm, villagers, seaside, damage.",
            "After the storm, the villagers gathered at "
            "the seaside to inspect the damage.",
        ),
        (
            "leaned, steep, breath, climb.",
            "He leaned against the steep cliff, catching his breath "
            "after the exhausting climb.",
        ),
        (
            "principal, encouraged, pupils, participate.",
            "The principal encouraged the pupils to participate in "
            "the science fair.",
        ),
        (
            "shelter, rough, timber, protect.",
            "They built a sturdy shelter out of rough timber "
            "to protect themselves from the rain.",
        ),
        (
            "cheerful, aunt, dozen, pies, Thursday.",
            "The cheerful aunt baked a dozen pies for "
            "the family gathering on Thursday.",
        ),
        (
            "castle, stood, rich.",
            "The old castle stood as a testament to the region’s "
            "rich and turbulent history.",
        ),
        (
            "frightened, burst, nest, hunter, bow.",
            "The frightened bird burst from its nest as the "
            "hunter approached with his bow.",
        ),
        (
            "thick, fog, valley, narrow, trail.",
            "A thick fog covered the valley, making it difficult "
            "to see beyond the narrow trail.",
        ),
        (
            "tailor, needle, thread, torn, fabric.",
            "The tailor used a fine needle and thread "
            "to repair the torn fabric.",
        ),
        (
            "failure, confident, pursue.",
            "Despite his failure, he remained confident and continued "
            "to pursue his goals.",
        ),
        (
            "flowers, clay, pot, window.",
            "She arranged the flowers in a clay pot and placed it near "
            "the window.",
        ),
        (
            "deer, riverbank, hunters.",
            "The deer grazed peacefully near the riverbank, unaware of "
            "the hunters lurking nearby.",
        ),
    ]

    phrases_words = get_phrases_words(phrases=phrases)
    print(f"Learning of {len(phrases_words)} words")
    print(phrases_words)

    print("\n")

    not_found_words = lookup_words(
        phrases_words,
        set(get_words_list("459_words.txt")),
    )
    print(f"Not found words count: {len(not_found_words)} words")
    print(not_found_words)

    # generate_audio(
    #     phrases=phrases,
    #     output_filename="output_audio.mp3",
    # )
