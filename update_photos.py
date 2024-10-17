from PIL import Image, ImageEnhance


def photos_changer(img_path, save_path):
    img = Image.open(img_path)
    img_resized = change_photos_size(img)
    img_contrast = change_contrast(img_resized)
    img_bright = change_brightness(img_contrast)
    img_colored = change_color_balance(img_bright)
    img_colored.save(save_path)


def change_photos_size(img):
    img = img.resize((572, 738))
    return img


def change_contrast(img):
    enhancer_contrast = ImageEnhance.Contrast(img)
    img_contrast = enhancer_contrast.enhance(0.99)
    return img_contrast


def change_brightness(img):
    enhancer_brightness = ImageEnhance.Brightness(img)
    img_bright = enhancer_brightness.enhance(1.0118)
    return img_bright


def change_color_balance(img):
    r, g, b = img.split()

    r = r.point(lambda i: i + 1.45)  # Збільшення червоного каналу
    g = g.point(lambda i: i + 1.39)  # Збільшення зеленого каналу
    b = b.point(lambda i: i + 0.44)  # Збільшення синього каналу

    img_colored = Image.merge('RGB', (r, g, b))
    return img_colored


# Приклад використання:
photos_changer('/Users/user/Desktop/projects/python_projects/vinted_aut/123.jpg',
               '/Users/user/Desktop/projects/python_projects/vinted_aut/test.jpg')


