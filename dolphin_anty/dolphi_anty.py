import os
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from db.models import SessionLocal, User, ProductImage, Product
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
from helpers.user_simulator import *
from selenium.common.exceptions import TimeoutException

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
                    time.sleep(2)

                except Exception as ex:


                    new_add_img_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            "//button[@aria-label='Dodaj zdjęcia']"
                        ))
                    )
                    new_add_img_btn.click()
                    random_timesleep()

                pyautogui.press('enter')
                time.sleep(2)
                pyautogui.hotkey('command', 'shift', 'g')
                time.sleep(2)

                image_name = os.path.basename(fake_image_el)

                image_directory = os.path.dirname(fake_image_el)
                pyperclip.copy(image_directory)
                pyautogui.hotkey('command', 'v')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

                if image_name:
                    pyperclip.copy(image_name)
                    pyautogui.hotkey('command', 'shift', 'g')
                    time.sleep(1)
                    pyautogui.hotkey('command', 'v')
                    time.sleep(2)
                    pyautogui.press('enter')
                    time.sleep(2)
                    pyautogui.press('enter')
                    random_timesleep()

                successful_uploads += 1

            except Exception as upload_ex:
                print(f"Error while uploading image {fake_image_el}: {upload_ex}")
                continue

    if successful_uploads == len(fake_image_paths):
        print("All images for this product have been uploaded successfully.")
        return True
    else:
        print("Some images were not uploaded successfully.")
        return False


def select_category_process(driver, product_cat_mas):
    try:
        selected_categories = set()
        # Wait for the dropdown to be present and click it
        category_vinted_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-input__content"))
        )
        category_vinted_dropdown.click()

        # Loop through categories

        while len(selected_categories) < len(product_cat_mas):
            # Wait for dropdown items to be present
            dropdown_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.web_ui__List__list li"))
            )

            for item in dropdown_items:
                try:
                    category_name = item.find_element(By.CLASS_NAME, "web_ui__Cell__title").text

                    if category_name in product_cat_mas and category_name not in selected_categories:
                        item.click()
                        random_timesleep()  # Random sleep after selection
                        print(f"Категорія '{category_name}' була обрана.")
                        selected_categories.add(category_name)
                        break

                except Exception as ex:
                    print("Stale element reference encountered. Refetching items...")
                    break  # Break to re-fetch dropdown items

            random_timesleep()
    except Exception as ex:
        print("Timeout while waiting for elements.")

    finally:
        print("Exiting category selection process.")


def select_product_marka_process(driver, marka_cat_mas):
    try:
        marka_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "div.c-input__content input[data-testid='brand-select-dropdown-input']")))
        marka_input.click()

        pyautogui.write(marka_cat_mas.title(), interval=0.1)
        time.sleep(1)

        marka_dropdown_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "li.pile__element > div.web_ui__Cell__cell.web_ui__Cell__default.web_ui__Cell__clickable[role='button'][tabindex='0'][aria-label][id^='brand-']")))

        for brand in marka_dropdown_items:
            brand_text = brand.text.strip().lower()
            input_brand_text = marka_cat_mas.title().lower()

            if brand_text == input_brand_text:
                time.sleep(1)
                brand.click()
                print(f'Selected brand: {brand.text}')
                return

        print(f'Brand {marka_cat_mas.title()} not found in the list.')
        time.sleep(2)
        print('марка обрана')

    except Exception as ex:
        print(f"Error with select marka: {ex}")


def select_product_size_process(driver, product_size_mas):
    try:
        size_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.c-input__content input[name='size_id']"))
        )

        size_input.click()
        random_timesleep()

        size_dropdown_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "li.pile__element > div[role='button'][data-testid^='size-']"))
        )

        for size_element in size_dropdown_elements:
            if size_element.text == product_size_mas:  # Порівняти з бажаним розміром
                size_element.click()  # Клікнути на потрібний розмір
                random_timesleep()
                print(f"Selected size: {size_element.text}")
                break
        else:
            print(f"Size '{product_size_mas}' not found in the dropdown.")

        arrow_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/div/div[7]/div[7]/div[1]/div[2]"))
        )
        arrow_icon.click()
        time.sleep(2)

    except Exception as ex:
        print(f"Error with select size: {ex}")


def select_product_condition_process(driver, product_condition_mas):
    try:
        condition_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#status_id"))
        )
        condition_input.click()
        random_timesleep()

        condition_dropdown_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 ".web_ui__Cell__cell.web_ui__Cell__default.web_ui__Cell__clickable .web_ui__Cell__title"))
        )

        for condition_element in condition_dropdown_elements:
            condition_text = condition_element.text.strip().lower()
            if condition_text == product_condition_mas.strip().lower():
                condition_element.click()
                random_timesleep()
                break
        else:
            print(f"Condition '{product_condition_mas}' not found in the dropdown.")

        time.sleep(2)
        print('Стан вибрано')

    except Exception as ex:
        print(f"Error with select condition: {ex}")


def select_product_color_process(driver, product_color_mas):
    try:

        product_color_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "div.c-input__content input[data-testid='color-select-dropdown-input'].c-input__value.c-input__value--with-suffix.u-cursor-pointer"))
        )

        product_color_input.click()
        random_timesleep()

        color_list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "ul.web_ui__List__list.web_ui__List__tight > li.web_ui__Item__item.web_ui__Item__with-divider > div.web_ui__Cell__cell.web_ui__Cell__default.web_ui__Cell__clickable[role='button'][tabindex='0'][id^='color-']"))
        )

        product_color_mas_clear = product_color_mas.strip().lower()
        color_list_mas = product_color_mas_clear.split(',')
        first_color = color_list_mas[0].strip()
        second_color = color_list_mas[1].strip() if len(color_list_mas) > 1 else None
        selected_colors = []

        for color_item in color_list_items:
            color_item_text = color_item.text.strip().lower()

            for color in color_list_mas:
                if color.strip() in color_item_text:
                    color_item.click()
                    selected_colors.append(color.strip())
                    random_timesleep()
                    break

            # Якщо вже вибрано необхідну кількість кольорів, виходимо з зовнішнього циклу
            if len(selected_colors) >= len(color_list_mas):
                break

        close_dropdown_arrow = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "[data-testid='color-select-dropdown-chevron-up']"))
        )
        close_dropdown_arrow.click()
        time.sleep(2)
        print('Колір обрано')

    except Exception as ex:
        print(f'Error with select color {ex}')


def select_product_price_process(driver, product_price_mas):
    try:
        price_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.web_ui__Input__content input#price"))
        )
        price_input.click()
        pyautogui.write(product_price_mas, interval=0.1)

    except Exception as ex:
        print(f"Error with select price {ex}")


def select_package_size_process(driver):
    try:
        package_size_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="medium-package-size--cell"]'))
        )
        package_size_element.click()

    except Exception as ex:
        print(f"Error selecting package size: {ex}")


def fill_title_input_process(driver, product_title_mas):
    try:
        title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="title--input"]'))
        )
        title_input.click()
        random_timesleep()

        # title_input.send_keys(product_title_mas.capitalize())
        pyautogui.write(product_title_mas.capitalize(), interval=0.1)

    except Exception as ex:
        print(f"Error filling title input: {ex}")


def fill_description_input_process(driver, product_description_mas):
    try:
        description_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='description--input']"))
        )

        description_input.click()
        random_timesleep()

        description_input.clear()
        pyautogui.write(product_description_mas, interval=0.1)
        time.sleep(1)

    except Exception as ex:
        print(f"Error filling description input: {ex}")


def click_add_button_process(driver):
    try:
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="upload-form-save-button"]'))
        )

        add_button.click()
        random_timesleep()

    except Exception as ex:
        print(f"Error clicking 'Dodaj' button: {ex}")


def mark_uploaded_product(product_id):
    session = SessionLocal()
    try:
        product = session.query(Product).get(product_id)
        if product:
            product.is_uploaded = True
            session.commit()
            print(f"Product {product_id} marked as uploaded.")
        else:
            print(f"Product with ID {product_id} not found.")
    except Exception as ex:
        print(f"Error updating product status: {ex}")
    finally:
        session.close()


# def reopen_add_product(driver):
#     try:
#         home = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
#                                                                                "//*[@id='__next']/div/div/div[1]/header/div/div/div[1]/a/div[2]")))
#
#         home.click()
#         random_timesleep()
#
#     except Exception as ex:
#         print(f"Error with open home page after adding, {ex}")


def success_add_modal(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "list-promotion")))

        button = driver.find_element(By.CSS_SELECTOR,
                                     "button[data-testid='list-promotion-submit-cta']")
        button.click()
        print("Кнопка 'Dodaj kolejne' була знайдена та натиснута.")

    except Exception as ex:
        print(f"Блок або кнопка 'Dodaj kolejne' не знайдені {ex}")


def question_modal_close(driver):
    try:

        question_modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                         "//span[@class='web_ui__Button__content']/span[@class='web_ui__Button__label' and text()='Dokończ później']")))
        if question_modal:
            random_timesleep()
            question_modal.click()
            print("Question modal closed")
    except TimeoutException:
        print("Question modal not found, continuing execution.")


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
    driver.maximize_window()

    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[-1])

    question_modal_close(driver)
    time.sleep(2)

    try:
        user_products = get_products_images(profile_id=profile_id)

        while user_products:
            add_product_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                            '//*[@id="__next"]/div/div/div[1]/header/div/div/div[3]/div[2]/a[1]/span')))
            add_product_btn.click()
            time.sleep(2)

            # second_modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            #                                                                                '//*[@id="onetrust-accept-btn-handler"]')))
            # if second_modal:
            #     second_modal.click()

            for user_product in user_products:
                product = session.query(Product).get(user_product['id'])

                if not product.is_active:
                    print(f"Продукт '{user_product['title']}' не активний. Пропускаємо.")
                    continue

                if product.is_uploaded:
                    print(f"Продукт '{user_product['title']}' вже був завантажений, пропускаємо.")
                    continue

                random_timesleep()

                images = user_product.get('images', [])
                fake_image_paths = [image['fake_image_path'] for image in images]

                if fake_image_paths:
                    print("Uploading images...")
                    upload_success = upload_product_images(driver, fake_image_paths)
                    if upload_success:
                        print(f"All images for product '{user_product['title']}' uploaded successfully.")
                    else:
                        print(f"Some images for product '{user_product['title']}' failed to upload.")
                else:
                    print("No images to upload for this product.")
                    continue
                print(f"Finished processing product '{user_product['title']}'.")

                fill_title_input_process(driver, user_product['title'])
                random_timesleep()
                random_scroll(driver)

                fill_description_input_process(driver, user_product['description'])
                random_timesleep()
                random_scroll(driver)
                time.sleep(2)

                select_category_process(driver, user_product['category'])
                random_timesleep()
                random_scroll(driver)

                select_product_marka_process(driver, user_product['company'])
                random_timesleep()
                random_scroll(driver)

                select_product_size_process(driver, user_product['size'])
                random_timesleep()

                select_product_condition_process(driver, user_product['condition'])
                random_timesleep()
                random_scroll(driver)

                select_product_color_process(driver, user_product['color'])
                random_timesleep()

                select_product_price_process(driver, user_product['price'])
                random_timesleep()

                select_package_size_process(driver)
                random_timesleep()
                click_empty_block(driver)
                random_scroll(driver)
                random_scroll(driver)
                click_add_button_process(driver)

                mark_uploaded_product(user_product['id'])

                #if product add successfully close succes modal
                question_modal_close(driver)
                random_timesleep()
                success_add_modal(driver)
                random_timesleep()
                # reopen_add_product(driver)

                print(f"Product '{user_product['title']}' uploaded and marked as uploaded in the database.")

            user_products = get_products_images(profile_id=profile_id)
            if not user_products:  # Якщо продукти більше не залишились, зупиняємо цикл
                print("Товари були успішно додані")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()











