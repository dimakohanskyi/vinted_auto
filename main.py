from parser_driver.parser import parsing_products_data
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db.models import User, SessionLocal, Product, ProductImage
from tkinter import PhotoImage
from helpers.helper import delete_user_products, ask_user_confirmation
from helpers.update_photos import process_images_folders
from dolphin_anty.dolphi_anty import dolphin_aut


root = tk.Tk()
root.title("Парсер Лисого")
root.geometry("1200x600")
notebook = ttk.Notebook(root)


#====================== First Tab ======================

def parsing_on_button_click():
    session = SessionLocal()
    user_input_url = entry_tab1_url.get().strip()

    if len(user_input_url) == 0:
        messagebox.showwarning("Увага", "Будь ласка, введіть URL!")
        return

    user = session.query(User).filter(User.account_url == user_input_url).first()

    if not user:
        label.config(text=f"User with URL: {user_input_url} doesn't exist")
        return

    try:
        products_exist = session.query(Product).filter(Product.user_id == user.id).count() > 0

        if products_exist:
            if delete_user_products(session, user):
                confirm_import = ask_user_confirmation("Імпорт",
                                                       "Продукти видалені. Ви бажаєте виконати імпорт нових даних?")
                if confirm_import:
                    start_import(user_input_url)
            else:
                label.config(text="Процес видалення було скасовано.")
        else:
            confirm_import = ask_user_confirmation("Імпорт",
                                                   "У користувача немає продуктів. Бажаєте імпортувати нові?")
            if confirm_import:
                start_import(user_input_url)
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
    user_input = entry_tab1_url.get()
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
        process_images_folders(user_login=user.login)
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

entry_tab1_url = tk.Entry(tab1, width=50)
entry_tab1_url.pack(pady=10)

button = tk.Button(tab1, text="Start-Parser", command=parsing_on_button_click)
button.pack(pady=10)

update_photos_button = tk.Button(tab1, text="Update Photos", command=update_photos)
update_photos_button.pack(pady=10)



#=========================  Second Tab ======================

def process_add_products():
    profile_anty_id = label_anty_id_entry.get()

    try:
        dolphin_aut(profile_id=profile_anty_id)
    except Exception as ex:
        print(ex)

    return None


tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Залив Оголошень")

background_label = tk.Label(tab2)
background_label.place(x=0, y=40, relwidth=1, relheight=1)

label_anty_id = tk.Label(tab2, text="Введіть anty-id:")
label_anty_id.pack(pady=10)

label_anty_id_entry = tk.Entry(tab2, width=50)
label_anty_id_entry.pack(pady=10)

button = tk.Button(tab2, text="add", command=process_add_products)
button.pack(pady=10)


#=========================  Third Tab ======================
def add_new_user():
    user_login = login_user_input.get()
    user_password = password_user_input.get()
    user_url = url_user_input.get()
    dolphin_anty_id = dolphin_profile_id.get()

    try:
        new_user = User(
            login=user_login,
            password=user_password,
            account_url=user_url,
            dolphin_anty_id=dolphin_anty_id
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


tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Add User")

label_add_user = tk.Label(tab3, text="Create User")
label_add_user.pack(pady=20)

label_login_user_input = tk.Label(tab3, text="Login")
label_login_user_input.pack(pady=5)
login_user_input = tk.Entry(tab3, width=40)
login_user_input.pack(pady=10)


label_password_user_input = tk.Label(tab3, text="Password")
label_password_user_input.pack(pady=5)
password_user_input = tk.Entry(tab3, width=40)
password_user_input.pack(pady=10)


label_url_user_input = tk.Label(tab3, text="Url")
label_url_user_input.pack(pady=5)
url_user_input = tk.Entry(tab3, width=40)
url_user_input.pack(pady=10)


label_dolphin_profile_id = tk.Label(tab3, text="dolphin profile id")
label_dolphin_profile_id.pack(pady=5)
dolphin_profile_id = tk.Entry(tab3, width=40)
dolphin_profile_id.pack(pady=10)


button_create_user = tk.Button(tab3, text="Create", command=add_new_user)
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


tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Delete User")

label_del_user = tk.Label(tab4, text="Delete User")
label_del_user.pack(pady=20)

label_del_user_input = tk.Label(tab4, text="Enter Login")
label_del_user_input.pack(pady=5)
del_user_input = tk.Entry(tab4, width=40)
del_user_input.pack(pady=10)


button_del_user = tk.Button(tab4, text="Delete", command=delete_user)
button_del_user.pack(pady=20)


#======================  Fouth Tab  ======================#

def show_user_products():
    user_login = user_login_input.get()

    try:
        session = SessionLocal()
        user = session.query(User).filter(User.login == user_login).first()

        if user:
            user_id = user.id
            user_products = session.query(Product).filter(Product.user_id == user_id).all()

            # Clear the text widget before displaying new results
            product_display.delete(1.0, tk.END)

            if user_products:
                for product in user_products:
                    product_display.insert(tk.END, "\n")
                    product_display.insert(tk.END, "\n")
                    product_display.insert(tk.END, f"   Product ID: {product.id}\n")
                    product_display.insert(tk.END, f"   Title: {product.title}\n")
                    product_display.insert(tk.END, f"   Marka: {product.company}\n")
                    product_display.insert(tk.END, f"   Price: {product.price}\n")
                    product_display.insert(tk.END, f"   Size: {product.size}\n")
                    product_display.insert(tk.END, f"   URL: {product.unique_identifier}\n")
                    product_display.insert(tk.END, f"   Active: {product.is_active}\n")
                    product_display.insert(tk.END, "\n")
                    product_display.insert(tk.END, "\n")
            else:
                product_display.insert(tk.END, "No products found for this user.\n")
        else:
            messagebox.showwarning("Warning", f"No user found with the login: '{user_login}'")

    except Exception as ex:
        messagebox.showerror("Error", f"Failed to fetch products: {ex}")

    finally:
        session.close()

# Create a new tab for displaying user products
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="Show User Products")

label_user_login = tk.Label(tab5, text="Enter User Login")
label_user_login.pack(pady=10)
user_login_input = tk.Entry(tab5, width=40)
user_login_input.pack(pady=10)

button_show_products = tk.Button(tab5, text="Show Products", command=show_user_products)
button_show_products.pack(pady=20)

# Text widget to display the products
product_display = tk.Text(tab5, wrap=tk.WORD, width=160, height=120)
product_display.pack(pady=10)


#======================  Fifth Tab  ======================#

def activate_product():
    product_id = product_id_input.get()

    try:
        session = SessionLocal()
        product = session.query(Product).filter(Product.id == product_id).first()

        if product:
            if product.is_active:
                messagebox.showinfo("Info", f"Product ID '{product_id}' is already active.")
            else:
                product.is_active = True
                session.commit()
                messagebox.showinfo("Success", f"Product ID '{product_id}' has been activated.")
        else:
            messagebox.showwarning("Warning", f"No product found with ID: '{product_id}'")

    except Exception as ex:
        session.rollback()
        messagebox.showerror("Error", f"Failed to activate product: {ex}")

    finally:
        session.close()


def deactivate_product():
    product_id = product_id_input.get()

    try:
        session = SessionLocal()
        product = session.query(Product).filter(Product.id == product_id).first()

        if product:
            if product.is_active:
                product.is_active = False
                session.commit()
                messagebox.showinfo("Success", f"Product ID '{product_id}' has been deactivated.")
        else:
            messagebox.showwarning("Warning", f"No product found with ID: '{product_id}'")

    except Exception as ex:
        session.rollback()
        messagebox.showerror("Error", f"Failed to activate product: {ex}")

    finally:
        session.close()


tab6 = ttk.Frame(notebook)
notebook.add(tab6, text="Activate Product")

label_product_id = tk.Label(tab6, text="Enter Product ID to Activate")
label_product_id.pack(pady=10)

product_id_input = tk.Entry(tab6, width=40)
product_id_input.pack(pady=10)

button_activate_product = tk.Button(tab6, text="Activate Product", command=activate_product)
button_activate_product.pack(pady=20)

button_activate_product = tk.Button(tab6, text="Deactivate Product", command=deactivate_product)
button_activate_product.pack(pady=20)










root.mainloop()