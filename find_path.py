import os
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


def find_path(name: str, path='C:\\'):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


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


def set_path_info(data: dict):
    if not get_path_info():
        settings = dict()
    else:
        settings = get_path_info()
    if type(data) is dict:
        settings.update(data)
        with open('settings.yaml', 'w+') as outfile:
            yaml.dump(settings, stream=outfile)


def find_app_path(app: str):
    drives = ('C:\\', 'D:\\', 'E:\\', 'F:\\')
    if app not in get_path_info():
        for drive in drives:
            try:
                if app == 'Discord.lnk':
                    path = find_path(app, drive)
                else:
                    path = find_path(f'{app}.exe', drive)
                if path is not None:
                    logger.info(f"{app} path found successfully: {path}")
                    path = "\"" + path + "\""
                    adder = {app.lower(): path}
                    logger.info(f"{app} path found successfully")
                    logger.info(adder)
                    return adder
            except:
                logger.error(f"{app} not found")
                return {app: '""'}


def set_paths():
    for app in apps:
        set_path_info(find_app_path(app))


def check_for_values_in_path():

    if len(apps) > len(get_path_info()):
        set_paths()


if __name__ == '__main__':
    set_paths()
