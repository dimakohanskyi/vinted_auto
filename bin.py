# dirt_product_price = driver.find_element(By.CSS_SELECTOR, '[data-testid="item-price"] p').text
# product_price = dirt_product_price.replace('zł', '').strip()
#
# product_company_block = driver.find_elements(By.CSS_SELECTOR,
#                                              '.details-list__item-value a span[itemprop="name"]')
#
# for product_company in product_company_block:
#     product_company = product_company.text.strip()
#
# size_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="size"]')
#
# for size_value in size_elements:
#     size_value = size_value.text
#
# product_condition_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="status"]')
#
# for product_condition_value in product_condition_elements:
#     product_condition_value = product_condition_value.text.strip()
#
# product_color_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="color"]')
#
# for product_color_value in product_color_elements:
#     product_color_value = product_color_value.text.strip()
#
# product_location_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="location"]')
#
# for product_location_values in product_location_elements:
#     product_location_values = product_location_values.text.strip()
#
# product_payment_method_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="payment_methods"]')
#
# for product_payment_method_value in product_payment_method_elements:
#     product_payment_method_value = product_payment_method_value.text.strip()
#
# product_title_elements = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="name"] h2')
#
# for product_title_value in product_title_elements:
#     product_title_value = product_title_value.text.strip()
#
# product_desc_elements = driver.find_elements(By.CSS_SELECTOR,
#                                              'div.u-text-wrap[itemprop="description"] > span > span')
#
# for product_desc_values in product_desc_elements:
#     product_desc_values = product_desc_values.text.strip()
#
# product_cat_elements = driver.find_elements(By.CSS_SELECTOR,
#                                             'ul.breadcrumbs > li.breadcrumbs__item > a > span[itemprop="title"]')
#
# if product_cat_elements:
#     product_cat_value = product_cat_elements[-1].text.strip()


#
# #create uniq directory
# product_directory = os.path.join("product_import", product_title_value.replace(" ", "_") + timestamp)
# if not os.path.exists(product_directory):
#     os.mkdir(product_directory)
#     print(f"Directory '{product_directory}' created.")
# else:
#     print(f"Directory '{product_directory}' already exists.")


#
# # get all images in list
# image_urls = []
# names_images_db = []
#
# try:
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CLASS_NAME, "item-photos"))
#     )
#
#     thumbnails = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='item-photo-1']")
#     for first_img_site in thumbnails:
#         first_img_site.click()
#         time.sleep(2)
#
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CLASS_NAME, "image-carousel__image"))
#     )
#
#     carousel_images = driver.find_elements(By.CLASS_NAME, "image-carousel__image")
#     for img in carousel_images:
#         img_url = img.get_attribute("src")
#         image_urls.append(img_url)
#
#     close_button = driver.find_element(By.CLASS_NAME, "image-carousel__button--close")
#     close_button.click()
#     time.sleep(1)
#
#     print(image_urls)
#
# except Exception as es:
#     print("An error occurred:", es)


# try:
#     # Чекаємо, поки карусель з'явиться на сторінці
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CLASS_NAME, "item-photos"))
#     )
#
#     # Знаходимо всі елементи з класом item-thumbnail
#     thumbnails = driver.find_elements(By.CLASS_NAME, "item-thumbnail")
#
#     # Проходимо через всі елементи та отримуємо URL зображень
#     for thumbnail in thumbnails:
#         img_element = thumbnail.find_element(By.TAG_NAME, "img")
#         img_url = img_element.get_attribute("src")
#         image_urls.append(img_url)  # Додаємо URL у список
#     print(image_urls)
#
# except Exception as es:
#     print(es)


# file_name = f"{product_title_value}_{product_price}_{timestamp}_rest.jpg"
# image_path = os.path.abspath(file_name)
# names_images_db.append(image_path)
# file_path = os.path.join(product_directory, file_name)

# downd all elements from list of urls
# while image_urls:
#     url_el = image_urls.pop(0)
#
#     file_name = f"{product_title_value}_{product_price}_{timestamp}_rest.jpg"
#     file_path = os.path.join(product_directory, file_name)
#
#     download_image(url_el, file_path)
#     names_images_db.append(file_path)
#     print(image_urls)
#     print(names_images_db)
#     time.sleep(1)
#
# print("All images downloaded.")

# for index, url_el in enumerate(image_urls):
#     # Generate a unique file name for each image
#     file_name = f"{product_title_value}_{product_price}_{timestamp}_img{index}.jpg"
#     file_path = os.path.join(product_directory, file_name)
#
#     download_image(url_el, file_path)
#     names_images_db.append(file_path)  # Add the path to your list of downloaded images
#     print(f"Downloaded image {index + 1} of {len(image_urls)}: {file_path}")
#     time.sleep(1)  # Maintain a delay to avoid overwhelming the server
#
# print("All images downloaded.")
#


# try:
#     add_data_db(
#         title=product_title_value,
#         price=product_price,
#         company=product_company,
#         size=size_value,
#         condition=product_condition_value,
#         color=product_color_value,
#         location=product_location_values,
#         payment_method=product_payment_method_value,
#         description=product_desc_values,
#         category=product_cat_value,
#         image_path=local_path_images_list,
#     )
#
#
#     time.sleep(2)
#
# except Exception as ex:
#     print(ex)


# html images elements
# first_product_images_block = driver.find_elements(By.CSS_SELECTOR,
#                                                   'img[data-testid="image-carousel-image-shown"]')
#
# for first_product_images_value in first_product_images_block:
#     first_product_images_value = first_product_images_value.get_attribute('src')
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     file_name = f"{product_title_value}_{timestamp}_rest.jpg"
#     image_path = os.path.abspath(file_name)
#     local_path_images_list.append(image_path)
#     file_path = os.path.join(product_directory, file_name)
#
#     # download_image(first_product_images_value, file_path)
#     time.sleep(2)
#
# rest_images_block = driver.find_elements(By.CSS_SELECTOR, 'img[data-testid="image-carousel-image"]')
#
# for rest_images_values in rest_images_block:
#     rest_images_values = rest_images_values.get_attribute('src')
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     file_name = f"{product_title_value}_{timestamp}_rest.jpg"
#     image_path = os.path.abspath(file_name)
#     local_path_images_list.append(image_path)
#     file_path = os.path.join(product_directory, file_name)
#
#     # download_image(rest_images_values, file_path)
#     print('========================================')
#     print(product_title_value)
#     print(product_price)
#     print(product_company)
#     print(size_value)
#     print(product_condition_value)
#     print(product_color_value)
#     print(product_location_values)
#     print(product_payment_method_value)
#     print(product_desc_values)
#     print(product_cat_value)
#     print(local_path_images_list)
#     print('========================================')
#     # time.sleep(2)


#     except Exception as ex:
#         print(ex)
#
#     finally:
#         driver.back()
#         time.sleep(3)
#
# driver.quit()
# return None