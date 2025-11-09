from constants import PLAYER_COLORS, MAX_TURNS_DEFAULT, BOARD_DIMENSION, MIN_DISTANCE_BETWEEN_BASES, SCREEN_SIZES, \
    AVAILABLE_RESOLUTIONS


class Config:
    MAX_TURNS = MAX_TURNS_DEFAULT
    BOARD_SIZE = BOARD_DIMENSION
    MIN_DISTANCE_BETWEEN_BASES = MIN_DISTANCE_BETWEEN_BASES
    SOUND_VOLUME = 0.4
    MUSIC_VOLUME = 0.4
    DB_NAME = 'game_data.db'
    PLAYER_COLORS = PLAYER_COLORS
    SCREEN_RESOLUTION = "Автоопределение"  # По умолчанию автоопределение
    SCREEN_SIZES = SCREEN_SIZES
    AVAILABLE_RESOLUTIONS = AVAILABLE_RESOLUTIONS

    @classmethod
    def get_screen_constants(cls, resolution=None):
        """Получить константы для выбранного разрешения"""
        if resolution is None:
            resolution = cls.SCREEN_RESOLUTION

        if resolution == "Автоопределение":
            # Автоопределение разрешения экрана
            try:
                from PyQt6.QtWidgets import QApplication
                app = QApplication.instance()
                if app:
                    screen = app.primaryScreen()
                    size = screen.size()
                    screen_res = f"{size.width()}x{size.height()}"

                    # Ищем ближайшее доступное разрешение
                    available_sizes = {
                        "1366x768": (1366, 768),
                        "1600x900": (1600, 900),
                        "1920x1080": (1920, 1080)
                    }

                    best_match = "default"
                    min_diff = float('inf')

                    for res_name, res_size in available_sizes.items():
                        diff = abs(size.width() - res_size[0]) + abs(size.height() - res_size[1])
                        if diff < min_diff:
                            min_diff = diff
                            best_match = res_name

                    return cls.SCREEN_SIZES.get(best_match, cls.SCREEN_SIZES["default"])
            except:
                pass

            return cls.SCREEN_SIZES["default"]
        else:
            return cls.SCREEN_SIZES.get(resolution, cls.SCREEN_SIZES["default"])