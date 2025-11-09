from constants import BOARD_SIZES, DIFFICULTY_LEVELS, BOARD_SHAPES


class Settings:
    def __init__(self):
        self.difficulty_levels = {
            "Лёгкая": {
                "bot_names": ["Новичок", "Ученик", "Стажер", "Рекрут", "Кадет"],
                "bot_intelligence": 0.3
            },
            "Средняя": {
                "bot_names": ["Стратег", "Тактик", "Ветеран", "Командир", "Офицер"],
                "bot_intelligence": 0.6
            },
            "Сложная": {
                "bot_names": ["Мастер", "Гуру", "Эксперт", "Профи", "Ас"],
                "bot_intelligence": 0.8
            },
            "Эксперт": {
                "bot_names": ["Легенда", "Титан", "Гений", "Виртуоз", "Маэстро"],
                "bot_intelligence": 0.95
            }
        }

        self.board_sizes = BOARD_SIZES
        self.board_shapes = BOARD_SHAPES