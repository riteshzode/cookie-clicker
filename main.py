import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = "C:\Development\chromedriver.exe"

service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get cookie to click on.
cookie = driver.find_element(By.ID, "cookie")
# cookie.click()

# Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")

items_id = [i.get_attribute("id") for i in items]

time_out = time.time() + 5
five_min = time.time() + 60 * 5

while True:

    cookie.click()

    # every 5 sec
    if time.time() > time_out:

        prices = driver.find_elements(By.CSS_SELECTOR, "#store b")

        item_prices = []
        for i in prices:
            element_text = i.text
            if element_text != "":
                item_prices.append(int(element_text.split("-")[1].replace(",", "")))

        money = driver.find_element(By.ID, "money").text

        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        cookie_update = {}

        for i in range(len(item_prices)):
            cookie_update[item_prices[i]] = items_id[i]

        affordable_upgrade = {}

        for price, idx in cookie_update.items():
            if cookie_count > price:
                affordable_upgrade[price] = idx

        max_price = max(affordable_upgrade)

        id_find = affordable_upgrade[max_price]

        driver.find_element(By.ID, id_find).click()

        # Add another 5 seconds until the next check
        time_out = time.time() + 5

        # After 5 minutes stop the bot and check the cookies per second count.
        if time.time() > five_min:
            cookie_per_sec = driver.find_element(By.ID, "cps").text
            print(cookie_per_sec)
            break



