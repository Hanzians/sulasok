from tkinter import Tk, Button, Entry, Frame, Label, Listbox, Canvas, StringVar, LEFT, RIGHT, CENTER, END, Toplevel
from tkinter import ttk, messagebox, font
import tkinter
from PIL import ImageTk, Image
import mysql.connector
import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox





# --------------- Database Connection (Reusable) ---------------
def connect_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin123",
            port=3305,
            database="milktea"
        )
        cursor = conn.cursor()
        return cursor, conn  # Return both cursor and connection objects
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to the database: {e}")
        return None, None  # Return None if connection fails


# --------------- Dashboard Data Fetching ---------------
def fetch_dashboard_data():
    """
    Fetch today’s stats:
      - total_orders from orders table,
      - total_sales from orders table,
      - total_expenses from expenses table,
      - profit calculated as sales minus expenses.
    """
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin123",
            database="milktea"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders WHERE DATE(date_ordered) = CURDATE()")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM orders WHERE DATE(date_ordered) = CURDATE()")
        total_sales = cursor.fetchone()[0]

        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses WHERE DATE(date) = CURDATE()")
        total_expenses = cursor.fetchone()[0]

        profit = total_sales - total_expenses

        conn.close()
    except mysql.connector.Error as err:
        print("Database error:", err)
        total_orders, total_sales, total_expenses, profit = 0, 0, 0, 0

    return total_orders, total_sales, total_expenses, profit


# --------------- Main Application Window ---------------
root = Tk()
root.geometry('1920x1080+0+0')
root.resizable(0, 0)
root.title('Milktea Inventory')
root.config(bg='white')

# Fonts
title_font = font.Font(family="Georgia", size=22, weight="bold")
stat_font = font.Font(family="Arial", size=14)

# ---------- Load Images (Update file paths as needed) ----------
icon_Label_img = Image.open(r"C:\Users\glycel\Downloads\inventoryy.png")
icon_Label_resized = icon_Label_img.resize((70, 70), Image.Resampling.LANCZOS)
icon_Label = ImageTk.PhotoImage(icon_Label_resized)

logoImage_img = Image.open(r"C:\Users\glycel\Downloads\Sulasok.png")
logoImage_resized = logoImage_img.resize((450, 400), Image.Resampling.LANCZOS)
logoImage = ImageTk.PhotoImage(logoImage_resized)
imageLabel = Label(image=logoImage)
imageLabel.place(x=0, y=640)

log_icon_img = Image.open(r"C:\Users\glycel\Downloads\logout.png")
log_icon_resized = log_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
log_icon = ImageTk.PhotoImage(log_icon_resized)

Sign_icon_img = Image.open(r"C:\Users\glycel\Downloads\Sign-in.png")
Sign_icon_resized = Sign_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
Sign_icon = ImageTk.PhotoImage(Sign_icon_resized)

dash_icon_img = Image.open(r"C:\Users\glycel\Downloads\dashboard.png")
dash_icon_resized = dash_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
dash_icon = ImageTk.PhotoImage(dash_icon_resized)

inv_icon_img = Image.open(r"C:\Users\glycel\Downloads\inventory.png")
inv_icon_resized = inv_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
inv_icon = ImageTk.PhotoImage(inv_icon_resized)

productm_icon_img = Image.open(r"C:\Users\glycel\Downloads\productm.png")
productm_icon_resized = productm_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
productm_icon = ImageTk.PhotoImage(productm_icon_resized)

supplier_icon_img = Image.open(r"C:\Users\glycel\Downloads\supplier.png")
supplier_icon_resized = supplier_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
supplier_icon = ImageTk.PhotoImage(supplier_icon_resized)

bell_icon_img = Image.open(r"C:\Users\glycel\Downloads\bell.png")
bell_icon_resized = bell_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
bell_icon = ImageTk.PhotoImage(bell_icon_resized)

userm_icon_img = Image.open(r"C:\Users\glycel\Downloads\userm.png")
userm_icon_resized = userm_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
userm_icon = ImageTk.PhotoImage(userm_icon_resized)

# Header Labels
Label1 = Label(root, image=icon_Label, compound=LEFT, text="Milktea Inventory", font=('Helvetica', 13, 'bold'),
               bg='#1e405d', fg='White', padx=90, pady=13.4, anchor='nw')
Label1.place(x=0, y=0)

Label2 = Label(root, bg='#244d6f', anchor='c', padx=900, pady=40)
Label2.place(x=450, y=0)


# ------------------ DASHBOARD ------------------
def dashboard():
    dashboard_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    dashboard_frame.place(x=450, y=100)

    # Header with Back Button
    headlabel = Label(dashboard_frame, text="Dashboard", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    # Undo Button
    undo_icon_img = Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(dashboard_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                       bg='#7aabd4', cursor='hand2', command=lambda: dashboard_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # Fetch updated stats
    orders, sales, expenses, profit = fetch_dashboard_data()

    # Stat Boxes
    profit_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    profit_box.place(x=100, y=100)
    Label(profit_box, text="Profit Today", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(profit_box, text=f"₱{profit:,.0f}", font=("Arial", 18, "bold"), bg="white", fg="#333").pack()

    expenses_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    expenses_box.place(x=400, y=100)
    Label(expenses_box, text="Expenses Today", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(expenses_box, text=f"₱{expenses:,.0f}", font=("Arial", 18, "bold"), bg="white", fg="#333").pack()

    orders_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    orders_box.place(x=700, y=100)
    Label(orders_box, text="Orders Today", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(orders_box, text=str(orders), font=("Arial", 18, "bold"), bg="white", fg="#333").pack()

    # Canvas visualization for Profit vs Expenses
    chart_canvas = Canvas(dashboard_frame, width=500, height=300, bg='white')
    chart_canvas.place(x=100, y=300)
    max_val = max(profit, expenses)
    if max_val == 0:
        max_val = 1
    profit_width = int((profit / max_val) * 400)
    expenses_width = int((expenses / max_val) * 400)
    # Draw profit bar (green)
    chart_canvas.create_rectangle(50, 50, 50 + profit_width, 100, fill="green")
    chart_canvas.create_text(50 + profit_width + 50, 75, text=f"Profit: ₱{profit:,.0f}", anchor="w",
                             font=("Arial", 12))
    # Draw expenses bar (red)
    chart_canvas.create_rectangle(50, 150, 50 + expenses_width, 200, fill="red")
    chart_canvas.create_text(50 + expenses_width + 50, 175, text=f"Expenses: ₱{expenses:,.0f}", anchor="w",
                             font=("Arial", 12))


# ------------------ INVENTORY ------------------
def inventory():
    global inv_treeview, item_name_entry, quantity_entry, category_entry, price_entry, unit_combobox

    inventory_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    inventory_frame.place(x=450, y=100)

    # Undo Icon (Back Button)
    undo_icon = Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized = undo_icon.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)

    headlabel2 = Label(inventory_frame, text="Inventory Management", font=('times new roman', 20, 'bold'),
                       bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel2.place(x=0, y=0)

    undolabel = Button(inventory_frame, image=undo_icon, compound=RIGHT, borderwidth='0', bg='#7aabd4',
                       cursor='hand2', command=lambda: inventory_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # --- Data Entry Frame (moved above table) ---
    entry_frame = Frame(inventory_frame, bg='#f0f0f0')
    entry_frame.place(x=100, y=80)  # << Moved up here

    Label(entry_frame, text='Item Name:', font=('times new roman', 15)).grid(row=0, column=0, padx=10, pady=10)
    item_name_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    item_name_entry.grid(row=0, column=1, padx=10)

    Label(entry_frame, text='Quantity:', font=('times new roman', 15)).grid(row=0, column=2, padx=10, pady=10)
    quantity_entry = Entry(entry_frame, font=('times new roman', 15), width=10)
    quantity_entry.grid(row=0, column=3, padx=10)

    Label(entry_frame, text='Unit:', font=('times new roman', 15)).grid(row=0, column=4, padx=10, pady=10)
    unit_combobox = ttk.Combobox(entry_frame, font=('times new roman', 15),
                                  values=['pcs', 'grams', 'ml', 'kg'], state='readonly', width=10)
    unit_combobox.grid(row=0, column=5, padx=10)
    unit_combobox.set("pcs")

    Label(entry_frame, text='Category:', font=('times new roman', 15)).grid(row=1, column=0, padx=10, pady=10)
    category_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    category_entry.grid(row=1, column=1, padx=10)

    Label(entry_frame, text='Price:', font=('times new roman', 15)).grid(row=1, column=2, padx=10, pady=10)
    price_entry = Entry(entry_frame, font=('times new roman', 15), width=10)
    price_entry.grid(row=1, column=3, padx=10)

    # --- Buttons Above Table ---
    Button(entry_frame, text="Add", font=('times new roman', 20), bg="#32d9dc", fg='white',
           command=add_inventory).grid(row=2, column=0, pady=20, padx=10)
    Button(entry_frame, text="Update", font=('times new roman', 20), bg="#F6D51A", fg='white',
           command=update_inventory).grid(row=2, column=1, pady=20, padx=10)
    Button(entry_frame, text="Delete", font=('times new roman', 20), bg="#D90B11", fg='white',
           command=delete_inventory).grid(row=2, column=4, pady=20, padx=10)
    Button(entry_frame, text="Clear", font=('times new roman', 20), bg="#9ba09d", fg='white',
           command=clear_inventory_fields).grid(row=2, column=2, pady=20, padx=10)

    # --- Inventory Table Frame ---
    tree_frame = Frame(inventory_frame, bg='white')
    tree_frame.place(x=50, y=300, width=1350, height=450) 

    style = ttk.Style()
    style.theme_use("clam")  # Use a theme that supports good customization
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")

    style.configure("Treeview.Heading",
                    background="lightblue",
                    foreground="black",
                    font=('Times New Roman', 13, 'bold'))

    style.map("Treeview",
            background=[('selected', 'yellow')],
            foreground=[('selected', 'black')])


    inv_treeview = ttk.Treeview(tree_frame, columns=('Item', 'Quantity', 'Unit', 'Category', 'Price'), show='headings')
    inv_treeview.tag_configure('evenrow', background='white')
    inv_treeview.tag_configure('oddrow', background='light blue')  # Light gray

    inv_treeview.heading('Item', text='Item Name')
    inv_treeview.heading('Quantity', text='Quantity')
    inv_treeview.heading('Category', text='Category')
    inv_treeview.heading('Price', text='Price')
    inv_treeview.heading('Unit', text='Unit')

    inv_treeview.column('Item', width=200)
    inv_treeview.column('Quantity', width=200)
    inv_treeview.column('Category', width=200)
    inv_treeview.column('Price', width=200)
    inv_treeview.column('Unit', width=100)

    inv_treeview.pack(fill='both', expand=True)
    inv_treeview.bind('<<TreeviewSelect>>', fill_inventory_fields)

    load_inventory_data()


def add_inventory():
    item = item_name_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    unit = unit_combobox.get()
    if item and quantity and category and price:
        cursor, conn = connect_database()
        if cursor:
            try:
                cursor.execute("INSERT INTO inventory (item_name, quantity, unit, category, price) VALUES (%s, %s, %s, %s, %s)",
                    (item, quantity, unit, category, price))
                conn.commit()
                messagebox.showinfo("Success", "Item added successfully!")
                add_notification(f"Added item '{item}' to inventory.")
                load_inventory_data()
                clear_inventory_fields()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add item: {e}")
            finally:
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

def load_inventory_data():
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("SELECT item_name, quantity, unit, category, price FROM inventory")
            rows = cursor.fetchall()
            inv_treeview.delete(*inv_treeview.get_children())

            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                inv_treeview.insert('', 'end', values=row, tags=(tag,))

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to load inventory data: {e}")
        finally:
            conn.close()

def update_inventory():
    selected = inv_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select an item to update.")
        return
    data = inv_treeview.item(selected, 'values')
    old_item = data[0]
    new_item = item_name_entry.get()
    new_quantity = quantity_entry.get()
    new_category = category_entry.get()
    new_price = price_entry.get()
    new_unit = unit_combobox.get()
    if not new_item or not new_quantity or not new_category or not new_price:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute(
                "UPDATE inventory SET item_name=%s, quantity=%s, unit=%s, category=%s, price=%s WHERE item_name=%s",
                (new_item, new_quantity, new_unit, new_category, new_price, old_item)
            )
            conn.commit()
            messagebox.showinfo("Success", "Item updated successfully!")
            add_notification(f"Updated item '{old_item}' to '{new_item}'.")
            load_inventory_data()
            clear_inventory_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")
        finally:
            conn.close()


def delete_inventory():
    selected = inv_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select an item to delete.")
        return
    data = inv_treeview.item(selected, 'values')
    item = data[0]
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("DELETE FROM inventory WHERE item_name = %s", (item,))
            conn.commit()
            messagebox.showinfo("Deleted", f"{item} has been deleted.")
            add_notification(f"Deleted item '{item}' from inventory.")
            load_inventory_data()
            clear_inventory_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to delete item: {e}")
        finally:
            conn.close()

def clear_inventory_fields():
    item_name_entry.delete(0, 'end')
    quantity_entry.delete(0, 'end')
    category_entry.delete(0, 'end')
    price_entry.delete(0, 'end')

def fill_inventory_fields(event):
    selected = inv_treeview.focus()
    if selected:
        values = inv_treeview.item(selected, 'values')
        if values:
            item_name_entry.delete(0, 'end')
            item_name_entry.insert(0, values[0])
            quantity_entry.delete(0, 'end')
            quantity_entry.insert(0, values[1])
            unit_combobox.set(values[2])
            category_entry.delete(0, 'end')
            category_entry.insert(0, values[3])
            price_entry.delete(0, 'end')
            price_entry.insert(0, values[4])


# ------------------ PRODUCT MANAGEMENT ------------------
def product_management():
    global product_treeview, product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    product_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    product_frame.place(x=450, y=100)

    headlabel = Label(product_frame, text="Product Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    # Undo Button
    undo_icon_img = Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(product_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                       bg='#7aabd4', cursor='hand2', command=lambda: product_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # Data Entry Frame
    entry_frame = Frame(product_frame, bg='#f0f0f0')
    entry_frame.place(x=100, y=80)
    Label(entry_frame, text='Product Name:', font=('times new roman', 15)).grid(row=0, column=0, padx=10, pady=10)
    product_name_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    product_name_entry.grid(row=0, column=1, padx=10)
    Label(entry_frame, text='Customers Count:', font=('times new roman', 15)).grid(row=0, column=2, padx=10, pady=10)
    customers_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    customers_entry.grid(row=0, column=3, padx=10)
    Label(entry_frame, text='Price:', font=('times new roman', 15)).grid(row=1, column=0, padx=10, pady=10)
    price_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    price_entry.grid(row=1, column=1, padx=10)
    Label(entry_frame, text='Quantity:', font=('times new roman', 15)).grid(row=1, column=2, padx=10, pady=10)
    quantity_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    quantity_entry.grid(row=1, column=3, padx=10)
    Label(entry_frame, text='Category:', font=('times new roman', 15)).grid(row=2, column=0, padx=10, pady=10)
    product_category_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    product_category_entry.grid(row=2, column=1, padx=10)
    Label(entry_frame, text='Order Date (YYYY-MM-DD):', font=('times new roman', 15)).grid(row=2, column=2, padx=10, pady=10)
    order_date_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    order_date_entry.grid(row=2, column=3, padx=10)

    # Buttons for Product Actions
    Button(entry_frame, text="Add", font=('times new roman', 20), bg="#32d9dc", fg='white',
           command=add_product).grid(row=3, column=0, pady=20, padx=10)
    Button(entry_frame, text="Update", font=('times new roman', 20), bg="#F6D51A", fg='white',
           command=update_product).grid(row=3, column=1, pady=20, padx=10)
    Button(entry_frame, text="Delete", font=('times new roman', 20), bg="#D90B11", fg='white',
           command=delete_product).grid(row=3, column=2, pady=20, padx=10)
    Button(entry_frame, text="Clear", font=('times new roman', 20), bg="#9ba09d", fg='white',
           command=clear_product_fields).grid(row=3, column=3, pady=20, padx=10)

    # Product Sales Table
    tree_frame = Frame(product_frame, bg='white')
    tree_frame.place(x=50, y=400, width=1350, height=450)
    
    style = ttk.Style()
    style.theme_use("clam")  # Use a theme that supports good customization
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")

    style.configure("Treeview.Heading",
                    background="lightblue",
                    foreground="black",
                    font=('Times New Roman', 13, 'bold'))

    style.map("Treeview",
            background=[('selected', 'yellow')],
            foreground=[('selected', 'black')])
    
    product_treeview = ttk.Treeview(tree_frame, columns=('Product', 'Customers', 'Price', 'Quantity', 'Category', 'OrderDate'),
                                    show='headings')
    product_treeview.heading('Product', text='Product Name')
    product_treeview.heading('Customers', text='Customers Count')
    product_treeview.heading('Price', text='Price')
    product_treeview.heading('Quantity', text='Quantity')
    product_treeview.heading('Category', text='Category')
    product_treeview.heading('OrderDate', text='Order Date')
    product_treeview.column('Product', width=200)
    product_treeview.column('Customers', width=150)
    product_treeview.column('Price', width=100)
    product_treeview.column('Quantity', width=100)
    product_treeview.column('Category', width=150)
    product_treeview.column('OrderDate', width=150)
    product_treeview.pack(fill='both', expand=True)
    product_treeview.bind('<<TreeviewSelect>>', fill_product_fields)
    load_product_data()


def add_product():
    global product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry, product_treeview
    product = product_name_entry.get()
    customers = customers_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    category = product_category_entry.get()
    order_date = order_date_entry.get()
    if product and customers and price and quantity and category and order_date:
        cursor, conn = connect_database()
        if cursor:
            try:
                cursor.execute("""
                    INSERT INTO product_sales (product_name, customers_count, price, quantity, category, order_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (product, customers, price, quantity, category, order_date))
                conn.commit()
                messagebox.showinfo("Success", "Product added successfully!")
                add_notification(f"Product added: {product}")
                load_product_data()
                clear_product_fields()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")


def load_product_data():
    global product_treeview
    cursor, conn = connect_database()
    if cursor:
        cursor.execute("SELECT product_name, customers_count, price, quantity, category, order_date FROM product_sales")
        rows = cursor.fetchall()
        product_treeview.delete(*product_treeview.get_children())

        # Define row tag styles
        product_treeview.tag_configure('oddrow', background='light blue')  
        product_treeview.tag_configure('evenrow', background='white')    

        for index, row in enumerate(rows):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            product_treeview.insert('', 'end', values=row, tags=(tag,))

        conn.close()



def update_product():
    global product_treeview, product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    selected = product_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to update.")
        return
    data = product_treeview.item(selected, 'values')
    old_product = data[0]
    new_product = product_name_entry.get()
    new_customers = customers_entry.get()
    new_price = price_entry.get()
    new_quantity = quantity_entry.get()
    new_category = product_category_entry.get()
    new_order_date = order_date_entry.get()
    if not new_product or not new_customers or not new_price or not new_quantity or not new_category or not new_order_date:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("""
                UPDATE product_sales 
                SET product_name=%s, customers_count=%s, price=%s, quantity=%s, category=%s, order_date=%s 
                WHERE product_name=%s
            """, (new_product, new_customers, new_price, new_quantity, new_category, new_order_date, old_product))
            conn.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            add_notification(f"Product updated: {new_product}")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")
        finally:
            conn.close()
        load_product_data()
        clear_product_fields()


def delete_product():
    global product_treeview
    selected = product_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to delete.")
        return
    data = product_treeview.item(selected, 'values')
    product = data[0]
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("DELETE FROM product_sales WHERE product_name = %s", (product,))
            conn.commit()
            messagebox.showinfo("Deleted", f"{product} has been deleted.")
            add_notification(f"Product deleted: {product}")
            load_product_data()
            clear_product_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


def clear_product_fields():
    global product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    product_name_entry.delete(0, END)
    customers_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    product_category_entry.delete(0, END)
    order_date_entry.delete(0, END)


def fill_product_fields(event):
    global product_treeview, product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    selected = product_treeview.focus()
    if selected:
        values = product_treeview.item(selected, 'values')
        if values:
            product_name_entry.delete(0, END)
            product_name_entry.insert(0, values[0])
            customers_entry.delete(0, END)
            customers_entry.insert(0, values[1])
            price_entry.delete(0, END)
            price_entry.insert(0, values[2])
            quantity_entry.delete(0, END)
            quantity_entry.insert(0, values[3])
            product_category_entry.delete(0, END)
            product_category_entry.insert(0, values[4])
            order_date_entry.delete(0, END)
            order_date_entry.insert(0, values[5])


# ------------------ SUPPLIER MANAGEMENT ------------------
def supplier():
    global supplier_treeview, name_entry_supp, contact_entry_supp, address_entry_supp, email_entry_supp, product_entry_supp

    supplier_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    supplier_frame.place(x=450, y=100)

    headlabel = Label(supplier_frame, text="Supplier Management", font=('times new roman', 20, 'bold'), bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    undo_icon = Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized = undo_icon.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(supplier_frame, image=undo_icon, borderwidth='0', bg='#7aabd4', cursor='hand2',
                       command=lambda: supplier_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    entry_frame = Frame(supplier_frame, bg='#f0f0f0')
    entry_frame.place(x=100, y=100)

    Label(entry_frame, text='Name:', font=('times new roman', 15)).grid(row=0, column=0, padx=10, pady=10)
    name_entry_supp = Entry(entry_frame, font=('times new roman', 15), width=20)
    name_entry_supp.grid(row=0, column=1, padx=10)

    Label(entry_frame, text='Contact:', font=('times new roman', 15)).grid(row=0, column=2, padx=10, pady=10)
    contact_entry_supp = Entry(entry_frame, font=('times new roman', 15), width=20)
    contact_entry_supp.grid(row=0, column=3, padx=10)

    Label(entry_frame, text='Email:', font=('times new roman', 15)).grid(row=1, column=0, padx=10, pady=10)
    email_entry_supp = Entry(entry_frame, font=('times new roman', 15), width=20)
    email_entry_supp.grid(row=1, column=1, padx=10)

    Label(entry_frame, text='Address:', font=('times new roman', 15)).grid(row=1, column=2, padx=10, pady=10)
    address_entry_supp = Entry(entry_frame, font=('times new roman', 15), width=20)
    address_entry_supp.grid(row=1, column=3, padx=10)

    Label(entry_frame, text='Product:', font=('times new roman', 15)).grid(row=2, column=0, padx=10, pady=10)
    product_entry_supp = Entry(entry_frame, font=('times new roman', 15), width=20)
    product_entry_supp.grid(row=2, column=1, padx=10)

    Button(entry_frame, text="Add", font=('times new roman', 20), bg='#0b8fcb', fg='white',
           command=add_supplier).grid(row=3, column=0, pady=20, padx=10)
    Button(entry_frame, text="Update", font=('times new roman', 20), bg='orange', fg='white',
           command=update_supplier).grid(row=3, column=1, pady=20, padx=10)
    Button(entry_frame, text="Delete", font=('times new roman', 20), bg='red', fg='white',
           command=delete_supplier).grid(row=3, column=3, pady=20, padx=10)
    Button(entry_frame, text="Clear", font=('times new roman', 20), bg='gray', fg='white',
           command=clear_supplier_fields).grid(row=3, column=2, pady=20, padx=10)

    tree_frame = Frame(supplier_frame)
    tree_frame.place(x=100, y=400, width=1350, height=400)

    style = ttk.Style()
    style.theme_use("clam")  # Use a theme that supports good customization
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")

    style.configure("Treeview.Heading",
                    background="lightblue",
                    foreground="black",
                    font=('Times New Roman', 13, 'bold'))

    style.map("Treeview",
            background=[('selected', 'yellow')],
            foreground=[('selected', 'black')])
    
    

    supplier_treeview = ttk.Treeview(tree_frame, columns=('Name', 'Contact', 'Email', 'Address', 'Product'), show='headings')
    supplier_treeview.tag_configure('evenrow', background='white')
    supplier_treeview.tag_configure('oddrow', background='light blue')  

    supplier_treeview.heading('Name', text='Name')
    supplier_treeview.heading('Contact', text='Contact')
    supplier_treeview.heading('Email', text='Email')
    supplier_treeview.heading('Address', text='Address')
    supplier_treeview.heading('Product', text='Product')

    supplier_treeview.column('Name', width=200)
    supplier_treeview.column('Contact', width=150)
    supplier_treeview.column('Email', width=250)
    supplier_treeview.column('Address', width=300)
    supplier_treeview.column('Product', width=200)

    supplier_treeview.pack(fill='both', expand=True)
    supplier_treeview.bind('<<TreeviewSelect>>', fill_supplier_fields)
    

    load_supplier_data()

def add_supplier():
    name = name_entry_supp.get()
    contact = contact_entry_supp.get()
    email = email_entry_supp.get()
    address = address_entry_supp.get()
    product = product_entry_supp.get()
    if not name or not contact or not email or not address or not product:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("INSERT INTO suppliers (name, contact, email, address, product) VALUES (%s, %s, %s, %s, %s)",
                           (name, contact, email, address, product))
            conn.commit()
            messagebox.showinfo("Success", "Supplier added successfully!")
            add_notification(f"Added supplier '{name}'.")
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

def load_supplier_data():
    cursor, conn = connect_database()
    if cursor:
        try:
            supplier_treeview.delete(*supplier_treeview.get_children())
            cursor.execute("SELECT name, contact, email, address, product FROM suppliers")
            rows = cursor.fetchall()
            for index, row in enumerate(rows):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                supplier_treeview.insert('', 'end', values=row, tags=(tag,))
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to load supplier data: {e}")
        finally:
            conn.close()


def clear_supplier_fields():
    name_entry_supp.delete(0, 'end')
    contact_entry_supp.delete(0, 'end')
    email_entry_supp.delete(0, 'end')
    address_entry_supp.delete(0, 'end')
    product_entry_supp.delete(0, 'end')

def fill_supplier_fields(event):
    selected = supplier_treeview.focus()
    if selected:
        values = supplier_treeview.item(selected, 'values')
        if values:
            name_entry_supp.delete(0, 'end')
            name_entry_supp.insert(0, values[0])
            contact_entry_supp.delete(0, 'end')
            contact_entry_supp.insert(0, values[1])
            email_entry_supp.delete(0, 'end')
            email_entry_supp.insert(0, values[2])
            address_entry_supp.delete(0, 'end')
            address_entry_supp.insert(0, values[3])
            product_entry_supp.delete(0, 'end')
            product_entry_supp.insert(0, values[4])

def update_supplier():
    selected = supplier_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a supplier to update.")
        return
    old_values = supplier_treeview.item(selected, 'values')
    old_name = old_values[0]
    new_name = name_entry_supp.get()
    new_contact = contact_entry_supp.get()
    new_email = email_entry_supp.get()
    new_address = address_entry_supp.get()
    new_product = product_entry_supp.get()
    if not new_name or not new_contact or not new_email or not new_address or not new_product:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("""
                UPDATE suppliers 
                SET name = %s, contact = %s, email = %s, address = %s, product = %s 
                WHERE name = %s
            """, (new_name, new_contact, new_email, new_address, new_product, old_name))
            conn.commit()
            messagebox.showinfo("Success", "Supplier updated successfully!")
            add_notification(f"Updated supplier '{old_name}' to '{new_name}'.")
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

def delete_supplier():
    selected = supplier_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a supplier to delete.")
        return
    values = supplier_treeview.item(selected, 'values')
    supplier_name = values[0]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{supplier_name}'?")
    if not confirm:
        return
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("DELETE FROM suppliers WHERE name = %s", (supplier_name,))
            conn.commit()
            messagebox.showinfo("Deleted", f"{supplier_name} has been deleted.")
            add_notification(f"Deleted supplier '{supplier_name}'.")
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



# ------------------ NOTIFICATIONS ------------------
def notification_df():
    notification_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    notification_frame.place(x=450, y=100)

    # Header
    headlabel5 = Label(notification_frame, text="Notifications", font=('times new roman', 20, 'bold'), bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel5.place(x=0, y=0)

    # Undo button
    undo_icon = Image.open(r"C:\Users\glycel\Downloads\undo.png").resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon)
    undolabel = Button(notification_frame, image=undo_icon, compound=RIGHT, borderwidth='0', bg='#7aabd4', cursor='hand2', command=lambda: notification_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # Scrollable Frame
    notif_container = Frame(notification_frame, bg='#f0f0f0')
    notif_container.place(x=50, y=80, width=1300, height=780)

    canvas = tkinter.Canvas(notif_container, bg='#f0f0f0', highlightthickness=0)
    scrollbar = ttk.Scrollbar(notif_container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    frame_inside = Frame(canvas, bg='#f0f0f0')
    canvas.create_window((0, 0), window=frame_inside, anchor='nw')
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Load and display notifications
    notifications = load_notifications()
    colors = {'info': '#dff0d8', 'warning': '#fcf8e3', 'error': '#f2dede'}

    for index, (message, created_at, notif_type) in enumerate(notifications):
        color = colors.get(notif_type, '#dff0d8')  # default to 'info'
        notif_box = Frame(frame_inside, bg=color, bd=1, relief='solid', padx=10, pady=5)
        notif_box.pack(anchor='w', pady=5, fill='x', padx=5)

        timestamp = created_at.strftime('%b %d, %Y - %I:%M %p')
        Label(notif_box, text=timestamp, font=('times new roman', 11, 'italic'), bg=color, anchor='w').pack(anchor='w')
        Label(notif_box, text=message, font=('times new roman', 13), bg=color, wraplength=1200, justify='left').pack(anchor='w')


def add_notification(message, notif_type='info'):
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute("INSERT INTO notifications (message, type) VALUES (%s, %s)", (message, notif_type))
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Notification Error", f"Failed to log notification: {e}")
        finally:
            conn.close()

def load_notifications():
    cursor, conn = connect_database()
    notifications = []
    if cursor:
        try:
            cursor.execute("SELECT message, created_at, type FROM notifications ORDER BY created_at DESC")
            notifications = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Notification Error", f"Failed to load notifications: {e}")
        finally:
            conn.close()
    return notifications



def usermanage():
    global back_image,employee_treeview
    global name_entry, email_entry, contact_entry, age_entry, address_entry, gender_entry
    undo_icon=Image.open(r"C:\Users\glycel\Downloads\undo.png")
    undo_icon_resized=undo_icon.resize((30,30),Image.Resampling.LANCZOS)
    undo_icon=ImageTk.PhotoImage(undo_icon_resized)
    usermanage_frame = Frame(root,width=1920,height=1000)
    usermanage_frame.place(x=450,y=100)

    headlabel6=Label(usermanage_frame,text="Employee Details",font=('times new roman',20,'bold'),bg='#7aabd4',fg='black',padx=680,pady=15)
    headlabel6.place(x=0,y=0)

    undolabel = Button(usermanage_frame, image=undo_icon ,compound=RIGHT,borderwidth='0',bg='#7aabd4',cursor='hand2',command=lambda: usermanage_frame.place_forget())
    undolabel.place(x=5,y=2)
    undolabel.image=undo_icon
    
    employee_frame = Frame(usermanage_frame,)
    employee_frame.place(x=0, y=79, relwidth=1, height=235)
    search_frame = Frame(employee_frame)
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Name', 'Email','Contact','Gender','Address','Age'), font=('times new roman', 12), state='readonly', justify=CENTER,)
    search_combobox.set('Search By') 
    search_combobox.grid(row=0, column=0)
    search_entry=Entry(search_frame,font=('times new roman',12))
    search_entry.grid(row=0,column=2)
    search_button=Button(search_frame,text='Search',font=('times new roman', 12))
    search_button.grid(row=0,column=3)
    
  
    employee_treeview= ttk.Treeview(employee_frame,columns=('Name','Email','Contact','Age','Address','Gender'),show='headings')
    employee_treeview.place(x=20 , y=50)

 

    employee_treeview.heading('Name',text='Name')
    employee_treeview.heading('Email',text='Email')
    employee_treeview.heading('Contact',text='Contact')
    employee_treeview.heading('Age',text='Age')
    employee_treeview.heading('Address',text='Address')
    employee_treeview.heading('Gender',text='Gender')

    employee_treeview.column('Name',width=210)
    employee_treeview.column('Contact',width=170)
    employee_treeview.column('Age',width=70)
    employee_treeview.column('Address',width=270)
    employee_treeview.column('Gender',width=70)
   
    treeview_data()
    

    detail_frame = Frame(usermanage_frame)  
    detail_frame.place(x=0, y=320)  

    emp_name = Label(detail_frame, text='Name:', font=('times new roman', 15))
    emp_name.grid(row=0, column=0,padx=20, pady=10)   
    name_entry=Entry(detail_frame,font=('times new roman', 12),width=20)
    name_entry.grid(row=0,column=1,padx=40)   
    
    emp_email = Label(detail_frame, text='Email:', font=('times new roman', 15))
    emp_email.grid(row=1, column=0, padx=20, pady=10) 
    email_entry=Entry(detail_frame,font=('times new roman', 12),width=20)
    email_entry.grid(row=1,column=1,padx=20,pady=10)

    emp_contact = Label(detail_frame, text='Contact:', font=('times new roman', 15))
    emp_contact.grid(row=0, column=3, padx=20, pady=10,sticky='w') 
    contact_entry=Entry(detail_frame,font=('times new roman', 12),width=20)
    contact_entry.grid(row=0,column=4)

    emp_age = Label(detail_frame, text='Age:', font=('times new roman', 15))
    emp_age.grid(row=1, column=3, padx=20, pady=10,sticky='w') 
    age_entry=Entry(detail_frame,font=('times new roman', 12),width=20)
    age_entry.grid(row=1,column=4)

    emp_address = Label(detail_frame, text='Address:', font=('times new roman', 15))
    emp_address.grid(row=2, column=0, padx=20, pady=10,sticky='w') 
    address_entry=Entry(detail_frame,font=('times new roman', 12),width=20)
    address_entry.grid(row=2,column=1)
    
    emp_gender = Label(detail_frame, text='Gender:', font=('times new roman', 15))
    emp_gender.grid(row=2, column=3, padx=10, pady=10,sticky='w') 
    gender_entry=Entry(detail_frame,font=('times new roman', 12),width=20)
    gender_entry.grid(row=2,column=4)

    save_button=Button(detail_frame,text='Update', font=('Helvetica',15),command=lambda: update(name_entry.get(),email_entry.get(),contact_entry.get(),age_entry.get(),address_entry.get(),gender_entry.get()),bg='#0b8fcb',padx=20,fg='white')
    save_button.grid(row=0,column=5,padx=50)

    add_button=Button(detail_frame,text='Add', font=('Helvetica',15),bg='#0b8fcb',padx=20,pady=3,command=add_employee,fg='white')
    add_button.grid(row=0,column=6,padx=15)

    clear_button=Button(detail_frame,text='Clear', font=('Helvetica',15),bg='#0b8fcb',command=lambda: clear(name_entry, email_entry, contact_entry, age_entry, gender_entry,address_entry),padx=20,fg='white')
    clear_button.grid(row=1,column=5,padx=50,pady=10)

    delete_button=Button(detail_frame,text='Delete', font=('Helvetica',15),command=lambda:delete_details(name_entry,email_entry,contact_entry,age_entry,gender_entry,address_entry),bg='#0b8fcb',padx=20,fg='white')
    delete_button.grid(row=1,column=6,padx=15)

    employee_treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,name_entry, email_entry, contact_entry, age_entry, gender_entry,address_entry))

def secondary_window():
    secondary_window = Toplevel()
    secondary_window.title("Log In")
    secondary_window.geometry('300x450+300+450') 
    secondary_window.config(bg='#30353a')
    
    def validate(event=None):
        user = username_entry.get()
        password = password_entry.get()

        correct_user = "admin"
        correct_password = "user"    

        if user == correct_user and password == correct_password:   
            messagebox.showinfo(title="Login ",message="Login Successful, Welcome " + user + "🙂")
            secondary_window.destroy()
            enable_button()
        else:
            messagebox.showerror(title="Login Failed",message="Invalid username and password")
        

    header_label= Label(secondary_window,padx=13,bg='#606b75',width=30,height=20)
    header_label.place(x=30,y=100)
    username_label = Label(secondary_window,text="Username:",font=('times new roman', 14),fg='white',bg='#606b75')
    username_label.place(x=40,y=200)
    password_label = Label(secondary_window,text="Password:",font=('times new roman', 14),fg='white',bg='#606b75')
    password_label.place(x=40,y=255)
    submit_button=Button(secondary_window,text="Login",background='white',fg='black',command=validate,font=('times new roman', 10))
    submit_button.place(x=140,y=300)

    username_entry=Entry(secondary_window, font=('times new roman', 10))
    username_entry.place(x=140, y=202, width=120,height=20)
    password_entry=Entry(secondary_window, font=('times new roman', 10),show='*')
    password_entry.place(x=140, y=255, width=120,height=20)
    secondary_window.bind("<Return>",lambda event:validate())



# ------------------ NAVIGATION BUTTONS ------------------
button_dash = Button(root, image=dash_icon, compound=LEFT, text="Dashboard", command=dashboard, bg='#d4d4ce',
                     font=('Times', 14), fg='black', padx=115, pady=11, borderwidth=0, cursor='hand2')
button_inv = Button(root, image=inv_icon, compound=LEFT, text="Inventory", command=inventory, font=('Times', 14),
                    bg='#d4d4ce', fg='black', padx=120, pady=11, borderwidth=0, cursor='hand2')
button_prodm = Button(root, image=productm_icon, compound=LEFT, command=product_management, text="Product Management",
                      bg='#d4d4ce', font=('Times', 14), fg='black', padx=76, pady=11, borderwidth=0, cursor='hand2')
button_supplier = Button(root, image=supplier_icon, compound=LEFT, command=supplier, text="Supplier", bg='#d4d4ce',
                         font=('Times', 14), fg='black', padx=124, pady=14, borderwidth=0, cursor='hand2')
notification_btn = Button(root, image=bell_icon, compound=LEFT, command=notification_df, text="Notification",
                          bg='#d4d4ce', font=('Times', 14), fg='black', padx=110, pady=12, borderwidth=0, cursor='hand2')
user_management_btn = Button(root, image=userm_icon, compound=LEFT, command=usermanage, text="User Management", bg='#d4d4ce',
                             font=('Times', 14), fg='black', padx=86, pady=15, borderwidth=0, cursor='hand2')
Logout_Btn = Button(root, image=log_icon, compound=RIGHT, text='Exit', command=exit,
                    font=('times new roman', 15, 'bold'), padx=13)
Signin_Btn = Button(root, image=Sign_icon, compound=RIGHT, text='Log In',
                    font=('times new roman', 15, 'bold'), padx=13)

button_dash.place(x=-40, y=100)
button_inv.place(x=-44, y=183)
button_prodm.place(x=0, y=266)
button_supplier.place(x=-50, y=350)
notification_btn.place(x=-38, y=450)
user_management_btn.place(x=-12, y=540)
Logout_Btn.place(x=1750, y=15)
Signin_Btn.place(x=1550, y=15)



root.mainloop()
