import telebot
from telebot import types
import find_path as fp
import configparser
import launch_apps as la
from time import time


def get_TOKEN():
    config = configparser.ConfigParser()
    config.read('telegram.ini')
    return config['DEFAULT']['TOKEN']


def get_ADMIN_ID():
    config = configparser.ConfigParser()
    config.read('telegram.ini')
    return int(config['DEFAULT']['ADMIN_ID'])


def check_exist_path_app():  # now unusable by modify find_app_path() and set_path_info() fuctions
    paths = fp.get_path_info()
    exist = {key: value for (key, value) in paths.items() if len(value) >= 5}
    return exist


def get_apps_launch_buttons():
    exist_apps = check_exist_path_app()
    buttons_names = list()
    buttons_names.append(types.KeyboardButton("🪄Игровой протокол🪄"))
    if 'steam' in exist_apps:
        buttons_names.append(types.KeyboardButton('♨️Steam✅'))
    if 'discord.lnk' in exist_apps:
        buttons_names.append(types.KeyboardButton('👾Discord✅'))
    if 'dota2' in exist_apps:
        buttons_names.append(types.KeyboardButton('👨🏽‍❤️‍💋‍👨🏽Dota 2✅'))
    if 'csgo' in exist_apps:
        buttons_names.append(types.KeyboardButton('🚮CS:GO✅'))
    if 'telegram' in exist_apps:
        buttons_names.append(types.KeyboardButton('📱Telegram✅'))
    if 'overwolf' in exist_apps:
        buttons_names.append(types.KeyboardButton('🐺Overwolf✅'))
    if 'epicgameslauncher' in exist_apps:
        buttons_names.append(types.KeyboardButton('🎮Epic Games Launcher✅'))
    buttons_names.append(types.KeyboardButton('🔙Back'))

    return buttons_names


def get_apps_close_buttons():
    exist_apps = check_exist_path_app()
    buttons_names = list()
    if 'steam' in exist_apps and la.is_running('steam'):
        buttons_names.append(types.KeyboardButton('♨️Steam❌'))

    if 'discord.lnk' in exist_apps and la.is_running('discord.lnk'):
        buttons_names.append(types.KeyboardButton('👾Discord❌'))

    if 'dota2' in exist_apps and la.is_running('dota2'):
        buttons_names.append(types.KeyboardButton('👨🏽‍❤️‍💋‍👨🏽Dota 2❌'))

    if 'csgo' in exist_apps and la.is_running('csgo'):
        buttons_names.append(types.KeyboardButton('🚮CS:GO❌'))

    if 'telegram' in exist_apps and la.is_running('telegram'):
        buttons_names.append(types.KeyboardButton('📱Telegram❌'))

    if 'epicgameslauncher' in exist_apps and la.is_running('epicgameslauncher'):
        buttons_names.append(types.KeyboardButton('🎮Epic Games Launcher❌'))

    buttons_names.append(types.KeyboardButton('🔙Back'))

    return buttons_names


# create a bot
bot = telebot.TeleBot(get_TOKEN())
bot.set_my_commands(
    commands=[  # types.BotCommand(command='/help', description='show help message'),
        types.BotCommand(command='/update', description='update paths to applications in filesystem'), ])


def markup_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton("📲Запуск приложений"),
               types.KeyboardButton("💀Закрытие приложений"),
               types.KeyboardButton("👁️Скриншот"),)
    for button in buttons:
        markup.add(button)
    return markup


@bot.message_handler(commands=['start', 'update'])
def hello_message(message):
    if message.from_user.id == get_ADMIN_ID():
        bot.send_message(chat_id=message.chat.id,
                         text="Привет, сейчас я найду все необходимые приложения на твоем компьютере и подключу их к телеграму! Это займет некоторое время, в зависимости от скорости твоего диска, подожди немного)")

        bot.send_message(chat_id=message.chat.id,
                         text='Начинаю поиск...')
        start = time()
        fp.check_for_values_in_path()
        bot.send_message(chat_id=message.chat.id,
                         text=f'Поиск завершен за {int(time() - start)} секунд(-ы)! Я готов к работе!')

        bot.send_message(
            message.chat.id, text="Что будем делать?", reply_markup=markup_main_menu())


@bot.message_handler(content_types=['text'])
def asnwer_message(message):
    if message.from_user.id == get_ADMIN_ID():
        if message.text == "📲Запуск приложений":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button in get_apps_launch_buttons():
                markup.add(button)
            bot.send_message(
                message.chat.id, text="Что запускаем?", reply_markup=markup)
        if message.text == '💀Закрытие приложений':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button in get_apps_close_buttons():
                markup.add(button)
            bot.send_message(
                message.chat.id, text="Что закрываем?", reply_markup=markup)
        if message.text == '👁️Скриншот':
            bot.send_photo(message.chat.id, la.pag.screenshot())

    match message.text:
        case '🔙Back':
            bot.send_message(
                message.chat.id, text="Что будем делать?", reply_markup=markup_main_menu())
        case '♨️Steam✅':
            la.launch_app('steam')
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n♨️Steam")
        case '👾Discord✅':
            la.launch_app('discord.lnk')
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n👾Discord")
        case '👨🏽‍❤️‍💋‍👨🏽Dota 2✅':
            la.launch_steam_game('dota2')
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n👨🏽‍❤️‍💋‍👨🏽Dota 2")
        case '🚮CS:GO✅':
            la.launch_steam_game('csgo')
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n🚮CS:GO")
        case '📱Telegram✅':
            la.launch_app('telegram')
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n📱Telegram")
        case '🐺Overwolf✅':
            la.launch_overwolf()
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n🐺Overwolf")
        case '🎮Epic Games Launcher✅':
            la.launch_app('epicgameslauncher')
            bot.send_message(
                message.chat.id, text=f"Приступаю к запуску\n🎮Epic Games Launcher")
        case '🪄Игровой протокол🪄':
            la.game_protocol()

        case '♨️Steam❌':
            la.terminate('steam', bot, message)
            bot.send_message(
                message.chat.id, text=f"Приступаю к закрытию\n♨️Steam")
        case '👾Discord❌':
            la.terminate('Discord', bot, message)
            bot.send_message(
                message.chat.id, text="Приступаю к закрытию\n👾Discord")
        case '👨🏽‍❤️‍💋‍👨🏽Dota 2❌':
            la.terminate('dota2', bot, message)
            bot.send_message(
                message.chat.id, text="Приступаю к закрытию\n👨🏽‍❤️‍💋‍👨🏽Dota 2")
        case '🚮CS:GO❌':
            la.terminate('csgo', bot, message)
            bot.send_message(
                message.chat.id, text="Приступаю к закрытию\n🚮CS:GO")
        case '📱Telegram❌':
            la.terminate('Telegram', bot, message)
            bot.send_message(
                message.chat.id, text="Приступаю к закрытию\n📱Telegram")
        case '🎮Epic Games Launcher❌':
            la.terminate('EpicGamesLauncher', bot, message)
            bot.send_message(
                message.chat.id, text="Приступаю к закрытию\n🎮Epic Games Launcher")


@fp.logger.catch
def start_bot():
    bot.send_animation(get_ADMIN_ID(), caption='🟢Online',
                       animation='https://tenor.com/bg6ns.gif')
    bot.polling(none_stop=True)


start_bot()
