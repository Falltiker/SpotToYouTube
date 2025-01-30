import logging
import os
from Selenium_template_Chrome import *


# Настройка логирования
logging.basicConfig(
    filename="debug.log",         # Логирование в файл debug.log
    level=logging.INFO,          # Уровень логирования DEBUG (записывает все сообщения)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения (включает время, уровень и текст)
    encoding="utf-8",  # Указываем кодировку UTF-8
    filemode='w'
)


# Config
workspace_path = os.path.join(os.path.dirname(__file__), "user data") # Папка для хранения профилей браузера



def verification_user_login(spotify_playlist):
    logging.info("Запуск функции verification_user_login().")
    
    # Проверяем авторизован ли пользователь на сайтах
    # Если ссылка ведет на лайкнутые треки, добавляем проверку
    verification_spotify = False
    if spotify_playlist.lower() == "https://open.spotify.com/collection/tracks":
        verification_spotify = True
        logging.info("Проверка на Spotify: ссылка на лайкнутые треки сработала.")
    else:
        logging.info("Ссылка на Spotify не совпала с лайкнутыми треками.")

    spotify_sing_up = True
    spotify_name = None
    ytmusic_sing_up = False
    ytmusic_name = None

    try:
        logging.info("Запуск браузера для проверки авторизации на сайтах.")
        driver = create_driver(headless=False, user_data_dir=workspace_path)
        logging.info("Браузер запущен и подключен")


        if verification_spotify:
            logging.info("Проверка авторизации на Spotify...")
            driver.get("https://open.spotify.com/collection/tracks")
            try:
                find_element(driver, By.XPATH, "/html/body/div[4]/div/div[2]/div[1]/div[3]/button/figure/div/img")
                logging.DEBUG("Аватарка пользователя найдено.")
                spotify_name = find_element(driver, 
                                            By.XPATH, 
                                            "/html/body/div[4]/div/div[2]/div[4]/div/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/div[1]/span/a",
                                            value=10)
                logging.DEBUG("Имя пользователя найдено.")
                spotify_sing_up = True
                logging.info("Пользователь успешно авторизован на Spotify.")
            except Exception as e:
                spotify_sing_up = False
                logging.error(f"Ошибка при проверке авторизации на Spotify: {e}")

        logging.info("Проверка авторизации на YouTube Music...")
        driver.get("https://music.youtube.com/")
        try:
            find_element(driver, By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[3]/ytmusic-settings-button/tp-yt-paper-icon-button/tp-yt-iron-icon/img")
            logging.DEBUG("Аватарка пользователя найдено.")
            ytmusic_name = find_element(driver, By.ID, "channel-handle", value=10)
            logging.DEBUG("Имя пользователя найдено.")
            ytmusic_sing_up = True
            logging.info("Пользователь успешно авторизован на YouTube Music.")
        except Exception as e:
            ytmusic_sing_up = False
            logging.error(f"Ошибка при проверке авторизации на YouTube Music: {e}")

        result = {
            "spotyfi": [spotify_sing_up, spotify_name],
            "ytmusic": [ytmusic_sing_up, ytmusic_name]
            }

        logging.info("Завершена проверка авторизации на платформах.")
        return result
    
    except:
        pass
    finally:
        driver.quit()
        logging.info("Браузер закрыт и завершен.")


def sing_up(spotyfi, ytmusic):
    logging.info("Запуск функции sing_up().")
    try:
        logging.info("Запуск браузера для регистрации на сайтах.")
        driver = create_driver(user_data_dir=workspace_path)
        logging.info("Браузер запущен и подключен")

        if not spotyfi:
            logging.info("Регистрация на Spotify...")
            driver.get("https://accounts.spotify.com/ru/login")
        if not ytmusic:
            logging.info("Регистрация на YouTube Music...")
            driver.get("https://music.youtube.com/")
    except:
        pass
    finally:
        driver.quit()
        logging.info("Браузер закрыт и завершен.")
    


def main():
    print("Программа копирует все треки с плейлиста Spotify в плейлист YouTube Music.\n"
        "Можно также и понравившиеся (лайкнутые) треки с Spotify перенести в плейлист или лайкнуть в YouTube Music.\n"
        "В YouTube Music придется зарегистрироваться в браузере, который предоставит программа.\n"
        "Если будете переносить понравившиеся треки со Spotify, то тоже придется зарегистрироваться и на этой платформе.")

    print("\n")

    print("Вставьте ссылку на плейлист (лайкнутые треки) Spotify (с которого будем копировать):")
    # spotify_playlist = input()
    spotify_playlist = "https://open.spotify.com/collection/tracks"
    logging.info(f"ССылка на плейлист Spotify: {spotify_playlist}")
    
    print("Вставьте ссылку на плейлист (лайкнутые треки) YouTube Music (куда копировать):")
    # ytmusic_playlist = input()
    # ytmusic_playlist = input()

    logging.info("Запуск проверки авторизации пользователей на сайтах.")
    result = verification_user_login(spotify_playlist)

    logging.info(f"Результаты проверки авторизации: {result}")
    
    if result["ytmusic"][0] or result["spotyfi"][0]:
        if result["ytmusic"][0]:
            print("Нужно войти в аккаунт YouTube Music.")
        if result["spotyfi"][0]:
            print("Нужно войти в аккаунт Spotify.")
        
        print("Сейчас будет запущен браузер, в котором нужно будет войти в аккаунт.")
        print("После входа закройте браузер.")


    logging.info("Завершение работы программы.")




if __name__ == "__main__":
    try:
        logging.info("Запуск программы.")
        main()
        logging.info("Программа завершила выполнение.")
    except:
        print("⚠️ Произошла ошибка.")
        print("Подробности в debug.log.")
        print("Отправьте пожалуйста файл debug.log на адрес ckbopec@gmail.com, спасибо.")
        print("Попробуйте перезапустить программу.")
    finally:
        logging.shutdown()