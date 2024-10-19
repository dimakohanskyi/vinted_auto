# delete_products.py
from tkinter import messagebox
from db.models import Product, ProductImage
from tkinter import Toplevel, Button, Label


def delete_user_products(session, user):
    try:
        products_to_delete = session.query(Product).filter(Product.user_id == user.id).all()

        if products_to_delete:
            confirm = messagebox.askyesno("Підтвердження", 
                                          f"User {user.login} має {len(products_to_delete)} продуктів. Ви бажаєте їх видалити?")
            if confirm:
                # Видаляємо зображення продуктів
                for product in products_to_delete:
                    session.query(ProductImage).filter(ProductImage.product_id == product.id).delete()

                # Видаляємо самі продукти
                session.query(Product).filter(Product.user_id == user.id).delete()
                session.commit()

                print(f"Deleted old products and images for user: {user.login}")
                return True  # Продукти видалені

            else:
                print("Процес видалення було скасовано.")
                return False  # Користувач скасував видалення

        else:
            print("У користувача немає продуктів.")
            return False  # Продуктів немає, видалення не потрібне

    except Exception as e:
        session.rollback()
        print(f"Error deleting old data: {e}")
        return False

    finally:
        session.close()


def ask_user_confirmation(title, message):
    # Створюємо нове вікно
    confirmation_window = Toplevel()
    confirmation_window.title(title)

    # Змінна для зберігання результату
    result = [None]  # Використовуємо список для зміни значення в замиканні

    # Додаємо мітку з повідомленням
    Label(confirmation_window, text=message).pack(pady=10)

    def on_yes():
        result[0] = True
        confirmation_window.destroy()  # Закриваємо вікно

    def on_no():
        result[0] = False
        confirmation_window.destroy()  # Закриваємо вікно

    # Додаємо кнопки
    Button(confirmation_window, text="Так", command=on_yes).pack(side="left", padx=20, pady=10)
    Button(confirmation_window, text="Ні", command=on_no).pack(side="right", padx=20, pady=10)

    confirmation_window.transient()  # Зробити вікно модальним
    confirmation_window.grab_set()    # Зафіксувати фокус на цьому вікні
    confirmation_window.wait_window()  # Очікувати закриття вікна

    return result[0]  # Повертаємо результат