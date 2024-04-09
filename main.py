import requests
import time
import telethon
from telethon.sync import TelegramClient
from yandex_music import Client
from yandex_music.exceptions import NetworkError

# сюда вся инфа ###
api_id = ''
api_hash = ''
phone_number = ''
music_token = ''
stock_bio = ''
###################

client_tele = TelegramClient('my_account', api_id, api_hash)
client_music = Client(music_token).init()

default = ''

count = 0
wave = False

async def main():
    global default, count, wave
    try:
        wave = False
        queues = client_music.queues_list()
        try:
            last_queue = client_music.queue(queues[0].id)
        except TypeError:
            print("Ошибка при получении очереди, это нормально для моей волны")
            async with client_tele:
                await client_tele(telethon.tl.functions.account.UpdateProfileRequest(
                    about=f"{stock_bio}"
                ))
            return
        last_track_id = last_queue.get_current_track()
        last_track = last_track_id.fetch_track()
        artists = ', '.join(last_track.artists_name())
        title = last_track.title
        if default != title:
            default = title
            async with client_tele:
                if len(f"{artists} - {title}") > 50:
                    if len("{stock_bio}" + " | " + title) > 50:
                        about_text = "{stock_bio}"
                    else:
                        about_text = f"{stock_bio} | listening: {title}"
                else:
                    about_text = f"{stock_bio} | listening: {title} - {artists}"
                await client_tele(telethon.tl.functions.account.UpdateProfileRequest(about=about_text))
        else:
            if count < 5:
                count += 1
            else:
                count = 0
                async with client_tele:
                    await client_tele(telethon.tl.functions.account.UpdateProfileRequest(
                        about=f"{stock_bio}"
                    ))
    except (IndexError, telethon.errors.AboutTooLongError):
        if wave:
            pass
        else:
            wave = True
            async with client_tele:
                await client_tele(telethon.tl.functions.account.UpdateProfileRequest(
                    about=f"{stock_bio}"
                ))

inte = 0

# чекер соединения
def check_internet():
    url = 'http://www.ya.ru/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print('Нет подключения к интернету. Ожидание восстановления подключения...')
        return False

# В основном цикле:
while True:
    print(inte)
    inte = inte + 1
    if check_internet():
        try:
            with client_tele:
                client_tele.loop.run_until_complete(main())
        except NetworkError:
            print('Произошла ошибка сети. Перезапуск через 30 секунд...')
            time.sleep(30)
            continue
    time.sleep(60)
