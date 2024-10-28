import os
import time
from dotenv import load_dotenv
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from db.models import SessionLocal, User, ProductImage, Product
import pprint
import pyautogui


load_dotenv()


def dolphin_get_port(profile_id):
    url = f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1'
    response = requests.get(url)

    if response.status_code == 200:
        start_info = response.json()
        if start_info['success']:
            port = start_info['automation']['port']
            ws_endpoint = start_info['automation']['wsEndpoint']
            return port, ws_endpoint
        else:
            print("Не вдалося запустити профіль:", start_info)
    else:
        print("Помилка при запуску профілю:", response.json())


def get_products_images(profile_id):
    session = SessionLocal()
    products_info = []

    try:
        user = session.query(User).filter(User.dolphin_anty_id == profile_id).first()

        if user:
            print(f'Dolphin find user_id={user.id} and related images')
            products = session.query(Product).filter(Product.user_id == user.id).all()

            for product in products:
                product_data = {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'company': product.company,
                    'size': product.size,
                    'condition': product.condition,
                    'color': product.color,
                    'location': product.location,
                    'payment_method': product.payment_method,
                    'description': product.description,
                    'category': product.category,
                    'images': []
                }

                images = session.query(ProductImage).filter(ProductImage.product_id == product.id).all()
                for img_element in images:
                    product_data['images'].append({
                        'id': img_element.id,
                        'fake_image_path': img_element.fake_image_path,
                    })

                products_info.append(product_data)

    except Exception as ex:
        print(ex)

    finally:
        session.close()

    return products_info


def upload_product_images(driver, fake_image_paths):
    """
      Завантажує зображення для конкретного продукту.
      Повертає True, якщо всі зображення успішно завантажені, інакше False.
    """

    successful_uploads = 0

    for fake_image_el in fake_image_paths:
        if fake_image_el:
            try:
                try:
                    first_add_img_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            '//*[@id="photos"]/div[2]/div/div/div/div[5]/div/button'
                        ))
                    )
                    first_add_img_btn.click()

                except Exception as ex:
                    print("First add image button not found, checking for new button.")

                    new_add_img_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            "//button[@aria-label='Add photos']"
                        ))
                    )
                    new_add_img_btn.click()

                # Додавання зображення через pyautogui
                pyautogui.press('enter')
                time.sleep(2)
                pyautogui.hotkey('command', 'shift', 'g')
                time.sleep(2)

                # Вказуємо директорію, де знаходиться зображення
                pyautogui.write(os.path.dirname(fake_image_el))
                pyautogui.press('enter')
                time.sleep(2)
                image_name = os.path.basename(fake_image_el)

                if image_name:
                    # Вибір імені файлу зображення
                    pyautogui.hotkey('command', 'shift', 'g')
                    time.sleep(2)
                    pyautogui.write(image_name)
                    time.sleep(2)
                    pyautogui.press('enter')
                    time.sleep(2)
                    pyautogui.press('enter')
                    time.sleep(4)

                # Збільшуємо лічильник успішних завантажень
                successful_uploads += 1

            except Exception as upload_ex:
                print(f"Error while uploading image {fake_image_el}: {upload_ex}")
                continue  # Пропускаємо поточне зображення та пробуємо наступне

    # Перевірка, чи всі фото успішно завантажені
    if successful_uploads == len(fake_image_paths):
        print("All images for this product have been uploaded successfully.")
        return True
    else:
        print("Some images were not uploaded successfully.")
        return False


def select_category_process(driver, product_cat_mas):
    try:
        # Wait for the dropdown to be present and click it
        category_vinted_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-input__content"))
        )
        category_vinted_dropdown.click()

        # Loop through categories

        while True:
            # Wait for dropdown items to be present
            dropdown_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.web_ui__List__list li"))
            )

            found_category = False

            for item in dropdown_items:
                try:
                    category_name = item.find_element(By.CLASS_NAME, "web_ui__Cell__title").text

                    if category_name in product_cat_mas:
                        print(f"Attempting to select category: {category_name}")
                        item.click()
                        random_timesleep()  # Random sleep after selection
                        print(f"Категорія '{category_name}' була обрана.")
                        found_category = True
                        break  # Break the loop if a category was selected

                except Exception as ex:
                    print("Stale element reference encountered. Refetching items...")
                    break  # Break to re-fetch dropdown items
                except Exception as ex:
                    print(f"Error encountered while processing category '{category_name}': {ex}")
                    break  # Exit the for loop to refetch items

            if found_category:
                # If a category was found and selected, we need to refetch the items again
                continue  # Loop back to fetch the items again to ensure we have the latest

    except Exception as ex:
        print("Timeout while waiting for elements.")

    finally:
        print("Exiting category selection process.")


def dolphin_aut(profile_id):
    session = SessionLocal()
    port, ws_endpoint = dolphin_get_port(profile_id)

    if port is None:
        print("Не вдалося отримати порт.")
        return

    # Launch the browser with the WebSocket port
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=pl')
    options.add_argument(f'--remote-debugging-port={port}')

    chrome_driver_path = '/Users/user/Desktop/projects/python_projects/vinted_aut/dolphin_anty/chromedriver'
    service = Service(chrome_driver_path)

    user = session.query(User).filter(User.dolphin_anty_id == profile_id).first()

    driver = webdriver.Chrome(service=service, options=options)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                    '//*[@id="__next"]/div/div/div[1]/header/div/div/div[3]/div[2]/a[1]/span'))).click()
    time.sleep(2)

    try:
        user_products = get_products_images(profile_id=profile_id)

        for user_product in user_products:

            images = user_product.get('images', [])
            fake_image_paths = [image['fake_image_path'] for image in images]
            # upload_product_images(driver, fake_image_paths)

            if not fake_image_paths:
                print("No images to upload for this product.")
                continue

            # product_cat_mas = user_product['category']
            # select_category_process(driver, product_cat_mas)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


def random_scroll(driver, min_pause=1, max_pause=5, min_scroll=100, max_scroll=500):
    pause_time = random.uniform(min_pause, max_pause)
    time.sleep(pause_time)
    scroll_distance = random.randint(min_scroll, max_scroll)
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
    print(f"Scrolled down {scroll_distance} pixels.")


def random_timesleep(min_seconds=1, max_seconds=5):
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)
    print(f"Slept for {sleep_time:.2f} seconds.")




# user_product
# {'id': 60,
#  'title': 'Calvin Klein',
#  'price': 'PLN 105.00',
#  'company': 'CALVIN KLEIN',
#  'size': '10',
#  'condition': 'VERY GOOD',
#  'color': 'WHITE',
#  'location': 'WARSZAWA, POLAND',
#  'payment_method': 'BANK CARD',
#  'description': 'Super stan, zapraszam do zakupuWysyłam paczkę w ciągu 1 dnia',
#  'category': ['Home', 'Women', 'Shoes', 'Sneakers', 'Calvin Klein Sneakers'],


#  'images': [{'id': 355, 'fake_image_path': '/Users/user/Desktop/projects/python_projects/vinted_aut/images/fake/profile_1/Calvin_KleinPLN 105.0010/Calvin Klein_10_PLN 105.00_379.jpg'},
#             {'id': 357, 'fake_image_path': '/Users/user/Desktop/projects/python_projects/vinted_aut/images/fake/profile_1/Calvin_KleinPLN 105.0010/Calvin Klein_10_PLN 105.00_834.jpg'},
#             {'id': 358, 'fake_image_path': '/Users/user/Desktop/projects/python_projects/vinted_aut/images/fake/profile_1/Calvin_KleinPLN 105.0010/Calvin Klein_10_PLN 105.00_349.jpg'},
#             {'id': 356, 'fake_image_path': '/Users/user/Desktop/projects/python_projects/vinted_aut/images/fake/profile_1/Calvin_KleinPLN 105.0010/Calvin Klein_10_PLN 105.00_133.jpg'},
#             {'id': 359, 'fake_image_path': '/Users/user/Desktop/projects/python_projects/vinted_aut/images/fake/profile_1/Calvin_KleinPLN 105.0010/Calvin Klein_10_PLN 105.00_804.jpg'}]}
#












