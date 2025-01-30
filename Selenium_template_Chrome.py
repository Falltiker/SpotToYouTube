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
import random
import socket
import time
import os



# Создаем драйвер
def create_driver(headless=True, defence=True, start_maximized=False, log_lvl=3, download_image=False, webnotifications=True, use_stealth=True):
    options = Options()

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu") 

    # Уровень логов
    if log_lvl == 0:
        pass
    elif log_lvl == 1:
        options.add_argument("--log_lvl-level=1")  # Показываются только ошибки
    elif log_lvl == 2:
        options.add_argument("--log_lvl-level=2")  # Ошибки и предупреждения
    elif log_lvl == 3:
        options.add_argument("--log_lvl-level=3")  # Только критические ошибки

    if start_maximized:
        options.add_argument("--start-maximized")

    if not download_image:
        prefs = {"profile.default_content_setting_values": {"images": 2}}
        options.add_experimental_option("prefs", prefs)

    if webnotifications:
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)

    if defence:
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # if use_stealth:
    #     stealth(
    #         driver,
    #         platform="Win32",
    #         fix_hairline=True
    #     )

    return driver




def create_driver_in_bat(
    headless=False,
    defence=True,
    chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
    start_maximized=True,
    log_lvl=3,
    download_image=True,
    webnotifications=False,
    use_stealth=True,
    port=9222,
    user_data_dir=None,
    profile_dir=None
):
    """Создает драйвер для Chrome с заданными параметрами."""

    if not os.path.exists(chrome_path.replace('"', '')):
        raise FileNotFoundError(f"Неверный путь к Chrome: {chrome_path}. Укажите путь к браузеру Google Chrome")

    def check_port(port, host="127.0.0.1"):
        """Проверяет, свободен ли порт."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return True
            except socket.error:
                return False


    def find_free_port(start_port=9222, host="127.0.0.1"):
        """Ищет свободный порт, начиная с указанного."""
        port = start_port
        while not check_port(port, host):
            port += 1
        return port


    def create_chrome_bat(port, user_data_dir, profile_dir, headless, defence, start_maximized, log_lvl, download_image, webnotifications):
        """Создает бат-файл для запуска Chrome."""

        # Базовая строка для батника
        bat_content = f'{chrome_path} --remote-debugging-port={port}'

        # Добавление параметров в батник в зависимости от аргументов
        if user_data_dir:
            bat_content += f'  --user-data-dir="{user_data_dir}"'

        if profile_dir:
            bat_content += f' --profile-directory="{profile_dir}"'

        if headless:
            bat_content += " --headless --disable-gpu --disable-dev-shm-usage"

        if start_maximized:
            bat_content += " --start-maximized"

        if log_lvl == 1:
            bat_content += " --log_lvl-level=1"  # Только ошибки
        elif log_lvl == 2:
            bat_content += " --log_lvl-level=2"  # Ошибки и предупреждения
        elif log_lvl == 3:
            bat_content += " --log_lvl-level=3"  # Критические ошибки
        else:
            pass

        if not download_image:
            bat_content += ' --disable-images'
        if not webnotifications:
            bat_content += ' --disable-notifications'

        if defence:
            bat_content += " --excludeSwitches=enable-automation --disable-extensions --disable-infobars --disable-popup-blocking --no-sandbox --disable-web-security --disable-blink-features=AutomationControlled"

        # Сохранение бат-файла
        bat_file = "start_chrome.bat"
        with open(bat_file, "w") as file:
            file.write(bat_content)

        return bat_file


    port = find_free_port(start_port=port)

    bat_file = create_chrome_bat(port, user_data_dir, profile_dir, headless, defence, start_maximized, log_lvl, download_image, webnotifications)
    subprocess.Popen([bat_file], shell=True)
    time.sleep(5)

    options = Options()

    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(options=options)

    # Удаление следов WebDriver
    if defence:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # if use_stealth:
    #     stealth(driver, platform="Win32", fix_hairline=True)

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