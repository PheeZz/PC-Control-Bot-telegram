import platform
import os
from webbrowser import get
import yaml
import datetime
from loguru import logger


# Update = Discord
apps = ('steam', 'Overwolf', 'dota2', 'csgo',
        'Telegram', 'Discord.lnk', 'EpicGamesLauncher')


def get_Datetime():
    now = datetime.datetime.now()
    pretty_str = now.strftime("%d.%m.%Y_%H.%M.%S")
    return pretty_str


# create logger
logger.add(f"logs/{get_Datetime()}.log", rotation='1 day', level="DEBUG")


def find_path(name, path="\\"):
    for dirpath, dirname, filenames in os.walk(path):
        if name in filenames:
            return os.path.join(dirpath, name)


def get_path_info():
    try:
        with open('settings.yaml', 'r') as stream:
            pass
    except FileNotFoundError:
        with open('settings.yaml', 'w+') as stream:
            stream.write('{}')
    finally:
        with open('settings.yaml', 'r') as stream:
            try:
                paths = yaml.full_load(stream)
                logger.info("Paths from .yaml loaded successfully")
            except yaml.YAMLError as exc:
                logger.error(exc)
    return paths


def set_path_info(data):
    if not get_path_info():
        settings = {}
    else:
        settings = get_path_info()
    settings.update(data)
    with open('settings.yaml', 'w+') as outfile:
        yaml.dump(settings, stream=outfile)


def find_app_path(app):
    drives = ('C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\')
    try:
        for drive in drives:
            if app == 'Discord.lnk':
                path = find_path(app, path=drive)
            else:
                path = find_path(f'{app}.exe', path=drive)
            if path:
                break
        path = "\"" + path + "\""
        adder = {app.lower(): path}
        logger.info(f"{app} path found successfully")
        logger.info(adder)
        return adder
    except:
        logger.error(f"{app} not found")


def set_paths():
    for app in apps:
        set_path_info(find_app_path(app))


def check_for_values_in_path():
    try:
        if len(apps) > len(get_path_info()):
            set_paths()
    except TypeError:
        set_paths()


if __name__ == '__main__':
    set_paths()
