import pyautogui as pag
import find_path as fp
from time import sleep
from os import startfile
import threading
import pygetwindow as gw
import webbrowser as webbr
from os import system

steam_game_ids = {'dota2': 570, 'csgo': 730}

# function to find the button on the screen


def get_image_coordinates(img, gray=True):
    try:
        coordinates = pag.locateCenterOnScreen(
            img, grayscale=gray, confidence=0.8)
        if coordinates is None:
            fp.logger.warning(f"{img} not found")
        else:
            fp.logger.info(
                f"{img} coordinates found successfully: {coordinates}")
            return coordinates
    except Exception as e:
        fp.logger.error(e)
        return False


def click_button(img):
    is_none = True
    while is_none:
        try:
            x, y = get_image_coordinates(img)
            if x is not None:
                pag.moveTo(x, y)
                sleep(0.05)
                pag.click()
                is_none = False
        except Exception as e:
            fp.logger.error(e)
            sleep(0.5)
    fp.logger.info(f"{img} clicked successfully")


def launch_thread(app):  # в threading.Thread нельзя передать длинный неитерируемый объект, т.е путь (костыль, че сказать)
    startfile(fp.get_path_info()[app])


def launch_app(app):
    path = fp.get_path_info()[app]
    if app == 'discord.lnk':
        threading.Thread(target=launch_thread, args=(('discord.lnk',))).start()
    elif app == 'telegram':
        threading.Thread(target=launch_thread, args=(('telegram',))).start()
    else:
        pag.hotkey('win', 'r')
        pag.write(path)
        pag.hotkey('enter')


def launch_steam_game(game):
    game_id = steam_game_ids[game]
    pag.hotkey('win', 'r')
    pag.write(f'steam://rungameid/{game_id}')
    pag.hotkey('enter')


def game_protocol():
    webbr.open_new_tab('https://music.yandex.ru/home')
    not_music_started = True
    while not_music_started:
        try:
            if len(gw.getWindowsWithTitle('Музыка')) != 0:
                gw.getWindowsWithTitle('Музыка')[0].activate()
                while not get_image_coordinates('assets/browser/pause_wave.png'):
                    click_button('assets/browser/my_wave.png')
                    pag.move(0, 50)
                    sleep(1)
                not_music_started = False
                gw.getActiveWindow().minimize()
        except Exception as e:
            fp.logger.error(e)
            sleep(0.5)

    launch_app('steam')
    launch_app('discord.lnk')
    try:
        gw.getWindowsWithTitle('steam')[0].minimize()
        gw.getWindowsWithTitle('discord.lnk')[0].minimize()
    except Exception as e:
        fp.logger.error(e)


def launch_overwolf():
    '''
    запуск доты через овервульф
    '''
    launch_app('overwolf')
    while(True):
        try:
            gw.getWindowsWithTitle('overwolf')[0].activate()
            click_button('assets/overwolf/login.png')
            click_button('assets/overwolf/launch.png')
            break
        except Exception as e:
            fp.logger.error(e)


def terminate(app, bot, message):
    if app == 'Discord.lnk':
        app = 'Discord'
    try:
        system(f'taskkill /f /im {app}.exe')
    except Exception as e:
        fp.logger.error(e)
        bot.send_message(message.chat.id, 'Не удалось завершить приложение')


def accept_game():
    '''
    автопринятие каточки
    '''
    click_button('assets/dota2/accept.png')
