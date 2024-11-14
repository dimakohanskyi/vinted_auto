import random
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import os
from db.models import Product, SessionLocal, User, ProductImage
import shutil
from selenium.webdriver.chrome.options import Options


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


def modal_choose_country(driver):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "domain-selection-link")))
        # poland_link = driver.find_element(By.XPATH, "//a[contains(@href, 'vinted.pl')]")
        poland_link = driver.find_element(By.XPATH, "//a[contains(@class, 'domain-selection-link') and contains(., 'Polska')]")
        poland_link.click()
    except Exception as ex:
        print(f"Error with choose the country modal{ex}")


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
    chrome_options = Options()
    chrome_options.add_argument("--lang=pl")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Встановлюємо заголовок
    driver.request_interceptor = lambda request: request.headers.update({'Accept-Language': 'pl-PL'})

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

    modal_choose_country(driver)
    time.sleep(1)
    close_modals(driver, '//*[@id="onetrust-accept-btn-handler"]')

    random_scroll(driver)
    product_links = collect_product_links(driver)
    print(f"Collected {len(product_links)} product links.")

    try:
        for product_link in product_links:
            driver.get(product_link)
            time.sleep(3)

            dirt_product_price = driver.find_element(By.CSS_SELECTOR, '[data-testid="item-price"]').text
            product_price = dirt_product_price.replace('zł', '').strip()

            product_title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.summary-max-lines-4 span.web_ui__Text__text'))
            ).text

            product_size = driver.find_element(By.CSS_SELECTOR,
                                               '[data-testid="item-attributes-size"] .details-list__item-value').text

            product_condition = driver.find_element(By.CSS_SELECTOR,
                                                    '[data-testid="item-attributes-status"] .details-list__item-value').text.strip()

            product_color = driver.find_element(By.CSS_SELECTOR,
                                                '[data-testid="item-attributes-color"] .details-list__item-value').text.strip()

            product_location = driver.find_element(By.CSS_SELECTOR,
                                                   '[data-testid="item-attributes-location"] .details-list__item-value').text.strip()

            payment_methods = driver.find_element(By.CSS_SELECTOR,
                                                  '[data-testid="item-attributes-payment_methods"] .details-list__item-value').text.strip()

            product_description = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"] span').text.strip()

            product_brand = driver.find_element(By.CSS_SELECTOR,
                                                '.details-list__item-value [itemprop="name"]').text

            category_elements = driver.find_elements(By.CSS_SELECTOR,
                                                     'ul.breadcrumbs li.breadcrumbs__item span[itemprop="title"]')
            categories = [category.text for category in category_elements]

            if categories and categories[0] == "Strona główna":
                categories.pop(0)
                print(f"updated {categories}")

            names_images_db = []
            downloaded_urls = set()  # Додано для унікальності

            product_directory = os.path.join(user_folder, product_title.replace(" ", "_") + product_price + product_size)

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
                    if img_url not in downloaded_urls:
                        downloaded_urls.add(img_url)
                        file_name = generator_uniq_images_names(title=product_title, price=product_price,
                                                                size=product_size)
                        file_path = os.path.join(product_directory, file_name)
                        download_image(img_url, file_path)
                        names_images_db.append(file_path)
                        print(f"Downloaded image: {product_title}, path={file_path}")
                        time.sleep(1)

                close_button = driver.find_element(By.CLASS_NAME, "image-carousel__button--close")
                close_button.click()
                time.sleep(1)

                try:
                    storing_data_db(
                        user_id=user.id,
                        title=product_title,
                        price=product_price,
                        company=product_brand,
                        size=product_size,
                        condition=product_condition,
                        color=product_color,
                        location=product_location,
                        payment_method=payment_methods,
                        description=product_description,
                        category=categories,
                        unique_identifier=product_link,
                        image_paths=names_images_db,

                    )
                except Exception as ex:
                    print(ex)

            except Exception as ex:
                print(ex)

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







