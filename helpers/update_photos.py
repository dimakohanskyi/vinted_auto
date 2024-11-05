import os
from db.models import SessionLocal, User, ProductImage, Product
from PIL import Image, ImageEnhance


def photos_changer(img_path, save_path):
    img = Image.open(img_path)

    img = img.convert('RGB')

    img_resized = change_photos_size(img)
    img_contrast = change_contrast(img_resized)
    img_bright = change_brightness(img_contrast)
    img_colored = change_color_balance(img_bright)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img_colored.save(save_path)


def change_photos_size(img):
    return img.resize((572, 738))


def change_contrast(img):
    enhancer_contrast = ImageEnhance.Contrast(img)
    return enhancer_contrast.enhance(1)


def change_brightness(img):
    enhancer_brightness = ImageEnhance.Brightness(img)
    return enhancer_brightness.enhance(1.1)


def change_color_balance(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(i, 253))
    g = g.point(lambda i: min(i, 253))
    b = b.point(lambda i: min(i, 253))
    return Image.merge('RGB', (r, g, b))


def process_images_folders(user_login):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.login == user_login).first()
        if not user:
            print(f"Користувача з логіном {user_login} не знайдено.")
            return

        product_images = session.query(ProductImage).join(ProductImage.product).filter(Product.user_id == user.id).all()

        if not product_images:
            print(f"Зображення для користувача {user_login} не знайдено.")
            return

        for product_image in product_images:
            original_image_path = product_image.original_image_path
            product_directory = os.path.basename(os.path.dirname(original_image_path))  # Назва директорії продукту

            fake_directory = os.path.join('images', 'fake', user_login, product_directory)  # Шлях до фейкової папки
            os.makedirs(fake_directory, exist_ok=True)  # Створюємо папку, якщо не існує

            fake_image_path = os.path.join(fake_directory,
                                           os.path.basename(original_image_path))  # Шлях до фейкового зображення

            if not os.path.exists(original_image_path):
                print(f"Original image not found: {original_image_path}")
                continue

            try:
                print(f"Processing: {original_image_path}")

                photos_changer(original_image_path, fake_image_path)

                if not os.path.exists(fake_image_path):
                    raise Exception(f"Failed to create fake image at {fake_image_path}")

                # Оновлюємо запис в базі, додаючи шлях до "fake" зображення
                product_image.fake_image_path = os.path.abspath(fake_image_path)
                session.commit()

                print(f"Processed and saved new fake image: {fake_image_path}")
            except Exception as e:
                print(f"Error processing {original_image_path}: {e}")
                session.rollback()

    except Exception as ex:
        print(f"Error accessing the database: {ex}")
        session.rollback()

    finally:
        session.close()










