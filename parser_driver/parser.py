import random
import requests
from selenium import webdriver
import time
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
from models import Product, SessionLocal, User, ProductImage

basic_url = 'https://www.vinted.pl/member/228609071'


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


def parsing_products_data(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    close_modals(driver, '/html/body/div[4]/div/div/div/div[1]/div/div[3]/button')
    close_modals(driver, '//*[@id="onetrust-accept-btn-handler"]')

    time.sleep(1)
    product_blocks = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')
    product_counter = 0

    for index in range(len(product_blocks)):
        try:
            random_scroll(driver)
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

            product_desc_elements = driver.find_elements(By.CSS_SELECTOR,
                                                         'div.u-text-wrap[itemprop="description"] > span > span')

            for product_desc_values in product_desc_elements:
                product_desc_values = product_desc_values.text.strip()

            product_cat_elements = driver.find_elements(By.CSS_SELECTOR,
                                                        'ul.breadcrumbs > li.breadcrumbs__item > a > span[itemprop="title"]')

            if product_cat_elements:
                product_cat_value = product_cat_elements[-1].text.strip()

            product_images_elements = driver.find_elements(By.CSS_SELECTOR, 'img[data-testid="item-photo-1--img"]')

            # product_directory = "product_import"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            product_directory = os.path.join("product_import", product_title_value.replace(" ", "_") + timestamp)

            if not os.path.exists(product_directory):
                os.mkdir(product_directory)
                print(f"Directory '{product_directory}' created.")
            else:
                print(f"Directory '{product_directory}' already exists.")

            local_path_images_list = []
            for img_elm in product_images_elements:
                img_elm.click()
                time.sleep(5)

                #html images elements
                first_product_images_block = driver.find_elements(By.CSS_SELECTOR,
                                                                  'img[data-testid="image-carousel-image-shown"]')

                for first_product_images_value in first_product_images_block:
                    first_product_images_value = first_product_images_value.get_attribute('src')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = f"{product_title_value}_{timestamp}_rest.jpg"
                    image_path = os.path.abspath(file_name)
                    local_path_images_list.append(image_path)
                    file_path = os.path.join(product_directory, file_name)

                    download_image(first_product_images_value, file_path)
                    time.sleep(2)

                rest_images_block = driver.find_elements(By.CSS_SELECTOR, 'img[data-testid="image-carousel-image"]')

                for rest_images_values in rest_images_block:
                    rest_images_values = rest_images_values.get_attribute('src')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = f"{product_title_value}_{timestamp}_rest.jpg"
                    image_path = os.path.abspath(file_name)
                    local_path_images_list.append(image_path)
                    file_path = os.path.join(product_directory, file_name)

                    download_image(rest_images_values, file_path)
                    time.sleep(2)

            try:
                add_data_db(
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
                    image_path=local_path_images_list,
                )

                local_path_images_list.clear()

                product_counter += 1
                if product_counter % 5 == 0:
                    random_scroll(driver)

                time.sleep(2)

            except Exception as ex:
                print(ex)

            time.sleep(2)
        except Exception as ex:
            print(ex)

        finally:
            driver.back()
            time.sleep(5)
            product_blocks = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')

    driver.quit()
    return None


def add_data_db(title, price, company, size, condition, color, location, payment_method, description, category,
                image_path):

    session = SessionLocal()
    unique_identifier = f"{title}_{price}_{company}".lower()

    try:
        existing_product = session.query(Product).filter(Product.unique_identifier == unique_identifier).first()

        if existing_product:
            print(f"Product '{title}' already exists in the database. Skipping.")

            for image in image_path:
                new_image = ProductImage(
                    product_id=existing_product.id,
                    image_path=image,
                )
                session.add(new_image)

        else:
            new_product = Product(
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

            for image in image_path:
                new_image = ProductImage(
                    product_id=new_product.id,
                    image_path=image,
                )
                session.add(new_image)

            session.commit()

            print(f"Product '{title}' and its images have been updated in the database.")

            session.commit()
            print(f"Product '{title}' added to database.")

    except Exception as e:
        session.rollback()
        print(f"Error adding product: {e}")

    finally:
        session.close()


def random_scroll(driver):

    driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))







