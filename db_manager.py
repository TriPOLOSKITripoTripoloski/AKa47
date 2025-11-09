import sqlite3
from datetime import datetime
import csv


class DBManager:
    """Менеджер статистики игр - работает с game_stats.db"""

    def __init__(self, db_name='game_stats.db'):
        self.db_name = db_name
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

    def get_game_settings(self):
        """Получение настроек игры"""
        try:
            self.cur.execute('SELECT * FROM game_settings')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения настроек: {e}")
            return []

    def save_game_setting(self, setting_name, setting_value, description=""):
        """Сохранение настройки игры"""
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