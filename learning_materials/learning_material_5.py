# flake8: noqa: E501

phrases = [
    # # =====================================================================
    # https://www.youtube.com/shorts/GKCQZ6VDPB4
    # never         0%
    # Hardly ever   10%
    # rarely        20%
    # seldom        30%
    # occasionally  40%
    # sometimes     50%
    # often         60%
    # frequently    70%
    # generally, normally     80%
    # usually       90%
    # always        100%
    # Hardly ever: 5-10%
    # Дуже близько до "rarely", але може звучати ще більш категорично, майже як "майже ніколи".
    # Приклад: "He hardly ever drinks coffee."
    # Scarcely: 5-10%
    # Дуже рідко, часто використовується у драматичному або старомодному контексті.
    # Приклад: "She scarcely speaks to him these days."
    # Rarely: 5-15%
    # Щось трапляється ще рідше, ніж "seldom", і зазвичай підкреслює винятковість.
    # Приклад: "She rarely goes to the gym."
    # Seldom: 10-20%
    # Події трапляються дуже рідко, але все ж не є надзвичайно винятковими.
    # Infrequently: 10-25%
    # Вказує на нерегулярність, але трохи більш імовірне, ніж "seldom".
    # Приклад: "He infrequently checks his emails."
    # Occasionally: 20-40%
    # Означає помірну частоту — щось трапляється час від часу.
    # Приклад: "She occasionally visits her hometown."
    # Once in a while: 15-30%
    # Щось трапляється нечасто, але й не надто рідко — акцент на випадковості.
    # Приклад: "We meet once in a while for coffee."
    # # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # # =====================================================================
    # # INTENT vs INTENTION
    # # приклади викорастання intent як noun або як adjective
    # # "intent" використовується як іменник в конкретному значенні або уточнюється
    # # тут використовується артикль
    # "He acted with an intent to deceive."
    # "The intent of this rule is clear."
    # # приклади абстрактниї іменник - не використовується артикль
    # "She acted with kindness." → "Вона діяла з добротою."
    # "He worked with dedication." → "Він працював із відданістю."
    # "Do it with intent"
    # "Do it with an intent mind." # → Тут "intent" описує стан розуму, тобто прикметник.
    # # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    (
        "clause",
        "пункт",
        "The clause in the sentence changed its meaning",
        "Підрядне речення у реченні змінило його значення",
    ),
    (
        "argue, due, clause",
        "аргументувати, належний, пункт",
        "The lawyer argued to use the due process clause in the case",
        "Адвокат наполягав на використанні пункту про належний процес у справі",
    ),
    (
        "welfare, clause",
        "добробут, пункт",
        "There's a general welfare clause in the constitution",
        "У конституції є пункт про загальний добробут",
    ),
    (
        "sour",
        "кислий",
        "The lemon has a sour taste",
        "Лимон має кислий смак",
    ),
    # spare me your sermons
    # spare myself this pain
    # there was spare capacity to make inexpensive vaccines
    (
        "spare",
        "запасний",
        "In her spare time, she reads a book",
        "У свій вільний час вона читає книгу",
    ),
    (
        "spare, sermon",
        "запасний, проповідь",
        "Please spare me your sermons",
        "Будь ласка, позбавте мене від ваших проповідей",
    ),
    (
        "spare",
        "запасний",
        "Unfortunately, they didn't have any money to spare",
        "На жаль, у них не було зайвих грошей",
    ),
    (
        "spare, capacity, inexpensive",
        "запасний, ємність, недорогий",
        "There was spare capacity to make inexpensive vaccines in the factory",
        "На заводі була додаткова потужність для виготовлення недорогих вакцин",
    ),
    # dull
    (
        "dull",
        "нудний",
        "The movie was dull and boring",
        "Фільм був нудним і нецікавим",
    ),
    (
        "striving, greatness, dare, dull",
        "прагнути, велич, наважитися, нудний",
        "Rather than striving for greatness, dare to be dull",
        "Замість того щоб прагнути величі, наважся бути нудним",
    ),
    (
        "dull",
        "нудний",
        "This leads to dull and repetitive gatherings",
        "Це призводить до нудних і повторюваних зібрань",
    ),
    (
        "dull, glow",
        "нудний, світіння",
        "After 14 billion years, it is just a dull glow",
        "Через 14 мільярдів років це лише тьмяне світіння",
    ),
    (
        "eventually",
        "зрештою",
        "Eventually, success came after hard work",
        "Зрештою, успіх прийшов після наполегливої праці",
    ),
    (
        "eventually",
        "зрештою",
        "a black hole eventually evaporates",
        "чорна діра зрештою випаровується",
    ),
    (
        "eventually",
        "зрештою",
        "Most great journeys eventually come to an end",
        "Більшість чудових подорожей зрештою закінчуються",
    ),
    (
        "interfere",
        "втручатися",
        "Do not interfere with my work",
        "Не втручайся в мою роботу",
    ),
    (
        "interfere",
        "втручатися",
        "don't interfere with that sacred right",
        "не порушуйте це святе право",
    ),
    (
        "interfere",
        "втручатися",
        "I just don't want to interfere with their law",
        "Я просто не хочу втручатися в їхній закон",
    ),
    (
        "vain",
        "марний",
        "His effort to win was in vain",
        "Його зусилля виграти були марними",
    ),
    (
        "vain, arrogant",
        "марний, зарозумілий",
        "Loving yourself is not being vain or arrogant",
        "Любити себе не означає бути марнославним чи зарозумілим",
    ),
    (
        "vain",
        "марний",
        "You can see their meal trying in vain to escape",
        "Ви можете побачити, як їхня їжа марно намагається втекти",
    ),
    (
        "vain, praise",
        "марний, похвала",
        "vain men never hear anything but praise",
        "марнославні люди ніколи не чують нічого, крім похвали",
    ),
    (
        "fond, childhood",
        "любити, дитинство",
        "She has fond memories of her childhood",
        "У неї теплі спогади про дитинство",
    ),
    (
        "fond",
        "захоплені",
        "They have two children who are fond of the dog",
        "У них двоє дітей, які захоплені собакою",
    ),
    (
        "fond",
        "захоплені",
        "They are remarkably fond of music",
        "Вони надзвичайно люблять музику",
    ),
    (
        "entertainment",
        "розвага",
        "The evening was filled with entertainment and music",
        "Вечір був наповнений розвагами та музикою",
    ),
    (
        "throat, sore",
        "горло, болить",
        "Her throat is sore because of the cold",
        "У неї болить горло через застуду",
    ),
    (
        "besides",
        "окрім",
        "Besides work, he has an interesting hobby",
        "Окрім роботи, у нього є цікаве хобі",
    ),
    (
        "worthy, besides",
        "гідний, окрім",
        # "no one is going to make you feel as worthy as you deserve besides you",
        "No one will make you feel worthy besides you",
        # "ніхто, окрім вас, не змусить вас відчути себе гідним того, чого ви заслуговуєте",
        "Ніхто не змусить вас почуватися гідними, крім вас самих",
    ),
    (
        "besides",
        "окрім",
        "what else besides the super strings do you see?",
        "що ще окрім суперструн ти бачиш?",
    ),
    (
        "cure",
        "лікувати",
        "This medicine can cure the disease",
        "Ці ліки можуть вилікувати хворобу",
    ),
    (
        "quarrel, siblings",
        "сварка, брати і сестри",
        "The siblings often quarrel over small things",
        "Брати і сестри часто сваряться через дрібниці",
    ),
    (
        "quarrel, eventually",
        "сварка, зрештою",
        "The political quarrel eventually turned into ethnic violence",
        "Політична сварка згодом переросла в етнічне насильство",
    ),
    (
        "admission",
        "прийом",
        "The admission fee to the museum is low",
        "Плата за вхід до музею низька",
    ),
    (
        "admission",
        "прийом",
        "An apology is an admission of guilt or wrongdoing",
        "Вибачення - це визнання провини або неправомірних вчинків",
    ),
    (
        "admission",
        "прийом",
        "College admission requires good grades",
        "Вступ до коледжу вимагає гарних оцінок",
    ),
    (
        "passage",
        "проходження",
        "She highlighted a passage in the book",
        "Вона підкреслила уривок у книзі",
    ),
    (
        "passage",
        "проходження",
        "I forget the passage of time",
        "Я забуваю про плин часу",
    ),
    (
        "passage",
        "проходження",
        "For our first passage just looking at the data",
        "Для нашого першого проходу просто дивимося на дані",
    ),
    (
        "passage",
        "проходження",
        "It's a story of great historical passage",
        "Це історія великого історичного переходу",
    ),
    # (
    #     "passage",
    #     "ухвалення",
    #     "The passage of the new law took several weeks",
    #     "Ухвалення нового закону зайняло кілька тижнів",
    # ),
    (
        "seize, opportunity",
        "захопити, можливість",
        "You should seize the opportunity quickly",
        "Тобі слід швидко скористатися можливістю",
    ),
    (
        "temper",
        "характер",
        "He tries to control his temper during arguments",
        "Він намагається контролювати свій характер під час суперечок",
    ),
    (
        "widespread",
        "поширений",
        "The widespread use of technology changed our lives",
        "Широке використання технологій змінило наше життя",
    ),
    (
        "ceiling",
        "стеля",
        "They painted the ceiling white",
        "Вони пофарбували стелю в білий колір",
    ),
    (
        "settlement",
        "поселення",
        "The small settlement was peaceful and quiet",
        "Маленьке поселення було спокійним і тихим",
    ),
    (
        "settlement",
        "врегулювання",
        # "The settlement doesn't require him to acknowledge fault or liability",
        "We reached a settlement agreement to keep the college open",
        "Ми досягли мирової угоди, щоб залишити коледж відкритим",
    ),
    (
        "settlement",
        "врегулювання",
        "The insurance company offered a settlement for the damages",
        "Страхова компанія запропонувала компенсацію за збитки",
    ),
    (
        "spot",
        "пляма",
        "There is a spot on his shirt",
        "На його сорочці є пляма",
    ),
    (
        "spot",
        "пляма",
        "It can help the spider spot something it wants to eat",
        "Це може допомогти павуку помітити те, що він хоче з’їсти",
    ),
    (
        "spot",
        "пляма",
        "Earth's orbit around the Sun is in kind of a sweet spot",
        "Орбіта Землі навколо Сонця є в своєрідному ідеальному положенні",
    ),
    (
        "spot",
        "пляма",
        "I'll tell you what I think is the sweet spot for most guys",
        "Я розповім вам, що, на мою думку, подобається більшості хлопців",
    ),
    (
        "spot",
        "пляма",
        "She quickly spotted the point where the mistake occurred",
        "Вона швидко помітила місце, де сталася помилка",
    ),
    (
        "explode",
        "вибухати",
        "The bomb exploded with a loud noise",
        "Бомба вибухнула з гучним звуком",
    ),
    (
        "explode, scene",
        "вибухати, сцена",
        "Food delivery apps had begun to explode on the scene",
        "Застосунки для доставки їжі почали стрімко набирати популярність",
    ),
    (
        "quotient, division",
        "частка, ділення",
        # "The quotient is the result of division",
        # "Частка — це результат ділення",
        "the result of the division is called the quotient",
        "результат ділення називається часткою",
    ),
    (
        "quotient",
        "частка",
        "For the quotient of two functions, it uses the quotient rule.",
        "Для частки двох функцій використовується правило частки.",
    ),
    (
        "distinguish",
        "розрізняти",
        "It's hard to distinguish colors in the dark",
        "Важко розрізняти кольори в темряві",
    ),
    (
        "distinguish",
        "розрізняти",
        "It's not that easy to distinguish between valid and invalid information.",
        "Не так просто відрізнити дійсну інформацію від недійсної.",
    ),
    (
        "distinguish",
        "розрізняти",
        "Man can distinguish from animals by consciousness",
        "Людину можна відрізнити від тварин за допомогою свідомості",
    ),
    (
        "band, performance",
        "гурт, виступ",
        "The band gave an amazing performance",
        "Гурт дав чудовий виступ",
    ),
    (
        "ban",
        "забороняти",
        "Smoking is banned in public places",
        "Куріння заборонено в громадських місцях",
    ),
    (
        "loss",
        "поразка",
        "The loss in the game disappointed the team",
        "Поразка в грі засмутила команду",
    ),
    (
        "chick",
        "пташеня",
        "The chick was too small to fly",
        "Пташеня було надто маленьким, щоб літати",
    ),
    (
        "drown",
        "тонути",
        "He saved the boy who was drowning in the river",
        "Він врятував хлопчика, який тонув у річці",
    ),
    (
        "drown",
        "тонути",
        "He saved the boy from drowning in the river.",
        "Він врятував хлопчика від утоплення в річці.",
    ),
    (
        "drown",
        "тонути",
        "I read slowly to drown out the noise",
        "Я читаю повільно, щоб заглушити шум",
    ),
    (
        "drown",
        "тонути",
        "I don't want to drown you in technical information",
        "Я не хочу засипати вас технічною інформацією",
    ),
    (
        "apparent, immediately",
        "очевидний, негайно",
        "The mistake was apparent immediately",
        "Помилка стала очевидною одразу",
    ),
    (
        "apparent, immediately",
        "очевидний, негайно",
        "This is a benefit that may not be apparent immediately",
        "Це перевага, яка може бути не одразу очевидною",
    ),
    (
        "apparent",
        "очевидний",
        "Over the past year, this truth has never been more apparent",
        "За останній рік ця правда ніколи не була більш очевидною",
    ),
    (
        "apparent",
        "очевидний",
        "They were dropped for no apparent reason",
        "Їх відкинули без очевидної причини",
    ),
    (
        "awake",
        "несплячий",
        "I was awake before the alarm rang",
        "Я був несплячий ще до того, як задзвонив будильник",
    ),
    (
        "offensive",
        "образливий",
        "His offensive remark made her angry",
        "Його образливе зауваження розлютило її",
    ),
    (
        "deaf",
        "глухий",
        "He is deaf and cannot hear the sound",
        "Він глухий і не може чути звук",
    ),
    (
        "rub",
        "терти",
        "She rubbed her hands to stay warm in the cold",
        "Вона терла руки, щоб зігрітися на холоді",
    ),
    (
        "locate",
        "знайти",
        "We need to locate the store on the map",
        "Нам потрібно знайти магазин на карті",
    ),
    (
        "cheque",
        "чек",
        "He cashed the cheque at the bank",
        "Він обміняв чек на готівку в банку",
    ),
    (
        "net",
        "сітка",
        "They used a net to catch fish",
        "Вони використовували сітку, щоб ловити рибу",
    ),
    (
        "scratch",
        "дряпати",
        "The cat scratched his hand during play",
        "Кіт подряпав йому руку під час гри",
    ),
    (
        "scratch",
        "дряпати",
        "I don't have to learn everything from scratch",
        "Мені не потрібно вчитися всьому з нуля",
    ),
    (
        "scratch",
        "дряпати",
        "He emerged without a scratch from the accident.",
        "Він вийшов з аварії без жодної подряпини",
    ),
    (
        "county, fair",
        "графство, ярмарок",
        "The county fair was the biggest event of the year",
        "Ярмарок у графстві був найбільшою подією року",
    ),
    (
        "resignation",
        "відставка",
        "His resignation from the job surprised everyone",
        "Його звільнення з роботи здивувало всіх",
    ),
    (
        "resign, outrage",
        "піти у відставку, обурення",
        "Public outrage forced the government to resign",
        "Обурення громадськості змусило уряд піти у відставку",
    ),
    (
        "resign, outrage",
        "піти у відставку, обурення",
        "it doesn't mean you need to resign yourself",
        "це не означає, що вам потрібно змиритися",
    ),
    (
        "moderate",
        "помірний",
        "The weather was moderate this season",
        "Цього сезону погода була помірною",
    ),
    (
        "moderate",
        "помірний",
        "My parents were quite moderate in their consumption",
        "Мої батьки були досить поміркованими у споживанні",
    ),
    # (
    #     "moderate",
    #     "помірний",
    #     "I see no political force in play for moderate cannabis policy",
    #     "Я не бачу жодної політичної сили, яка виступає за помірковану політику щодо канабісу",
    # ),
    (
        "moderate",
        "помірний",
        "A moderate majority often goes unheard",
        "Помірна більшість часто залишається непочутою",
    ),
    (
        "asleep",
        "спати",
        "The child was already asleep in bed",
        "Дитина вже спала в ліжку",
    ),
    (
        "asleep",
        "спати",
        "1, 2, 3, deep asleep, fast asleep",
        "1, 2, 3, глибокий сон, міцний сон",
    ),
    (
        "asleep",
        "спати",
        "Is my boy still fast asleep?",
        "Мій хлопчик ще міцно спить?",
    ),
    (
        "tension",
        "напруження",
        "The tension in the conflict began to rise",
        "напруження в конфлікті почало зростати",
    ),
    (
        "relieve, tension",
        "полегшити, напруження",
        "They joked to relieve the tension.",
        "Вони пожартували, щоб зняти напруження.",
    ),
    (
        "tension",
        "напруження",
        "She tried to ease the tension and smooth over the conflict.",
        "Вона намагалася зняти напруження і згладити конфлікт.",
    ),
    (
        "flesh",
        "плоть",
        "The wound exposed the flesh beneath the skin",
        "Рана оголила плоть під шкірою",
    ),
    (
        "succulent, flesh",
        "соковитий, плоть",
        "the succulent flesh of these plants is a water source",
        "соковита м’якоть цих рослин є джерелом води",
    ),
    (
        "flesh",
        "плоть",
        "this fish has a very firm flesh",
        "ця риба має дуже тверде м'ясо.",
    ),
    (
        "flesh",
        "плоть",
        "They're made of flesh and blood the way we are",
        "Вони зроблені з плоті та крові так само, як і ми",
    ),
    (
        "race",
        "гонка",
        "The athlete won the race with ease",
        "Атлет легко виграв гонку",
    ),
    (
        "tour",
        "тур",
        "The guide took us on a tour of the city",
        "Гід провів нас на екскурсію містом",
    ),
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
    (
        "fur",
        "хутро",
        "The coat is made of soft fur",
        "Пальто зроблене з м'якого хутра",
    ),
    (
        "nod",
        "кивок",
        "He gave a nod of agreement silently",
        "Він мовчки кивнув у знак згоди",
    ),
    (
        "fade",
        "зникати",
        "The color of the painting faded over time",
        "Колір картини з часом зник",
    ),
    (
        "fade",
        "зникати",
        "These things fade after a while",
        "Ці речі зникають з часом.",
    ),
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
    (
        "situate",
        "розташувати",
        "The house is situated on top of the hill",
        "Будинок розташований на вершині пагорба",
    ),
    (
        "situate",
        "розташувати",
        "we must constantly situate our efforts to defend the human rights",
        "ми повинні постійно спрямовувати наші зусилля на захист прав людини",
    ),
    (
        "situate, convener",
        "розташувати, організатор",
        "we are trying to situate ourselves as a neutral convener",
        "ми намагаємося позиціонувати себе як нейтрального організатора",
    ),
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
]
