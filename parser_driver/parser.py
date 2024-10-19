import random
import requests
from selenium import webdriver
import time
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import os
from db.models import Product, SessionLocal, User, ProductImage
import shutil


def download_image(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:

            with open(file_path, "wb") as file:
                file.write(response.content)
                print('Image downloaded successfully.')
        else:
            print(f"Failed to download image: {url}. Status code: {response.status_code}")
    except Exception as ex:
        print(ex)


def close_modals(driver, xpath):
    try:
        modal_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        modal_close_button.click()
        print("Modal closed.")
    except Exception as e:
        print("Failed to close modal:", e)
    time.sleep(1)


def random_scroll(driver, pause_time=2, max_scrolls=50):

    """ Скролимо сторінку вниз до самого низу, поки не перестануть підвантажуватись нові елементи """
    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0
    while scroll_count < max_scrolls:  # Ліміт на кількість скролінгів
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("Reached the bottom of the page, no more elements to load.")
            break

        last_height = new_height
        scroll_count += 1


def collect_product_links(driver):
    """ Збираємо всі лінки на товари зі сторінки після скролінгу """
    product_links = set()

    try:
        product_blocks = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'feed-grid__item'))
        )

        for product_block in product_blocks:
            try:
                product_link_element = product_block.find_element(By.TAG_NAME, 'a')
                product_link = product_link_element.get_attribute('href')

                if product_link not in product_links:
                    product_links.add(product_link)

            except StaleElementReferenceException:
                print("Stale element detected, skipping this element.")
                continue

    except TimeoutException:
        print("Timeout while waiting for product elements.")

    return product_links


def generator_uniq_images_names(title, price, size):
    number = random.randint(100, 999)
    db_uniq_image_name = f"{title}_{size}_{price}_{number}.jpg"

    return db_uniq_image_name


def parsing_products_data(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    session = SessionLocal()
    user = session.query(User).filter(User.account_url == url).first()

    # Create folder structure based on user login
    user_folder = os.path.join("images", "original", user.login)  # Assuming `user.login` is the user's login name

    # Remove existing user folder if it exists
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        print(f"Removed existing directory: {user_folder}")

    os.makedirs(user_folder)

    try:
        close_modals(driver, '/html/body/div[4]/div/div/div/div[1]/div/div[3]/button')
        close_modals(driver, '//*[@id="onetrust-accept-btn-handler"]')
    except Exception as e:
        print("No modals to close or failed to close modal:", e)

    random_scroll(driver)
    product_links = collect_product_links(driver)
    print(f"Collected {len(product_links)} product links.")

    for product_link in product_links:
        driver.get(product_link)  # Відкриваємо сторінку товару
        time.sleep(3)

        try:
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

            product_desc_elements = driver.find_elements(By.CSS_SELECTOR,
                                                         'div.u-text-wrap[itemprop="description"] > span > span')

            for product_desc_values in product_desc_elements:
                product_desc_values = product_desc_values.text.strip()

            product_cat_elements = driver.find_elements(By.CSS_SELECTOR,
                                                        'ul.breadcrumbs > li.breadcrumbs__item > a > span[itemprop="title"]')

            if product_cat_elements:
                product_cat_value = product_cat_elements[-1].text.strip()

            image_urls = []
            names_images_db = []

            product_directory = os.path.join(user_folder, product_title_value.replace(" ", "_") + product_price + size_value)

            if not os.path.exists(product_directory):
                os.mkdir(product_directory)
                print(f"Directory '{product_directory}' created.")
            else:
                print(f"Directory '{product_directory}' already exists.")

            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "item-photos"))
                )

                thumbnails = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='item-photo-1']")
                for first_img_site in thumbnails:
                    first_img_site.click()
                    time.sleep(2)

                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "image-carousel__image"))
                )

                carousel_images = driver.find_elements(By.CLASS_NAME, "image-carousel__image")
                for img in carousel_images:
                    img_url = img.get_attribute("src")
                    image_urls.append(img_url)


                for url_el in image_urls:
                    file_name = generator_uniq_images_names(title=product_title_value, price=product_price,
                                                            size=size_value)

                    file_path = os.path.join(product_directory, file_name)

                    # Викликаємо download_image з URL
                    download_image(url_el, file_path)

                    names_images_db.append(file_path)
                    print(f"Downloaded image: {file_path}")
                    time.sleep(1)

                close_button = driver.find_element(By.CLASS_NAME, "image-carousel__button--close")
                close_button.click()
                time.sleep(1)

            except Exception as es:
                print("An error occurred:", es)

            storing_data_db(
                user_id=user.id,
                title=product_title_value,
                price=product_price,
                company=product_company,
                size=size_value,
                condition=product_condition_value,
                color=product_color_value,
                location=product_location_values,
                payment_method=product_payment_method_value,
                description=product_desc_values,
                category=product_cat_value,
                unique_identifier=product_link,
                image_paths=names_images_db
            )

        except Exception as ex:
            print(ex)

    driver.quit()


def storing_data_db(user_id, title, price, company, size, condition, color,
                    location, payment_method, description, category, unique_identifier, image_paths):
    session = SessionLocal()

    try:
        existing_product = session.query(Product).filter_by(unique_identifier=unique_identifier).first()

        if existing_product:
            print(f"Продукт з ідентифікатором {unique_identifier} вже існує в базі.")
            return

        new_product = Product(
            user_id=user_id,
            title=title,
            price=price,
            company=company,
            size=size,
            condition=condition,
            color=color,
            location=location,
            payment_method=payment_method,
            description=description,
            category=category,
            unique_identifier=unique_identifier
        )

        session.add(new_product)
        session.commit()

        if image_paths:
            for image_path in image_paths:
                new_image = ProductImage(
                    product_id=new_product.id,  # Використовуємо ID новоствореного продукту
                    original_image_path=os.path.abspath(image_path)
                )
                session.add(new_image)

            session.commit()
        print(f"Продукт '{title}' успішно збережений в базу даних разом з {len(image_paths)} зображеннями.")

    except Exception as e:
        session.rollback()  # Відкочуємо зміни у разі помилки
        print(f"Помилка при збереженні продукту в базу даних: {e}")

    finally:
        session.close()







