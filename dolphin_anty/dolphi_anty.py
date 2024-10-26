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
# profile_id = '474806975'


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


def dolphin_aut(profile_id):
    session = SessionLocal()
    port, ws_endpoint = dolphin_get_port(profile_id)

    if port is None:
        print("Не вдалося отримати порт.")
        return

    # Launch the browser with the WebSocket port
    options = webdriver.ChromeOptions()
    options.add_argument(f'--remote-debugging-port={port}')

    chrome_driver_path = '/Users/user/Desktop/projects/python_projects/vinted_aut/dolphin_anty/chromedriver'
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    try:
        main_profile_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[1]/header/div/div/div[3]/div[2]/a[1]/span'))).click()
        time.sleep(2)

        user_products = get_products_images(profile_id=profile_id)
        for user_product in user_products:
            add_image_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="photos"]/div[2]/div/div/div/div[5]/div/button'))).click()
            time.sleep(1)

            pyautogui.hotkey('command', 'f')
            time.sleep(1)
            pyautogui.write('zaebis')







    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()





def random_scroll(driver, scroll_pause_time=2, scroll_amount=300):
    ...


def random_timesleep():
    ...



