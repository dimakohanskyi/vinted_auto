from parser_driver.parser import parsing_products_data
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db.models import User, SessionLocal, Product, ProductImage
from tkinter import PhotoImage
from helpers.helper import delete_user_products, ask_user_confirmation
from helpers.update_photos import process_images_folders


root = tk.Tk()
root.title("Парсер Лисого")
root.geometry("1200x600")
notebook = ttk.Notebook(root)



#TODO винести функцію в окремий потік, щоб не блокувався графічний інтерфейс і показувались логи (не пріорітeтно)
#TODO зробити логи в першому табі (не пріорітeтно)



#====================== First Tab ======================


def parsing_on_button_click():
    session = SessionLocal()
    user_input = entry.get()

    if not user_input:
        messagebox.showwarning("Увага", "Будь ласка, введіть URL!")
        return

    user = session.query(User).filter(User.account_url == user_input).first()

    if not user:
        label.config(text=f"User with URL: {user_input} doesn't exist")
        return

    try:
        products_exist = session.query(Product).filter(Product.user_id == user.id).count() > 0

        if products_exist:
            if delete_user_products(session, user):
                confirm_import = ask_user_confirmation("Імпорт",
                                                       "Продукти видалені. Ви бажаєте виконати імпорт нових даних?")
                if confirm_import:
                    start_import(user_input)
            else:
                label.config(text="Процес видалення було скасовано.")
        else:
            confirm_import = ask_user_confirmation("Імпорт",
                                                   "У користувача немає продуктів. Бажаєте імпортувати нові?")
            if confirm_import:
                start_import(user_input)
            else:
                label.config(text="Імпорт даних було скасовано.")

    except Exception as e:
        session.rollback()
        label.config(text="Сталася помилка при обробці.")
        print(f"Error: {e}")

    finally:
        session.close()


def start_import(user_input):
    try:
        label.config(text=f"Start parsing data from: {user_input}")
        parsing_products_data(user_input)
    except Exception as e:
        label.config(text="Сталася помилка під час парсингу.")
        print(f"Error during parsing: {e}")


def update_photos():
    user_input = entry.get()
    session = SessionLocal()

    if not user_input:
        messagebox.showwarning("Увага", "Будь ласка, введіть URL користувача!")
        return

    user = session.query(User).filter(User.account_url == user_input).first()

    if not user:
        messagebox.showerror("Помилка", "Користувача не знайдено!")
        return

    print(f"Користувач знайдений: {user.login}")

    # Виклик функції оновлення фотографій
    try:
        process_images_folders(user_login=user.login)  # Тут викликаємо вашу функцію обробки фото
        messagebox.showinfo("Успіх", "Фотографії успішно оновлено!")
    except Exception as e:
        print(f"Помилка при оновленні фото: {e}")
        messagebox.showerror("Помилка", f"Помилка при оновленні фото: {e}")
    finally:
        session.close()  # Закриваємо сесію з базою даних після завершення




tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Parser")

background_label = tk.Label(tab1)
background_label.place(x=0, y=40, relwidth=1, relheight=1)

label = tk.Label(tab1, text="Введіть URL:")
label.pack(pady=10)

entry = tk.Entry(tab1, width=50)
entry.pack(pady=10)

button = tk.Button(tab1, text="Start-Parser", command=parsing_on_button_click)
button.pack(pady=10)

update_photos_button = tk.Button(tab1, text="Update Photos", command=update_photos)
update_photos_button.pack(pady=10)



#=========================  Second Tab ======================
def add_new_user():
    user_login = login_user_input.get()
    user_password = password_user_input.get()
    user_url = url_user_input.get()

    try:
        new_user = User(
            login=user_login,
            password=user_password,
            account_url=user_url,
        )
        session = SessionLocal()
        session.add(new_user)
        session.commit()

        messagebox.showinfo("Success", f"User '{user_login}' created successfully.")

    except Exception as ex:
        session.rollback()
        messagebox.showerror("Error", f"Failed to create user: {ex}")

    finally:
        session.close()


tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Add User")

label_add_user = tk.Label(tab2, text="Create User")
label_add_user.pack(pady=20)

label_login_user_input = tk.Label(tab2, text="Login")
label_login_user_input.pack(pady=5)
login_user_input = tk.Entry(tab2, width=40)
login_user_input.pack(pady=10)


label_password_user_input = tk.Label(tab2, text="Password")
label_password_user_input.pack(pady=5)
password_user_input = tk.Entry(tab2, width=40)
password_user_input.pack(pady=10)


label_url_user_input = tk.Label(tab2, text="Url")
label_url_user_input.pack(pady=5)
url_user_input = tk.Entry(tab2, width=40)
url_user_input.pack(pady=10)

button_create_user = tk.Button(tab2, text="Create", command=add_new_user)
button_create_user.pack(pady=20)

notebook.pack(expand=True, fill='both')


#======================  Third Tab  ======================
def delete_user():
    user_login = del_user_input.get()

    try:
        session = SessionLocal()
        user_to_delete = session.query(User).filter(User.login == user_login).first()

        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            messagebox.showinfo("Success", f"User '{user_login}' has been deleted successfully.")
        else:
            messagebox.showwarning("Warning", f"No user found with the login: '{user_login}'")

    except Exception as ex:
        session.rollback()
        messagebox.showerror("Error", f"Failed to create user: {ex}")

    finally:
        session.close()


tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Delete User")

label_del_user = tk.Label(tab3, text="Delete User")
label_del_user.pack(pady=20)

label_del_user_input = tk.Label(tab3, text="Enter Login")
label_del_user_input.pack(pady=5)
del_user_input = tk.Entry(tab3, width=40)
del_user_input.pack(pady=10)


button_del_user = tk.Button(tab3, text="Delete", command=delete_user)
button_del_user.pack(pady=20)


root.mainloop()