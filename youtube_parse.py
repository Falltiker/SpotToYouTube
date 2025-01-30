from Selenium_template_Chrome import *
from bs4 import BeautifulSoup as BS
import time
import random



email = "ckbopec@gmail.com"
password = "FAltiker255623SKIF"


options = Options()

driver = webdriver.Chrome(options=options)








# driver = create_driver(False)

# driver.get("https://music.youtube.com/")

# sing_up_input = find_element(driver, By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[3]/a")
# move_to_element_click(driver, sing_up_input)


driver.get("https://accounts.google.com/signin/oauth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3ABBC%2C16%3A9b15b0994c6df9fc%2C10%3A1591711286%2C16%3A66b338ce162d6599%2Ca78a0c663f0beb12c0559379b61a9f5d62868c4fbd2f00e46a86ac26796507a1%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22921f8f04441041069683cc2377152422%22%7D&response_type=code&o2v=1&as=NCQvtBXI4prkLLDbn4Re0w&flowName=GeneralOAuthFlow")

time.sleep(9999)
time.sleep(1)

email_input = find_element(driver, By.ID, "identifierId")
email_input.send_keys(email)

time.sleep(2)

button_next = find_element(driver, By.ID, "identifierNext")
move_to_element_click(driver, button_next)

time.sleep(9999)
