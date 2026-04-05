"""
ОЦБК — Android приложение на Kivy
Цифро-Буквенная Кодировка для мобильных устройств
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import random

# Импортируем логику из ocbk_app
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ocbk_app import OCBKEncoder, WordFinder, OCBKTrainer, OCBK_TABLE


# Цветовая схема (Material Design)
class Colors:
    """Material Design цвета"""
    PRIMARY = '#5B7C99'
    PRIMARY_DARK = '#4A6A89'
    ACCENT = '#6B8CA9'
    BACKGROUND = '#121218'
    SURFACE = '#1A1A24'
    SURFACE_LIGHT = '#242430'
    CARD = '#2D2D3A'
    TEXT_PRIMARY = '#D0D0D8'
    TEXT_SECONDARY = '#8890A0'
    TEXT_MUTED = '#606878'
    SUCCESS = '#5A8F7A'
    WARNING = '#C9A95A'
    ERROR = '#B96A6A'
    BORDER = '#2A2A38'


class OCBKApp(App):
    """Главное приложение ОЦБК"""
    
    def build(self):
        """Построение приложения"""
        Window.clearcolor = get_color_from_hex(Colors.BACKGROUND)
        
        # Инициализация компонентов
        self.encoder = OCBKEncoder()
        self.word_finder = WordFinder()
        self.trainer = OCBKTrainer()
        
        # Менеджер экранов
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TableScreen(name='table'))
        sm.add_widget(EncodeScreen(name='encode'))
        sm.add_widget(DecodeScreen(name='decode'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(TrainerScreen(name='trainer'))
        
        return sm


class MainScreen(Screen):
    """Главный экран с навигацией"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Заголовок
        title = Label(
            text='[b]🎯 ОЦБК[/b]\nЦифро-Буквенная Кодировка',
            markup=True,
            font_size=sp(28),
            color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(100)
        )
        layout.add_widget(title)
        
        # Подзаголовок
        subtitle = Label(
            text='Запоминайте числа с помощью букв',
            font_size=sp(14),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(subtitle)
        
        # Кнопки навигации
        nav_buttons = [
            ('📊 Таблица ОЦБК', 'table'),
            ('🔤 Кодирование', 'encode'),
            ('🔢 Декодирование', 'decode'),
            ('🔍 Поиск слов', 'search'),
            ('🧠 Тренажёр', 'trainer'),
        ]
        
        for text, screen_name in nav_buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(60),
                background_color=get_color_from_hex(Colors.CARD),
                color=get_color_from_hex(Colors.TEXT_PRIMARY),
                font_size=sp(16)
            )
            btn.bind(on_release=lambda x, name=screen_name: self.go_to_screen(name))
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def go_to_screen(self, screen_name):
        """Переход к экрану"""
        self.manager.current = screen_name


class TableScreen(Screen):
    """Экран с таблицей ОЦБК"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='← Назад',
            size_hint_x=None,
            width=dp(100),
            background_color=get_color_from_hex(Colors.CARD),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        back_btn.bind(on_release=lambda x: self.manager.go_back())
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]📊 Таблица ОЦБК[/b]',
            markup=True,
            font_size=sp(18),
            color=get_color_from_hex(Colors.PRIMARY)
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Таблица с прокруткой
        scroll = ScrollView()
        table_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))
        
        # Заголовки
        headers = BoxLayout(size_hint_y=None, height=dp(40))
        for text, width in [('Цифра', 0.15), ('Колонка 1', 0.25), ('Колонка 2', 0.25), ('Якорь', 0.35)]:
            label = Label(
                text=f'[b]{text}[/b]',
                markup=True,
                font_size=sp(12),
                color=get_color_from_hex(Colors.ACCENT),
                size_hint_x=width
            )
            headers.add_widget(label)
        table_layout.add_widget(headers)
        
        # Данные
        for digit in sorted(OCBK_TABLE.keys()):
            m = OCBK_TABLE[digit]
            row = BoxLayout(size_hint_y=None, height=dp(50))
            
            row.add_widget(self._make_label(digit, 0.15))
            row.add_widget(self._make_label(m.col1, 0.25))
            row.add_widget(self._make_label(m.col2, 0.25))
            row.add_widget(self._make_label(m.anchor, 0.35, size=sp(10)))
            
            table_layout.add_widget(row)
        
        scroll.add_widget(table_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def _make_label(self, text, width, size=sp(12)):
        """Создать лейбл"""
        return Label(
            text=text,
            font_size=size,
            color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_x=width
        )


class EncodeScreen(Screen):
    """Экран кодирования"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='← Назад',
            size_hint_x=None,
            width=dp(100),
            background_color=get_color_from_hex(Colors.CARD),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        back_btn.bind(on_release=lambda x: self.manager.go_back())
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]🔤 Кодирование[/b]',
            markup=True,
            font_size=sp(18),
            color=get_color_from_hex(Colors.PRIMARY)
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Поле ввода
        input_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.number_input = TextInput(
            hint_text='Введите число...',
            multiline=False,
            font_size=sp(16),
            background_color=get_color_from_hex(Colors.SURFACE_LIGHT),
            foreground_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            hint_text_color=get_color_from_hex(Colors.TEXT_MUTED)
        )
        input_layout.add_widget(self.number_input)
        
        encode_btn = Button(
            text='Закодировать',
            size_hint_x=None,
            width=dp(150),
            background_color=get_color_from_hex(Colors.PRIMARY),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        encode_btn.bind(on_release=self.do_encode)
        input_layout.add_widget(encode_btn)
        
        layout.add_widget(input_layout)
        
        # Результат
        self.result_label = Label(
            text='Введите число для кодирования',
            font_size=sp(14),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            halign='left',
            valign='top',
            markup=True
        )
        scroll = ScrollView()
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def do_encode(self, instance):
        """Кодирование числа"""
        number = self.number_input.text.strip()
        
        if not number.isdigit():
            self.result_label.text = '[color=#B96A6A]❌ Введите корректное число![/color]'
            return
        
        app = App.get_running_app()
        encoded = app.encoder.encode_number(number)
        pattern = app.encoder.get_pattern(number)
        words = app.word_finder.find_words_for_code(number, max_results=10)
        combinations = app.word_finder.find_all_combinations(number)
        
        result = f'[b]📝 Число:[/b] {number}\n'
        result += f'[b]📝 Шаблон:[/b] {pattern}\n\n'
        result += '[b]📝 Буквы:[/b]\n'
        for digit, letters in encoded:
            m = OCBK_TABLE[digit]
            result += f'   {digit} → {m.col1} / {m.col2}\n'
        
        result += f'\n[b]💡 Комбинации ({len(combinations)}):[/b]\n'
        for i, combo in enumerate(combinations[:20], 1):
            result += f'   {i}. {combo}\n'
        
        if words:
            result += f'\n[color=#5A8F7A][b]✅ Слова:[/b] {", ".join(words)}[/color]'
        else:
            result += f'\n[color=#C9A95A]⚠️ Слов не найдено. Придумайте по шаблону {pattern}![/color]'
        
        self.result_label.text = result


class DecodeScreen(Screen):
    """Экран декодирования"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='← Назад',
            size_hint_x=None,
            width=dp(100),
            background_color=get_color_from_hex(Colors.CARD),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        back_btn.bind(on_release=lambda x: self.manager.go_back())
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]🔢 Декодирование[/b]',
            markup=True,
            font_size=sp(18),
            color=get_color_from_hex(Colors.PRIMARY)
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Поле ввода
        input_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.word_input = TextInput(
            hint_text='Введите слово...',
            multiline=False,
            font_size=sp(16),
            background_color=get_color_from_hex(Colors.SURFACE_LIGHT),
            foreground_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            hint_text_color=get_color_from_hex(Colors.TEXT_MUTED)
        )
        input_layout.add_widget(self.word_input)
        
        decode_btn = Button(
            text='Декодировать',
            size_hint_x=None,
            width=dp(150),
            background_color=get_color_from_hex(Colors.PRIMARY),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        decode_btn.bind(on_release=self.do_decode)
        input_layout.add_widget(decode_btn)
        
        layout.add_widget(input_layout)
        
        # Результат
        self.result_label = Label(
            text='Введите слово для декодирования',
            font_size=sp(14),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            halign='left',
            valign='top',
            markup=True
        )
        scroll = ScrollView()
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def do_decode(self, instance):
        """Декодирование слова"""
        phrase = self.word_input.text.strip()
        
        if not phrase:
            self.result_label.text = '[color=#B96A6A]❌ Введите текст![/color]'
            return
        
        app = App.get_running_app()
        result = app.encoder.decode_phrase(phrase)
        
        output = f'[b]📝 Фраза:[/b] {phrase}\n\n[b]📝 Декодирование:[/b]\n'
        
        for word, code in result:
            output += f'   {word} → {code}\n'
        
        full_code = ''.join([code for _, code in result])
        if full_code:
            output += f'\n[b]💡 Полный код:[/b] {full_code}'
            words = app.word_finder.find_words_for_code(full_code, max_results=5)
            if words:
                output += f'\n[color=#5A8F7A][b]💡 Другие слова:[/b] {", ".join(words)}[/color]'
        
        self.result_label.text = output


class SearchScreen(Screen):
    """Экран поиска слов"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='← Назад',
            size_hint_x=None,
            width=dp(100),
            background_color=get_color_from_hex(Colors.CARD),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        back_btn.bind(on_release=lambda x: self.manager.go_back())
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]🔍 Поиск слов[/b]',
            markup=True,
            font_size=sp(18),
            color=get_color_from_hex(Colors.PRIMARY)
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Поле ввода
        input_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.code_input = TextInput(
            hint_text='Введите код...',
            multiline=False,
            font_size=sp(16),
            background_color=get_color_from_hex(Colors.SURFACE_LIGHT),
            foreground_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            hint_text_color=get_color_from_hex(Colors.TEXT_MUTED)
        )
        input_layout.add_widget(self.code_input)
        
        search_btn = Button(
            text='Найти',
            size_hint_x=None,
            width=dp(150),
            background_color=get_color_from_hex(Colors.PRIMARY),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        search_btn.bind(on_release=self.do_search)
        input_layout.add_widget(search_btn)
        
        layout.add_widget(input_layout)
        
        # Результат
        self.result_label = Label(
            text='Введите код для поиска слов',
            font_size=sp(14),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            halign='left',
            valign='top',
            markup=True
        )
        scroll = ScrollView()
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def do_search(self, instance):
        """Поиск слов по коду"""
        code = self.code_input.text.strip()
        
        if not code.isdigit():
            self.result_label.text = '[color=#B96A6A]❌ Введите корректный код![/color]'
            return
        
        app = App.get_running_app()
        words = app.word_finder.find_words_for_code(code, max_results=50)
        pattern = app.encoder.get_pattern(code)
        
        output = f'[b]📝 Код:[/b] {code}\n[b]📝 Шаблон:[/b] {pattern}\n\n'
        
        if words:
            output += f'[color=#5A8F7A][b]✅ Найдено:[/b] {len(words)}[/color]\n\n'
            for i, word in enumerate(words, 1):
                output += f'   {i}. {word}\n'
        else:
            output += '[color=#C9A95A]⚠️ Слов не найдено.[/color]\n'
            combinations = app.word_finder.find_all_combinations(code)
            output += f'\n[b]💡 Комбинации:[/b]\n'
            for combo in combinations[:10]:
                output += f'   {combo}\n'
        
        self.result_label.text = output


class TrainerScreen(Screen):
    """Экран тренажёра"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='← Назад',
            size_hint_x=None,
            width=dp(100),
            background_color=get_color_from_hex(Colors.CARD),
            color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        back_btn.bind(on_release=lambda x: self.manager.go_back())
        header.add_widget(back_btn)
        
        title = Label(
            text='[b]🧠 Тренажёр[/b]',
            markup=True,
            font_size=sp(18),
            color=get_color_from_hex(Colors.PRIMARY)
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Режимы тренировки
        modes = [
            ('📇 Карточки', 'cards'),
            ('🧠 Тест', 'quiz'),
            ('⚡ Блиц', 'blitz'),
        ]
        
        for text, mode in modes:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(60),
                background_color=get_color_from_hex(Colors.CARD),
                color=get_color_from_hex(Colors.TEXT_PRIMARY),
                font_size=sp(16)
            )
            btn.bind(on_release=lambda x, m=mode: self.start_mode(m))
            layout.add_widget(btn)
        
        # Контейнер для контента
        self.content_container = BoxLayout(orientation='vertical', spacing=dp(10))
        layout.add_widget(self.content_container)
        
        self.add_widget(layout)
        
        # Переменные состояния
        self.cards = []
        self.card_index = 0
        self.show_answer = False
        self.quiz = []
        self.quiz_index = 0
        self.quiz_score = 0
    
    def start_mode(self, mode):
        """Запуск режима тренировки"""
        self.content_container.clear_widgets()
        
        if mode == 'cards':
            self.show_cards_mode()
        elif mode == 'quiz':
            self.show_quiz_mode()
        elif mode == 'blitz':
            self.show_blitz_mode()
    
    def show_cards_mode(self):
        """Режим карточек"""
        app = App.get_running_app()
        self.cards = app.trainer.generate_flashcards()
        self.card_index = 0
        self.show_answer = False
        
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        # Карточка
        self.card_question = Label(
            text='',
            font_size=sp(18),
            color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_y=None,
            height=dp(100),
            markup=True
        )
        layout.add_widget(self.card_question)
        
        self.card_answer = Label(
            text='',
            font_size=sp(16),
            color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(80),
            markup=True
        )
        layout.add_widget(self.card_answer)
        
        self.card_hint = Label(
            text='',
            font_size=sp(12),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            size_hint_y=None,
            height=dp(50),
            markup=True
        )
        layout.add_widget(self.card_hint)
        
        # Кнопки
        btn_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        prev_btn = Button(text='← Назад', background_color=get_color_from_hex(Colors.CARD))
        prev_btn.bind(on_release=lambda x: self.prev_card())
        btn_layout.add_widget(prev_btn)
        
        self.toggle_btn = Button(text='👁 Показать', background_color=get_color_from_hex(Colors.PRIMARY))
        self.toggle_btn.bind(on_release=lambda x: self.toggle_answer())
        btn_layout.add_widget(self.toggle_btn)
        
        next_btn = Button(text='Вперёд →', background_color=get_color_from_hex(Colors.CARD))
        next_btn.bind(on_release=lambda x: self.next_card())
        btn_layout.add_widget(next_btn)
        
        layout.add_widget(btn_layout)
        
        self.content_container.add_widget(layout)
        self.show_card(0)
    
    def show_card(self, index):
        """Показать карточку"""
        if not self.cards or index < 0 or index >= len(self.cards):
            return
        
        self.card_index = index
        card = self.cards[index]
        
        self.card_question.text = f'[b]❓ {card["question"]}[/b]'
        self.card_answer.text = f'[b]✅ {card["answer"]}[/b]' if self.show_answer else ''
        self.card_hint.text = f'💡 {card["hint"]}'
        self.toggle_btn.text = '🙁 Скрыть' if self.show_answer else '👁 Показать'
    
    def toggle_answer(self):
        """Показать/скрыть ответ"""
        self.show_answer = not self.show_answer
        self.show_card(self.card_index)
    
    def next_card(self):
        """Следующая карточка"""
        if self.card_index < len(self.cards) - 1:
            self.show_answer = False
            self.show_card(self.card_index + 1)
    
    def prev_card(self):
        """Предыдущая карточка"""
        if self.card_index > 0:
            self.show_answer = False
            self.show_card(self.card_index - 1)
    
    def show_quiz_mode(self):
        """Режим теста"""
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        info = Label(
            text='[b]🧠 Блиц-тест[/b]\n\n'
                 '• Выберите правильный ответ\n'
                 '• В конце — статистика\n\n'
                 'Выберите количество вопросов:',
            font_size=sp(14),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            markup=True,
            size_hint_y=None,
            height=dp(150)
        )
        layout.add_widget(info)
        
        # Выбор количества вопросов
        count_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        self.quiz_count = 20
        for count in [10, 20, 50]:
            btn = Button(
                text=str(count),
                background_color=get_color_from_hex(Colors.CARD),
                color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
            btn.bind(on_release=lambda x, c=count: self.start_quiz(c))
            count_layout.add_widget(btn)
        
        layout.add_widget(count_layout)
        self.content_container.add_widget(layout)
    
    def start_quiz(self, count):
        """Начать тест"""
        app = App.get_running_app()
        self.quiz = app.trainer.generate_quiz(count, blitz_mode=True)
        self.quiz_index = 0
        self.quiz_score = 0
        
        self.content_container.clear_widgets()
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Показать вопрос теста"""
        if self.quiz_index >= len(self.quiz):
            self.show_quiz_results()
            return
        
        q = self.quiz[self.quiz_index]
        
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        # Вопрос
        question_label = Label(
            text=f'Вопрос {self.quiz_index + 1}/{len(self.quiz)}\n\n{q["question"]}',
            font_size=sp(16),
            color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_y=None,
            height=dp(100),
            markup=True
        )
        layout.add_widget(question_label)
        
        # Варианты ответов
        options = q.get('options', [q['correct_answer']])
        random.shuffle(options)
        options = options[:4]
        
        for option in options:
            btn = Button(
                text=str(option),
                size_hint_y=None,
                height=dp(50),
                background_color=get_color_from_hex(Colors.CARD),
                color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
            btn.bind(on_release=lambda x, opt=option: self.check_quiz_answer(opt, q))
            layout.add_widget(btn)
        
        self.content_container.clear_widgets()
        self.content_container.add_widget(layout)
    
    def check_quiz_answer(self, selected, question):
        """Проверить ответ теста"""
        self.content_container.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        if selected == question['correct_answer']:
            self.quiz_score += 1
            result_text = '[color=#5A8F7A][b]✅ Верно![/b][/color]'
        else:
            result_text = f'[color=#B96A6A][b]❌ Правильно: {question["correct_answer"]}[/b][/color]'
        
        result_label = Label(
            text=result_text,
            font_size=sp(18),
            markup=True,
            size_hint_y=None,
            height=dp(80)
        )
        layout.add_widget(result_label)
        
        next_btn = Button(
            text='Следующий вопрос →',
            background_color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(50)
        )
        next_btn.bind(on_release=lambda x: self.next_quiz_question())
        layout.add_widget(next_btn)
        
        self.content_container.add_widget(layout)
    
    def next_quiz_question(self):
        """Следующий вопрос"""
        self.quiz_index += 1
        self.show_quiz_question()
    
    def show_quiz_results(self):
        """Показать результаты теста"""
        self.content_container.clear_widgets()
        
        percentage = self.quiz_score / len(self.quiz) * 100
        
        if percentage == 100:
            emoji, msg = "🏆", "Отлично! Вы мастер ОЦБК!"
        elif percentage >= 80:
            emoji, msg = "👍", "Хороший результат!"
        elif percentage >= 60:
            emoji, msg = "👌", "Неплохо!"
        else:
            emoji, msg = "📚", "Стоит повторить"
        
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        result_label = Label(
            text=f'[b]{emoji} {msg}[/b]\n\n'
                 f'Правильных: {self.quiz_score} из {len(self.quiz)}\n'
                 f'Процент: {percentage:.0f}%',
            font_size=sp(18),
            color=get_color_from_hex(Colors.PRIMARY),
            markup=True,
            size_hint_y=None,
            height=dp(200)
        )
        layout.add_widget(result_label)
        
        btn_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        retry_btn = Button(
            text='🔄 Ещё раз',
            background_color=get_color_from_hex(Colors.PRIMARY)
        )
        retry_btn.bind(on_release=lambda x: self.show_quiz_mode())
        btn_layout.add_widget(retry_btn)
        
        cards_btn = Button(
            text='📇 Карточки',
            background_color=get_color_from_hex(Colors.CARD)
        )
        cards_btn.bind(on_release=lambda x: self.show_cards_mode())
        btn_layout.add_widget(cards_btn)
        
        layout.add_widget(btn_layout)
        self.content_container.add_widget(layout)
    
    def show_blitz_mode(self):
        """Режим блица"""
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        info = Label(
            text='[b]⚡ Блиц-опрос[/b]\n\n'
                 '• Быстрое декодирование слов\n'
                 '• Выберите правильный ответ\n\n'
                 'Выберите количество вопросов:',
            font_size=sp(14),
            color=get_color_from_hex(Colors.TEXT_SECONDARY),
            markup=True,
            size_hint_y=None,
            height=dp(150)
        )
        layout.add_widget(info)
        
        # Выбор количества вопросов
        count_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        for count in [10, 50, 100]:
            btn = Button(
                text=str(count),
                background_color=get_color_from_hex(Colors.CARD),
                color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
            btn.bind(on_release=lambda x, c=count: self.start_blitz(c))
            count_layout.add_widget(btn)
        
        layout.add_widget(count_layout)
        self.content_container.add_widget(layout)
    
    def start_blitz(self, count):
        """Начать блиц"""
        app = App.get_running_app()
        self.quiz = app.trainer.generate_blitz(count)
        self.quiz_index = 0
        self.quiz_score = 0
        
        self.content_container.clear_widgets()
        self.show_blitz_question()
    
    def show_blitz_question(self):
        """Показать вопрос блица"""
        if self.quiz_index >= len(self.quiz):
            self.show_quiz_results()
            return
        
        q = self.quiz[self.quiz_index]
        
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        # Вопрос
        question_label = Label(
            text=f'Вопрос {self.quiz_index + 1}/{len(self.quiz)}\n\n{q["question"]}',
            font_size=sp(16),
            color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_y=None,
            height=dp(100),
            markup=True
        )
        layout.add_widget(question_label)
        
        # Варианты ответов
        options = q.get('options', [q['correct_answer']])
        random.shuffle(options)
        options = options[:4]
        
        for option in options:
            btn = Button(
                text=str(option),
                size_hint_y=None,
                height=dp(50),
                background_color=get_color_from_hex(Colors.CARD),
                color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
            btn.bind(on_release=lambda x, opt=option: self.check_blitz_answer(opt, q))
            layout.add_widget(btn)
        
        self.content_container.clear_widgets()
        self.content_container.add_widget(layout)
    
    def check_blitz_answer(self, selected, question):
        """Проверить ответ блица"""
        self.content_container.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        if selected == question['correct_answer']:
            self.quiz_score += 1
            result_text = '[color=#5A8F7A][b]✅ Верно![/b][/color]'
        else:
            result_text = f'[color=#B96A6A][b]❌ Правильно: {question["correct_answer"]}[/b][/color]'
        
        result_label = Label(
            text=result_text,
            font_size=sp(18),
            markup=True,
            size_hint_y=None,
            height=dp(80)
        )
        layout.add_widget(result_label)
        
        next_btn = Button(
            text='Следующий →',
            background_color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(50)
        )
        next_btn.bind(on_release=lambda x: self.next_blitz_question())
        layout.add_widget(next_btn)
        
        self.content_container.add_widget(layout)
    
    def next_blitz_question(self):
        """Следующий вопрос блица"""
        self.quiz_index += 1
        self.show_blitz_question()


if __name__ == '__main__':
    OCBKApp().run()
