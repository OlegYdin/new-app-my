"""
ОЦБК — Основная Цифро-Буквенная Кодировка
Приложение для кодирования чисел в буквы и поиска слов по коду
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DigitMapping:
    """Маппинг одной цифры на две буквы"""
    digit: str
    col1: str  # Интуитивная колонка
    col2: str  # Компенсационная колонка
    anchor: str  # Якорь для запоминания


# Таблица ОЦБК
OCBK_TABLE = {
    '0': DigitMapping('0', 'Н', 'Ф', 'Ноль → Начало / Форма кольца'),
    '1': DigitMapping('1', 'Р', 'Ц', 'Раз → один / Цель (фокус на одном)'),
    '2': DigitMapping('2', 'Д', 'Б', 'Два / Близнецы (Б-Б)'),
    '3': DigitMapping('3', 'Т', 'Щ', 'Три черты / Щ три зубца + черта'),
    '4': DigitMapping('4', 'Ч', 'К', 'Четыре угла / Каркас'),
    '5': DigitMapping('5', 'П', 'Г', 'Пять пальцев / Горсть'),
    '6': DigitMapping('6', 'Ш', 'Л', 'Шесть линий / Лесенка (6 ступеней)'),
    '7': DigitMapping('7', 'С', 'Ж', 'Семь дней / Жизнь (неделя)'),
    '8': DigitMapping('8', 'В', 'Х', 'Восьмёрка / Х (перекрёстье двух колец)'),
    '9': DigitMapping('9', 'З', 'М', 'Зеркальная 9 / Максимум цифры'),
}

# Частоты согласных (для справки)
CONSONANT_FREQUENCY = {
    'Н': 0.082, 'Р': 0.048, 'С': 0.055, 'Т': 0.063, 'Л': 0.044, 'В': 0.047, 'К': 0.035,
    'П': 0.028, 'М': 0.032, 'Д': 0.030, 'Г': 0.017, 'З': 0.017, 'Б': 0.015,
    'Ч': 0.015, 'Ж': 0.010, 'Х': 0.010, 'Ф': 0.003, 'Ц': 0.005, 'Щ': 0.001,
}


class OCBKEncoder:
    """Кодер/декодер системы ОЦБК"""
    
    def __init__(self, use_col1: bool = True, use_col2: bool = True):
        """
        Инициализация кодера
        
        Args:
            use_col1: Использовать первую колонку (интуитивную)
            use_col2: Использовать вторую колонку (компенсационную)
        """
        self.use_col1 = use_col1
        self.use_col2 = use_col2
    
    def encode_digit(self, digit: str) -> List[str]:
        """
        Кодировать одну цифру в буквы
        
        Returns:
            Список возможных букв для данной цифры
        """
        if digit not in OCBK_TABLE:
            return []
        
        mapping = OCBK_TABLE[digit]
        result = []
        
        if self.use_col1:
            result.append(mapping.col1)
        if self.use_col2:
            result.append(mapping.col2)
        
        return result
    
    def encode_number(self, number: str) -> List[Tuple[str, List[str]]]:
        """
        Кодировать число в последовательность букв
        
        Args:
            number: Строка с цифрами (например, "863")
            
        Returns:
            Список кортежей (цифра, [возможные буквы])
        """
        result = []
        for digit in number:
            if digit.isdigit():
                letters = self.encode_digit(digit)
                result.append((digit, letters))
        return result
    
    def get_pattern(self, number: str) -> str:
        """
        Получить шаблон согласных для числа
        Использует только первую колонку для простоты
        
        Args:
            number: Строка с цифрами
            
        Returns:
            Строка с буквами-якорями
        """
        result = []
        for digit in number:
            if digit.isdigit() and digit in OCBK_TABLE:
                result.append(OCBK_TABLE[digit].col1)
        return ''.join(result)
    
    def decode_word(self, word: str) -> Optional[str]:
        """
        Декодировать слово обратно в цифры
        Извлекает только согласные из таблицы ОЦБК
        
        Args:
            word: Слово для декодирования
            
        Returns:
            Строка с цифрами или None если не найдено совпадений
        """
        # Создаем обратный маппинг: буква -> цифра
        reverse_map = {}
        for digit, mapping in OCBK_TABLE.items():
            reverse_map[mapping.col1] = digit
            reverse_map[mapping.col2] = digit
        
        result = []
        word_upper = word.upper()
        
        for char in word_upper:
            if char in reverse_map:
                result.append(reverse_map[char])
        
        return ''.join(result) if result else None
    
    def decode_phrase(self, phrase: str) -> List[Tuple[str, str]]:
        """
        Декодировать фразу (несколько слов)
        
        Args:
            phrase: Фраза для декодирования
            
        Returns:
            Список кортежей (слово, код)
        """
        result = []
        words = re.findall(r'[а-яА-ЯёЁ]+', phrase)
        
        for word in words:
            code = self.decode_word(word)
            if code:
                result.append((word, code))
        
        return result


class WordFinder:
    """Поиск слов по коду ОЦБК"""
    
    def __init__(self, dictionary_path: Optional[str] = None):
        """
        Инициализация поисковика слов
        
        Args:
            dictionary_path: Путь к файлу со словарём (одно слово на строку)
        """
        self.encoder = OCBKEncoder()
        self.dictionary: List[str] = []
        
        # Пробуем загрузить словарь по умолчанию
        default_paths = [
            'russian_dictionary.txt',
            'dictionary.txt',
            'словарь.txt'
        ]
        
        if dictionary_path:
            self.load_dictionary(dictionary_path)
        else:
            # Пытаемся найти словарь в текущей директории
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            for path in default_paths:
                full_path = os.path.join(script_dir, path)
                if os.path.exists(full_path):
                    self.load_dictionary(full_path)
                    break
            else:
                # Базовый словарь для демонстрации
                self._load_basic_dictionary()
    
    def _load_basic_dictionary(self):
        """Загрузить базовый словарь для тестирования"""
        self.dictionary = [
            'хвост', 'ваш', 'тост', 'высота', 'хват', 'шест', 'шесть',
            'позвонить', 'газон', 'зона', 'понизить', 'запонка', 'пони',
            'дама', 'дом', 'дым', 'дыня', 'демон', 'дно', 'дана',
            'театр', 'тротуар', 'тщета', 'щит', 'трещина', 'тест',
            'чердак', 'очередь', 'чреда', 'очерк', 'чек', 'ключ',
            'школа', 'жизнь', 'шалаш', 'желудь', 'жила', 'шла',
            'восемь', 'восьмой', 'выход', 'ход', 'воздух', 'вздох',
            'зеркало', 'замок', 'зима', 'земля', 'знамя', 'знак',
            'ноль', 'нос', 'фон', 'нога', 'флаг', 'небо',
            'раз', 'рак', 'центр', 'ряд', 'бор', 'бар',
            'два', 'дуб', 'бог', 'бык', 'бак', 'бок',
            'три', 'тьма', 'щи', 'щавель', 'трещотка',
            'четыре', 'кулак', 'каркас', 'кочка', 'качка',
            'пять', 'гвоздь', 'паук', 'гусь', 'пугало',
            'шесть', 'лес', 'лестница', 'шест', 'шелк',
            'семь', 'жизнь', 'сено', 'жесть', 'сажа',
            'восемь', 'восьмерка', 'хохот', 'вздох', 'муха',
            'девять', 'замок', 'меч', 'мачта', 'змея',
            # Добавочные слова для примеров
            'доска', 'босой', 'бес', 'спас', 'сачок', 'плащ',
            'плещет', 'пещера', 'чаща', 'чаща', 'клещ', 'лещ',
            'газон', 'гонза', 'поза', 'запор', 'пора', 'пара',
            'нора', 'фарс', 'фарт', 'перс', 'цена', 'цирк',
            'близнец', 'брат', 'драма', 'брама', 'дрожь', 'брошь',
            'трещина', 'щи', 'троста', 'трость', 'чадо', 'кадка',
            'год', 'кот', 'кит', 'год', 'гуд', 'гут',
        ]
    
    def load_dictionary(self, path: str):
        """
        Загрузить словарь из файла
        
        Args:
            path: Путь к файлу словаря
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.dictionary = [line.strip().lower() for line in f if line.strip()]
            print(f"✓ Загружено {len(self.dictionary)} слов из словаря")
        except FileNotFoundError:
            print(f"✗ Файл словаря не найден: {path}")
            print("  Используем базовый словарь")
    
    def word_matches_pattern(self, word: str, pattern: str) -> bool:
        """
        Проверить, соответствует ли слово шаблону согласных
        
        Args:
            word: Слово для проверки
            pattern: Шаблон согласных (например, "ВШТ")
            
        Returns:
            True если слово соответствует шаблону
        """
        # Извлекаем согласные из слова (только те, что в таблице ОЦБК)
        word_consonants = ''
        for char in word.upper():
            for digit, mapping in OCBK_TABLE.items():
                if char == mapping.col1 or char == mapping.col2:
                    word_consonants += char
                    break
        
        # Проверяем соответствие шаблону (длина и символы)
        if len(word_consonants) != len(pattern):
            return False
        
        # Каждая буква слова должна соответствовать одной из букв в шаблоне
        for i, char in enumerate(word_consonants):
            pattern_chars = self._get_letters_for_pattern_char(pattern[i])
            if char not in pattern_chars:
                return False
        
        return True
    
    def _get_letters_for_pattern_char(self, pattern_char: str) -> List[str]:
        """
        Получить все возможные буквы для символа шаблона
        
        Например, для 'В' вернёт ['В', 'Х'] (обе колонки для цифры 8)
        """
        result = [pattern_char]
        
        # Находим, какой цифре соответствует этот символ
        for digit, mapping in OCBK_TABLE.items():
            if mapping.col1 == pattern_char:
                result.append(mapping.col2)
                break
            elif mapping.col2 == pattern_char:
                result.append(mapping.col1)
                break
        
        return result
    
    def find_words_for_code(self, code: str, max_results: int = 20) -> List[str]:
        """
        Найти слова для заданного кода
        Учитывает ОБЕ колонки (интуитивную и компенсационную)

        Args:
            code: Код цифры (например, "863")
            max_results: Максимальное количество результатов

        Returns:
            Список подходящих слов
        """
        # Создаём список: для каждой позиции кода - список букв
        code_letters = []
        for digit in code:
            if digit.isdigit() and digit in OCBK_TABLE:
                mapping = OCBK_TABLE[digit]
                code_letters.append([mapping.col1, mapping.col2])

        results = []
        for word in self.dictionary:
            if self._word_matches_code_v2(word, code_letters):
                results.append(word)
                if len(results) >= max_results:
                    break

        return results
    
    def _word_matches_code_v2(self, word: str, code_letters: list) -> bool:
        """
        Проверить, соответствует ли слово коду (с учётом обеих колонок)
        
        Args:
            word: Слово для проверки
            code_letters: Список списков букв для каждой позиции кода
                         например, для '979': [['З','М'], ['С','Ж'], ['З','М']]
        
        Returns:
            True если слово соответствует коду
        """
        # Извлекаем из слова только буквы, которые есть в таблице ОЦБК
        word_letters = []
        for char in word.upper():
            for digit, letters in OCBK_TABLE.items():
                if char == letters.col1 or char == letters.col2:
                    word_letters.append(char)
                    break
        
        # Длина должна совпадать с длиной кода
        if len(word_letters) != len(code_letters):
            return False
        
        # Проверяем каждую букву слова
        for i, allowed_letters in enumerate(code_letters):
            if word_letters[i] not in allowed_letters:
                return False
        
        return True
    
    def find_all_combinations(self, code: str) -> List[str]:
        """
        Найти все возможные буквенные комбинации для кода
        (без проверки по словарю, просто перебор)
        
        Args:
            code: Код цифры
            
        Returns:
            Список всех комбинаций букв
        """
        encoder = OCBKEncoder()
        encoded = encoder.encode_number(code)
        
        if not encoded:
            return []
        
        # Генерируем все комбинации
        combinations = ['']
        for digit, letters in encoded:
            new_combinations = []
            for combo in combinations:
                for letter in letters:
                    new_combinations.append(combo + letter)
            combinations = new_combinations
        
        return combinations


class OCBKTrainer:
    """Тренажёр для запоминания таблицы ОЦБК"""
    
    def __init__(self):
        self.encoder = OCBKEncoder()
        self.word_finder = WordFinder()
    
    def generate_flashcards(self) -> List[dict]:
        """
        Сгенерировать карточки для запоминания
        
        Returns:
            Список карточек в формате {вопрос, ответ, подсказка}
        """
        cards = []
        
        # Карточки на запоминание букв для каждой цифры
        for digit, mapping in OCBK_TABLE.items():
            cards.append({
                'type': 'digit_to_letters',
                'question': f"Какие буквы соответствуют цифре {digit}?",
                'answer': f"Колонка 1: {mapping.col1}\nКолонка 2: {mapping.col2}",
                'hint': mapping.anchor
            })
        
        # Карточки на декодирование
        cards.append({
            'type': 'decode',
            'question': "Декодируйте слово: ШКОЛА",
            'answer': "646 (Ш-К-Л, буква А игнорируется)",
            'hint': "Извлекайте только согласные из таблицы"
        })

        cards.append({
            'type': 'decode',
            'question': "Декодируйте слово: ЖИЗНЬ",
            'answer': "790 (Ж-З-Н, буква Ь игнорируется)",
            'hint': "Ь и Ь игнорируются"
        })
        
        # Карточки на кодирование
        test_codes = ['863', '5901', '2746', '412']
        for code in test_codes:
            pattern = self.encoder.get_pattern(code)
            words = self.word_finder.find_words_for_code(code, max_results=5)
            
            cards.append({
                'type': 'encode',
                'question': f"Закодируйте число {code} (шаблон: {pattern})",
                'answer': f"Слова: {', '.join(words) if words else 'найдите свои'}",
                'hint': f"Буквы: {pattern}"
            })
        
        return cards
    
    def generate_quiz(self, num_questions: int = 10, blitz_mode: bool = False, 
                      focus_mode: str = 'all') -> List[dict]:
        """
        Сгенерировать тест для проверки знаний

        Args:
            num_questions: Количество вопросов
            blitz_mode: Если True, генерировать больше разнообразных вопросов
            focus_mode: 'digit_to_letter' (цифра→буква), 'letter_to_digit' (буква→цифра), 
                       'both' (оба направления), 'all' (все типы)

        Returns:
            Список вопросов
        """
        import random

        questions = []
        digits = list(OCBK_TABLE.keys())

        # Собираем все буквы в плоский список для генерации вопросов
        all_letters = []
        for digit, mapping in OCBK_TABLE.items():
            all_letters.append((mapping.col1, digit, 'col1'))
            all_letters.append((mapping.col2, digit, 'col2'))

        # Вопросы: Цифра → Буква (какая буква из 1-й или 2-й колонки?)
        if focus_mode in ['digit_to_letter', 'both', 'all']:
            for _ in range(num_questions // 2):
                digit = random.choice(digits)
                mapping = OCBK_TABLE[digit]
                
                # Случайно выбираем: 1-я или 2-я колонка
                col_choice = random.choice(['col1', 'col2'])
                if col_choice == 'col1':
                    correct = mapping.col1
                    col_name = "1"
                else:
                    correct = mapping.col2
                    col_name = "2"
                
                # Генерируем неправильные варианты (другие буквы)
                wrong_options = set()
                while len(wrong_options) < 3:
                    wrong_digit = random.choice(digits)
                    wrong_mapping = OCBK_TABLE[wrong_digit]
                    # Берём букву из той же колонки
                    wrong_letter = wrong_mapping.col1 if col_choice == 'col1' else wrong_mapping.col2
                    if wrong_letter != correct:
                        wrong_options.add(wrong_letter)
                
                questions.append({
                    'question': f"{digit} (колонка {col_name})",
                    'correct_answer': correct,
                    'options': [correct] + list(wrong_options),
                    'type': 'digit_to_letter'
                })

        # Вопросы: Буква → Цифра (какой цифре соответствует эта буква?)
        if focus_mode in ['letter_to_digit', 'both', 'all']:
            for _ in range(num_questions // 2):
                letter, digit, col_type = random.choice(all_letters)
                
                # Генерируем неправильные варианты (другие цифры)
                wrong_options = set()
                while len(wrong_options) < 3:
                    wrong_digit = random.choice(digits)
                    if wrong_digit != digit:
                        wrong_options.add(wrong_digit)
                
                questions.append({
                    'question': f"{letter}",
                    'correct_answer': digit,
                    'options': [digit] + list(wrong_options),
                    'type': 'letter_to_digit'
                })

        # Перемешиваем и ограничиваем количество
        random.shuffle(questions)
        return questions[:num_questions]
    
    def generate_blitz(self, num_questions: int = 10) -> List[dict]:
        """
        Сгенерировать блиц-вопросы на декодирование чисел и слов
        
        Args:
            num_questions: Количество вопросов
            
        Returns:
            Список вопросов
        """
        import random
        
        questions = []
        digits = list(OCBK_TABLE.keys())
        
        # Тип 1: Декодирование слов (какое слово соответствует коду?)
        words_list = list(self.word_finder.dictionary)
        random.shuffle(words_list)
        
        for word in words_list[:num_questions // 3]:
            code = self.encoder.decode_word(word)
            if code and len(code) >= 2:
                # Генерируем неправильные варианты (другие коды)
                wrong_codes = set()
                while len(wrong_codes) < 3:
                    wrong_word = random.choice(words_list)
                    wrong_code = self.encoder.decode_word(wrong_word)
                    if wrong_code and wrong_code != code and len(wrong_code) == len(code):
                        wrong_codes.add(wrong_code)
                
                questions.append({
                    'question': f"Закодируйте слово '{word.upper()}'",
                    'correct_answer': code,
                    'options': [code] + list(wrong_codes),
                    'type': 'encode_word'
                })
        
        # Тип 2: Кодирование чисел (какое слово соответствует числу?)
        # Используем только коды, для которых есть слова
        valid_codes = []
        for _ in range(50):
            code_length = random.randint(2, 4)
            code = ''.join(random.choices(digits, k=code_length))
            words = self.word_finder.find_words_for_code(code, max_results=5)
            if words:
                valid_codes.append((code, words))
        
        for code, words in valid_codes[:num_questions // 3]:
            correct_word = random.choice(words)
            
            # Генерируем неправильные варианты (другие слова для других кодов)
            wrong_words = set()
            for _, other_words in valid_codes:
                if other_words != words:
                    wrong_words.add(random.choice(other_words))
                if len(wrong_words) >= 3:
                    break
            
            # Если не хватило, добавляем случайные слова
            while len(wrong_words) < 3:
                wrong_word = random.choice(words_list)
                if wrong_word != correct_word:
                    wrong_words.add(wrong_word)
            
            questions.append({
                'question': f"Найдите слово для кода {code}",
                'correct_answer': correct_word,
                'options': [correct_word] + list(wrong_words),
                'type': 'decode_code'
            })
        
        # Тип 3: Шаблон согласных (какой шаблон у числа?)
        for _ in range(num_questions // 3):
            code_length = random.randint(2, 4)
            code = ''.join(random.choices(digits, k=code_length))
            pattern = self.encoder.get_pattern(code)
            
            # Генерируем неправильные шаблоны
            wrong_patterns = set()
            while len(wrong_patterns) < 3:
                wrong_code = ''.join(random.choices(digits, k=code_length))
                wrong_pattern = self.encoder.get_pattern(wrong_code)
                if wrong_pattern != pattern and len(wrong_pattern) == len(pattern):
                    wrong_patterns.add(wrong_pattern)
            
            questions.append({
                'question': f"Шаблон согласных для числа {code}",
                'correct_answer': pattern,
                'options': [pattern] + list(wrong_patterns),
                'type': 'pattern'
            })
        
        # Перемешиваем и ограничиваем
        random.shuffle(questions)
        return questions[:num_questions]


def print_table():
    """Вывести красивую таблицу ОЦБК"""
    print("\n" + "=" * 70)
    print(" " * 20 + "ТАБЛИЦА ОЦБК")
    print("=" * 70)
    print(f"{'Цифра':<8} {'Колонка 1':<15} {'Колонка 2':<15} {'Якорь':<30}")
    print("-" * 70)
    
    for digit in sorted(OCBK_TABLE.keys()):
        mapping = OCBK_TABLE[digit]
        print(f"{digit:<8} {mapping.col1:<15} {mapping.col2:<15} {mapping.anchor:<30}")
    
    print("=" * 70 + "\n")


def interactive_mode():
    """Интерактивный режим работы с приложением"""
    encoder = OCBKEncoder()
    word_finder = WordFinder()
    trainer = OCBKTrainer()
    
    print("\n" + "🎯 " * 10)
    print("ДОБРО ПОЖАЛОВАТЬ В ОЦБК — СИСТЕМУ ЦИФРО-БУКВЕННОЙ КОДИРОВКИ")
    print("🎯 " * 10)
    
    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ:")
        print("1. Показать таблицу ОЦБК")
        print("2. Закодировать число в буквы")
        print("3. Декодировать слово/фразу в цифры")
        print("4. Найти слова для кода")
        print("5. Пройти тест")
        print("6. Показать карточки для запоминания")
        print("7. Выход")
        print("-" * 50)
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == '1':
            print_table()
        
        elif choice == '2':
            number = input("Введите число для кодирования: ").strip()
            if number.isdigit():
                encoded = encoder.encode_number(number)
                pattern = encoder.get_pattern(number)
                print(f"\n📝 Число: {number}")
                print(f"📝 Шаблон согласных: {pattern}")
                print(f"📝 Возможные буквы для каждой цифры:")
                for digit, letters in encoded:
                    print(f"   {digit} → {', '.join(letters)}")
                
                # Ищем слова
                words = word_finder.find_words_for_code(number)
                if words:
                    print(f"\n💡 Примеры слов: {', '.join(words)}")
            else:
                print("❌ Введите корректное число!")
        
        elif choice == '3':
            phrase = input("Введите слово или фразу для декодирования: ").strip()
            if phrase:
                result = encoder.decode_phrase(phrase)
                print(f"\n📝 Фраза: {phrase}")
                print(f"📝 Декодирование:")
                for word, code in result:
                    print(f"   {word} → {code}")
                
                full_code = ''.join([code for _, code in result])
                if full_code:
                    print(f"\n💡 Полный код: {full_code}")
            else:
                print("❌ Введите текст!")
        
        elif choice == '4':
            code = input("Введите код (цифры) для поиска слов: ").strip()
            if code.isdigit():
                words = word_finder.find_words_for_code(code)
                combinations = word_finder.find_all_combinations(code)
                
                print(f"\n📝 Код: {code}")
                print(f"📝 Шаблон согласных: {encoder.get_pattern(code)}")
                print(f"\n💡 Все буквенные комбинации:")
                for combo in combinations[:10]:  # Показываем первые 10
                    print(f"   {combo}")
                if len(combinations) > 10:
                    print(f"   ... и ещё {len(combinations) - 10}")
                
                if words:
                    print(f"\n💡 Найденные слова: {', '.join(words)}")
                else:
                    print("\n⚠️  Слов не найдено в базовом словаре.")
                    print("   Придумайте своё слово по шаблону!")
            else:
                print("❌ Введите корректный код!")
        
        elif choice == '5':
            print("\n🧠 ЗАПУСК ТЕСТА...")
            quiz = trainer.generate_quiz(num_questions=5)
            score = 0
            
            for i, q in enumerate(quiz, 1):
                print(f"\n{'='*50}")
                print(f"Вопрос {i}: {q['question']}")
                user_answer = input("Ваш ответ: ").strip()
                
                if user_answer.upper() == q['correct_answer'].upper():
                    print("✅ Верно!")
                    score += 1
                else:
                    print(f"❌ Неверно. Правильный ответ: {q['correct_answer']}")
            
            print(f"\n{'='*50}")
            print(f"📊 Ваш результат: {score}/{len(quiz)}")
            if score == len(quiz):
                print("🏆 Отлично! Вы мастер ОЦБК!")
            elif score >= len(quiz) // 2:
                print("👍 Хорошо! Продолжайте тренироваться!")
            else:
                print("📚 Стоит повторить таблицу ещё раз!")
        
        elif choice == '6':
            print("\n📇 КАРТОЧКИ ДЛЯ ЗАПОМИНАНИЯ:")
            print("=" * 60)
            cards = trainer.generate_flashcards()
            
            for i, card in enumerate(cards[:5], 1):  # Показываем первые 5
                print(f"\nКарточка {i}:")
                print(f"  Вопрос: {card['question']}")
                input("  Нажмите Enter для ответа...")
                print(f"  Ответ: {card['answer']}")
                print(f"  Подсказка: {card['hint']}")
            
            if len(cards) > 5:
                print(f"\n... и ещё {len(cards) - 5} карточек")
        
        elif choice == '7':
            print("\n👋 До свидания! Удачной тренировки!")
            break
        
        else:
            print("❌ Неверный выбор. Попробуйте снова.")


def main():
    """Точка входа в приложение"""
    import sys
    
    if len(sys.argv) > 1:
        # Режим командной строки
        command = sys.argv[1]
        
        if command == 'table':
            print_table()
        
        elif command == 'encode' and len(sys.argv) > 2:
            encoder = OCBKEncoder()
            number = sys.argv[2]
            pattern = encoder.get_pattern(number)
            print(f"Число: {number}")
            print(f"Шаблон: {pattern}")
        
        elif command == 'decode' and len(sys.argv) > 2:
            encoder = OCBKEncoder()
            phrase = ' '.join(sys.argv[2:])
            result = encoder.decode_phrase(phrase)
            for word, code in result:
                print(f"{word} → {code}")
        
        elif command == 'find' and len(sys.argv) > 2:
            word_finder = WordFinder()
            code = sys.argv[2]
            words = word_finder.find_words_for_code(code)
            print(f"Код: {code}")
            print(f"Слова: {', '.join(words) if words else 'не найдено'}")
        
        elif command == 'test':
            trainer = OCBKTrainer()
            quiz = trainer.generate_quiz(5)
            for i, q in enumerate(quiz, 1):
                print(f"{i}. {q['question']}")
    else:
        # Интерактивный режим
        interactive_mode()


if __name__ == '__main__':
    main()
