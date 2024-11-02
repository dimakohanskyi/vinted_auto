# def dolphin_aut(profile_id):
#     session = SessionLocal()
#     port, ws_endpoint = dolphin_get_port(profile_id)
#
#     if port is None:
#         print("Не вдалося отримати порт.")
#         return
#
#     # Launch the browser with the WebSocket port
#     options = webdriver.ChromeOptions()
#     options.add_argument(f'--remote-debugging-port={port}')
#
#     chrome_driver_path = '/Users/user/Desktop/projects/python_projects/vinted_aut/dolphin_anty/chromedriver'
#     service = Service(chrome_driver_path)
#
#     user = session.query(User).filter(User.dolphin_anty_id == profile_id).first()
#
#     driver = webdriver.Chrome(service=service, options=options)
#
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
#                                                                     '//*[@id="__next"]/div/div/div[1]/header/div/div/div[3]/div[2]/a[1]/span'))).click()
#     time.sleep(2)
#
#     try:
#         user_products = get_products_images(profile_id=profile_id)
#
#         for user_product in user_products:
#             images = user_product.get('images', [])
#             fake_image_paths = [image['fake_image_path'] for image in images]
#
#             if not fake_image_paths:
#                 print("No images to upload for this product.")
#                 continue  # Пропускаємо продукт, якщо немає зображень
#
#             successful_uploads = 0
#
#             for fake_image_el in fake_image_paths:
#
#                 if fake_image_el:
#                     try:
#                         try:
#
#                             first_add_img_btn = WebDriverWait(driver, 10).until(
#                                 EC.presence_of_element_located((
#                                     By.XPATH,
#                                     '//*[@id="photos"]/div[2]/div/div/div/div[5]/div/button'
#                                 ))
#                             )
#                             first_add_img_btn.click()
#
#                         except Exception as ex:
#                             print("First add image button not found, checking for new button.")
#
#                             new_add_img_btn = WebDriverWait(driver, 10).until(
#                                 EC.presence_of_element_located((
#                                     By.XPATH,
#                                     "//button[@aria-label='Add photos']"
#                                 ))
#                             )
#                             new_add_img_btn.click()
#
#
#                         pyautogui.press('enter')
#                         time.sleep(2)
#                         pyautogui.hotkey('command', 'shift', 'g')
#                         time.sleep(2)
#
#                         # Write the directory where the image is located
#                         pyautogui.write(os.path.dirname(fake_image_el))
#                         pyautogui.press('enter')
#                         time.sleep(2)
#                         image_name = os.path.basename(fake_image_el)
#
#                         if image_name:
#                             # Select the image file
#                             pyautogui.hotkey('command', 'shift', 'g')
#                             time.sleep(2)
#                             pyautogui.write(image_name)
#                             time.sleep(2)
#                             pyautogui.press('enter')
#                             time.sleep(2)
#                             pyautogui.press('enter')
#                             time.sleep(4)
#
#                         successful_uploads += 1
#
#                         if successful_uploads == len(fake_image_paths):
#                             print(f"All images for product {user_product['id']} have been uploaded.")
#                             break
#
#                     except Exception as upload_ex:
#                         print(f"Error while uploading image {fake_image_el}: {upload_ex}")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     finally:
#         driver.quit()



a = {'pidar': 'xyi'}
print(a['p'].title())