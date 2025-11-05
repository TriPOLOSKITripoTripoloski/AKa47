import PyInstaller.__main__
import os
import shutil


def build_app():
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    args = [
        'main.py',
        '--onefile',
        '--windowed',
        '--name=InfluenceGame',
        '--add-data=sounds;sounds',
        '--add-data=config.py;.',
        '--add-data=settings.py;.',
        '--add-data=db_manager.py;.',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=pygame',
        '--collect-all=pygame',
        '--clean',
        '--noconfirm'
    ]

    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')

    try:
        PyInstaller.__main__.run(args)
        print("УСПЕХ: Сборка завершена успешно!")

        sounds_dist = os.path.join('dist', 'sounds')
        if os.path.exists(sounds_dist):
            sound_files = os.listdir(sounds_dist)
            print(f"Звуковые файлы скопированы: {len(sound_files)} файлов")
        else:
            print("ПРЕДУПРЕЖДЕНИЕ: Папка sounds не скопирована!")

        print("EXE-файл: dist\\InfluenceGame.exe")
    except Exception as e:
        print(f"ОШИБКА: {e}")


if __name__ == '__main__':
    build_app()