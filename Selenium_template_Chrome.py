# Шаблон для удобного использования селениума
# Пока что библиотека selenium_stealth мне только мешала
# Из за неё сайты воспринимали браузер как автоматизированое ПО



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium_stealth import stealth
import subprocess
import logging
import random
import socket
import time
import shutil
import os




def create_driver(
    headless=False,
    defence=False,
    chrome_path=r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
    start_maximized=False,
    log_lvl=0,
    disable_images=False,
    webnotifications=True,
    use_stealth=True,
    port=9222,
    user_data_dir=None,
    profile=None
):
    """Создает драйвер для Chrome с заданными параметрами."""

    logging.info(f"Начало создания драйвера с параметрами: headless={headless}, defence={defence}, "
                 f"chrome_path={chrome_path}, start_maximized={start_maximized}, log_lvl={log_lvl}, "
                 f"disable_images={disable_images}, webnotifications={webnotifications}, use_stealth={use_stealth}, "
                 f"port={port}, user_data_dir={user_data_dir}, profile={profile}")

    if not os.path.exists(chrome_path.replace('"', '')):
        logging.error(f"Неверный путь к Chrome: {chrome_path}. Укажите правильный путь к браузеру Google Chrome.")
        raise FileNotFoundError(f"Неверный путь к Chrome: {chrome_path}. Укажите путь к браузеру Google Chrome.")
    
    logging.info("Путь к Chrome проверен и корректен.")

    def check_port(port, host="127.0.0.1"):
        """Проверяет, свободен ли порт."""
        logging.debug(f"Проверка порта {port} на доступность.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                logging.debug(f"Порт {port} свободен.")
                return True
            except socket.error:
                logging.debug(f"Порт {port} занят.")
                return False

    def find_free_port(start_port=9222, host="127.0.0.1"):
        """Ищет свободный порт, начиная с указанного."""
        logging.debug(f"Поиск свободного порта начиная с {start_port}.")
        port = start_port
        while not check_port(port, host):
            port += 1
        logging.info(f"Найден свободный порт: {port}.")
        time.sleep(2)  # Даем время на освобождение порта
        return port

    def create_chrome_bat(port, user_data_dir, profile, headless, defence, start_maximized, log_lvl, disable_images, webnotifications):
        """Создает бат-файл для запуска Chrome."""
        logging.info("Создание бат-файла для запуска Chrome.")
        
        bat_content = f'{chrome_path} --remote-debugging-port={port}'

        if user_data_dir:
            bat_content += f'  --user-data-dir="{user_data_dir}"'
            logging.debug(f"Добавлен параметр user_data_dir: {user_data_dir}")

        if profile:
            bat_content += f' --profile-directory="{profile}"'
            logging.debug(f"Добавлен параметр profile: {profile}")

        if headless:
            bat_content += " --headless --disable-gpu --disable-dev-shm-usage"
            logging.debug("Добавлены параметры для запуска Chrome в headless-режиме.")

        if start_maximized:
            bat_content += " --start-maximized"
            logging.debug("Добавлен параметр для запуска Chrome в развернутом окне.")

        if log_lvl == 0:
            bat_content += " --log-level=0" 
            logging.debug("Установлен уровень логирования: только критические ошибки.")
        elif log_lvl == 1:
            bat_content += " --log-level=2" 
            logging.debug("Установлен уровень логирования: только ошибки..")
        elif log_lvl == 2:
            bat_content += " --log-level=2" 
            logging.debug("Установлен уровень логирования: ошибки и предупреждения.")
        elif log_lvl == 3:
            bat_content += " --log-level=3" 
            logging.debug("Установлен уровень логирования: все сообщения.")
        else:
            logging.warning("Неизвестный уровень логирования, параметры по умолчанию.")

        if disable_images:
            bat_content += ' --disable-images'
            logging.debug("Отключены изображения в браузере.")

        if webnotifications:
            bat_content += ' --disable-notifications'
            logging.debug("Отключены веб-уведомления в браузере.")

        if defence:
            bat_content += " --excludeSwitches=enable-automation --disable-extensions --disable-infobars --disable-popup-blocking --no-sandbox --disable-web-security --disable-blink-features=AutomationControlled"
            logging.debug("Добавлены параметры защиты от автоматизации.")

        bat_file = "start_chrome.bat"
        logging.info(f"Сохраняем бат-файл в {bat_file}.")
        with open(bat_file, "w") as file:
            file.write(bat_content)

        logging.info(f"Бат-файл {bat_file} успешно создан.")
        return bat_file

    # Найдем свободный порт
    port = find_free_port(start_port=port)

    # Создадим бат-файл и запустим его
    bat_file = create_chrome_bat(port, user_data_dir, profile, headless, defence, start_maximized, log_lvl, disable_images, webnotifications)
    
    logging.info(f"Запуск бат-файла: {bat_file}")
    subprocess.Popen([bat_file], shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w')) # Такая команда не выводит ничего в консоль
    time.sleep(5)  # Задержка для корректной инициализации браузера
    logging.info("Браузер Chrome успешно запущен.")

    # Инициализация драйвера
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    logging.info(f"Настройка драйвера с использованием порта {port}.")
    
    try:
        driver = webdriver.Chrome(options=options)
        logging.info("Драйвер Chrome успешно инициализирован.")
    except Exception as e:
        logging.error(f"Ошибка при инициализации драйвера: {e}")
        raise

    # Удаление следов WebDriver
    if defence:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        logging.info("Следы WebDriver удалены.")

    logging.info("Драйвер успешно создан и возвращен.")
    return driver





# Поиск элемента с ожиданием
def find_element(driver, by, value, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )





# Клик с движение мыши
def move_to_element_click(driver, element, click=True):
    actions = ActionChains(driver)
    for _ in range(random.randint(3, 8)):
        x_offset = random.randint(-20, 20)
        y_offset = random.randint(-20, 20)
        actions.move_to_element_with_offset(element, x_offset, y_offset).perform()
        time.sleep(random.uniform(0.1, 0.2))
    actions.move_to_element(element).perform()
    if click:
        actions.click().perform()





# Прокрутка к элементу или в конец страницы
def scroll_to_page(driver, element=None, delay_range=(1, 2)):
    if element:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", element)
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(*delay_range))