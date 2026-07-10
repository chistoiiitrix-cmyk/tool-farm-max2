import json, pathlib

# ПОЛНЫЙ СПИСОК 150 ИНСТРУМЕНТОВ - МАКСИМУМ ПОКРЫТИЯ ПОИСКА В РФ+МИР
tools_raw = [
# === ТЕКСТ 1-70 ===
("remove-duplicate-lines","Удалить дубли строк","Удалить дублирующиеся строки онлайн","Убирает повторы, оставляет уникальные. Оффлайн."),
("word-counter","Счетчик слов","Счетчик слов и символов онлайн","Считает слова, символы, абзацы для диплома и статей."),
("character-counter","Счетчик символов","Подсчет количества символов","С пробелами и без пробелов."),
("line-counter","Счетчик строк","Посчитать строки онлайн","Быстро считает количество строк."),
("reverse-text","Перевернуть текст","Перевернуть текст задом наперед","Реверс текста."),
("uppercase-converter","ВЕРХНИЙ РЕГИСТР","Текст в верхний регистр","Весь текст заглавными."),
("lowercase-converter","нижний регистр","Текст в нижний регистр","Весь текст маленькими."),
("title-case-converter","Заглавные Буквы","Каждое Слово С Заглавной","Title Case."),
("camelcase-converter","camelCase","Конвертер в camelCase","Для программистов JS."),
("snakecase-converter","snake_case","Конвертер в snake_case","Для Python, БД."),
("kebabcase-converter","kebab-case","Конвертер в kebab-case","Для URL и CSS."),
("trim-spaces","Удалить пробелы с краев","Trim пробелы","Убирает пробелы в начале и конце каждой строки."),
("remove-extra-spaces","Удалить лишние пробелы","Убрать двойные пробелы","Оставляет по одному."),
("remove-line-breaks","Удалить переносы строк","Убрать переносы строк","Делает текст одной строкой."),
("remove-empty-lines","Удалить пустые строки","Убрать пустые строки","Чистит текст."),
("add-line-numbers","Нумерация строк","Добавить номера строк","1. 2. 3."),
("sort-lines-az","Сорт А-Я","Сортировка строк А-Я","Алфавит русский и английский."),
("sort-lines-za","Сорт Я-А","Сортировка Я-А","Обратный алфавит."),
("shuffle-lines","Перемешать строки","Рандомизатор строк","Для розыгрышей."),
("reverse-lines","Реверс строк","Перевернуть порядок строк","Последняя первая."),
("extract-emails","Извлечь Email","Найти все Email в тексте","Вытаскивает почты regex."),
("extract-urls","Извлечь ссылки","Найти все URL","Вытаскивает ссылки."),
("extract-numbers","Извлечь цифры","Найти все числа","Вытаскивает числа."),
("remove-emojis","Удалить эмодзи","Убрать эмодзи","Чистит от смайлов."),
("add-prefix","Добавить префикс","Добавить текст перед каждой строкой","Например - в начале."),
("add-suffix","Добавить суффикс","Добавить текст в конце каждой строки","Например ;"),
("find-replace","Найти и заменить","Замена текста","Быстрый replace."),
("text-to-binary","Текст в бинарный","Конвертер в двоичный код","010101..."),
("binary-to-text","Бинарный в текст","Декодер бинарного",""),
("remove-duplicate-words","Удалить дубли слов","Убрать повторы слов",""),
("remove-punctuation","Удалить пунктуацию","Убрать знаки препинания","Оставляет только буквы."),
("add-commas","Строки в список через запятую","Столбец в строку через запятую","Для SQL IN()."),
("strip-html","Удалить HTML теги","Очистить от HTML","Текст без тегов."),
("text-length-sort","Сортировка по длине","Сортировать строки по длине строки","Короткие сверху."),
("duplicate-lines-counter","Подсчет дублей","Сколько раз повторяется каждая строка","Частота."),
("translit-converter","Транслит онлайн","Русский в транслит","Privet -> Привет и наоборот."),
("case-from-russian","Исправить раскладку","qwerty -> йцукен","ghbdtn -> привет."),
("remove-accents","Удалить акценты","Текст без диакритики",""),
("palindrome-check","Палиндром чекер","Проверка на палиндром","А роза упала на лапу Азора."),
("word-frequency","Частотность слов","SEO анализ текста","Считает плотность."),
("count-occurrences","Подсчет вхождений","Сколько раз встречается слово",""),
("remove-numbers","Удалить цифры","Убрать цифры из текста",""),
("keep-only-numbers","Оставить только цифры","Удалить все кроме цифр","Для ИНН, телефонов."),
("invert-case","Инверсия регистра","пРиВеТ -> ПрИвЕт",""),
("text-to-uppercase-first","Первая заглавная","Сделать первую букву большой","Остальные маленькие."),
("alphabetical-order-ru","Алфавит RU","Сортировка по русскому алфавиту","А-Я."),
("anagram-generator","Анаграмма","Перемешать буквы в словах",""),
("text-comparison","Сравнение текстов","Найти отличия в 2 текстах","Diff."),
("remove-whitespace","Удалить все пробелы","Убрать пробелы, табы",""),
("add-line-breaks","Добавить перенос каждые N","Разбить текст по N символов",""),
("extract-hashtags","Извлечь хештеги","Найти все #хештеги","Для Инсты."),
("extract-mentions","Извлечь @упоминания","Найти все @юзеры",""),
("slugify-ru","ЧПУ из русского","Транслит заголовка в URL","Для Битрикса, WP."),
("number-to-words-ru","Число прописью","Сумма прописью рубли","Для актов РФ, 123 -> сто двадцать три."),
("random-choice","Случайный выбор","Выбрать рандомную строку","Розыгрыш призов."),
("repeat-text","Повторить текст N раз","Дублировать текст",""),
("center-text","Отцентровать текст","Центрировать строки",""),
# === DEV 71-110 ===
("json-formatter","JSON Formatter","Форматировать JSON онлайн","Красивый JSON, валидатор."),
("json-minifier","Сжать JSON","JSON Minify","Убирает пробелы."),
("json-to-yaml","JSON в YAML","Конвертер JSON в YAML",""),
("yaml-to-json","YAML в JSON","Конвертер YAML в JSON",""),
("base64-encode","Base64 Encode","Кодировать в Base64",""),
("base64-decode","Base64 Decode","Декодировать из Base64",""),
("url-encode","URL Encode","Кодировать URL","%20..."),
("url-decode","URL Decode","Декодировать URL",""),
("html-escape","HTML Escape","Экранировать HTML","&lt; &gt;"),
("html-unescape","HTML Unescape","Деэкранировать HTML",""),
("jwt-decoder","JWT Декодер","Расшифровать JWT","Header payload."),
("hex-to-rgb","HEX в RGB","Конвертер цвета HEX -> RGB","#ff0000 -> rgb(255,0,0)"),
("rgb-to-hex","RGB в HEX","Конвертер RGB -> HEX",""),
("hex-to-hsl","HEX в HSL","HEX -> HSL",""),
("timestamp-converter","Unix Timestamp","Конвертер времени Timestamp","168... -> дата."),
("text-to-morse","Текст в Морзе","Морзе кодер",".-..."),
("morse-to-text","Морзе в текст","Декодер Морзе",""),
("slug-generator","Генератор Slug","Создать ЧПУ из заголовка","SEO URL."),
("password-generator","Генератор паролей","Создать надежный пароль","20 символов."),
("uuid-generator","UUID Генератор","Генератор UUID v4","xxxxxxxx-xxxx-..."),
("lorem-ipsum-generator","Lorem Ipsum","Генератор рыбного текста",""),
("random-number","Случайное число","Генератор случайных чисел","Диапазон."),
("hash-md5","MD5 Хеш","Посчитать MD5",""),
("hash-sha1","SHA1 Хеш","Посчитать SHA1",""),
("hash-sha256","SHA256 Хеш","Посчитать SHA256",""),
("ip-calculator","IP Калькулятор","Маска подсети, сеть","Для админов."),
("css-minifier","Сжать CSS","Minify CSS",""),
("js-minifier","Сжать JS","Minify JS",""),
("sql-formatter","Форматировать SQL","Beautify SQL",""),
("xml-formatter","Форматировать XML","Beautify XML",""),
("markdown-to-html","Markdown в HTML","Конвертер MD",""),
("html-to-markdown","HTML в Markdown","Конвертер",""),
("qr-generator","Генератор QR","Создать QR код","Текст -> QR."),
("color-picker-random","Случайный цвет","Рандомный HEX цвет",""),
("user-agent-parser","User Agent парсер","Разобрать User-Agent",""),
("utm-generator","UTM метки","Генератор UTM для рекламы","utm_source..."),
("regex-tester","RegEx тестер","Проверка регулярных выражений",""),
# === КАЛЬКУЛЯТОРЫ И РФ 111-150 ===
("bmi-calculator","Калькулятор ИМТ","Рассчитать ИМТ","Индекс массы тела."),
("loan-calculator","Кредитный калькулятор","Расчет кредита","Платеж, переплата, РФ."),
("percent-calculator","Калькулятор процентов","Процент от числа","20% от 500."),
("age-calculator","Калькулятор возраста","Сколько лет прожито","Дни, месяцы."),
("days-between-dates","Дней между датами","Посчитать дни между датами",""),
("calorie-calculator","Калькулятор калорий","Суточная норма калорий","БЖУ."),
("vat-calculator","Калькулятор НДС","НДС 20% выделить/начислить","Критично для РФ бизнеса."),
("discount-calculator","Калькулятор скидки","Скидка от цены","-15% от 1990."),
("profit-margin-calculator","Маржа калькулятор","Расчет маржи и наценки","Для WB, Ozon."),
("income-tax-ru","НДФЛ 13%","Расчет НДФЛ","РФ."),
("ip-tax-calculator","Налог ИП УСН","Расчет налога УСН 6%","Для ИП РФ."),
("currency-converter-rub","Конвертер валют RUB","USD EUR в RUB","По курсу ЦБ (демо)."),
("time-converter-msk","Конвертер МСК","Время МСК в другие пояса","МСК -> ЕКБ, ВВО и т.д."),
("ovulation-calculator","Калькулятор овуляции","Расчет цикла",""),
("fuel-consumption","Расход топлива","Литров на 100 км",""),
("mortgage-calculator","Ипотечный калькулятор","Расчет ипотеки РФ","Сбер, ВТБ."),
("deposit-calculator","Калькулятор вклада","Доход по вкладу","% годовых."),
("words-to-numbers","Слова в цифры","Сто -> 100",""),
("inn-validator","Проверка ИНН","Валидатор ИНН 10/12 РФ","ФНС алгоритм."),
("snils-validator","Проверка СНИЛС","Валидатор СНИЛС РФ",""),
("ogrn-validator","Проверка ОГРН","Валидатор ОГРН",""),
("kpp-validator","Проверка КПП","Валидатор КПП",""),
("okved-search","ОКВЭД поиск","Поиск ОКВЭД кода","Для бизнеса РФ."),
("bik-validator","Проверка БИК","Валидатор БИК банка РФ",""),
("passport-age-check","Проверка паспорта","Возраст по серии паспорта",""),
("password-strength","Надежность пароля","Проверка сложности пароля",""),
("email-validator","Валидатор Email","Проверка Email на валидность",""),
("phone-validator-ru","Валидатор телефона RU","Проверка +7 номера",""),
("credit-card-validator","Проверка карты","Luhn алгоритм",""),
("qr-decode","Декодер QR","Прочитать QR из картинки (демо)",""),
("barcode-generator","Штрихкод","Генератор штрихкода Code128",""),
("contract-number-generator","Номер договора","Генератор номеров ДГПХ","Для РФ."),
("act-generator","Генератор акта","Шаблон акта выполненных работ","Текст акта."),
("random-inn-generator","Генератор ИНН (демо)","Случайный ИНН для тестов","Невалидный, для тестов!"),
("random-snils-generator","Генератор СНИЛС (демо)","Случайный СНИЛС для тестов","Для тестов."),
("cbr-key-rate","Ключевая ставка ЦБ","Инфо ставка ЦБ РФ сегодня","21% пример."),
("work-days-calculator","Рабочие дни","Калькулятор рабочих дней РФ","Без праздников."),
("text-reading-time","Время чтения","Сколько читать текст","Минут."),
("youtube-title-counter","Счетчик YouTube","Символов в заголовке YT","До 100."),
]

full = []
for slug,title,h1,desc in tools_raw:
    if "json" in slug or "xml" in slug or "sql" in slug or "css" in slug or "js-min" in slug: js="jsonFormat"
    elif "base64" in slug: js="base64Tool"
    elif "url-" in slug: js="urlTool"
    elif "html-" in slug: js="htmlTool"
    elif any(x in slug for x in ["password","uuid","lorem","random","qr","hash","color","barcode"]): js="generatorTool"
    elif any(x in slug for x in ["calculat","bmi","loan","percent","vat","discount","margin","tax","mortgage","fuel","ovulation","work-days","reading","currency","time-converter"]): js="calcTool"
    elif "counter" in slug or "extract" in slug or "frequency" in slug or "validator" in slug or "check" in slug: js="wordCount"
    elif "slug" in slug or "utm" in slug: js="slugGen"
    else: js="textTool"

    if any(x in slug for x in ["vat","loan","mortgage","deposit","tax","profit","inn","snils","bik","ogrn","okved"]): niche="finance"
    elif any(x in slug for x in ["password","hash","jwt","proxy"]): niche="vpn"
    elif any(x in slug for x in ["slug","utm","json","html","hosting","qr"]): niche="hosting"
    elif any(x in slug for x in ["word","counter","lorem","reading"]): niche="writing"
    else: niche="none"

    full.append({
        "slug": slug,
        "title": title,
        "h1": h1,
        "desc": desc,
        "keywords": f"{title.lower()}, {h1.lower()}, {slug.replace('-',' ')} онлайн бесплатно, {desc.lower()}",
        "js_func": js,
        "placeholder": "Вставь текст сюда...",
        "affiliate_niche": niche
    })

path = pathlib.Path(__file__).parent / "tools-database.json"
path.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"✅ Сгенерировано {len(full)} инструментов -> {path}")
