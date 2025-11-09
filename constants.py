SOUND_FILES = {
    'menu': 'sounds/menu_song.mp3',
    'game': 'sounds/game_song.mp3',
    'attack': 'sounds/attack.mp3',
    'win': 'sounds/win.mp3',
    'lose': 'sounds/lose.mp3',
    'zastavka': 'sounds/zastavrf.mp3'
}

# Константы для размеров и времени
SPLASH_SCREEN_DURATION = 3000
ANIMATION_DURATION = 500
ANIMATION_TIMER_INTERVAL = 30
BOT_TURN_DELAY = 1000
ATTACK_ANIMATION_DELAY = 600

# Размеры окон для разных разрешений
SCREEN_SIZES = {
    "1366x768": {
        "SPLASH_SIZE": (700, 500),
        "MAIN_WINDOW_SIZE": (1200, 700),
        "STATS_DIALOG_SIZE": (900, 550),
        "ENERGY_DIALOG_SIZE": (350, 200),
        "COLOR_DIALOG_SIZE": (500, 400),
        "SETUP_DIALOG_SIZE": (500, 400),
        "ADVANCED_SETTINGS_SIZE": (600, 500),
        "CELL_SIZE": 55,
        "FONT_SIZE_SMALL": 8,
        "FONT_SIZE_MEDIUM": 10,
        "FONT_SIZE_LARGE": 12,
        "FONT_SIZE_TITLE": 14,
        "BUTTON_PADDING": "5px",
        "LAYOUT_SPACING": 6,
        "GROUP_BOX_MARGINS": 6
    },
    "1600x900": {
        "SPLASH_SIZE": (800, 600),
        "MAIN_WINDOW_SIZE": (1400, 800),
        "STATS_DIALOG_SIZE": (1000, 650),
        "ENERGY_DIALOG_SIZE": (400, 250),
        "COLOR_DIALOG_SIZE": (600, 500),
        "SETUP_DIALOG_SIZE": (600, 500),
        "ADVANCED_SETTINGS_SIZE": (700, 600),
        "CELL_SIZE": 65,
        "FONT_SIZE_SMALL": 9,
        "FONT_SIZE_MEDIUM": 11,
        "FONT_SIZE_LARGE": 13,
        "FONT_SIZE_TITLE": 16,
        "BUTTON_PADDING": "6px",
        "LAYOUT_SPACING": 8,
        "GROUP_BOX_MARGINS": 8
    },
    "1920x1080": {
        "SPLASH_SIZE": (900, 700),
        "MAIN_WINDOW_SIZE": (1600, 900),
        "STATS_DIALOG_SIZE": (1200, 800),
        "ENERGY_DIALOG_SIZE": (500, 300),
        "COLOR_DIALOG_SIZE": (700, 600),
        "SETUP_DIALOG_SIZE": (700, 600),
        "ADVANCED_SETTINGS_SIZE": (800, 700),
        "CELL_SIZE": 75,
        "FONT_SIZE_SMALL": 10,
        "FONT_SIZE_MEDIUM": 12,
        "FONT_SIZE_LARGE": 14,
        "FONT_SIZE_TITLE": 18,
        "BUTTON_PADDING": "7px",
        "LAYOUT_SPACING": 9,
        "GROUP_BOX_MARGINS": 9
    },
    "default": {
        "SPLASH_SIZE": (900, 700),
        "MAIN_WINDOW_SIZE": (1400, 900),
        "STATS_DIALOG_SIZE": (1200, 800),
        "ENERGY_DIALOG_SIZE": (500, 300),
        "COLOR_DIALOG_SIZE": (700, 600),
        "SETUP_DIALOG_SIZE": (700, 600),
        "ADVANCED_SETTINGS_SIZE": (800, 700),
        "CELL_SIZE": 80,
        "FONT_SIZE_SMALL": 11,
        "FONT_SIZE_MEDIUM": 14,
        "FONT_SIZE_LARGE": 16,
        "FONT_SIZE_TITLE": 24,
        "BUTTON_PADDING": "8px",
        "LAYOUT_SPACING": 10,
        "GROUP_BOX_MARGINS": 10
    }
}

# Доступные разрешения экрана
AVAILABLE_RESOLUTIONS = ["1366x768", "1600x900", "1920x1080", "Автоопределение"]

# Константы для игрового поля
GRID_SPACING = 2
BOARD_DIMENSION = 8
MIN_DISTANCE_BETWEEN_BASES = 2
MAX_TURNS_DEFAULT = 50
MAX_PLAYERS = 8

# Константы для анимаций
ANIMATION_START_OPACITY = 0.3
ANIMATION_END_OPACITY = 1.0

# Константы для генерации карты
SHAPE_SIZES = {
    "Маленький": 3,
    "Средний": 4,
    "Большой": 5,
    "Огромный": 6
}

# Текстовые константы
TEXTS = {
    "GAME_TITLE": "ВЛИЯНИЕ",
    "GAME_SUBTITLE": "Стратегическая игра",
    "ATTACK_PHASE": "⚔️ Фаза атаки",
    "ENERGY_PHASE": "🎲 Фаза энергии",
    "SELECT_ATTACK": "Выберите клетку для атаки",
    "SELECT_TARGET": "Выберите цель для атаки",
    "ATTACK_COMPLETE": "Атака завершена!",
    "NO_ENERGY": "Нет энергии!",
    "ENERGY_DISTRIBUTED": "Энергия распределена. Завершите ход.",
    "OWN_CELLS_ONLY": "Только в свои клетки!",
    "NOT_ENOUGH_ENERGY": "Недостаточно энергии!",
    "GAME_END": "=== ИГРА ОКОНЧЕНА ===",
    "WINNER": "🏆 Победитель",
    "STATS_TITLE": "📊 Статистика и управление данными",
    "SETTINGS_TITLE": "🎮 НАСТРОЙКИ ИГРЫ",
    "RULES_TITLE": "Правила",
    "ACTIONS_TITLE": "Действия",
    "MENU_TITLE": "Меню",
    "LOG_TITLE": "Журнал",
    "READY_TO_PLAY": "Готов к игре"
}

# Цвета игроков
PLAYER_COLORS = [
    "#4169E1", "#DC143C", "#32CD32", "#9370DB",
    "#FF8C00", "#FFD700", "#FF7F50", "#1E90FF"
]

# Названия форм карт
BOARD_SHAPES = [
    "Квадрат", "Треугольник", "Сердце", "Шестиугольник",
    "Спираль", "Круг", "Крест", "Звезда"
]

# Уровни сложности
DIFFICULTY_LEVELS = ["Лёгкая", "Средняя", "Сложная", "Эксперт"]

# Размеры карт
BOARD_SIZES = ["Маленький", "Средний", "Большой", "Огромный"]

# Достижения
ACHIEVEMENTS = [
    "🎯 Первая победа",
    "⚔️ Захватчик",
    "🏰 Защитник",
    "💎 Коллекционер",
    "🌟 Легенда",
    "🚀 Быстрая победа",
    "🎪 Мастер тактики",
    "🏆 Чемпион"
]

# Правила игры
GAME_RULES = [
    "1. ⚔️ АТАКА: Выберите свою клетку",
    "2. ⚔️ АТАКА: Выберите цель",
    "3. 🎲 ЭНЕРГИЯ: Получите энергию",
    "4. ⏭️ ЗАВЕРШЕНИЕ: Передайте ход"
]

# Цвета для доступных ячеек
CELL_COLORS = {
    "NEUTRAL_BG": "#444444",
    "NEUTRAL_TEXT": "#888",
    "ROAD_BG": "#666666",
    "ROAD_TEXT": "white",
    "BORDER": "1px solid #555",
    "BASE_BORDER": "3px solid #ffd700",
    "TARGET_BORDER": "3px solid #00ff00",
    "ATTACK_BORDER": "3px solid #ff4444",
    "SELECTED_ATTACK_BORDER": "4px solid #ffff00",
    "SELECTED_TARGET_BORDER": "4px solid #00ffff"
}

# Настройки анимации атаки
ATTACK_ANIMATION = {
    "SIZE_FACTOR": 25,
    "ALPHA_FACTOR": 255,
    "PROGRESS_STEP": 0.05,
    "COLOR": (255, 100, 100)
}