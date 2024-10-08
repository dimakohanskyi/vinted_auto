from selenium import webdriver
import time
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

basic_url = 'https://www.vinted.pl/member/228609071'
# user_profile_url = 'member/228609071'
product_block = 'profile u-flex-direction-column'


# def parsing_products_data(url):
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(10)
#     product_elements = driver.find_elements(By.CLASS_NAME, 'feed-grid')
#     # all_product = product_elements.find
#     for block_all_products in product_elements:
#         all_product = block_all_products.find_elements(By.CLASS_NAME, 'feed-grid__item')
#         product_link = block.find_element(By.TAG_NAME, 'a')
#         print(all_product)
#
#     time.sleep(5)
#
#     return None


def parsing_products_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(10)

    try:
        modal_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[1]/div/div[3]/button'))
        )
        modal_close_button.click()
        print("Модальне вікно закрито.")
    except Exception as e:
        print("Не вдалося знайти або закрити модальне вікно:", e)

    time.sleep(2)

    try:
        second_modal_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
        )
        second_modal_btn.click()
        print("2 Модальне вікно закрито.")
    except Exception as e:
        print("Не вдалося знайти або закрити модальне вікно:", e)

    time.sleep(2)

    product_blocks = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')

    for index in range(len(product_blocks)):
        product_link = product_blocks[index].find_element(By.TAG_NAME, 'a')
        product_link.click()
        time.sleep(5)

        driver.back()
        time.sleep(5)
        product_blocks = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')

    driver.quit()


parsing_products_data(url=basic_url)


