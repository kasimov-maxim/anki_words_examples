import os
import random
import shutil
import subprocess
from typing import Sequence

from gtts import gTTS


def save_phrase_as_audio(
    phrase: str,
    output_path: str,
    slow: bool = False,
    lang: str = "en",
    append_audio: str = None,
) -> None:
    """
    Generates an audio file for a given phrase
    and optionally appends it to an existing audio file.
    """
    tmp_output_path = f"{output_path}.gtts"

    # Generate TTS audio
    tts = gTTS(phrase, lang=lang, slow=slow)
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

        # If an additional audio file needs to be appended
        if append_audio:
            if not os.path.exists(append_audio):
                raise FileNotFoundError(
                    f"Append audio file not found: {append_audio}",
                )

            concat_path = f"{output_path}.concat"
            os.rename(output_path, concat_path)

            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    f"concat:{concat_path}|{append_audio}",
                    "-c",
                    "copy",
                    output_path,
                ],
                check=True,
            )
            os.remove(concat_path)

    finally:
        # Clean up temporary file
        if os.path.exists(tmp_output_path):
            os.remove(tmp_output_path)


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

    def make_words_list(words_string: str):
        return map(lambda x: x.strip(), words_string.strip().split(","))

    # ^--

    temp_dir = "temp_audio"
    concat_list = "concat_list.txt"
    temp_files = []
    audio_id = 0

    def make_audio_file(
        word: str,
        lang: str,
        slow: bool = False,
        copy_count: int = 0,
        repeat_count: int = 0,
        append_audio: str = None,
    ):
        """
        Make audio-file and append it's name to list of audio files
        """
        nonlocal audio_id
        audio_id += 1

        temp_file = os.path.join(
            temp_dir,
            f"{audio_id}.mp3",
        )
        save_phrase_as_audio(
            (
                word
                if not repeat_count
                else ".\n / / / / / / / / ".join([word] * repeat_count)
            ),
            temp_file,
            slow=slow,
            lang=lang,
            append_audio=append_audio,
        )
        temp_files.append(temp_file)

        copy_files = []
        for i in range(copy_count):
            copy_filename = os.path.join(
                temp_dir,
                f"{audio_id}_{i}.mp3",
            )
            shutil.copy(temp_file, copy_filename)
            copy_files.append(copy_filename)

        return copy_files

    # Create a temporary directory for storing individual audio files
    os.makedirs(temp_dir, exist_ok=True)

    silence_file = os.path.join(
        temp_dir,
        "silence.mp3",
    )
    generate_silence(2, silence_file)

    # Save each phrase as a separate audio file
    phrases_files_list = []
    for phrase in phrases:
        words, words_translate, sentence, sentence_translate = phrase
        print(f"Generating audio for: {phrase}")

        for uk_word, en_word in zip(
            make_words_list(words_translate),
            make_words_list(words),
        ):
            make_audio_file(word=uk_word, lang="uk", append_audio=silence_file)
            make_audio_file(word=en_word, lang="en", repeat_count=3, slow=True)
        # ^---
        make_audio_file(word=sentence_translate, lang="uk")

        # for speed in ("slow", "slow"):
        for i in range(2):
            phrases_files_list.extend(
                make_audio_file(
                    word=sentence,
                    lang="en",
                    # slow=speed == "slow",
                    slow="slow",
                    # copy_count=5 if speed == "norm" else 0,
                    copy_count=5 if i == 1 else 0,
                ),
            )

    random.shuffle(phrases_files_list)
    temp_files.extend(phrases_files_list)

    # Create a concatenation file for ffmpeg
    create_concat_file(temp_files, concat_list)

    # Combine individual audio files into a single file
    os.system(
        f"ffmpeg -f concat -safe 0 -i {concat_list} -c copy {output_filename}",
    )

    # Clean up temporary files and directories
    clean_up(temp_files + [concat_list, silence_file], directories=[temp_dir])


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
        words, _, _, _ = phrase

        for word in map(lambda x: x.strip(), words.strip(".").split(",")):
            res.add(word)

    return res


def get_words_list(filename: str) -> set:
    with open(filename, encoding="utf-8") as f:
        return (
            word for word in map(lambda x: x.strip(), f.readlines()) if word
        )


def lookup_words(phrases_words, words_list) -> tuple[set, set]:
    not_found, found = set(), set()
    for word in phrases_words:
        if word not in words_list:
            not_found.add(word)
        else:
            found.add(word)

    return not_found, found


if __name__ == "__main__":

    phrases = [
        # # (
        # #     en_words,
        # #     uk_words,
        # #     en_sentence,
        # #     uk_sentence,
        # # )
        # shorts
        (
            "blanket, curtain",
            "ковдра, штора",
            "She hid under the blanket and closed the curtain.",
            "Вона сховалася під ковдру і закрила штору.",
        ),
        (
            "persuade, pursue",
            "переконувати, переслідувати",
            "He tried to persuade her to pursue her dreams.",
            "Він намагався переконати її переслідувати свої мрії.",
        ),
        (
            "eerie, curtain",
            "моторошний, штора",
            "The wind moved the curtain in an eerie way.",
            "Вітер моторошно ворушив штору.",
        ),
        (
            "blanket, pursue",
            "ковдра, переслідувати",
            "They carried a blanket as they pursued the trail.",
            "Вони несли ковдру, переслідуючи слід.",
        ),
        (
            "eerie, persuade",
            "моторошний, переконувати",
            "The eerie silence persuaded them to leave quickly.",
            "Моторошна тиша переконала їх швидко піти.",
        ),
        (
            "curtain, pursue",
            "штора, переслідувати",
            "He peeked behind the curtain to pursue the sound.",
            "Він заглянув за штору, щоб переслідувати звук.",
        ),
        (
            "blanket, eerie",
            "ковдра, моторошний",
            "The eerie glow made the blanket seem alive.",
            "Моторошне сяйво змусило ковдру здаватися живою.",
        ),
        (
            "persuade, blanket",
            "переконувати, ковдра",
            "She persuaded him to bring an extra blanket.",
            "Вона переконала його принести додаткову ковдру.",
        ),
        (
            "eerie, pursue",
            "моторошний, переслідувати",
            "An eerie howl urged them to pursue the creature.",
            "Моторошне виття змусило їх переслідувати істоту.",
        ),
        (
            "curtain, blanket",
            "штора, ковдра",
            "She pulled the curtain and grabbed a blanket.",
            "Вона потягнула штору і схопила ковдру.",
        ),
        (
            "threat, steep",
            "загроза, крутий",
            "The steep path was a threat.",
            "Крута стежка була загрозою.",
        ),
        (
            "beside, narrow",
            "поруч, вузький",
            "She stood beside the narrow door.",
            "Вона стояла поруч з вузькими дверима.",
        ),
        (
            "frighten, aunt",
            "лякати, тітка",
            "The noise frightened my aunt.",
            "Шум налякав мою тітку.",
        ),
        (
            "fancy, lawyer",
            "вишуканий, адвокат",
            "The lawyer wore a fancy suit.",
            "Адвокат був у вишуканому костюмі.",
        ),
        (
            "failure, modest",
            "провал, скромний",
            "Her failure made her modest.",
            "Її провал зробив її скромною.",
        ),
        (
            "swing, broad",
            "гойдалка, широкий",
            "The swing hung from a broad tree.",
            "Гойдалка висіла на широкому дереві.",
        ),
        (
            "reveal, evident",
            "розкривати, очевидний",
            "His smile revealed his evident joy.",
            "Його усмішка розкривала його очевидну радість.",
        ),
        (
            "thin, clever",
            "тонкий, розумний",
            "The clever cat slipped through a thin gap.",
            "Розумний кіт прослизнув через тонку щілину.",
        ),
        (
            "shelter, cattle",
            "укриття, худоба",
            "The cattle found shelter in the barn.",
            "Худоба знайшла укриття в сараї.",
        ),
        (
            "pursue, sight",
            "переслідувати, зір",
            "He pursued the deer in his sight.",
            "Він переслідував оленя, який був у нього на виду.",
        ),
        (
            "dozen, afterward",
            "дюжина, потім",
            "We baked a dozen pies and ate them afterward.",
            "Ми спекли дюжину пирогів і потім їх з'їли.",
        ),
        (
            "valley, clay",
            "долина, глина",
            "The valley had rich clay for pottery.",
            "У долині була багата глина для гончарства.",
        ),
        (
            "slope, burst",
            "схил, вибухати",
            "Water burst down the steep slope.",
            "Вода вибухнула вниз по крутому схилу.",
        ),
        (
            "blanket, breath",
            "ковдра, подих",
            "She wrapped in a blanket and took a deep breath.",
            "Вона загорнулася в ковдру і зробила глибокий вдих.",
        ),
        (
            "pole, beneath",
            "жердина, під",
            "He hid beneath the wooden pole.",
            "Він сховався під дерев'яною жердиною.",
        ),
        (
            "audience, merchant",
            "аудиторія, торговець",
            "The merchant charmed the audience with his tale.",
            "Торговець зачарував аудиторію своєю історією.",
        ),
        (
            "persuade, climb",
            "переконати, підніматися",
            "She persuaded him to climb the mountain.",
            "Вона переконала його піднятися на гору.",
        ),
        (
            "seaside, harvest",
            "узбережжя, врожай",
            "We celebrated the harvest by the seaside.",
            "Ми святкували врожай біля узбережжя.",
        ),
        (
            "deer, needle",
            "олень, голка",
            "The deer stepped on a sharp needle.",
            "Олень наступив на гостру голку.",
        ),
        (
            "nest, principal",
            "гніздо, директор",
            "The principal showed us a bird's nest.",
            "Директор показав нам пташине гніздо.",
        ),
        (
            "chair, thick",
            "стілець, товстий",
            "He sat on a thick wooden chair.",
            "Він сидів на товстому дерев'яному стільці.",
        ),
        (
            "council, fence",
            "рада, паркан",
            "The council decided to build a fence.",
            "Рада вирішила побудувати паркан.",
        ),
        (
            "pot, wooden",
            "горщик, дерев'яний",
            "She placed the pot on a wooden table.",
            "Вона поставила горщик на дерев'яний стіл.",
        ),
        (
            "faithful, curtain",
            "вірний, штора",
            "The faithful dog slept behind the curtain.",
            "Вірний пес спав за шторою.",
        ),
        (
            "cupboard, leather",
            "шафа, шкіра",
            "He stored his leather boots in the cupboard.",
            "Він зберігав свої шкіряні чоботи в шафі.",
        ),
        (
            "soil, rich",
            "ґрунт, багатий",
            "The soil here is rich and fertile.",
            "Ґрунт тут багатий і родючий.",
        ),
        (
            "rough, castle",
            "грубий, замок",
            "The rough path led to the old castle.",
            "Груба стежка вела до старого замку.",
        ),
        (
            "fellow, mud",
            "хлопець, бруд",
            "The fellow fell into the mud while running.",
            "Хлопець впав у бруд, коли біг.",
        ),
        (
            "tie, struggled",
            "зав'язати, боровся",
            "He struggled to tie the rope tightly.",
            "Він боровся, щоб міцно зав'язати мотузку.",
        ),
        (
            "crafted, riverbank",
            "виготовлений, берег річки",
            "They crafted a boat on the riverbank.",
            "Вони виготовили човен на березі річки.",
        ),
        (
            "trail, timber",
            "стежка, деревина",
            "The trail led to a pile of timber.",
            "Стежка вела до купи деревини.",
        ),
        (
            "thrilled, pouring",
            "захоплений, ллється",
            "She was thrilled by the pouring rain.",
            "Вона була захоплена дощем, що лився.",
        ),
        (
            "gloves, confident",
            "рукавички, впевнений",
            "He put on gloves and felt confident.",
            "Він одягнув рукавички і відчув упевненість.",
        ),
        (
            "daring, countryside",
            "сміливий, сільська місцевість",
            "The daring explorer roamed the countryside.",
            "Сміливий дослідник блукав сільською місцевістю.",
        ),
        (
            "sow, thread",
            "сіяти, нитка",
            "She used thread to mend her sowing sack.",
            "Вона використала нитку, щоб полагодити мішок для сівби.",
        ),
        (
            "seeds, fabric",
            "насіння, тканина",
            "He wrapped seeds in a piece of fabric.",
            "Він загорнув насіння в шматок тканини.",
        ),
        (
            "damage, bow",
            "пошкодження, лук",
            "The bow had slight damage from the fall.",
            "Лук отримав невеликі пошкодження від падіння.",
        ),
        (
            "fold, fog",
            "скласти, туман",
            "He folded his map in the dense fog.",
            "Він склав карту в густому тумані.",
        ),
        (
            "pies, pupils",
            "пироги, учні",
            "The pupils baked delicious pies together.",
            "Учні разом пекли смачні пироги.",
        ),
        # ^--
        (
            "reached, curtain, reveal, pouring",
            "досяг, завіса, розкрити, ллється",
            "She reached for the curtain to reveal the bright sunshine "
            "pouring into the room.",
            "Вона потягнулася до штори, щоб відкрити яскраве сонячне світло, "
            "що вливалося в кімнату.",
        ),
        (
            "failure, crops, faithful, harvest",
            "невдача, посіви, вірний, урожай",
            "Despite the failure of their crops, the farmers remained "
            "faithful and hopeful for the next harvest.",
            "Незважаючи на неврожай, фермери залишилися "
            "вірними та сподівалися на наступний урожай.",
        ),
        (
            "thick, mud, struggled, climb, steep, slope",
            "товстий, бруд, боровся, підйом, крутий, схил",
            "The thick mud stuck to his boots as he struggled to "
            "climb the steep slope.",
            "Густа багнюка прилипла до його черевиків, коли він намагався "
            "піднятися на крутий схил.",
        ),
        (
            "frighten, fellow, beneath, cupboard.",
            "лякати, друже, під шафою.",
            "The frightened fellow hid beneath the cupboard during "
            "the thunderstorm.",
            "Наляканий хлопець під час грози сховався під шафою",
        ),
        (
            "dozen, cattle, broad, countryside.",
            "десяток, худоба, широкий, сільська місцевість.",
            "A dozen cattle wandered across the broad countryside as "
            "the sun set.",
            "Дюжина великої рогатої худоби блукала по широкій місцевості, "
            "коли сонце заходило.",
        ),
        (
            "tied, wooden, pole, swing.",
            "зв'язаний, дерев'яний, стовп, гойдалка.",
            "She tied the rope tightly around the wooden pole "
            "to secure the swing.",
            "Вона міцно прив’язала мотузку до дерев’яного стовпа, "
            "щоб закріпити гойдалку.",
        ),
        (
            "evident, threat, sow, seeds, muddy, soil.",
            "очевидний, загроза, сіяти, насіння, брудний, ґрунт.",
            "Despite the evident threat of rain, the farmer decided "
            "to sow seeds in the muddy soil.",
            "Незважаючи на очевидну загрозу дощу, фермер вирішив "
            "посіяти насіння в мулистий ґрунт.",
        ),
        (
            "merchant, fancy, leather, gloves.",
            "торговець, фантазія, шкіра, рукавички.",
            "The merchant sold fancy leather gloves at "
            "the bustling marketplace.",
            "Продавець продавав шикарні шкіряні рукавички "
            "на гамірному базарі.",
        ),
        (
            "audience, thrilled, daring, breathtaking.",
            "аудиторія, схвильована, смілива, захоплююча.",
            "The audience was thrilled by the daring acrobat's "
            "breathtaking performance.",
            "Глядачі були в захваті від "
            "захоплюючого виступу сміливого акробата",
        ),
        (
            "folded, thick, blanket, beside.",
            "складений, товстий, ковдра, поруч.",
            "She folded the thick blanket neatly and placed it on "
            "the shelf beside the lamp.",
            "Вона акуратно склала товсту ковдру і поклала її на "
            "полицю біля лампи.",
        ),
        (
            "modest, carpenter, chair, crafted, wood.",
            "скромний, тесля, стілець, виготовлений, дерево.",
            "The modest carpenter crafted a beautiful chair "
            "from fine oak wood.",
            "Скромний тесля виготовив гарне крісло з добірної деревини дуба.",
        ),
        (
            "storm, villagers, seaside, damage.",
            "шторм, селяни, узбережжя, пошкодження.",
            "After the storm, the villagers gathered at "
            "the seaside to inspect the damage.",
            "Після шторму селяни зібралися на "
            "березі моря, щоб оглянути збитки.",
        ),
        (
            "leaned, steep, breath, climb.",
            "нахилився, крутий, дихання, підйом.",
            "He leaned against the steep cliff, catching his breath "
            "after the exhausting climb.",
            "Він притулився до крутої скелі, переводячи подих "
            "після виснажливого підйому.",
        ),
        (
            "principal, encouraged, pupils, participate.",
            "директор, заохочується, учні, брати участь.",
            "The principal encouraged the pupils to participate in "
            "the science fair.",
            "Директор закликав учнів взяти участь у " "науковому ярмарку.",
        ),
        (
            "shelter, rough, timber, protect.",
            "притулок, грубий, деревина, захистити.",
            "They built a sturdy shelter out of rough timber "
            "to protect themselves from the rain.",
            "Вони побудували міцне укриття з грубої деревини, "
            "щоб захиститися від дощу.",
        ),
        (
            "cheerful, aunt, dozen, pies, Thursday.",
            "веселий, тітка, дюжина, пиріжки, четвер.",
            "The cheerful aunt baked a dozen pies for "
            "the family gathering on Thursday.",
            "Весела тітка спекла десяток пирогів для "
            "сімейних зборів у четвер",
        ),
        (
            "castle, stood, rich.",
            "замок, стояв, багатий.",
            "The old castle stood as a testament to the region’s "
            "rich and turbulent history.",
            "Старий замок стояв як свідчення "
            "багатої та бурхливої історії регіону.",
        ),
        (
            "frightened, burst, nest, hunter, bow.",
            "злякався, лопнув, гніздо, мисливець, лук.",
            "The frightened bird burst from its nest as the "
            "hunter approached with his bow.",
            "Переляканий птах вирвався з гнізда, коли "
            "мисливець наблизився з луком.",
        ),
        (
            "thick, fog, valley, narrow, trail.",
            "густий, туман, долина, вузька, стежка.",
            "A thick fog covered the valley, making it difficult "
            "to see beyond the narrow trail.",
            "Густий туман вкрив долину, тому було важко "
            "бачити за вузькою стежкою.",
        ),
        (
            "tailor, needle, thread, torn, fabric.",
            "кравець, голка, нитка, рвана, тканина.",
            "The tailor used a fine needle and thread "
            "to repair the torn fabric.",
            "Кравець використав тонку голку та нитку, "
            "щоб відремонтувати порвану тканину.",
        ),
        (
            "failure, confident, pursue.",
            "невдача, впевнений, переслідувати.",
            "Despite his failure, he remained confident and "
            "continued to pursue his goals.",
            "Незважаючи на свою невдачу, він залишався впевненим і "
            "продовжував йти до своїх цілей.",
        ),
        (
            "flowers, clay, pot, window.",
            "квіти, глина, горщик, вікно.",
            "She arranged the flowers in a clay pot and placed it near "
            "the window.",
            "Вона поклала квіти в глиняний горщик і поставила біля вікна.",
        ),
        (
            "deer, riverbank, hunters.",
            "олені, берег річки, мисливці.",
            "The deer grazed peacefully near the riverbank, unaware of "
            "the hunters lurking nearby.",
            "Олень мирно пасся біля берега річки, не підозрюючи про "
            "мисливців, що чатують поблизу.",
        ),
        (
            "broad, valley, thin, sight, mist, eerie",
            "широкий, долина, тонкий, вид, туман, моторошний",
            "The broad valley was covered in a thin layer of mist, "
            "making the sight both eerie and beautiful.",
            "Широка долина була вкрита тонким шаром туману, "
            "що робило видовище одночасно моторошним і прекрасним.",
        ),
        (
            "afterward, clever, lawyer, persuade, council",
            "згодом, розумний, юрист, переконати, рада",
            "Afterward, the clever lawyer managed to persuade the council "
            "to reconsider their decision.",
            "Згодом спритний юрист зумів переконати раду "
            "переглянути своє рішення.",
        ),
        (
            "wooden, fence, stood, beside, narrow, castle",
            "дерев'яний, паркан, стояв, поруч, вузький, замок",
            "The wooden fence stood beside the narrow path, leading to an "
            "old castle on the hill.",
            "Дерев'яна огорожа стояла біля вузької стежки, що вела до "
            "старого замку на пагорбі.",
        ),
        # ^--
    ]

    phrases_words = get_phrases_words(phrases=phrases)
    print(f"Learning of {len(phrases_words)} words")
    print(phrases_words)

    print("\n")

    not_found_words, found_words = lookup_words(
        phrases_words,
        set(get_words_list("459_words.txt")),
    )
    print(f"Not found words count: {len(not_found_words)} words")
    print(not_found_words)

    print(f"Found words count: {len(found_words)} words")
    print(found_words)

    generate_audio(
        phrases=phrases,
        output_filename="output_audio.mp3",
    )
