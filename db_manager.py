import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self, db_name='game_data.db'):
        self.db_name = db_name
        self.conn = None
        self.cur = None
        self.init_db()

    def init_db(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Ошибка инициализации БД: {e}")

    def create_tables(self):
        tables = [
            '''CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                color TEXT,
                created_date TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY,
                player_name TEXT,
                score INTEGER,
                turns INTEGER,
                game_date TEXT,
                result TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY,
                player_name TEXT,
                achievement TEXT,
                achieved_date TEXT
            )'''
        ]

        for table in tables:
            try:
                self.cur.execute(table)
            except sqlite3.Error as e:
                print(f"Ошибка создания таблицы: {e}")

        self.conn.commit()

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

    def save_game(self, pname, score, turns, result):
        try:
            if not isinstance(pname, str) or not pname.strip():
                pname = "Игрок"
            else:
                pname = ''.join(char for char in pname if char.isalnum() or char.isspace())
                if not pname:
                    pname = "Игрок"

            if result not in ["Победа", "Поражение"]:
                result = "Неизвестно"

            self.cur.execute(
                'INSERT INTO game_stats (player_name, score, turns, game_date, result) VALUES (?, ?, ?, ?, ?)',
                (pname, score, turns, datetime.now().isoformat(), result)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения игры: {e}")
            return False

    def save_achievement(self, pname, achievement):
        try:
            self.cur.execute(
                'INSERT INTO achievements (player_name, achievement, achieved_date) VALUES (?, ?, ?)',
                (pname, achievement, datetime.now().isoformat())
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения достижения: {e}")
            return False

    def get_stats(self):
        try:
            self.cur.execute('SELECT * FROM game_stats ORDER BY score DESC LIMIT 10')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения статистики: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()