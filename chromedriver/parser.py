from selenium import webdriver
import time
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

basic_url = 'https://www.vinted.pl/member/228609071'


def parsing_products_data(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

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

    product_blocks = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')

    for index in range(len(product_blocks)):
        product_link = product_blocks[index].find_element(By.TAG_NAME, 'a')
        product_link.click()
        time.sleep(3)

        dirt_product_price = driver.find_element(By.CSS_SELECTOR, '[data-testid="item-price"] p').text
        product_price = dirt_product_price.replace('zł', '').strip()

        product_company_block = driver.find_elements(By.CSS_SELECTOR,
                                               '.details-list__item-value a span[itemprop="name"]')

        for product_company in product_company_block:
            product_company = product_company.text.strip()

        size_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="size"]')
        for size_value in size_elements:
            size_value = size_value.text

        product_condition_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="status"]')
        for product_condition_value in product_condition_elements:
            product_condition_value = product_condition_value.text.strip()

        product_color_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="color"]')
        for product_color_value in product_color_elements:
            product_color_value = product_color_value.text.strip()

        product_location_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="location"]')
        for product_location_values in product_location_elements:
            product_location_values = product_location_values.text.strip()

        product_payment_method_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="payment_methods"]')
        for product_payment_method_value in product_payment_method_elements:
            product_payment_method_value = product_payment_method_value.text.strip()

        product_title_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="name"] h2')
        for product_title_value in product_title_elements:
            product_title_value = product_title_value.text.strip()

        product_desc_elements = driver.find_elements(By.CSS_SELECTOR, 'div.u-text-wrap[itemprop="description"] > span > span')
        for product_desc_values in product_desc_elements:
            product_desc_values = product_desc_values.text.strip()

        product_cat_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.breadcrumbs > li.breadcrumbs__item > a > span[itemprop="title"]')
        if product_cat_elements:
            product_cat_value = product_cat_elements[-1].text.strip()

        product_images_elements = driver.find_elements(By.CSS_SELECTOR, 'img[data-testid="item-photo-1--img"]')
        for img_elm in product_images_elements:
            img_elm.click()
            all_images_carousel = driver.find_elements(By.CSS_SELECTOR, 'img[data-testid="image-carousel-image"]')
            for i in all_images_carousel:
                image_url = i.get_attribute('src')
                print(image_url)




        time.sleep(2)
            # print('==================================')
            # print(product_price)
            # print(product_company)
            # print(size_value)
            # print(product_condition_value)
            # print(product_color_value)
            # print(product_location_values)
            # print(product_payment_method_value)
            # print(product_title_value)
            # print(product_desc_values)
            # print(product_cat_value)
            # print('==================================')














        driver.back()
        time.sleep(5)
        product_blocks = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')

    driver.quit()


parsing_products_data(url=basic_url)


