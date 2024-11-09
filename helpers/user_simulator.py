import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def random_scroll(driver, min_pause=1, max_pause=5, min_scroll=100, max_scroll=300):
    pause_time = random.uniform(min_pause, max_pause)
    time.sleep(pause_time)
    direction = random.choice([-1, 1])
    scroll_distance = direction * random.randint(min_scroll, max_scroll)
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")


def random_timesleep(min_seconds=1, max_seconds=5):
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)


def is_blank_space(driver, x, y):
    js_code = f"""
        var elem = document.elementFromPoint({x}, {y});
        return elem === document.body || elem === null;
    """
    return driver.execute_script(js_code)


def random_click_on_blank_space(driver):
    viewport_width = driver.execute_script("return window.innerWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    max_attempts = 10  # Limit attempts to find a blank space

    for _ in range(max_attempts):
        x = random.randint(0, viewport_width - 1)
        y = random.randint(0, viewport_height - 1)

        if is_blank_space(driver, x, y):
            ActionChains(driver).move_by_offset(x, y).click().perform()
            print(f"Clicked on blank space at ({x}, {y})")
            return


def random_mouse_movement(driver):
    viewport_width = driver.execute_script("return window.innerWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    x = random.randint(0, viewport_width - 1)
    y = random.randint(0, viewport_height - 1)
    ActionChains(driver).move_by_offset(x, y).perform()
    print(f"Moved mouse to ({x}, {y})")


# def click_empty_block(driver):
#     empty_blocks = driver.find_elements(By.XPATH, "//div[not(node()) or normalize-space(text())='']")
#
#     if empty_blocks:
#         empty_block = random.choice(empty_blocks)
#
#         ActionChains(driver).move_to_element(empty_block).click().perform()


def click_empty_block(driver):
    empty_blocks = driver.find_elements(By.XPATH, "//div")

    empty_blocks = [block for block in empty_blocks if block.text.strip() == '' and len(block.find_elements(By.XPATH, "./*")) == 0]

    if empty_blocks:
        empty_block = random.choice(empty_blocks)
        ActionChains(driver).move_to_element(empty_block).click().perform()
    else:
        print("Не знайдено порожніх блоків для кліку.")






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
