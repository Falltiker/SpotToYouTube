from Selenium_template_Chrome import *
from bs4 import BeautifulSoup as BS
import time
import csv


def main(url):

    file_name = "tracks.csv"

    url = "https://open.spotify.com/collection/tracks"

    # Создаем веб-драйвер
    driver = create_driver(False)

    # Логинимся, если будем парсить любимые треки
    if url == "https://open.spotify.com/collection/tracks":

        driver.get("https://accounts.spotify.com/ru/login")

        # Используем ожидания, чтобы убедиться, что элементы готовы к взаимодействию
        input_login = find_element(driver, By.ID, "login-username")
        input_login.send_keys(login)
        input_password = find_element(driver, By.ID, "login-password")
        input_password.send_keys(password)

        button_finish = find_element(driver, By.ID, "login-button")
        move_to_element_click(driver, button_finish)
        print("Регистрация прошла успешно!")
        time.sleep(5) 

    # Переходим к плейлисту
    driver.get(url)
    time.sleep(5)

    # Уникальные треки
    track_list = list()

    # Условие выхода из цикла
    max_attempts = 5  # Число попыток, при которых новых треков не найдено
    attempt = 0

    while attempt < max_attempts:
        # Находим все видимые элементы треков
        tracks = driver.find_elements(By.XPATH, "/html/body/div[4]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[4]/div/div[2]/div[2]/div")
        # print(f"Найдено {len(tracks)} видимых треков.")

        # Обрабатываем каждый трек
        for track in tracks:
            try:
                # Получаем HTML трека
                res = track.get_attribute('outerHTML')
                soup = BS(res, "lxml")
                track_name = soup.find("a").find("div").text.strip()
                track_group = soup.find_all("a")[-1].text.strip()
                track_temp = [track_name, track_group]
                # Добавляем трек, если его еще нет
                if track_temp not in track_list:
                    # print(f"Добавлен новый трек: {track_temp}")
                    track_list.append(track_temp)
                    attempt = 0  # Сброс попыток, так как нашли новый трек
                else:
                    # print(f"Трек уже в списке: {soup}")
                    pass
            except Exception as e:
                # print(f"Ошибка при обработке трека: {e}")
                pass

        # Прокручиваем к последнему видимому элементу
        if tracks:
            try:
                last_track = tracks[-1]
                scroll_to_page(driver, last_track)
                # print("Проскролили к последнему элементу.")
            except Exception as e:
                # print(f"Ошибка при скролле к последнему треку: {e}")
                pass
        else:
            # print("Нет видимых треков для скролла.")
            pass

        time.sleep(1)  # Ждем подгрузку новых треков
        attempt += 1  # Увеличиваем число попыток, если новых треков не найдено

    print(f"Собрано {len(track_list)} уникальных треков.")
    # print(track_list)

    with open(file_name, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Track", "Group"])
        writer.writerows(track_list)

    print(f"==========Список успешно сохранён в файл {file_name}===========")

    driver.quit()



if __name__ == "__main__":
    main("https://open.spotify.com/collection/tracks")