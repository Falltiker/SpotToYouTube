from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Selenium_template_Chrome import *

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)


driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Faccounts.google.com%2F&followup=https%3A%2F%2Faccounts.google.com%2F&passive=1209600&ifkv=AeZLP99__G5gRyR-BzSFZrLlIhyfrDu8SMnbaHVwEsGRNwH0RZVFTmOU0RsimYYafnJlviWPrYjYcA&ddm=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

email_input = find_element(driver, By.ID, "identifierId")
email_input.send_keys("ckbopec")

button_next = find_element(driver, By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button")
button_next.click()

time.sleep(2)

password_input = find_element(driver, By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
password_input.send_keys("FAltiker255623SKIF")

button_next = find_element(driver, By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button")
button_next.click()

# driver.get("https://youtube.com")