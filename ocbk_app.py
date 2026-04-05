"""
ОЦБК — GUI приложение с современным дизайном
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ocbk_app import OCBKEncoder, WordFinder, OCBKTrainer, OCBK_TABLE
import random


class ModernStyle:
    """Современная цветовая схема (Dashboard в стиле ClynHealth)"""
    # Основные цвета фона (мягкие, низкий контраст)
    BG_DARK = '#121218'       # Мягкий тёмный
    BG_MEDIUM = '#1a1a24'     # Панель (чуть светлее)
    BG_LIGHT = '#242430'      # Карточка (ещё светлее)
    BG_ELEVATED = '#2d2d3a'   # Приподнятые элементы
    
    # Градиентные акценты (приглушённый синий)
    ACCENT = '#5b7c99'        # Мягкий сине-серый
    ACCENT_HOVER = '#6b8ca9'  # Чуть светлее
    ACCENT_SOFT = '#4a5a6a'   # Мягкий акцент для границ
    
    # Статусы (приглушённые)
    SUCCESS = '#5a8f7a'       # Мягкий зелёный
    WARNING = '#c9a95a'       # Мягкий жёлтый
    ERROR = '#b96a6a'         # Мягкий красный
    
    # Текст (пониженная контрастность)
    TEXT_PRIMARY = '#d0d0d8'      # Мягкий белый
    TEXT_SECONDARY = '#8890a0'    # Приглушённый серо-синий
    TEXT_MUTED = '#606878'        # Тихий текст
    
    # Границы (очень мягкие)
    BORDER = '#2a2a38'        # Едва заметная
    BORDER_SOFT = '#323242'   # Мягкая граница
    BORDER_ACTIVE = '#4a5a6a' # Акцентная граница


class OCBKApp:
    """Графический интерфейс с современным дизайном"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ОЦБК — Цифро-Буквенная Кодировка")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=ModernStyle.BG_DARK)

        # Настройка прозрачности и стиля окна (для Windows 10/11)
        try:
            self.root.attributes('-alpha', 0.98)
        except:
            pass

        self._setup_styles()

        self.encoder = OCBKEncoder()
        self.word_finder = WordFinder()
        self.trainer = OCBKTrainer()

        self._create_widgets()
    
    def _setup_styles(self):
        """Настройка современных стилей (мягкий Dashboard)"""
        style = ttk.Style()
        style.theme_use('clam')

        # Фон
        style.configure('TFrame', background=ModernStyle.BG_DARK)
        style.configure('TLabel', background=ModernStyle.BG_DARK,
                       foreground=ModernStyle.TEXT_PRIMARY,
                       font=('Segoe UI', 11))
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'),
                       foreground=ModernStyle.ACCENT)
        style.configure('Heading.TLabel', font=('Segoe UI', 13, 'bold'),
                       foreground=ModernStyle.TEXT_PRIMARY)

        # Кнопки с мягким акцентом
        style.configure('TButton', font=('Segoe UI', 10, 'bold'),
                       padding=14, foreground=ModernStyle.TEXT_PRIMARY)
        style.map('TButton', 
                 background=[('active', ModernStyle.ACCENT_HOVER), ('!active', ModernStyle.ACCENT_SOFT)],
                 foreground=[('active', ModernStyle.TEXT_PRIMARY)])

        # Поля ввода
        style.configure('TEntry', fieldbackground=ModernStyle.BG_LIGHT,
                       foreground=ModernStyle.TEXT_PRIMARY,
                       padding=14, insertcolor=ModernStyle.ACCENT,
                       bordercolor=ModernStyle.BORDER_SOFT,
                       lightcolor=ModernStyle.BORDER_SOFT,
                       darkcolor=ModernStyle.BORDER_SOFT)

        # Notebook (вкладки)
        style.configure('TNotebook', background=ModernStyle.BG_DARK, padding=8)
        style.configure('TNotebook.Tab', padding=[30, 14],
                       font=('Segoe UI', 10, 'bold'),
                       background=ModernStyle.BG_MEDIUM,
                       foreground=ModernStyle.TEXT_SECONDARY,
                       bordercolor=ModernStyle.BORDER)
        style.map('TNotebook.Tab',
                 background=[('selected', ModernStyle.BG_LIGHT)],
                 foreground=[('selected', ModernStyle.ACCENT)],
                 bordercolor=[('selected', ModernStyle.BORDER_ACTIVE)])

        # Treeview (таблица)
        style.configure('Treeview', background=ModernStyle.BG_LIGHT,
                       foreground=ModernStyle.TEXT_PRIMARY,
                       fieldbackground=ModernStyle.BG_LIGHT,
                       rowheight=38, bordercolor=ModernStyle.BORDER,
                       lightcolor=ModernStyle.BORDER)
        style.configure('Treeview.Heading', background=ModernStyle.BG_MEDIUM,
                       foreground=ModernStyle.ACCENT,
                       font=('Segoe UI', 10, 'bold'),
                       bordercolor=ModernStyle.BORDER)

        # Progressbar с мягким цветом
        style.configure('TProgressbar', background=ModernStyle.ACCENT_SOFT,
                       troughcolor=ModernStyle.BG_MEDIUM,
                       bordercolor=ModernStyle.BORDER,
                       lightcolor=ModernStyle.ACCENT_SOFT,
                       darkcolor=ModernStyle.ACCENT)

        # LabelFrame (карточки)
        style.configure('TLabelframe', background=ModernStyle.BG_MEDIUM,
                       foreground=ModernStyle.TEXT_SECONDARY,
                       bordercolor=ModernStyle.BORDER_SOFT)
        style.configure('TLabelframe.Label', background=ModernStyle.BG_MEDIUM,
                       foreground=ModernStyle.TEXT_SECONDARY,
                       font=('Segoe UI', 10, 'bold'))
    
    def _create_widgets(self):
        """Создать элементы интерфейса"""
        # Заголовок
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=40, pady=(20, 10))

        # Логотип/название
        title_container = ttk.Frame(header_frame)
        title_container.pack(side='left')
        
        ttk.Label(title_container, text="🎯 ОЦБК",
                 style='Title.TLabel').pack(side='left')
        ttk.Label(title_container, text="| Цифро-Буквенная Кодировка",
                 style='TLabel',
                 foreground=ModernStyle.TEXT_SECONDARY).pack(side='left', padx=15)
        
        # Мягкая разделительная линия
        separator = tk.Frame(self.root, height=1, bg=ModernStyle.BORDER)
        separator.pack(fill='x', padx=40, pady=(5, 10))

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Вкладка 1: Таблица
        tab_table = ttk.Frame(self.notebook)
        self.notebook.add(tab_table, text="📊 Таблица")
        self._create_table_tab(tab_table)
        
        # Вкладка 2: Кодирование
        tab_encode = ttk.Frame(self.notebook)
        self.notebook.add(tab_encode, text="🔤 Кодирование")
        self._create_encode_tab(tab_encode)
        
        # Вкладка 3: Декодирование
        tab_decode = ttk.Frame(self.notebook)
        self.notebook.add(tab_decode, text="🔢 Декодирование")
        self._create_decode_tab(tab_decode)
        
        # Вкладка 4: Поиск слов
        tab_search = ttk.Frame(self.notebook)
        self.notebook.add(tab_search, text="🔍 Поиск слов")
        self._create_search_tab(tab_search)
        
        # Вкладка 5: Тренажёр
        tab_trainer = ttk.Frame(self.notebook)
        self.notebook.add(tab_trainer, text="🧠 Тренажёр")
        self._create_trainer_tab(tab_trainer)
    
    def _create_table_tab(self, parent):
        """Вкладка с таблицей"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="📊 Таблица ОЦБК", 
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 15))
        
        # Таблица
        table_frame = ttk.LabelFrame(container, text="Соответствие цифр и букв")
        table_frame.pack(fill='both', expand=True)
        
        columns = ('digit', 'col1', 'col2', 'anchor')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        tree.heading('digit', text='Цифра')
        tree.heading('col1', text='Колонка 1 (Интуитивная)')
        tree.heading('col2', text='Колонка 2 (Компенсационная)')
        tree.heading('anchor', text='Якорь для памяти')
        
        tree.column('digit', width=80, anchor='center')
        tree.column('col1', width=180, anchor='center')
        tree.column('col2', width=200, anchor='center')
        tree.column('anchor', width=450)
        
        for digit in sorted(OCBK_TABLE.keys()):
            m = OCBK_TABLE[digit]
            tree.insert('', 'end', values=(digit, f"{m.col1}", f"{m.col2}", m.anchor))
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _create_encode_tab(self, parent):
        """Вкладка кодирования"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="🔤 Кодирование числа", 
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 15))
        
        input_card = ttk.LabelFrame(container, text="Введите число")
        input_card.pack(fill='x', pady=(0, 15))
        
        input_frame = ttk.Frame(input_card)
        input_frame.pack(fill='x', padx=15, pady=15)
        
        self.encode_entry = ttk.Entry(input_frame, font=('Segoe UI', 13))
        self.encode_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.encode_entry.bind('<Return>', lambda e: self._do_encode())
        
        ttk.Button(input_frame, text="Закодировать", 
                  command=self._do_encode).pack(side='left')
        
        result_card = ttk.LabelFrame(container, text="Результат")
        result_card.pack(fill='both', expand=True)
        
        self.encode_result = scrolledtext.ScrolledText(result_card,
                                                       font=('Consolas', 10),
                                                       bg=ModernStyle.BG_LIGHT,
                                                       fg=ModernStyle.TEXT_PRIMARY,
                                                       borderwidth=1,
                                                       relief='flat',
                                                       padx=15, pady=15,
                                                       insertbackground=ModernStyle.ACCENT,
                                                       selectbackground=ModernStyle.ACCENT,
                                                       selectforeground=ModernStyle.TEXT_PRIMARY)
        self.encode_result.pack(fill='both', expand=True, padx=10, pady=10)
    
    def _do_encode(self):
        number = self.encode_entry.get().strip()
        if not number.isdigit():
            messagebox.showerror("Ошибка", "Введите корректное число!")
            return
        
        encoded = self.encoder.encode_number(number)
        pattern = self.encoder.get_pattern(number)
        words = self.word_finder.find_words_for_code(number, max_results=10)
        combinations = self.word_finder.find_all_combinations(number)
        
        result = f"📝 Число: {number}\n"
        result += f"📝 Шаблон: {pattern}\n\n"
        result += f"📝 Буквы:\n"
        for digit, letters in encoded:
            m = OCBK_TABLE[digit]
            result += f"   {digit} → {m.col1} / {m.col2}\n"
        
        result += f"\n💡 Комбинации ({len(combinations)}):\n"
        for i, combo in enumerate(combinations[:20], 1):
            result += f"   {i}. {combo}\n"
        
        if words:
            result += f"\n✅ Слова: {', '.join(words)}"
        else:
            result += f"\n⚠️ Слов не найдено. Придумайте по шаблону {pattern}!"
        
        self.encode_result.delete('1.0', 'end')
        self.encode_result.insert('1.0', result)
    
    def _create_decode_tab(self, parent):
        """Вкладка декодирования"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="🔢 Декодирование слова", 
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 15))
        
        input_card = ttk.LabelFrame(container, text="Введите слово или фразу")
        input_card.pack(fill='x', pady=(0, 15))
        
        input_frame = ttk.Frame(input_card)
        input_frame.pack(fill='x', padx=15, pady=15)
        
        self.decode_entry = ttk.Entry(input_frame, font=('Segoe UI', 13))
        self.decode_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.decode_entry.bind('<Return>', lambda e: self._do_decode())
        
        ttk.Button(input_frame, text="Декодировать", 
                  command=self._do_decode).pack(side='left')
        
        result_card = ttk.LabelFrame(container, text="Результат")
        result_card.pack(fill='both', expand=True)
        
        self.decode_result = scrolledtext.ScrolledText(result_card,
                                                       font=('Consolas', 10),
                                                       bg=ModernStyle.BG_LIGHT,
                                                       fg=ModernStyle.TEXT_PRIMARY,
                                                       borderwidth=1,
                                                       relief='flat',
                                                       padx=15, pady=15,
                                                       insertbackground=ModernStyle.ACCENT,
                                                       selectbackground=ModernStyle.ACCENT,
                                                       selectforeground=ModernStyle.TEXT_PRIMARY)
        self.decode_result.pack(fill='both', expand=True, padx=10, pady=10)
    
    def _do_decode(self):
        phrase = self.decode_entry.get().strip()
        if not phrase:
            messagebox.showerror("Ошибка", "Введите текст!")
            return
        
        result = self.encoder.decode_phrase(phrase)
        output = f"📝 Фраза: {phrase}\n\n📝 Декодирование:\n"
        
        for word, code in result:
            output += f"   {word} → {code}\n"
        
        full_code = ''.join([code for _, code in result])
        if full_code:
            output += f"\n💡 Полный код: {full_code}"
            words = self.word_finder.find_words_for_code(full_code, max_results=5)
            if words:
                output += f"\n💡 Другие слова: {', '.join(words)}"
        
        self.decode_result.delete('1.0', 'end')
        self.decode_result.insert('1.0', output)
    
    def _create_search_tab(self, parent):
        """Вкладка поиска слов"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="🔍 Поиск слов по коду", 
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 15))
        
        input_card = ttk.LabelFrame(container, text="Введите код")
        input_card.pack(fill='x', pady=(0, 15))
        
        input_frame = ttk.Frame(input_card)
        input_frame.pack(fill='x', padx=15, pady=15)
        
        self.search_entry = ttk.Entry(input_frame, font=('Segoe UI', 13))
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self._do_search())
        
        ttk.Button(input_frame, text="Найти слова", 
                  command=self._do_search).pack(side='left')
        
        result_card = ttk.LabelFrame(container, text="Результаты")
        result_card.pack(fill='both', expand=True)
        
        self.search_result = scrolledtext.ScrolledText(result_card,
                                                       font=('Consolas', 10),
                                                       bg=ModernStyle.BG_LIGHT,
                                                       fg=ModernStyle.TEXT_PRIMARY,
                                                       borderwidth=1,
                                                       relief='flat',
                                                       padx=15, pady=15,
                                                       insertbackground=ModernStyle.ACCENT,
                                                       selectbackground=ModernStyle.ACCENT,
                                                       selectforeground=ModernStyle.TEXT_PRIMARY)
        self.search_result.pack(fill='both', expand=True, padx=10, pady=10)
    
    def _do_search(self):
        code = self.search_entry.get().strip()
        if not code.isdigit():
            messagebox.showerror("Ошибка", "Введите корректный код!")
            return
        
        words = self.word_finder.find_words_for_code(code, max_results=50)
        pattern = self.encoder.get_pattern(code)
        
        output = f"📝 Код: {code}\n📝 Шаблон: {pattern}\n\n"
        
        if words:
            output += f"✅ Найдено: {len(words)}\n\n"
            for i, word in enumerate(words, 1):
                output += f"   {i}. {word}\n"
        else:
            output += "⚠️ Слов не найдено.\n"
            combinations = self.word_finder.find_all_combinations(code)
            output += f"💡 Комбинации:\n"
            for combo in combinations[:10]:
                output += f"   {combo}\n"
        
        self.search_result.delete('1.0', 'end')
        self.search_result.insert('1.0', output)
    
    def _create_trainer_tab(self, parent):
        """Вкладка тренажёра"""
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="🧠 Тренажёр", 
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 10))
        
        mode_frame = ttk.Frame(container)
        mode_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Button(mode_frame, text="📇 Карточки",
                  command=self._show_cards_mode).pack(side='left', padx=5)
        ttk.Button(mode_frame, text="🧠 Тест",
                  command=self._show_quiz_mode).pack(side='left', padx=5)
        ttk.Button(mode_frame, text="⚡ Блиц",
                  command=self._show_blitz_mode).pack(side='left', padx=5)
        ttk.Button(mode_frame, text="✍️ Кодирование",
                  command=self._show_encode_mode).pack(side='left', padx=5)
        
        self.trainer_container = ttk.Frame(container)
        self.trainer_container.pack(fill='both', expand=True)
        
        self.card_index = 0
        self.cards = []
        self.show_answer = False
        
        self._show_cards_mode()
    
    def _clear_container(self):
        for widget in self.trainer_container.winfo_children():
            widget.destroy()
    
    def _show_cards_mode(self):
        self._clear_container()
        
        card_frame = ttk.LabelFrame(self.trainer_container, text="📇 Карточки")
        card_frame.pack(fill='both', expand=True)
        
        ttk.Label(card_frame, text="💡 Просматривайте карточки, пытайтесь вспомнить ответ",
                 foreground=ModernStyle.TEXT_SECONDARY).pack(padx=10, pady=5)
        
        self.card_index = 0
        self.cards = self.trainer.generate_flashcards()
        self.show_answer = False
        
        self.card_question = ttk.Label(card_frame, text="", 
                                       font=('Segoe UI', 14, 'bold'),
                                       wraplength=700, justify='center')
        self.card_question.pack(padx=20, pady=30)
        
        self.card_answer = ttk.Label(card_frame, text="", 
                                     font=('Segoe UI', 12),
                                     wraplength=700, foreground=ModernStyle.ACCENT)
        self.card_answer.pack(padx=20, pady=10)
        
        self.card_hint = ttk.Label(card_frame, text="", 
                                   font=('Segoe UI', 10, 'italic'),
                                   foreground=ModernStyle.TEXT_SECONDARY)
        self.card_hint.pack(padx=20, pady=10)
        
        btn_frame = ttk.Frame(card_frame)
        btn_frame.pack(padx=20, pady=20)
        
        ttk.Button(btn_frame, text="← Назад", 
                  command=self._prev_card).pack(side='left', padx=10)
        self.toggle_btn = ttk.Button(btn_frame, text="👁 Показать ответ", 
                                    command=self._toggle_answer)
        self.toggle_btn.pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Вперёд →", 
                  command=self._next_card).pack(side='left', padx=10)
        
        self.card_counter = ttk.Label(btn_frame, text="1 / " + str(len(self.cards)))
        self.card_counter.pack(side='left', padx=20)
        
        self._show_card(0)
    
    def _show_card(self, index):
        if not self.cards or index < 0 or index >= len(self.cards):
            return
        
        self.card_index = index
        card = self.cards[index]
        
        self.card_question.config(text=f"❓ {card['question']}")
        self.card_answer.config(text=f"✅ {card['answer']}" if self.show_answer else "")
        self.card_hint.config(text=f"💡 {card['hint']}")
        self.card_counter.config(text=f"{index + 1} / {len(self.cards)}")
        
        self.toggle_btn.config(text="🙁 Скрыть ответ" if self.show_answer else "👁 Показать ответ")
    
    def _toggle_answer(self):
        self.show_answer = not self.show_answer
        self._show_card(self.card_index)
    
    def _next_card(self):
        if self.card_index < len(self.cards) - 1:
            self.show_answer = False
            self._show_card(self.card_index + 1)
    
    def _prev_card(self):
        if self.card_index > 0:
            self.show_answer = False
            self._show_card(self.card_index - 1)

    def _show_encode_mode(self):
        """Режим кодирования - даётся число, нужно ввести слово"""
        self._clear_container()

        encode_frame = ttk.LabelFrame(self.trainer_container, text="✍️ Кодирование")
        encode_frame.pack(fill='both', expand=True)

        info_text = (
            "✍️ Правила:\n"
            "• Вам дано число - закодируйте его в слово или словосочетание\n"
            "• Используйте буквы из таблицы ОЦБК\n"
            "• Можно включить подсказки (буквы для каждой цифры)\n\n"
            "📝 Пример: 374 → ТЩЧ (Трещина, Трещотка)"
        )
        ttk.Label(encode_frame, text=info_text, justify='left').pack(padx=20, pady=15, anchor='w')

        ttk.Button(encode_frame, text="▶ Начать",
                  command=self._start_encode).pack(pady=20)
    
    def _start_encode(self):
        """Начать режим кодирования"""
        self._clear_container()

        import random
        digits = list(OCBK_TABLE.keys())
        
        # Генерируем случайное число (2-5 цифр)
        code_length = random.randint(2, 5)
        self.encode_code = ''.join(random.choices(digits, k=code_length))
        self.encode_hints_on = False
        self.encode_combos_on = False
        self.encode_score = 0
        self.encode_total = 0

        encode_frame = ttk.Frame(self.trainer_container)
        encode_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Прогресс
        ttk.Label(encode_frame, text="Прогресс:").pack(anchor='w')
        self.encode_progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(encode_frame, variable=self.encode_progress_var,
                                       maximum=10, mode='determinate',
                                       length=400)
        progress_bar.pack(fill='x', pady=5)

        # Число для кодирования
        self.encode_code_label = ttk.Label(encode_frame, text="",
                                           font=('Segoe UI', 18, 'bold'),
                                           foreground=ModernStyle.ACCENT)
        self.encode_code_label.pack(pady=20)

        # Подсказки (буквы для цифр)
        self.encode_hint_label = ttk.Label(encode_frame, text="",
                                          font=('Segoe UI', 12),
                                          foreground=ModernStyle.TEXT_SECONDARY)
        self.encode_hint_label.pack(pady=5)

        # Кнопки подсказок в ряд
        hint_frame = ttk.Frame(encode_frame)
        hint_frame.pack(pady=5)
        
        self.encode_hint_btn = ttk.Button(hint_frame, text="💡 Показать подсказки",
                                         command=self._toggle_encode_hint)
        self.encode_hint_btn.pack(side='left', padx=5)
        
        self.encode_combo_btn = ttk.Button(hint_frame, text="🔤 Показать комбинации букв",
                                          command=self._toggle_encode_combo)
        self.encode_combo_btn.pack(side='left', padx=5)
        
        # Метка для комбинаций
        self.encode_combo_label = ttk.Label(encode_frame, text="",
                                           font=('Segoe UI', 11),
                                           foreground=ModernStyle.TEXT_SECONDARY,
                                           wraplength=700)
        self.encode_combo_label.pack(pady=5)

        # Поле ввода
        input_frame = ttk.Frame(encode_frame)
        input_frame.pack(pady=15, fill='x')

        ttk.Label(input_frame, text="Ваше слово:").pack(side='left', padx=5)
        self.encode_entry = ttk.Entry(input_frame, font=('Segoe UI', 14))
        self.encode_entry.pack(side='left', padx=10, fill='x', expand=True)
        self.encode_entry.bind('<Return>', lambda e: self._check_encode_answer())

        # Кнопки
        btn_frame = ttk.Frame(encode_frame)
        btn_frame.pack(pady=10)

        self.encode_check_btn = ttk.Button(btn_frame, text="✓ Ответить",
                                          command=self._check_encode_answer)
        self.encode_check_btn.pack(side='left', padx=10)

        self.encode_next_btn = ttk.Button(btn_frame, text="Следующее →",
                                         command=self._next_encode_question)
        self.encode_next_btn.pack(side='left', padx=10)
        self.encode_next_btn.config(state='disabled')

        # Результат
        self.encode_result = ttk.Label(encode_frame, text="",
                                      font=('Segoe UI', 12),
                                      wraplength=700)
        self.encode_result.pack(pady=15)

        # Счёт
        self.encode_score_label = ttk.Label(encode_frame, text="Правильно: 0 / 0",
                                           font=('Segoe UI', 11),
                                           foreground=ModernStyle.TEXT_SECONDARY)
        self.encode_score_label.pack(pady=5)

        self._show_encode_question()
    
    def _show_encode_question(self):
        """Показать новое задание на кодирование"""
        import random
        digits = list(OCBK_TABLE.keys())
        
        # Генерируем случайное число (2-5 цифр)
        code_length = random.randint(2, 5)
        self.encode_code = ''.join(random.choices(digits, k=code_length))
        self.encode_hints_on = False
        self.encode_combos_on = False
        self.encode_answered = False

        self.encode_code_label_text = f"Закодируйте число: {self.encode_code}"
        self.encode_code_label.config(text=self.encode_code_label_text)
        
        # Скрываем подсказку и комбинации
        self.encode_hint_label.config(text="")
        self.encode_hint_btn.config(text="💡 Показать подсказки")
        self.encode_combo_label.config(text="")
        self.encode_combo_btn.config(text="🔤 Показать комбинации букв")
        
        # Очищаем поле ввода
        self.encode_entry.config(state='normal')
        self.encode_entry.delete(0, 'end')
        self.encode_entry.focus_set()
        
        # Сбрасываем результат
        self.encode_result.config(text="")
        self.encode_next_btn.config(state='disabled')
        self.encode_check_btn.config(state='normal')
    
    def _toggle_encode_hint(self):
        """Включить/выключить подсказки"""
        self.encode_hints_on = not self.encode_hints_on
        
        if self.encode_hints_on:
            # Показываем буквы для каждой цифры
            hints = []
            for digit in self.encode_code:
                if digit in OCBK_TABLE:
                    m = OCBK_TABLE[digit]
                    hints.append(f"{digit}→{m.col1}/{m.col2}")
            hint_text = " | ".join(hints)
            self.encode_hint_label.config(text=f"Подсказка: {hint_text}")
            self.encode_hint_btn.config(text="🙁 Скрыть подсказки")
        else:
            self.encode_hint_label.config(text="")
            self.encode_hint_btn.config(text="💡 Показать подсказки")
    
    def _toggle_encode_combo(self):
        """Включить/выключить комбинации букв"""
        self.encode_combos_on = not self.encode_combos_on
        
        if self.encode_combos_on:
            # Показываем все комбинации букв в виде сетки
            combinations = self.word_finder.find_all_combinations(self.encode_code)
            if combinations:
                # Формируем сетку: 5 столбцов
                cols = 5
                combo_text = "🔤 Комбинации:\n"
                
                # Разбиваем на строки по 5 элементов
                for i in range(0, len(combinations), cols):
                    row_items = combinations[i:i+cols]
                    # Формируем строку с выравниванием
                    row_text = "   ".join(f"{combo:<10}" for combo in row_items)
                    combo_text += f"   {row_text}\n"
                
                self.encode_combo_label.config(text=combo_text)
                self.encode_combo_btn.config(text="🙁 Скрыть комбинации")
            else:
                self.encode_combo_label.config(text="Нет комбинаций")
                self.encode_combo_btn.config(text="🔤 Показать комбинации букв")
        else:
            self.encode_combo_label.config(text="")
            self.encode_combo_btn.config(text="🔤 Показать комбинации букв")
    
    def _check_encode_answer(self):
        """Проверить ответ кодирования"""
        if self.encode_answered:
            return

        user_word = self.encode_entry.get().strip()
        if not user_word:
            messagebox.showwarning("Внимание", "Введите слово!")
            return

        self.encode_entry.config(state='disabled')
        self.encode_answered = True
        self.encode_check_btn.config(state='disabled')
        self.encode_next_btn.config(state='normal')
        self.encode_total += 1

        # Декодируем слово пользователя
        decoded = self.encoder.decode_word(user_word)
        
        # Ищем альтернативные варианты (слова из словаря)
        # ВАЖНО: проверяем КАЖДОЕ слово что оно декодируется в ТОТ ЖЕ код
        alt_words = []
        for word in self.word_finder.dictionary:
            word_code = self.encoder.decode_word(word)
            # Проверяем ТОЧНОЕ соответствие кода
            if word_code == self.encode_code and word.lower() != user_word.lower():
                alt_words.append(word)
                if len(alt_words) >= 15:
                    break
        
        if decoded == self.encode_code:
            self.encode_score += 1
            result_text = f"✅ Верно! '{user_word.upper()}' → {decoded}"
            
            # Добавляем альтернативные варианты в виде сетки
            if alt_words:
                result_text += f"\n\n📝 Другие слова:\n"
                cols = 5
                for i in range(0, len(alt_words), cols):
                    row_items = alt_words[i:i+cols]
                    row_text = "   ".join(f"{word.upper():<12}" for word in row_items)
                    result_text += f"   {row_text}\n"
            
            self.encode_result.config(text=result_text, foreground=ModernStyle.SUCCESS)
        else:
            # Формируем текст ошибки с альтернативами
            error_text = f"❌ Неверно.\n"
            
            if decoded:
                error_text += f"Ваше слово '{user_word.upper()}' → {decoded}\n"
            else:
                error_text += f"Ваше слово '{user_word.upper()}' не декодируется\n"
            
            error_text += f"\nНужно: {self.encode_code}"
            
            # Добавляем правильные варианты в виде сетки
            if alt_words:
                error_text += f"\n\n📝 Правильные слова:\n"
                cols = 5
                for i in range(0, len(alt_words), cols):
                    row_items = alt_words[i:i+cols]
                    row_text = "   ".join(f"{word.upper():<12}" for word in row_items)
                    error_text += f"   {row_text}\n"
            else:
                # Если слов нет, показываем комбинации букв
                combinations = self.word_finder.find_all_combinations(self.encode_code)
                if combinations and len(combinations) <= 32:  # Показываем только если не слишком много
                    error_text += f"\n\n� Комбинации букв:\n"
                    cols = 5
                    for i in range(0, len(combinations), cols):
                        row_items = combinations[i:i+cols]
                        row_text = "   ".join(f"{combo:<10}" for combo in row_items)
                        error_text += f"   {row_text}\n"
                else:
                    error_text += f"\n\n💡 Шаблон: {self.encoder.get_pattern(self.encode_code)}"
            
            self.encode_result.config(text=error_text, foreground=ModernStyle.ERROR)

        self.encode_score_label.config(text=f"Правильно: {self.encode_score} / {self.encode_total}")
        self.encode_progress_var.set(self.encode_total % 10)
    
    def _next_encode_question(self):
        """Следующее задание"""
        self._show_encode_question()
    
    def _show_quiz_mode(self):
        """Режим блиц-тестирования с вариантами ответов"""
        self._clear_container()

        quiz_frame = ttk.LabelFrame(self.trainer_container, text="🧠 Блиц-тест")
        quiz_frame.pack(fill='both', expand=True)

        info_text = (
            "⚡ Правила:\n"
            "• Вопросы на запоминание соответствий цифр и букв\n"
            "• Выберите правильный ответ из 4-х вариантов\n"
            "• В конце — статистика\n\n"
            "📝 Типы вопросов:\n"
            "• 5 (колонка 1) → П\n"
            "• В → 8\n\n"
            "💡 Для запоминания: проходите тест много раз!"
        )
        ttk.Label(quiz_frame, text=info_text, justify='left').pack(padx=20, pady=15, anchor='w')

        # Выбор количества вопросов
        select_frame = ttk.Frame(quiz_frame)
        select_frame.pack(pady=15)

        ttk.Label(select_frame, text="Количество вопросов:",
                 font=('Segoe UI', 11, 'bold')).pack(side='left', padx=10)

        self.quiz_questions_var = tk.StringVar(value="20")
        question_options = ["10", "20", "50", "100", "200"]
        
        option_menu = ttk.Combobox(select_frame, textvariable=self.quiz_questions_var,
                                   values=question_options, state='readonly',
                                   width=10, font=('Segoe UI', 11))
        option_menu.pack(side='left', padx=10)

        ttk.Button(quiz_frame, text="▶ Начать блиц-тест",
                  command=self._start_quiz).pack(pady=20)
    
    def _start_quiz(self):
        """Начать блиц-тест с выбранным количеством вопросов"""
        self._clear_container()

        # Получаем выбранное количество вопросов
        try:
            num_questions = int(self.quiz_questions_var.get())
        except ValueError:
            num_questions = 20

        # Генерируем вопросы для блиц-теста
        self.quiz = self.trainer.generate_quiz(num_questions, blitz_mode=True)
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_answers = []
        self.answer_checked = False

        quiz_frame = ttk.Frame(self.trainer_container)
        quiz_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(quiz_frame, text="Прогресс:").pack(anchor='w')
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(quiz_frame, variable=self.progress_var,
                                       maximum=len(self.quiz), mode='determinate',
                                       length=400)
        progress_bar.pack(fill='x', pady=5)

        self.q_label = ttk.Label(quiz_frame, text="",
                                 font=('Segoe UI', 14, 'bold'),
                                 wraplength=700, justify='center')
        self.q_label.pack(pady=20)

        # Переменная для вариантов ответов
        self.quiz_var = tk.StringVar()
        self.quiz_options_frame = ttk.Frame(quiz_frame)
        self.quiz_options_frame.pack(pady=10)

        self.quiz_radios = []
        for i in range(4):
            radio = ttk.Radiobutton(self.quiz_options_frame, text="",
                                   variable=self.quiz_var, value="",
                                   command=self._enable_quiz_check)
            radio.pack(pady=5, fill='x', padx=20)
            self.quiz_radios.append(radio)

        self.check_btn = ttk.Button(quiz_frame, text="✓ Проверить",
                                   command=self._check_quiz_answer,
                                   state='disabled')
        self.check_btn.pack(pady=10)
        
        # Кнопка пропуска
        self.skip_btn = ttk.Button(quiz_frame, text="⏭ Пропустить",
                                  command=self._skip_quiz_question)
        self.skip_btn.pack(pady=5)

        self.q_result = ttk.Label(quiz_frame, text="",
                                  font=('Segoe UI', 11),
                                  wraplength=700)
        self.q_result.pack(pady=10)

        self.next_btn = ttk.Button(quiz_frame, text="Следующий вопрос →",
                                  command=self._next_quiz_question)
        self.next_btn.pack(pady=10)
        self.next_btn.config(state='disabled')
        
        # Счётчик вопросов
        self.quiz_counter_label = ttk.Label(quiz_frame, text=f"Вопрос 1 из {len(self.quiz)}",
                                           foreground=ModernStyle.TEXT_SECONDARY)
        self.quiz_counter_label.pack(pady=5)

        self._show_quiz_question()
    
    def _enable_quiz_check(self):
        """Включить кнопку проверки при выборе варианта"""
        if self.quiz_var.get():
            self.check_btn.config(state='normal')
    
    def _show_quiz_question(self):
        """Показать вопрос блиц-теста с вариантами ответов"""
        if self.quiz_index >= len(self.quiz):
            self._show_quiz_results()
            return

        q = self.quiz[self.quiz_index]
        self.progress_var.set(self.quiz_index)
        self.answer_checked = False

        self.q_label.config(text=f"Вопрос {self.quiz_index + 1}/{len(self.quiz)}\n\n{q['question']}")
        self.q_result.config(text="")
        self.next_btn.config(state='disabled')
        self.check_btn.config(state='disabled')
        self.skip_btn.config(state='normal')
        
        # Обновляем счётчик
        self.quiz_counter_label.config(text=f"Вопрос {self.quiz_index + 1} из {len(self.quiz)}")

        # Используем готовые варианты из вопроса
        options = q.get('options', [q['correct_answer']])
        
        # Если вариантов меньше 4, добавляем случайные
        while len(options) < 4:
            digit = random.choice(list(OCBK_TABLE.keys()))
            mapping = OCBK_TABLE[digit]
            if q['type'] == 'digit_to_letter':
                # Добавляем буквы из той же колонки
                if "(колонка 1)" in q['question']:
                    wrong = mapping.col1
                else:
                    wrong = mapping.col2
                if wrong not in options:
                    options.append(wrong)
            else:
                # Добавляем цифры
                if digit not in options:
                    options.append(digit)
        
        # Перемешиваем варианты (правильно!)
        random.shuffle(options)
        options = options[:4]

        self.quiz_var.set("")
        for i, radio in enumerate(self.quiz_radios):
            radio.config(text=options[i], value=options[i], state='normal')
    
    def _check_quiz_answer(self):
        """Проверить ответ в блиц-тесте"""
        if self.answer_checked:
            return

        selected = self.quiz_var.get()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите вариант!")
            return

        q = self.quiz[self.quiz_index]

        # Блокируем все варианты
        for radio in self.quiz_radios:
            radio.config(state='disabled')

        self.answer_checked = True
        self.check_btn.config(state='disabled')
        self.skip_btn.config(state='disabled')
        self.next_btn.config(state='normal')

        if selected == q['correct_answer']:
            self.quiz_score += 1
            self.q_result.config(text="✅ Верно!", foreground=ModernStyle.SUCCESS)
        else:
            self.q_result.config(text=f"❌ Правильно: {q['correct_answer']}",
                                foreground=ModernStyle.ERROR)
        
        self.quiz_answers.append((q['question'], selected, q['correct_answer'], selected == q['correct_answer']))
    
    def _skip_quiz_question(self):
        """Пропустить вопрос (считается как неправильный)"""
        if self.answer_checked:
            return

        q = self.quiz[self.quiz_index]

        # Блокируем все варианты
        for radio in self.quiz_radios:
            radio.config(state='disabled')

        self.answer_checked = True
        self.check_btn.config(state='disabled')
        self.skip_btn.config(state='disabled')
        self.next_btn.config(state='normal')

        self.q_result.config(text=f"⏭ Пропущено. Правильно: {q['correct_answer']}",
                            foreground=ModernStyle.WARNING)
        
        self.quiz_answers.append((q['question'], "Пропущено", q['correct_answer'], False))
    
    def _next_quiz_question(self):
        self.quiz_index += 1
        self._show_quiz_question()
    
    def _show_quiz_results(self):
        self._clear_container()
        
        result_frame = ttk.Frame(self.trainer_container)
        result_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        percentage = self.quiz_score / len(self.quiz) * 100
        
        if percentage == 100:
            emoji, msg = "🏆", "Отлично! Вы мастер ОЦБК!"
        elif percentage >= 80:
            emoji, msg = "👍", "Хороший результат!"
        elif percentage >= 60:
            emoji, msg = "👌", "Неплохо!"
        else:
            emoji, msg = "📚", "Стоит повторить"
        
        ttk.Label(result_frame, text=f"{emoji} {msg}", 
                 font=('Segoe UI', 16, 'bold'),
                 foreground=ModernStyle.ACCENT).pack(pady=20)
        
        stats_text = f"Правильных: {self.quiz_score} из {len(self.quiz)}\nПроцент: {percentage:.0f}%"
        ttk.Label(result_frame, text=stats_text, 
                 font=('Segoe UI', 12)).pack(pady=10)
        
        if self.quiz_answers:
            details_frame = ttk.LabelFrame(result_frame, text="📋 Детали")
            details_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scroll = scrolledtext.ScrolledText(details_frame, height=8,
                                              bg=ModernStyle.BG_LIGHT,
                                              fg=ModernStyle.TEXT_PRIMARY,
                                              borderwidth=1,
                                              relief='flat',
                                              insertbackground=ModernStyle.ACCENT,
                                              selectbackground=ModernStyle.ACCENT,
                                              selectforeground=ModernStyle.TEXT_PRIMARY)
            scroll.pack(fill='both', expand=True, padx=5, pady=5)
            
            for i, (question, user_ans, correct_ans, is_correct) in enumerate(self.quiz_answers, 1):
                status = "✅" if is_correct else "❌"
                detail_text = f"{i}. {status} {question}\nВаш ответ: {user_ans}\nПравильно: {correct_ans}\n\n"
                scroll.insert('end', detail_text)
            
            scroll.config(state='disabled')
        
        btn_frame = ttk.Frame(result_frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="🔄 Ещё раз",
                  command=self._show_quiz_mode).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="📇 Карточки",
                  command=self._show_cards_mode).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="⚡ Блиц",
                  command=self._show_blitz_mode).pack(side='left', padx=10)

    def _show_blitz_mode(self):
        """Режим блиц-опроса с декодированием чисел и слов"""
        self._clear_container()

        blitz_frame = ttk.LabelFrame(self.trainer_container, text="⚡ Блиц")
        blitz_frame.pack(fill='both', expand=True)

        info_text = (
            "⚡ Правила:\n"
            "• Блиц на применение ОЦБК (числа и слова)\n"
            "• Выберите правильный ответ из 4-х вариантов\n"
            "• В конце — статистика\n\n"
            "📝 Типы вопросов:\n"
            "• Закодируйте слово в цифры\n"
            "• Найдите слово для кода\n"
            "• Шаблон согласных для числа"
        )
        ttk.Label(blitz_frame, text=info_text, justify='left').pack(padx=20, pady=15, anchor='w')

        # Выбор количества вопросов
        select_frame = ttk.Frame(blitz_frame)
        select_frame.pack(pady=20)

        ttk.Label(select_frame, text="Количество вопросов:",
                 font=('Segoe UI', 11, 'bold')).pack(side='left', padx=10)

        self.blitz_questions_var = tk.StringVar(value="50")
        question_options = ["10", "50", "100", "200", "500", "1000"]
        
        option_menu = ttk.Combobox(select_frame, textvariable=self.blitz_questions_var,
                                   values=question_options, state='readonly',
                                   width=10, font=('Segoe UI', 11))
        option_menu.pack(side='left', padx=10)

        ttk.Button(blitz_frame, text="🚀 Начать блиц",
                  command=self._start_blitz).pack(pady=20)
    
    def _start_blitz(self):
        """Начать блиц с выбранным количеством вопросов"""
        self._clear_container()

        # Получаем выбранное количество вопросов
        try:
            num_questions = int(self.blitz_questions_var.get())
        except ValueError:
            num_questions = 50

        # Генерируем блиц-вопросы на декодирование
        self.blitz = self.trainer.generate_blitz(num_questions)
        self.blitz_index = 0
        self.blitz_score = 0
        self._blitz_checked = False

        blitz_frame = ttk.Frame(self.trainer_container)
        blitz_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(blitz_frame, text="Прогресс:").pack(anchor='w')
        self.blitz_progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(blitz_frame, variable=self.blitz_progress_var,
                                       maximum=len(self.blitz), mode='determinate',
                                       length=400)
        progress_bar.pack(fill='x', pady=5)

        self.blitz_q_label = ttk.Label(blitz_frame, text="",
                                       font=('Segoe UI', 14, 'bold'),
                                       wraplength=700, justify='center')
        self.blitz_q_label.pack(pady=20)

        self.blitz_var = tk.StringVar()
        self.blitz_options_frame = ttk.Frame(blitz_frame)
        self.blitz_options_frame.pack(pady=10)

        self.blitz_radios = []
        for i in range(4):
            radio = ttk.Radiobutton(self.blitz_options_frame, text="",
                                   variable=self.blitz_var, value="",
                                   command=self._enable_blitz_check)
            radio.pack(pady=5, fill='x', padx=20)
            self.blitz_radios.append(radio)

        self.blitz_check_btn = ttk.Button(blitz_frame, text="✓ Ответить",
                                         command=self._check_blitz_answer)
        self.blitz_check_btn.pack(pady=10)
        
        # Кнопка пропуска для длинных сессий
        self.blitz_skip_btn = ttk.Button(blitz_frame, text="⏭ Пропустить",
                                         command=self._skip_blitz_question)
        self.blitz_skip_btn.pack(pady=5)

        self.blitz_result = ttk.Label(blitz_frame, text="",
                                      font=('Segoe UI', 11))
        self.blitz_result.pack(pady=10)

        self.blitz_next_btn = ttk.Button(blitz_frame, text="Следующий →",
                                        command=self._next_blitz_question)
        self.blitz_next_btn.pack(pady=10)
        self.blitz_next_btn.config(state='disabled')

        # Счётчик текущего вопроса
        self.blitz_counter_label = ttk.Label(blitz_frame, text=f"Вопрос 1 из {len(self.blitz)}",
                                             foreground=ModernStyle.TEXT_SECONDARY)
        self.blitz_counter_label.pack(pady=5)

        self._show_blitz_question()
    
    def _show_blitz_question(self):
        """Показать вопрос блица с вариантами ответов"""
        if self.blitz_index >= len(self.blitz):
            self._show_blitz_results()
            return

        q = self.blitz[self.blitz_index]
        self.blitz_progress_var.set(self.blitz_index)
        self._blitz_checked = False

        self.blitz_q_label.config(text=f"Вопрос {self.blitz_index + 1}/{len(self.blitz)}\n\n{q['question']}")
        self.blitz_result.config(text="")
        self.blitz_next_btn.config(state='disabled')
        self.blitz_check_btn.config(state='normal')
        self.blitz_skip_btn.config(state='normal')
        
        # Обновляем счётчик
        self.blitz_counter_label.config(text=f"Вопрос {self.blitz_index + 1} из {len(self.blitz)}")

        # Используем готовые варианты из вопроса
        options = q.get('options', [q['correct_answer']])
        
        # Если вариантов меньше 4, добавляем случайные
        while len(options) < 4:
            if q['type'] == 'encode_word':
                # Добавляем случайные коды
                wrong_code = str(random.randint(10, 9999))
                if wrong_code not in options:
                    options.append(wrong_code)
            elif q['type'] == 'decode_code':
                # Добавляем случайные слова
                wrong_word = random.choice(self.trainer.word_finder.dictionary)
                if wrong_word not in options:
                    options.append(wrong_word)
            else:
                # Для шаблонов добавляем случайные буквы
                digits = list(OCBK_TABLE.keys())
                wrong_pattern = ''.join(random.choices([OCBK_TABLE[d].col1 for d in digits], k=len(q['correct_answer'])))
                if wrong_pattern not in options:
                    options.append(wrong_pattern)
        
        # Перемешиваем варианты
        random.shuffle(options)
        options = options[:4]

        self.blitz_var.set("")
        for i, radio in enumerate(self.blitz_radios):
            radio.config(text=options[i], value=options[i], state='normal')
    
    def _enable_blitz_check(self):
        self.blitz_check_btn.config(state='normal')
    
    def _check_blitz_answer(self):
        if self._blitz_checked:
            return

        selected = self.blitz_var.get()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите вариант!")
            return

        q = self.blitz[self.blitz_index]

        for radio in self.blitz_radios:
            radio.config(state='disabled')

        self._blitz_checked = True
        self.blitz_check_btn.config(state='disabled')
        self.blitz_skip_btn.config(state='disabled')
        self.blitz_next_btn.config(state='normal')

        if selected == q['correct_answer']:
            self.blitz_score += 1
            self.blitz_result.config(text="✅ Верно!", foreground=ModernStyle.SUCCESS)
        else:
            self.blitz_result.config(text=f"❌ Правильно: {q['correct_answer']}",
                                    foreground=ModernStyle.ERROR)

    def _skip_blitz_question(self):
        """Пропустить текущий вопрос (считается как неправильный)"""
        if self._blitz_checked:
            return

        q = self.blitz[self.blitz_index]

        for radio in self.blitz_radios:
            radio.config(state='disabled')

        self._blitz_checked = True
        self.blitz_check_btn.config(state='disabled')
        self.blitz_skip_btn.config(state='disabled')
        self.blitz_next_btn.config(state='normal')

        self.blitz_result.config(text=f"⏭ Пропущено. Правильно: {q['correct_answer']}",
                                foreground=ModernStyle.WARNING)
    
    def _next_blitz_question(self):
        self.blitz_index += 1
        self._show_blitz_question()
    
    def _show_blitz_results(self):
        self._clear_container()
        
        result_frame = ttk.Frame(self.trainer_container)
        result_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        percentage = self.blitz_score / len(self.blitz) * 100
        
        if percentage >= 90:
            emoji, msg = "⚡🏆", "Молниеносно! Эксперт ОЦБК!"
        elif percentage >= 70:
            emoji, msg = "⚡👍", "Отличная скорость!"
        elif percentage >= 50:
            emoji, msg = "⚡👌", "Хорошо!"
        else:
            emoji, msg = "⚡📚", "Нужно тренироваться"
        
        ttk.Label(result_frame, text=f"{emoji} {msg}", 
                 font=('Segoe UI', 16, 'bold'),
                 foreground=ModernStyle.ACCENT).pack(pady=20)
        
        stats_text = f"Правильных: {self.blitz_score} из {len(self.blitz)}\nПроцент: {percentage:.0f}%"
        ttk.Label(result_frame, text=stats_text, 
                 font=('Segoe UI', 12)).pack(pady=10)
        
        btn_frame = ttk.Frame(result_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="🔄 Ещё блиц", 
                  command=self._start_blitz).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="🧠 Тест", 
                  command=self._show_quiz_mode).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="📇 Карточки", 
                  command=self._show_cards_mode).pack(side='left', padx=10)


def main():
    root = tk.Tk()
    app = OCBKApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
