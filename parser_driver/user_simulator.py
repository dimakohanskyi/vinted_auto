import random
import time


def random_scroll(driver, min_pause=1, max_pause=5, min_scroll=100, max_scroll=500):
    pause_time = random.uniform(min_pause, max_pause)
    time.sleep(pause_time)
    scroll_distance = random.randint(min_scroll, max_scroll)
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")


def random_timesleep(min_seconds=1, max_seconds=5):
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)



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
