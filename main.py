import sys
import random
import math
import sqlite3
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QTextEdit, QGroupBox,
    QMessageBox, QComboBox, QSpinBox, QDialog, QSlider, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QProgressBar, QCheckBox, QRadioButton, QListWidget, QListWidgetItem,
    QSplitter, QToolBar, QStatusBar, QLineEdit, QFormLayout,
    QInputDialog, QFontDialog, QColorDialog
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QSize
from PyQt6.QtGui import QPalette, QColor, QFont, QPainter, QIcon, QPixmap, QAction
import pygame

from config import Config
from settings import Settings
from db_manager import DBManager
from constants import *

# Глобальная переменная для хранения текущих констант экрана
SCREEN_CONSTANTS = Config.get_screen_constants()

# Инициализация звуковой системы
pygame.mixer.init()
sounds = {}

for name, path in SOUND_FILES.items():
    try:
        sounds[name] = pygame.mixer.Sound(path)
    except:
        print(f"Не удалось загрузить звук: {name}")
        pass

# Инициализация звуковой системы
pygame.mixer.init()
sounds = {}

for name, path in SOUND_FILES.items():
    try:
        sounds[name] = pygame.mixer.Sound(path)
    except:
        print(f"Не удалось загрузить звук: {name}")
        pass

# Константы для звуков
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

# размеры окон
SPLASH_SIZE = (900, 700)
MAIN_WINDOW_SIZE = (1400, 900)
STATS_DIALOG_SIZE = (1200, 800)
ENERGY_DIALOG_SIZE = (500, 300)
COLOR_DIALOG_SIZE = (700, 600)
SETUP_DIALOG_SIZE = (700, 600)
ADVANCED_SETTINGS_SIZE = (800, 700)

# Константы для игрового поля
CELL_SIZE = 80
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

# Инициализация звуковой системы
pygame.mixer.init()
sounds = {}

for name, path in SOUND_FILES.items():
    try:
        sounds[name] = pygame.mixer.Sound(path)
    except:
        print(f"Не удалось загрузить звук: {name}")
        pass


def play_sound(sound_name):
    """Воспроизведение звуков и музыки"""
    try:
        if sound_name in ['menu', 'game', 'zastavka']:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            try:
                pygame.mixer.music.load(SOUND_FILES[sound_name])
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            except:
                pass
        elif sound_name in sounds:
            sounds[sound_name].play()
    except Exception as e:
        print(f"Ошибка воспроизведения звука {sound_name}: {e}")


def stop_music():
    """Остановка музыки"""
    try:
        pygame.mixer.music.stop()
    except:
        pass


class TextEditorDialog(QDialog):
    """Простой текстовый редактор для файлов .txt"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Текстовый редактор")
        self.setFixedSize(700, 600)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()

        # Панель инструментов
        toolbar = QHBoxLayout()
        open_btn = QPushButton("📁 Открыть")
        open_btn.clicked.connect(self.open_file)
        save_btn = QPushButton("💾 Сохранить")
        save_btn.clicked.connect(self.save_file)
        toolbar.addWidget(open_btn)
        toolbar.addWidget(save_btn)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Текстовое поле
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("font-size: 12px; background: #1a1a1a; color: white;")
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Успех", "Файл сохранен!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")


class ImageViewerDialog(QDialog):
    """Просмотрщик изображений"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр изображений")
        self.setFixedSize(700, 600)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()

        # Панель инструментов
        toolbar = QHBoxLayout()
        open_btn = QPushButton("📁 Открыть изображение")
        open_btn.clicked.connect(self.open_image)
        toolbar.addWidget(open_btn)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Метка для изображения
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: #1a1a1a; border: 1px solid #555; min-height: 400px;")
        self.image_label.setText("Откройте изображение...")
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def open_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть изображение",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if filename:
            try:
                pixmap = QPixmap(filename)
                if not pixmap.isNull():
                    # Масштабируем изображение под размер диалога
                    scaled_pixmap = pixmap.scaled(650, 500, Qt.AspectRatioMode.KeepAspectRatio)
                    self.image_label.setPixmap(scaled_pixmap)
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка загрузки: {str(e)}")


class AdvancedSettingsDialog(QDialog):
    """Расширенные настройки с дополнительными виджетами"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Расширенные настройки")
        self.setFixedSize(*ADVANCED_SETTINGS_SIZE)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()

        # Прогресс бар
        progress_group = QGroupBox("Прогресс обучения")
        progress_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD;}")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(45)
        progress_layout.addWidget(QLabel("Уровень освоения игры:"))
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Чекбоксы
        check_group = QGroupBox("Настройки геймплея")
        check_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD;}")
        check_layout = QVBoxLayout()
        self.fog_of_war = QCheckBox("Туман войны")
        self.quick_combat = QCheckBox("Быстрый бой")
        self.diplomacy = QCheckBox("Система дипломатии")
        self.auto_save = QCheckBox("Автосохранение")
        check_layout.addWidget(self.fog_of_war)
        check_layout.addWidget(self.quick_combat)
        check_layout.addWidget(self.diplomacy)
        check_layout.addWidget(self.auto_save)
        check_group.setLayout(check_layout)
        layout.addWidget(check_group)

        # Радио кнопки
        radio_group = QGroupBox("Режим отображения")
        radio_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD;}")
        radio_layout = QVBoxLayout()
        self.simple_view = QRadioButton("Простой вид")
        self.detailed_view = QRadioButton("Детальный вид")
        self.expert_view = QRadioButton("Экспертный вид")
        self.detailed_view.setChecked(True)
        radio_layout.addWidget(self.simple_view)
        radio_layout.addWidget(self.detailed_view)
        radio_layout.addWidget(self.expert_view)
        radio_group.setLayout(radio_layout)
        layout.addWidget(radio_group)

        # Список
        list_group = QGroupBox("Достижения")
        list_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD;}")
        list_layout = QVBoxLayout()
        self.achievements_list = QListWidget()
        self.achievements_list.addItems([
            "🎯 Первая победа",
            "⚔️ Захватчик",
            "🏰 Защитник",
            "💎 Коллекционер",
            "🌟 Легенда",
            "🚀 Быстрая победа",
            "🎪 Мастер тактики",
            "🏆 Чемпион"
        ])
        self.achievements_list.setMinimumHeight(150)
        list_layout.addWidget(self.achievements_list)
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)

        # Кнопки
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Применить настройки")
        ok_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        ok_btn.clicked.connect(self.apply_settings)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def apply_settings(self):
        QMessageBox.information(self, "Настройки", "Настройки применены!")
        self.accept()


class SplashScreen(QDialog):
    """Экран загрузки при запуске игры"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Влияние")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(*SPLASH_SIZE)

        play_sound('zastavka')
        self.setup_ui()
        QTimer.singleShot(SPLASH_SCREEN_DURATION, self.close_splash)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("🎮 ВЛИЯНИЕ")
        title_label.setStyleSheet(
            "font-size: 80px; font-weight: bold; color: #6A5ACD; background: rgba(0, 0, 0, 0.8); padding: 30px; border-radius: 20px; border: 3px solid #FFD700;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel("Стратегическая игра")
        subtitle_label.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #FFD700; background: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 15px; margin-top: 20px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        self.setLayout(layout)

    def close_splash(self):
        self.accept()


class DBManager:
    """Менеджер базы данных для сохранения статистики и достижений"""

    def __init__(self):
        self.db_name = 'game_stats.db'
        self.conn = None
        self.cur = None
        self.init_db()

    def init_db(self):
        """Инициализация базы статистики"""
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cur = self.conn.cursor()

            # Основная таблица статистики игр
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS game_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    score INTEGER,
                    turns INTEGER,
                    game_date TEXT,
                    result TEXT,
                    map_shape TEXT,
                    difficulty TEXT,
                    game_duration INTEGER DEFAULT 0,
                    players_count INTEGER DEFAULT 2
                )
            ''')

            # Таблица игроков
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    color TEXT,
                    created_date TEXT,
                    level INTEGER DEFAULT 1,
                    experience INTEGER DEFAULT 0
                )
            ''')

            # Таблица достижений
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    achievement TEXT,
                    achieved_date TEXT,
                    points INTEGER DEFAULT 0
                )
            ''')

            # Таблица глобальных настроек игры
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS game_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_name TEXT UNIQUE,
                    setting_value TEXT,
                    description TEXT
                )
            ''')

            # Таблица рекордов
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS high_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    score INTEGER,
                    game_date TEXT,
                    map_shape TEXT,
                    difficulty TEXT
                )
            ''')

            # Вставляем настройки по умолчанию
            default_settings = [
                ('max_turns', '50', 'Максимальное количество ходов'),
                ('default_difficulty', 'Средняя', 'Сложность по умолчанию'),
                ('music_volume', '0.4', 'Громкость музыки'),
                ('sound_volume', '0.4', 'Громкость звуков')
            ]

            for setting in default_settings:
                self.cur.execute(
                    'INSERT OR IGNORE INTO game_settings (setting_name, setting_value, description) VALUES (?, ?, ?)',
                    setting
                )

            self.conn.commit()
            print("База статистики инициализирована успешно")
        except sqlite3.Error as e:
            print(f"Ошибка инициализации БД статистики: {e}")

    def save_game(self, player_name, score, turns, result, map_shape="", difficulty="", duration=0, players_count=2):
        """Сохранение статистики игры"""
        try:
            # Валидация данных
            if not isinstance(player_name, str) or not player_name.strip():
                player_name = "Игрок"

            if result not in ["Победа", "Поражение", "Ничья"]:
                result = "Неизвестно"

            self.cur.execute(
                '''INSERT INTO game_stats 
                (player_name, score, turns, game_date, result, map_shape, difficulty, game_duration, players_count) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (player_name, score, turns, datetime.now().isoformat(), result, map_shape, difficulty, duration,
                 players_count)
            )

            # Обновляем таблицу рекордов
            if score > 0:
                self.cur.execute(
                    '''INSERT INTO high_scores (player_name, score, game_date, map_shape, difficulty)
                    VALUES (?, ?, ?, ?, ?)''',
                    (player_name, score, datetime.now().isoformat(), map_shape, difficulty)
                )

                # Оставляем только топ-20 рекордов
                self.cur.execute('''
                    DELETE FROM high_scores 
                    WHERE id NOT IN (
                        SELECT id FROM high_scores 
                        ORDER BY score DESC, game_date ASC 
                        LIMIT 20
                    )
                ''')

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения игры: {e}")
            return False

    def save_player(self, name, color):
        try:
            self.cur.execute(
                'INSERT OR REPLACE INTO players (name, color, created_date) VALUES (?, ?, ?)',
                (name, color, datetime.now().isoformat())
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения игрока: {e}")
            return False

    def save_achievement(self, pname, achievement, points=0):
        try:
            self.cur.execute(
                'INSERT INTO achievements (player_name, achievement, achieved_date, points) VALUES (?, ?, ?, ?)',
                (pname, achievement, datetime.now().isoformat(), points)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения достижения: {e}")
            return False

    def get_stats(self, limit=10):
        """Получение статистики игр"""
        try:
            self.cur.execute(
                'SELECT * FROM game_stats ORDER BY game_date DESC LIMIT ?',
                (limit,)
            )
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения статистики: {e}")
            return []

    def get_players(self):
        """Получить список всех игроков"""
        try:
            self.cur.execute('SELECT * FROM players ORDER BY name')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения игроков: {e}")
            return []

    def get_achievements(self):
        """Получить список достижений"""
        try:
            self.cur.execute('SELECT * FROM achievements ORDER BY achieved_date DESC LIMIT 20')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения достижений: {e}")
            return []

    def update_player_level(self, player_name, level, experience):
        """Обновить уровень и опыт игрока"""
        try:
            self.cur.execute(
                'UPDATE players SET level = ?, experience = ? WHERE name = ?',
                (level, experience, player_name)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка обновления игрока: {e}")
            return False

    def get_game_settings(self):
        """Получить настройки игры"""
        try:
            self.cur.execute('SELECT * FROM game_settings')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения настроек: {e}")
            return []

    def save_game_setting(self, setting_name, setting_value, description=""):
        """Сохранить настройку игры"""
        try:
            self.cur.execute(
                '''INSERT OR REPLACE INTO game_settings 
                (setting_name, setting_value, description) 
                VALUES (?, ?, ?)''',
                (setting_name, setting_value, description)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения настройки: {e}")
            return False

    def delete_player(self, player_id):
        """Удалить игрока"""
        try:
            self.cur.execute('DELETE FROM players WHERE id = ?', (player_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления игрока: {e}")
            return False

    def delete_stat(self, stat_id):
        """Удалить запись статистики"""
        try:
            self.cur.execute('DELETE FROM game_stats WHERE id = ?', (stat_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления статистики: {e}")
            return False

    def get_high_scores(self, limit=10):
        """Получение таблицы рекордов"""
        try:
            self.cur.execute(
                'SELECT * FROM high_scores ORDER BY score DESC, game_date ASC LIMIT ?',
                (limit,)
            )
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения рекордов: {e}")
            return []

    def get_player_game_history(self, player_name, limit=5):
        """Получение истории игр конкретного игрока"""
        try:
            self.cur.execute(
                '''SELECT * FROM game_stats 
                WHERE player_name = ? 
                ORDER BY game_date DESC 
                LIMIT ?''',
                (player_name, limit)
            )
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения истории игр: {e}")
            return []

    def export_to_csv(self, filename):
        """Экспорт статистики в CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    ['ID', 'Игрок', 'Счёт', 'Ходы', 'Результат', 'Карта', 'Сложность', 'Дата', 'Длительность',
                     'Игроков'])
                stats = self.get_stats(1000)
                for stat in stats:
                    writer.writerow(stat)
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False

    def import_from_csv(self, filename):
        """Импорт статистики из CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)
                imported = 0
                for row in reader:
                    if len(row) >= 7:
                        # row[0] - ID, row[1] - player_name, row[2] - score, row[3] - turns, row[4] - result
                        if self.save_game(row[1], int(row[2]), int(row[3]), row[4]):
                            imported += 1
                return imported
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return 0

    def close(self):
        """Закрытие соединения"""
        if self.conn:
            self.conn.close()


class AtkAnim(QWidget):
    """Анимация атаки между клетками"""

    def __init__(self, start_pos, end_pos, parent=None):
        super().__init__(parent)
        self.start_p = start_pos
        self.end_p = end_pos
        self.prog = 0
        self.setFixedSize(parent.size())
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.timer = QTimer()
        self.timer.timeout.connect(self.upd_anim)
        self.timer.start(ANIMATION_TIMER_INTERVAL)

    def upd_anim(self):
        self.prog += 0.05
        if self.prog >= 1:
            self.timer.stop()
            self.hide()
            self.deleteLater()
            return
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Расчет текущей позиции анимации
        curr_x = self.start_p.x() + (self.end_p.x() - self.start_p.x()) * self.prog + 50
        curr_y = self.start_p.y() + (self.end_p.y() - self.start_p.y()) * self.prog + 50
        size = 30 * (1 - abs(self.prog - 0.5) * 1.5)
        alpha = 255 * (1 - self.prog)
        painter.setBrush(QColor(255, 100, 100, int(alpha)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(curr_x - size / 2), int(curr_y - size / 2), int(size), int(size))


class Cell(QPushButton):
    """Класс клетки игрового поля"""

    def __init__(self, r, c):
        super().__init__()
        self.row = r
        self.col = c
        self.owner = None
        self.power = 0
        self.is_base = False
        self.is_road = False
        self._opa = 1.0
        self.setFixedSize(CELL_SIZE, CELL_SIZE)
        self.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.update_style()

    def get_opa(self):
        return self._opa

    def set_opa(self, val):
        self._opa = val
        self.update_style()

    opa = pyqtProperty(float, get_opa, set_opa)

    def update_style(self):
        # Определение стиля клетки в зависимости от состояния
        if self.owner:
            bg_color = self.owner.color
            text_color = "white"
            border = "2px solid white"
        elif self.is_road:
            bg_color = "#666666"
            text_color = "white"
            border = "1px solid #555"
        else:
            bg_color = "#444444"
            text_color = "#888"
            border = "1px solid #555"

        style = f"""
            QPushButton {{
                background: {bg_color};
                color: {text_color};
                font-weight: bold;
                font-size: 16px;
                border: {border};
                border-radius: 8px;
        """

        if self.is_base:
            style += "border: 3px solid #ffd700;"

        style += "}"

        self.setStyleSheet(style)
        txt = str(self.power) if self.power > 0 else ""
        self.setText(txt)


class Player:
    """Класс игрока (человек или бот)"""

    def __init__(self, name, color, ptype="human"):
        self.name = name
        self.color = color
        self.type = ptype
        self.energy = 0
        self.score = 0
        self.achievements = []
        self.got_energy = False
        self.level = 1
        self.experience = 0


class StatsDialog(QDialog):
    """Диалог статистики игр с несколькими таблицами"""

    def __init__(self, db_mgr, parent=None):
        super().__init__(parent)
        self.db_mgr = db_mgr
        self.stats_table = None
        self.players_table = None
        self.achievements_table = None
        self.setWindowTitle("Статистика и управление данными")
        self.setFixedSize(*STATS_DIALOG_SIZE)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("📊 Статистика и управление данными")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #6A5ACD; margin: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #6A5ACD;
                background: #2a2a2a;
            }
            QTabBar::tab {
                background: #3a3a3a;
                color: white;
                padding: 8px 16px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #6A5ACD;
            }
        """)

        # Вкладка статистики игр
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(7)
        self.stats_table.setHorizontalHeaderLabels(["ID", "Игрок", "Счёт", "Ходы", "Результат", "Карта", "Дата"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stats_table.setStyleSheet("font-size: 12px;")
        self.stats_table.setMinimumHeight(400)

        # Кнопки управления для статистики
        stats_btn_layout = QHBoxLayout()
        delete_stat_btn = QPushButton("🗑️ Удалить запись")
        delete_stat_btn.setStyleSheet("font-size: 12px; padding: 8px;")
        delete_stat_btn.clicked.connect(self.delete_stat_record)
        update_stat_btn = QPushButton("🔄 Обновить статистику")
        update_stat_btn.setStyleSheet("font-size: 12px; padding: 8px;")
        update_stat_btn.clicked.connect(self.load_stats)
        stats_btn_layout.addWidget(delete_stat_btn)
        stats_btn_layout.addWidget(update_stat_btn)
        stats_btn_layout.addStretch()

        stats_layout.addLayout(stats_btn_layout)
        stats_layout.addWidget(self.stats_table)
        stats_tab.setLayout(stats_layout)
        tabs.addTab(stats_tab, "📈 Статистика игр")

        # Вкладка игроков
        players_tab = QWidget()
        players_layout = QVBoxLayout()
        self.players_table = QTableWidget()
        self.players_table.setColumnCount(6)
        self.players_table.setHorizontalHeaderLabels(["ID", "Имя", "Цвет", "Уровень", "Опыт", "Дата создания"])
        self.players_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.players_table.setMinimumHeight(400)

        # Кнопки управления для игроков
        players_btn_layout = QHBoxLayout()
        add_player_btn = QPushButton("➕ Добавить игрока")
        add_player_btn.setStyleSheet("font-size: 12px; padding: 8px;")
        add_player_btn.clicked.connect(self.add_player)
        edit_player_btn = QPushButton("✏️ Редактировать")
        edit_player_btn.setStyleSheet("font-size: 12px; padding: 8px;")
        edit_player_btn.clicked.connect(self.edit_player)
        delete_player_btn = QPushButton("🗑️ Удалить игрока")
        delete_player_btn.setStyleSheet("font-size: 12px; padding: 8px;")
        delete_player_btn.clicked.connect(self.delete_player)
        players_btn_layout.addWidget(add_player_btn)
        players_btn_layout.addWidget(edit_player_btn)
        players_btn_layout.addWidget(delete_player_btn)
        players_btn_layout.addStretch()

        players_layout.addLayout(players_btn_layout)
        players_layout.addWidget(self.players_table)
        players_tab.setLayout(players_layout)
        tabs.addTab(players_tab, "👥 Игроки")

        # Вкладка достижений
        achievements_tab = QWidget()
        achievements_layout = QVBoxLayout()
        self.achievements_table = QTableWidget()
        self.achievements_table.setColumnCount(5)
        self.achievements_table.setHorizontalHeaderLabels(["ID", "Игрок", "Достижение", "Очки", "Дата"])
        self.achievements_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.achievements_table.setMinimumHeight(400)

        achievements_btn_layout = QHBoxLayout()
        update_ach_btn = QPushButton("🔄 Обновить")
        update_ach_btn.setStyleSheet("font-size: 12px; padding: 8px;")
        update_ach_btn.clicked.connect(self.load_achievements)
        achievements_btn_layout.addWidget(update_ach_btn)
        achievements_btn_layout.addStretch()

        achievements_layout.addLayout(achievements_btn_layout)
        achievements_layout.addWidget(self.achievements_table)
        achievements_tab.setLayout(achievements_layout)
        tabs.addTab(achievements_tab, "🏆 Достижения")

        # Вкладка файлов
        file_tab = QWidget()
        file_layout = QVBoxLayout()
        file_layout.setSpacing(15)

        txt_btn = QPushButton("📝 Текстовый редактор")
        txt_btn.setStyleSheet("font-size: 14px; padding: 12px;")
        txt_btn.clicked.connect(self.open_text_editor)
        file_layout.addWidget(txt_btn)

        image_btn = QPushButton("🖼️ Просмотр изображений")
        image_btn.setStyleSheet("font-size: 14px; padding: 12px;")
        image_btn.clicked.connect(self.open_image_viewer)
        file_layout.addWidget(image_btn)

        export_btn = QPushButton("📤 Экспорт CSV")
        export_btn.setStyleSheet("font-size: 14px; padding: 12px;")
        export_btn.clicked.connect(self.export_csv)
        file_layout.addWidget(export_btn)

        import_btn = QPushButton("📥 Импорт CSV")
        import_btn.setStyleSheet("font-size: 14px; padding: 12px;")
        import_btn.clicked.connect(self.import_csv)
        file_layout.addWidget(import_btn)

        file_tab.setLayout(file_layout)
        tabs.addTab(file_tab, "📁 Файлы")

        layout.addWidget(tabs)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("font-size: 14px; padding: 10px; margin: 10px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)
        self.load_all_data()

    def load_all_data(self):
        self.load_stats()
        self.load_players()
        self.load_achievements()

    def load_stats(self):
        try:
            stats = self.db_mgr.get_stats()
            self.stats_table.setRowCount(len(stats))
            for i, stat in enumerate(stats):
                for j, val in enumerate(stat):
                    self.stats_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            print(f"Ошибка загрузки статистики: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить статистику: {str(e)}")

    def load_players(self):
        try:
            players = self.db_mgr.get_players()
            self.players_table.setRowCount(len(players))
            for i, player in enumerate(players):
                for j, val in enumerate(player):
                    self.players_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            print(f"Ошибка загрузки игроков: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить игроков: {str(e)}")

    def load_achievements(self):
        try:
            achievements = self.db_mgr.get_achievements()
            self.achievements_table.setRowCount(len(achievements))
            for i, ach in enumerate(achievements):
                for j, val in enumerate(ach):
                    self.achievements_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            print(f"Ошибка загрузки достижений: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить достижения: {str(e)}")

    def delete_stat_record(self):
        current_row = self.stats_table.currentRow()
        if current_row >= 0:
            stat_id = self.stats_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Удаление", "Удалить выбранную запись?")
            if reply == QMessageBox.StandardButton.Yes:
                if self.db_mgr.delete_stat(int(stat_id)):
                    self.stats_table.removeRow(current_row)
                    QMessageBox.information(self, "Успех", "Запись удалена!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить запись")

    def add_player(self):
        name, ok = QInputDialog.getText(self, "Новый игрок", "Введите имя игрока:")
        if ok and name:
            color = QColorDialog.getColor().name()
            if color:
                if self.db_mgr.save_player(name, color):
                    self.load_players()
                    QMessageBox.information(self, "Успех", "Игрок добавлен!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить игрока")

    def edit_player(self):
        current_row = self.players_table.currentRow()
        if current_row >= 0:
            player_id = self.players_table.item(current_row, 0).text()
            level, ok = QInputDialog.getInt(self, "Редактирование", "Введите уровень:", 1, 1, 100)
            if ok:
                player_name = self.players_table.item(current_row, 1).text()
                if self.db_mgr.update_player_level(player_name, level, 0):
                    self.load_players()
                    QMessageBox.information(self, "Успех", "Данные обновлены!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные")

    def delete_player(self):
        current_row = self.players_table.currentRow()
        if current_row >= 0:
            player_id = self.players_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Удаление", "Удалить выбранного игрока?")
            if reply == QMessageBox.StandardButton.Yes:
                if self.db_mgr.delete_player(int(player_id)):
                    self.players_table.removeRow(current_row)
                    QMessageBox.information(self, "Успех", "Игрок удален!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить игрока")

    def open_text_editor(self):
        editor = TextEditorDialog(self)
        editor.exec()

    def open_image_viewer(self):
        viewer = ImageViewerDialog(self)
        viewer.exec()

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Экспорт статистики", "", "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(['ID', 'Игрок', 'Счёт', 'Ходы', 'Результат', 'Карта', 'Дата'])
                    stats = self.db_mgr.get_stats()
                    for stat in stats:
                        writer.writerow(stat)
                QMessageBox.information(self, "Успех", "Данные экспортированы!")
            except Exception as err:
                QMessageBox.warning(self, "Ошибка", f"Ошибка экспорта: {str(err)}")

    def import_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Импорт статистики", "", "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    next(reader)  # Пропускаем заголовок
                    imported = 0
                    for row in reader:
                        if len(row) >= 5:
                            # row[0] - ID, row[1] - player_name, row[2] - score, row[3] - turns, row[4] - result
                            if self.db_mgr.save_game(row[1], int(row[2]), int(row[3]), row[4]):
                                imported += 1
                self.load_stats()
                QMessageBox.information(self, "Успех", f"Импортировано {imported} записей!")
            except Exception as err:
                QMessageBox.warning(self, "Ошибка", f"Ошибка импорта: {str(err)}")


class GameBoard(QWidget):
    """Виджет игрового поля"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid = QGridLayout(self)
        self.grid.setSpacing(GRID_SPACING)
        self.cells = {}
        self.sel_attack = None
        self.sel_target = None
        self.attack_cells = set()
        self.target_cells = set()

    def init_board(self, board_shape):
        # Создание клеток поля согласно выбранной форме
        for r in range(BOARD_DIMENSION):
            for c in range(BOARD_DIMENSION):
                if (r, c) in board_shape:
                    cell = Cell(r, c)
                    cell.clicked.connect(lambda ch, row=r, col=c: self.cell_click(row, col))
                    self.grid.addWidget(cell, r, c)
                    self.cells[(r, c)] = cell
                else:
                    spacer = QWidget()
                    spacer.setFixedSize(CELL_SIZE, CELL_SIZE)
                    self.grid.addWidget(spacer, r, c)
        self.update_display()

    def cell_click(self, r, c):
        self.parent.handle_click(r, c)

    def update_display(self):
        for r in range(BOARD_DIMENSION):
            for c in range(BOARD_DIMENSION):
                if (r, c) not in self.cells:
                    continue
                cell_widget = self.cells[(r, c)]
                cell_obj = self.parent.board[r][c]
                cell_widget.owner = cell_obj.owner
                cell_widget.power = cell_obj.power
                cell_widget.is_base = cell_obj.is_base
                cell_widget.is_road = cell_obj.is_road
                cell_widget.update_style()

                base_style = cell_widget.styleSheet()

                # Подсветка доступных целей и выбранных клеток
                if (r, c) in self.target_cells:
                    base_style += "border: 3px solid #00ff00;"
                elif (r, c) in self.attack_cells:
                    base_style += "border: 3px solid #ff4444;"
                if self.sel_attack == (r, c):
                    base_style += "border: 4px solid #ffff00;"
                elif self.sel_target == (r, c):
                    base_style += "border: 4px solid #00ffff;"

                cell_widget.setStyleSheet(base_style)

    def animate_cell(self, r, c):
        if (r, c) in self.cells:
            cell = self.cells[(r, c)]
            anim = QPropertyAnimation(cell, b"opa")
            anim.setDuration(ANIMATION_DURATION)
            anim.setStartValue(ANIMATION_START_OPACITY)
            anim.setEndValue(ANIMATION_END_OPACITY)
            anim.start()

    def show_attack_anim(self, start_r, start_c, end_r, end_c):
        start_cell = self.cells.get((start_r, start_c))
        end_cell = self.cells.get((end_r, end_c))
        if start_cell and end_cell:
            start_pos = start_cell.pos()
            end_pos = end_cell.pos()
            anim = AtkAnim(start_pos, end_pos, self)
            anim.show()
            anim.raise_()


class EnergyDialog(QDialog):
    """Диалог распределения энергии"""

    def __init__(self, parent, energy_amount, sel_cell):
        super().__init__(parent)
        self.energy_amount = energy_amount
        self.sel_cell = sel_cell
        self.energy_given = 1
        self.setWindowTitle("Энергия")
        self.setFixedSize(*ENERGY_DIALOG_SIZE)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel(f"Энергия ({self.energy_amount} доступно)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #6A5ACD; margin: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        slider_layout = QVBoxLayout()
        slider_label = QLabel(f"Энергия: {self.energy_given}")
        slider_label.setStyleSheet("font-size: 16px; color: #ccc; margin: 10px;")
        slider_layout.addWidget(slider_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(self.energy_amount)
        self.slider.setValue(1)
        self.slider.setStyleSheet("font-size: 14px;")
        self.slider.valueChanged.connect(lambda v: slider_label.setText(f"Энергия: {v}"))
        self.slider.valueChanged.connect(lambda v: setattr(self, 'energy_given', v))
        slider_layout.addWidget(self.slider)

        layout.addLayout(slider_layout)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton(f"✅ Добавить {self.energy_given}")
        self.ok_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.ok_btn.clicked.connect(lambda: self.done(1))
        btn_layout.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton("❌ Отмена")
        self.cancel_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)


class ColorSelectDialog(QDialog):
    """Диалог выбора цветов для игроков"""

    def __init__(self, total_players, parent=None):
        super().__init__(parent)
        self.total_players = total_players
        self.player_colors = {}
        self.color_widgets = []
        self.setWindowTitle("Выбор цветов")
        self.setFixedSize(*COLOR_DIALOG_SIZE)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("🎨 ВЫБОР ЦВЕТОВ ДЛЯ ИГРОКОВ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #6A5ACD; margin: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        available_colors = [
            ("🔵 Синий", "#4169E1"),
            ("🔴 Красный", "#DC143C"),
            ("🟢 Зеленый", "#32CD32"),
            ("🟣 Фиолетовый", "#9370DB"),
            ("🟠 Оранжевый", "#FF8C00"),
            ("🟡 Желтый", "#FFD700"),
            ("🔶 Коралловый", "#FF7F50"),
            ("🟦 Голубой", "#1E90FF")
        ]

        self.color_widgets = []

        for i in range(self.total_players):
            player_layout = QHBoxLayout()
            player_label = QLabel(f"Игрок {i + 1}:" if i == 0 else f"Бот {i}:")
            player_label.setStyleSheet("font-size: 14px; color: white; min-width: 100px;")
            player_layout.addWidget(player_label)

            color_combo = QComboBox()
            color_combo.setStyleSheet("font-size: 12px; padding: 5px; min-width: 150px;")
            for name, color in available_colors:
                color_combo.addItem(name, color)
            color_combo.setCurrentIndex(min(i, len(available_colors) - 1))

            preview_label = QLabel("■■■■■■")
            preview_label.setFixedSize(80, 25)
            default_color = available_colors[min(i, len(available_colors) - 1)][1]
            preview_label.setStyleSheet(f"background: {default_color}; border: 1px solid white; border-radius: 3px;")

            color_combo.currentIndexChanged.connect(lambda idx, lbl=preview_label, cmb=color_combo:
                                                    lbl.setStyleSheet(
                                                        f"background: {cmb.currentData()}; border: 1px solid white; border-radius: 3px;"))

            player_layout.addWidget(color_combo)
            player_layout.addWidget(preview_label)
            player_layout.addStretch()

            self.color_widgets.append((color_combo, preview_label))
            layout.addLayout(player_layout)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("✅ Сохранить цвета")
        ok_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        ok_btn.clicked.connect(self.save_colors)
        btn_layout.addWidget(ok_btn)

        random_btn = QPushButton("🎲 Случайные цвета")
        random_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        random_btn.clicked.connect(self.random_colors)
        btn_layout.addWidget(random_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def random_colors(self):
        available_colors = [
            "#4169E1", "#DC143C", "#32CD32", "#9370DB",
            "#FF8C00", "#FFD700", "#FF7F50", "#1E90FF"
        ]
        random.shuffle(available_colors)
        for i, (color_combo, preview_label) in enumerate(self.color_widgets):
            if i < len(available_colors):
                for idx in range(color_combo.count()):
                    if color_combo.itemData(idx) == available_colors[i]:
                        color_combo.setCurrentIndex(idx)
                        break

    def save_colors(self):
        self.player_colors = {}
        for i, (color_combo, preview_label) in enumerate(self.color_widgets):
            self.player_colors[i] = color_combo.currentData()
        self.accept()


class GameSetupDialog(QDialog):
    """Диалог настройки игры"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.players_spin = None
        self.shape_combo = None
        self.size_combo = None
        self.diff_combo = None
        self.start_btn = None
        self.stats_btn = None
        self.exit_btn = None
        self.setWindowTitle("Настройки игры")
        self.setFixedSize(*SETUP_DIALOG_SIZE)
        self.setup_ui()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("🎮 НАСТРОЙКИ ИГРЫ")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #6A5ACD; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        players_group = QGroupBox("Количество игроков")
        players_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 16px; color: #6A5ACD;}")
        players_layout = QVBoxLayout()
        self.players_spin = QSpinBox()
        self.players_spin.setRange(2, MAX_PLAYERS)
        self.players_spin.setValue(3)
        self.players_spin.setStyleSheet("font-size: 14px; padding: 8px;")
        players_layout.addWidget(self.players_spin)
        players_group.setLayout(players_layout)
        layout.addWidget(players_group)

        shape_group = QGroupBox("Форма карты")
        shape_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 16px; color: #6A5ACD;}")
        shape_layout = QVBoxLayout()
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(
            ["Квадрат", "Треугольник", "Сердце", "Шестиугольник", "Спираль", "Круг", "Крест", "Звезда"])
        self.shape_combo.setStyleSheet("font-size: 14px; padding: 8px;")
        shape_layout.addWidget(self.shape_combo)
        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)

        size_group = QGroupBox("Размер карты")
        size_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 16px; color: #6A5ACD;}")
        size_layout = QVBoxLayout()
        self.size_combo = QComboBox()
        self.size_combo.addItems(["Маленький", "Средний", "Большой", "Огромный"])
        self.size_combo.setCurrentIndex(1)
        self.size_combo.setStyleSheet("font-size: 14px; padding: 8px;")
        size_layout.addWidget(self.size_combo)
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        diff_group = QGroupBox("Сложность ИИ")
        diff_group.setStyleSheet("QGroupBox{font-weight: bold; font-size: 16px; color: #6A5ACD;}")
        diff_layout = QVBoxLayout()
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["Лёгкая", "Средняя", "Сложная", "Эксперт"])
        self.diff_combo.setCurrentIndex(1)
        self.diff_combo.setStyleSheet("font-size: 14px; padding: 8px;")
        diff_layout.addWidget(self.diff_combo)
        diff_group.setLayout(diff_layout)
        layout.addWidget(diff_group)

        layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("🎮 НАЧАТЬ ИГРУ")
        self.start_btn.setStyleSheet("font-size: 16px; padding: 12px;")
        self.start_btn.clicked.connect(self.accept)

        self.stats_btn = QPushButton("📊 СТАТИСТИКА")
        self.stats_btn.setStyleSheet("font-size: 16px; padding: 12px;")

        advanced_btn = QPushButton("⚙️ Расширенные настройки")
        advanced_btn.setStyleSheet("font-size: 16px; padding: 12px;")
        advanced_btn.clicked.connect(self.open_advanced_settings)

        self.exit_btn = QPushButton("🚪 ВЫХОД")
        self.exit_btn.setStyleSheet("font-size: 16px; padding: 12px;")
        self.exit_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stats_btn)
        btn_layout.addWidget(advanced_btn)
        btn_layout.addWidget(self.exit_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def open_advanced_settings(self):
        settings_dialog = AdvancedSettingsDialog(self)
        settings_dialog.exec()


class InfluenceGame(QMainWindow):
    """Главный класс игры с расширенным функционалом"""

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.settings = Settings()
        self.db_man = DBManager()

        self.players = []
        self.cur_player = 0
        self.board = []
        self.turn_num = 0
        self.max_turns = MAX_TURNS_DEFAULT
        self.sel_attack = None
        self.sel_target = None
        self.game_active = False
        self.board_size = self.config.BOARD_SIZE
        self.difficulty = "Средняя"
        self.phase = "attack"
        self.board_shape = set()
        self.player_name = "Игрок"
        self.player_color = self.config.PLAYER_COLORS[0]
        self.player_colors = {}

        self.board_widget = None
        self.phase_label = None
        self.status_label = None
        self.energy_label = None
        self.score_label = None
        self.turn_label = None
        self.attack_btn = None
        self.energy_btn = None
        self.end_btn = None
        self.log_text = None

        self.apply_dark_theme()
        self.setWindowIcon(QIcon('icon.ico'))

        splash = SplashScreen()
        splash.exec()
        self.show_menu()

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(dark_palette)

    def show_menu(self):
        play_sound('menu')
        dlg = GameSetupDialog(self)
        dlg.stats_btn.clicked.connect(self.show_stats)
        if dlg.exec():
            shape = dlg.shape_combo.currentText()
            size = dlg.size_combo.currentText()
            self.difficulty = dlg.diff_combo.currentText()
            total_players = dlg.players_spin.value()

            color_dlg = ColorSelectDialog(total_players, self)
            if color_dlg.exec():
                self.player_colors = color_dlg.player_colors
                self.board_shape = self.generate_shape(shape, size)
                self.init_game(total_players)
                self.init_ui()
        else:
            sys.exit()

    def show_stats(self):
        try:
            dlg = StatsDialog(self.db_man, self)
            dlg.exec()
        except Exception as e:
            print(f"Ошибка открытия статистики: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть статистику: {str(e)}")

    @staticmethod
    def generate_shape(shape, size):
        """Генерация различных форм игрового поля"""
        cells = set()
        radius = SHAPE_SIZES.get(size, 4)
        center = 3.5

        if shape == "Квадрат":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    if abs(r - center) <= radius and abs(c - center) <= radius:
                        cells.add((r, c))
        elif shape == "Треугольник":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    if r >= center - radius and abs(c - center) <= (r - center + radius):
                        cells.add((r, c))
        elif shape == "Сердце":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    x = (c - center) / radius
                    y = (r - center) / radius
                    if (x * x + y * y - 1) ** 3 - x * x * y * y * y < 0.1:
                        cells.add((r, c))
        elif shape == "Шестиугольник":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    dx = abs(c - center)
                    dy = abs(r - center)
                    if dx <= radius and dy <= radius and dx + dy * 0.7 <= radius * 1.2:
                        cells.add((r, c))
        elif shape == "Спираль":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    dist = math.sqrt((r - center) ** 2 + (c - center) ** 2)
                    angle = math.atan2(r - center, c - center)
                    if dist < radius and abs(math.sin(dist * 2 + angle)) < 0.3:
                        cells.add((r, c))
        elif shape == "Круг":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    dist = math.sqrt((r - center) ** 2 + (c - center) ** 2)
                    if dist <= radius:
                        cells.add((r, c))
        elif shape == "Крест":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    if abs(r - center) <= radius / 2 or abs(c - center) <= radius / 2:
                        cells.add((r, c))
        elif shape == "Звезда":
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    angle = math.atan2(r - center, c - center)
                    dist = math.sqrt((r - center) ** 2 + (c - center) ** 2)
                    star_radius = radius * (0.5 + 0.5 * math.sin(5 * angle) * 0.3)
                    if dist <= star_radius:
                        cells.add((r, c))
        else:
            # По умолчанию - квадрат
            for r in range(BOARD_DIMENSION):
                for c in range(BOARD_DIMENSION):
                    if abs(r - center) <= radius and abs(c - center) <= radius:
                        cells.add((r, c))

        return cells

    def generate_roads(self):
        """Генерация дорог между клетками для обеспечения связности"""
        roads = set()
        shape_list = list(self.board_shape)

        if not shape_list:
            return roads

        visited = set()
        queue = [shape_list[0]]

        # Алгоритм поиска в ширину для создания связной карты
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue

            visited.add(current)
            r, c = current

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                neighbor = (nr, nc)

                if neighbor in self.board_shape and neighbor not in visited:
                    roads.add(current)
                    roads.add(neighbor)
                    queue.append(neighbor)

        return roads

    def is_far_enough(self, pos, placed_positions, min_distance=MIN_DISTANCE_BETWEEN_BASES):
        """Проверка расстояния между базами игроков"""
        if not placed_positions:
            return True

        for placed_pos in placed_positions:
            distance = max(abs(pos[0] - placed_pos[0]), abs(pos[1] - placed_pos[1]))
            if distance < min_distance:
                return False
        return True

    def init_game(self, total_players):
        """Инициализация игрового состояния"""
        self.players = []

        # Получаем настройки сложности
        current_difficulty = {
            "Лёгкая": {"bot_names": ["Новичок", "Ученик"]},
            "Средняя": {"bot_names": ["Ветеран", "Стратег"]},
            "Сложная": {"bot_names": ["Мастер", "Гений"]},
            "Эксперт": {"bot_names": ["Легенда", "Титан"]}
        }.get(self.difficulty, {"bot_names": ["Бот", "ИИ"]})

        names = current_difficulty["bot_names"]

        human_color = self.player_colors.get(0, self.config.PLAYER_COLORS[0])
        self.players.append(Player("Вы", human_color, "human"))

        for i in range(1, total_players):
            bot_color = self.player_colors.get(i, self.config.PLAYER_COLORS[i % len(self.config.PLAYER_COLORS)])
            bot_name = names[(i - 1) % len(names)] + f" {i}"
            self.players.append(Player(bot_name, bot_color, "bot"))

        self.cur_player = 0
        self.turn_num = 1
        self.game_active = True
        self.phase = "attack"
        self.board = []
        roads = self.generate_roads()

        # Создание игрового поля
        for r in range(BOARD_DIMENSION):
            board_row = []
            for c in range(BOARD_DIMENSION):
                cell = Cell(r, c)
                if (r, c) in self.board_shape:
                    if (r, c) in roads:
                        cell.is_road = True
                else:
                    cell.owner = None
                    cell.power = 0
                board_row.append(cell)
            self.board.append(board_row)

        # Размещение баз игроков
        start_cells = list(self.board_shape)
        random.shuffle(start_cells)

        placed_bases = []
        successful_placements = 0
        max_attempts = len(start_cells) * 2

        for attempt in range(max_attempts):
            if successful_placements >= min(len(self.players), len(start_cells)):
                break

            for cell_pos in start_cells:
                if successful_placements >= min(len(self.players), len(start_cells)):
                    break

                if cell_pos not in placed_bases and self.is_far_enough(cell_pos, placed_bases,
                                                                       MIN_DISTANCE_BETWEEN_BASES):
                    r, c = cell_pos
                    cell = self.board[r][c]
                    cell.owner = self.players[successful_placements]
                    cell.power = 2
                    cell.is_base = True
                    cell.is_road = True
                    self.players[successful_placements].score = 1
                    placed_bases.append(cell_pos)
                    successful_placements += 1

        if successful_placements < len(self.players):
            remaining_players = len(self.players) - successful_placements
            remaining_cells = [pos for pos in start_cells if pos not in placed_bases]

            for i in range(min(remaining_players, len(remaining_cells))):
                r, c = remaining_cells[i]
                cell = self.board[r][c]
                cell.owner = self.players[successful_placements + i]
                cell.power = 2
                cell.is_base = True
                cell.is_road = True
                self.players[successful_placements + i].score = 1
                placed_bases.append((r, c))

    def init_ui(self):
        stop_music()
        play_sound('game')

        if hasattr(self, 'centralWidget') and self.centralWidget():
            self.centralWidget().deleteLater()

        self.setWindowTitle("Влияние - Стратегическая игра")
        self.setFixedSize(1600, 950)

        toolbar = QToolBar("Основные инструменты")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        new_game_action = QAction("🆕 Новая игра", self)
        new_game_action.triggered.connect(self.back_to_menu)
        toolbar.addAction(new_game_action)

        stats_action = QAction("📊 Статистика", self)
        stats_action.triggered.connect(self.show_stats)
        toolbar.addAction(stats_action)

        toolbar.addSeparator()

        save_action = QAction("💾 Сохранить", self)
        save_action.triggered.connect(self.save_game_state)
        toolbar.addAction(save_action)

        load_action = QAction("📂 Загрузить", self)
        load_action.triggered.connect(self.load_game_state)
        toolbar.addAction(load_action)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Готов к игре")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.board_widget = GameBoard(self)
        self.board_widget.init_board(self.board_shape)
        splitter.addWidget(self.board_widget)

        info_panel = QWidget()
        info_panel.setMinimumWidth(500)
        info_layout = QVBoxLayout(info_panel)
        info_layout.setSpacing(10)
        info_layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("🎮 ВЛИЯНИЕ")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #6A5ACD; margin: 8px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(title)

        self.phase_label = QLabel("⚔️ Фаза атаки")
        self.phase_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; background: #333; padding: 10px; border-radius: 6px; color: white;")
        self.phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phase_label.setMinimumHeight(35)
        info_layout.addWidget(self.phase_label)

        self.status_label = QLabel("Выберите клетку для атаки")
        self.status_label.setStyleSheet(
            "font-size: 13px; padding: 8px; background: #252525; border-radius: 5px; color: #ccc;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMinimumHeight(30)
        info_layout.addWidget(self.status_label)

        stats_container = QWidget()
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(5)

        self.energy_label = QLabel("⚡ Энергия: 0")
        self.energy_label.setStyleSheet(
            "font-size: 13px; padding: 8px; background: #252525; border-radius: 5px; color: #ccc;")
        self.energy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.energy_label.setMinimumHeight(28)
        stats_layout.addWidget(self.energy_label)

        self.score_label = QLabel("Счёт: Вы: 1")
        self.score_label.setStyleSheet(
            "font-size: 12px; padding: 8px; background: #252525; border-radius: 5px; color: #ccc;")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setMinimumHeight(28)
        stats_layout.addWidget(self.score_label)

        self.turn_label = QLabel("Ход: 1/50")
        self.turn_label.setStyleSheet(
            "font-size: 12px; padding: 8px; background: #252525; border-radius: 5px; color: #ccc;")
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setMinimumHeight(28)
        stats_layout.addWidget(self.turn_label)

        info_layout.addWidget(stats_container)
        info_layout.addSpacing(10)

        action_group = QGroupBox("Действия")
        action_group.setStyleSheet(
            "QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD; padding: 10px; border: 2px solid #6A5ACD; border-radius: 8px;}")
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(6)

        self.attack_btn = QPushButton("⚔️ АТАКОВАТЬ")
        self.attack_btn.clicked.connect(self.do_attack)
        self.attack_btn.setStyleSheet(
            "font-size: 12px; padding: 8px; background: #5a4cbf; color: white; border-radius: 5px;")
        action_layout.addWidget(self.attack_btn)

        self.energy_btn = QPushButton("🎲 ПОЛУЧИТЬ ЭНЕРГИЮ")
        self.energy_btn.clicked.connect(self.get_energy)
        self.energy_btn.setStyleSheet(
            "font-size: 12px; padding: 8px; background: #4c8b4c; color: white; border-radius: 5px;")
        action_layout.addWidget(self.energy_btn)

        self.end_btn = QPushButton("⏭️ ЗАВЕРШИТЬ ХОД")
        self.end_btn.clicked.connect(self.end_turn)
        self.end_btn.setStyleSheet(
            "font-size: 12px; padding: 8px; background: #bf4c4c; color: white; border-radius: 5px;")
        action_layout.addWidget(self.end_btn)

        info_layout.addWidget(action_group)
        info_layout.addSpacing(10)

        rules_group = QGroupBox("Правила")
        rules_group.setStyleSheet(
            "QGroupBox{font-weight: bold; font-size: 14px; color: #FFD700; padding: 10px; border: 2px solid #FFD700; border-radius: 8px;}")
        rules_layout = QVBoxLayout(rules_group)

        rules_text = QLabel(
            "1. ⚔️ АТАКА: Выберите свою клетку\n" +
            "2. ⚔️ АТАКА: Выберите цель\n" +
            "3. 🎲 ЭНЕРГИЯ: Получите энергию\n" +
            "4. ⏭️ ЗАВЕРШЕНИЕ: Передайте ход")
        rules_text.setStyleSheet(
            "font-size: 11px; color: #ccc; padding: 8px; line-height: 1.4; background: #1a1a1a; border-radius: 5px;")
        rules_text.setWordWrap(True)
        rules_text.setMinimumHeight(70)
        rules_layout.addWidget(rules_text)

        info_layout.addWidget(rules_group)
        info_layout.addSpacing(10)

        menu_group = QGroupBox("Меню")
        menu_group.setStyleSheet(
            "QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD; padding: 10px; border: 2px solid #6A5ACD; border-radius: 8px;}")
        menu_layout = QVBoxLayout(menu_group)
        menu_layout.setSpacing(6)

        stats_btn = QPushButton("📊 СТАТИСТИКА")
        stats_btn.setStyleSheet("font-size: 11px; padding: 8px; background: #3a3a3a; color: white; border-radius: 5px;")
        stats_btn.clicked.connect(self.show_stats)
        menu_layout.addWidget(stats_btn)

        settings_btn = QPushButton("⚙️ Настройки")
        settings_btn.setStyleSheet(
            "font-size: 11px; padding: 8px; background: #3a3a3a; color: white; border-radius: 5px;")
        settings_btn.clicked.connect(self.show_settings)
        menu_layout.addWidget(settings_btn)

        menu_btn = QPushButton("🏠 ГЛАВНОЕ МЕНЮ")
        menu_btn.setStyleSheet("font-size: 11px; padding: 8px; background: #3a3a3a; color: white; border-radius: 5px;")
        menu_btn.clicked.connect(self.back_to_menu)
        menu_layout.addWidget(menu_btn)

        info_layout.addWidget(menu_group)
        info_layout.addSpacing(10)

        log_group = QGroupBox("Журнал")
        log_group.setStyleSheet(
            "QGroupBox{font-weight: bold; font-size: 14px; color: #6A5ACD; padding: 10px; border: 2px solid #6A5ACD; border-radius: 8px;}")
        log_layout = QVBoxLayout(log_group)

        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet(
            "font-size: 11px; background: #1a1a1a; color: #ccc; padding: 8px; border-radius: 5px;")
        log_layout.addWidget(self.log_text)

        info_layout.addWidget(log_group)

        info_layout.addStretch()

        splitter.addWidget(info_panel)
        splitter.setSizes([1000, 500])

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.addWidget(splitter)

        self.log_text.append("=== ВЛИЯНИЕ ===")
        self.log_text.append("Игра началась! Фаза атаки.")
        self.update_ui()

        if self.get_current_player().type == "bot":
            QTimer.singleShot(BOT_TURN_DELAY, self.bot_turn)

    def update_ui(self):
        if not self.game_active:
            return
        player = self.get_current_player()
        if self.phase == "attack":
            self.phase_label.setText("⚔️ Фаза атаки")
            self.board_widget.attack_cells = self.get_attack_cells(player)
        elif self.phase == "nrg":
            self.phase_label.setText("🎲 Фаза энергии")
            self.board_widget.attack_cells = set()

        self.energy_label.setText(f"⚡ Энергия: {player.energy}")
        self.turn_label.setText(f"📊 Ход: {self.turn_num}/{self.max_turns}")

        score_parts = []
        for plr in self.players:
            if plr.name == "Вы":
                score_parts.append(f"Вы:{plr.score}")
            else:
                short_name = plr.name.split()[0]
                score_parts.append(f"{short_name}:{plr.score}")

        scores = " | ".join(score_parts)
        self.score_label.setText(f"🏆 {scores}")

        self.board_widget.sel_attack = self.sel_attack
        self.board_widget.sel_target = self.sel_target
        is_human = player.type == "human"
        has_both = bool(self.sel_attack and self.sel_target)

        can_attack = is_human and self.phase == "attack" and has_both and not player.got_energy
        can_get_energy = is_human and self.phase == "attack" and not player.got_energy
        can_end_turn = is_human

        self.attack_btn.setEnabled(can_attack)
        self.energy_btn.setEnabled(can_get_energy)
        self.end_btn.setEnabled(can_end_turn)

        self.board_widget.update_display()

    def show_settings(self):
        """Показать диалог настроек"""
        font, ok = QFontDialog.getFont(self)
        if ok:
            self.log_text.setFont(font)
            QMessageBox.information(self, "Настройки", "Шрифт изменен!")

    def save_game_state(self):
        """Сохранение состояния игры"""
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить игру", "", "Game Files (*.sav)")
        if filename:
            try:
                # Здесь должна быть логика сохранения состояния игры
                QMessageBox.information(self, "Сохранение", "Игра сохранена!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить игру: {str(e)}")

    def load_game_state(self):
        """Загрузка состояния игры"""
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить игру", "", "Game Files (*.sav)")
        if filename:
            try:
                # Здесь должна быть логика загрузки состояния игры
                QMessageBox.information(self, "Загрузка", "Игра загружена!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить игру: {str(e)}")

    def back_to_menu(self):
        stop_music()
        play_sound('menu')
        reply = QMessageBox.question(self, "Меню", "Вернуться в меню? Текущая игра будет потеряна.")
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            new_game = InfluenceGame()
            new_game.show()

    def get_current_player(self):
        return self.players[self.cur_player]

    @staticmethod
    def calculate_energy(player):
        return player.score

    def get_attack_cells(self, player):
        attack_cells = set()
        for r, c in self.board_shape:
            cell = self.board[r][c]
            if cell.owner == player and cell.power > 1:
                attack_cells.add((r, c))
        return attack_cells

    def get_target_cells(self, attack_r, attack_c):
        target_cells = set()
        player = self.get_current_player()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = attack_r + dr, attack_c + dc
            if (r, c) in self.board_shape and self.board[r][c].is_road:
                cell = self.board[r][c]
                if cell.owner != player:
                    target_cells.add((r, c))
        return target_cells

    def handle_click(self, r, c):
        if not self.game_active or (r, c) not in self.board_shape:
            return
        current = self.get_current_player()
        if current.type != "human":
            return
        cell = self.board[r][c]
        if self.phase == "attack":
            if cell.owner == current and cell.power > 1:
                self.sel_attack = (r, c)
                self.sel_target = None
                self.board_widget.target_cells = self.get_target_cells(r, c)
                self.status_label.setText(f"Атака: ({r},{c}) - Выберите цель")
                self.board_widget.animate_cell(r, c)
            elif self.sel_attack and (r, c) in self.board_widget.target_cells:
                self.sel_target = (r, c)
                self.status_label.setText(f"Цель: ({r},{c}) - Атаковать")
                self.board_widget.animate_cell(r, c)
        elif self.phase == "nrg":
            if cell.owner == current:
                self.sel_attack = (r, c)
                self.show_energy_dialog(r, c)
            else:
                self.status_label.setText("Выберите свою клетку!")
        self.update_ui()

    def do_attack(self):
        if not self.sel_attack or not self.sel_target:
            self.status_label.setText("Выберите клетку и цель!")
            return

        attack_r, attack_c = self.sel_attack
        target_r, target_c = self.sel_target

        self.board_widget.show_attack_anim(attack_r, attack_c, target_r, target_c)
        QTimer.singleShot(ATTACK_ANIMATION_DELAY, self.execute_attack)

    def execute_attack(self):
        play_sound('attack')
        attack_r, attack_c = self.sel_attack
        target_r, target_c = self.sel_target
        attack_cell = self.board[attack_r][attack_c]
        target_cell = self.board[target_r][target_c]
        player = self.get_current_player()

        if target_cell.owner == player:
            self.status_label.setText("Нельзя атаковать свою клетку!")
            return

        # Логика атаки на пустую клетку
        if target_cell.owner is None:
            target_cell.owner = player
            target_cell.power = attack_cell.power - 1
            attack_cell.power = 1
            player.score += 1
            self.log_text.append(f"⚔️ Захвачена клетка ({target_r},{target_c})")
            self.board_widget.animate_cell(target_r, target_c)
        else:
            # Логика атаки на клетку противника
            if attack_cell.power > target_cell.power:
                old_owner = target_cell.owner
                old_owner.score -= 1
                target_cell.owner = player
                target_cell.power = attack_cell.power - target_cell.power
                attack_cell.power = 1
                player.score += 1
                self.log_text.append(f"⚔️ Захвачена клетка у {old_owner.name}")
                self.board_widget.animate_cell(target_r, target_c)
            else:
                self.status_label.setText("Недостаточно силы!")
                return

        self.sel_attack = None
        self.sel_target = None
        self.board_widget.target_cells = set()
        self.status_label.setText("Атака завершена!")
        self.check_achievement(player)
        self.check_game_end()
        self.update_ui()

    def get_energy(self):
        if self.phase != "attack":
            return
        self.phase = "nrg"
        player = self.get_current_player()
        player.energy = self.calculate_energy(player)
        player.got_energy = True
        self.log_text.append(f"🎲 Получено {player.energy} энергии")
        self.status_label.setText(f"Распределите {player.energy} энергии")
        self.update_ui()

    def show_energy_dialog(self, r, c):
        player = self.get_current_player()
        if player.energy <= 0:
            self.status_label.setText("Нет энергии!")
            return
        dlg = EnergyDialog(self, player.energy, (r, c))
        if dlg.exec():
            energy_given = dlg.energy_given
            if energy_given <= player.energy:
                cell = self.board[r][c]
                if cell.owner == player:
                    cell.power += energy_given
                    player.energy -= energy_given
                    self.log_text.append(f"🎯 Добавлено {energy_given} энергии в ({r},{c})")
                    self.board_widget.animate_cell(r, c)
                    if player.energy == 0:
                        self.status_label.setText("Энергия распределена. Завершите ход.")
                else:
                    self.status_label.setText("Только в свои клетки!")
            else:
                self.status_label.setText("Недостаточно энергии!")
        self.update_ui()

    def bot_turn(self):
        if not self.game_active:
            return
        bot = self.get_current_player()
        self.log_text.append(f"🤖 Ход {bot.name}")

        self.bot_attack(bot)
        bot.energy = self.calculate_energy(bot)
        if bot.energy > 0:
            self.bot_energy(bot)

        QTimer.singleShot(BOT_TURN_DELAY, self.end_turn)

    def bot_attack(self, bot):
        attack_cells = self.get_attack_cells(bot)
        if not attack_cells:
            return

        for attack_r, attack_c in list(attack_cells):
            target_cells = self.get_target_cells(attack_r, attack_c)
            if target_cells:
                target_r, target_c = random.choice(list(target_cells))
                self.execute_bot_attack(bot, attack_r, attack_c, target_r, target_c)
                return

    def execute_bot_attack(self, bot, attack_r, attack_c, target_r, target_c):
        play_sound('attack')
        attack_cell = self.board[attack_r][attack_c]
        target_cell = self.board[target_r][target_c]

        if target_cell.owner is None:
            target_cell.owner = bot
            target_cell.power = attack_cell.power - 1
            attack_cell.power = 1
            bot.score += 1
            self.log_text.append(f"{bot.name} захватил клетку ({target_r},{target_c})")
        elif target_cell.owner and attack_cell.power > target_cell.power:
            old = target_cell.owner
            old.score -= 1
            target_cell.owner = bot
            target_cell.power = attack_cell.power - target_cell.power
            attack_cell.power = 1
            bot.score += 1
            self.log_text.append(f"{bot.name} захватил клетку у {old.name}")

        self.board_widget.show_attack_anim(attack_r, attack_c, target_r, target_c)
        self.check_game_end()
        self.update_ui()

    def bot_energy(self, bot):
        if bot.energy > 0:
            own_cells = [(r, c) for r, c in self.board_shape
                         if self.board[r][c].owner == bot]
            if own_cells:
                weak = min(own_cells, key=lambda pos: self.board[pos[0]][pos[1]].power)
                self.board[weak[0]][weak[1]].power += bot.energy
                self.log_text.append(f"{bot.name} усилил клетку ({weak[0]},{weak[1]})")
                bot.energy = 0

    def end_turn(self):
        if not self.game_active:
            return

        self.cur_player = (self.cur_player + 1) % len(self.players)
        self.turn_num += 1
        self.sel_attack = None
        self.sel_target = None
        self.phase = "attack"

        for player in self.players:
            player.got_energy = False

        if self.turn_num >= self.max_turns:
            self.game_end()
            return

        self.log_text.append(f"--- Ход {self.turn_num} ---")
        self.update_ui()

        if self.get_current_player().type == "bot":
            QTimer.singleShot(BOT_TURN_DELAY, self.bot_turn)

    def check_game_end(self):
        active_players = set()
        for r, c in self.board_shape:
            cell = self.board[r][c]
            if cell.owner and cell.power > 0:
                active_players.add(cell.owner)

        if len(active_players) == 1:
            winner = active_players.pop()
            self.game_end_early(winner)
            return True
        return False

    def game_end_early(self, winner):
        self.game_active = False
        self.log_text.append(f"🎉 {winner.name} захватил все клетки!")

        for player in self.players:
            result = "Победа" if player == winner else "Поражение"
            self.db_man.save_game(player.name, player.score, self.turn_num, result)

        result_text = "=== ИГРА ОКОНЧЕНА ===\n"
        result_text += f"После {self.turn_num} ходов:\n"
        for plr in sorted(self.players, key=lambda x: x.score, reverse=True):
            result_text += f"{plr.name}: {plr.score} очков\n"
        result_text += f"\n🏆 Победитель: {winner.name}!"
        self.log_text.append(result_text)

        stop_music()
        play_sound('win')

        msg = QMessageBox()
        msg.setWindowTitle("Конец игры")
        msg.setText(f"Игра завершена!\n{winner.name} побеждает с {winner.score} очками!")
        msg.exec()

    def game_end(self):
        self.game_active = False
        winner = max(self.players, key=lambda p: p.score)

        for player in self.players:
            result = "Победа" if player == winner else "Поражение"
            self.db_man.save_game(player.name, player.score, self.turn_num, result)

        result_text = "=== ИГРА ОКОНЧЕНА ===\n"
        result_text += f"После {self.turn_num} ходов:\n"
        for plr in sorted(self.players, key=lambda x: x.score, reverse=True):
            result_text += f"{plr.name}: {plr.score} очков\n"
        result_text += f"\n🏆 Победитель: {winner.name}!"
        self.log_text.append(result_text)

        stop_music()
        play_sound('win')

        msg = QMessageBox()
        msg.setWindowTitle("Конец игры")
        msg.setText(f"Игра завершена!\n{winner.name} побеждает с {winner.score} очками!")
        msg.exec()

    def check_achievement(self, player):
        if player.score >= 10 and "Первопроходец" not in player.achievements:
            player.achievements.append("Первопроходец")
            self.db_man.save_achievement(player.name, "Первопроходец")
            self.log_text.append("🎖️ Достижение: Первопроходец")

    def update_ui(self):
        if not self.game_active:
            return
        player = self.get_current_player()
        if self.phase == "attack":
            self.phase_label.setText("⚔️ Фаза атаки")
            self.board_widget.attack_cells = self.get_attack_cells(player)
        elif self.phase == "nrg":
            self.phase_label.setText("🎲 Фаза энергии")
            self.board_widget.attack_cells = set()
        self.energy_label.setText(f"⚡ Энергия: {player.energy}")
        self.turn_label.setText(f"📊 Ход: {self.turn_num}/{self.max_turns}")
        scores = " | ".join([f"{plr.name}: {plr.score}" for plr in self.players])
        self.score_label.setText(f"🏆 Счёт: {scores}")
        self.board_widget.sel_attack = self.sel_attack
        self.board_widget.sel_target = self.sel_target
        is_human = player.type == "human"
        has_both = bool(self.sel_attack and self.sel_target)

        can_attack = is_human and self.phase == "attack" and has_both and not player.got_energy
        can_get_energy = is_human and self.phase == "attack" and not player.got_energy
        can_end_turn = is_human

        self.attack_btn.setEnabled(can_attack)
        self.energy_btn.setEnabled(can_get_energy)
        self.end_btn.setEnabled(can_end_turn)

        self.board_widget.update_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(10)  # Увеличим базовый размер шрифта
    app.setFont(font)
    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    app.setPalette(dark_palette)

    try:
        game = InfluenceGame()
        game.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        QMessageBox.critical(None, "Ошибка", f"Произошла критическая ошибка: {str(e)}")