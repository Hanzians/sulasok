from tkinter import Tk, Button, Entry, Frame, Label, Listbox, Canvas, StringVar, LEFT, RIGHT, CENTER, END
from tkinter import ttk, messagebox, font
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import datetime

# ---------------- Global Notifications ----------------
notifications_list = []  # Will store notification messages

def add_notification(message):
    """Append a new notification with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notification_data = {
        'message': message,
        'timestamp': timestamp,
        'full_message': f"{timestamp} - {message}"
    }
    notifications_list.append(notification_data)


# --------------- Database Connection (Reusable) ---------------
def connect_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin123",
            port=3306,
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
    Total Sales = SUM(price * quantity) from product_sales (customer orders)
    Expenses = SUM(price * quantity) from inventory (your purchases)
    Net Profit = Total Sales - Expenses
    Orders = count of product_sales rows today
    """
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin123",
            database="milktea"
        )
        cursor = conn.cursor()

        # 1. Total Sales (customer orders)
        cursor.execute("""
            SELECT IFNULL(SUM(price * quantity), 0)
            FROM product_sales
            WHERE DATE(order_date) = CURDATE()
        """)
        total_sales = cursor.fetchone()[0]

        # 2. Expenses (from inventory)
        cursor.execute("""
            SELECT IFNULL(SUM(price * quantity), 0)
            FROM inventory
            WHERE DATE(created_at) = CURDATE()
        """)
        total_expenses = cursor.fetchone()[0]

        # 3. Net Profit
        net_profit = total_sales - total_expenses

        # 4. Orders Today
        cursor.execute("SELECT COUNT(*) FROM product_sales WHERE DATE(order_date) = CURDATE()")
        total_orders = cursor.fetchone()[0]

        conn.close()
    except mysql.connector.Error as err:
        print("❌ Database error:", err)
        total_sales, total_expenses, net_profit, total_orders = 0, 0, 0, 0

    return total_orders, total_sales, total_expenses, net_profit


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
icon_Label_img = Image.open(r"D:\Downloads\inventoryy.png") 
icon_Label_resized = icon_Label_img.resize((70, 70), Image.Resampling.LANCZOS)
icon_Label = ImageTk.PhotoImage(icon_Label_resized)

logoImage_img = Image.open(r"D:\Downloads\Sulasok.png")
logoImage_resized = logoImage_img.resize((450, 400), Image.Resampling.LANCZOS)
logoImage = ImageTk.PhotoImage(logoImage_resized)
imageLabel = Label(image=logoImage)
imageLabel.place(x=0, y=640)

log_icon_img = Image.open(r"D:\Downloads\logout.png")
log_icon_resized = log_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
log_icon = ImageTk.PhotoImage(log_icon_resized)

Sign_icon_img = Image.open(r"D:\Downloads\Sign-in.png")
Sign_icon_resized = Sign_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
Sign_icon = ImageTk.PhotoImage(Sign_icon_resized)

dash_icon_img = Image.open(r"D:\Downloads\dashboard.png")
dash_icon_resized = dash_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
dash_icon = ImageTk.PhotoImage(dash_icon_resized)

inv_icon_img = Image.open(r"D:\Downloads\inventory.png")
inv_icon_resized = inv_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
inv_icon = ImageTk.PhotoImage(inv_icon_resized)

productm_icon_img = Image.open(r"D:\Downloads\productm.png")
productm_icon_resized = productm_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
productm_icon = ImageTk.PhotoImage(productm_icon_resized)

supplier_icon_img = Image.open(r"D:\Downloads\supplier.png")
supplier_icon_resized = supplier_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
supplier_icon = ImageTk.PhotoImage(supplier_icon_resized)

bell_icon_img = Image.open(r"D:\Downloads\bell.png")
bell_icon_resized = bell_icon_img.resize((70, 70), Image.Resampling.LANCZOS)
bell_icon = ImageTk.PhotoImage(bell_icon_resized)

userm_icon_img = Image.open(r"D:\Downloads\userm.png")
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
    undo_icon_img = Image.open(r"D:\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(dashboard_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                       bg='#7aabd4', cursor='hand2', command=lambda: dashboard_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # Fetch updated stats
    orders, total_sales, total_expenses, profit = fetch_dashboard_data()

    # Stat Boxes
    sales_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    sales_box.place(x=100, y=100)
    Label(sales_box, text="Total Sales", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(sales_box, text=f"₱{total_sales:,.0f}", font=("Arial", 18, "bold"), bg="white", fg="#333").pack()

    expenses_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    expenses_box.place(x=400, y=100)
    Label(expenses_box, text="Expenses Today", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(expenses_box, text=f"₱{total_expenses:,.0f}", font=("Arial", 18, "bold"), bg="white", fg="#333").pack()

    orders_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    orders_box.place(x=700, y=100)
    Label(orders_box, text="Orders Today", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(orders_box, text=str(orders), font=("Arial", 18, "bold"), bg="white", fg="#333").pack()

    # Net Profit = Total Sales - Expenses
    netprofit_box = Frame(dashboard_frame, bg="white", bd=2, relief="groove", padx=20, pady=20)
    netprofit_box.place(x=1000, y=100)
    Label(netprofit_box, text="Net Profit", font=("Arial", 14), bg="white", fg="#666").pack()
    Label(netprofit_box, text=f"₱{profit:,.0f}", font=("Arial", 18, "bold"), bg="white", fg="green").pack()

    # Create chart canvas
    chart_canvas = Canvas(dashboard_frame, width=500, height=250, bg='white')
    chart_canvas.place(x=100, y=300)

    # Calculate scale
    max_val = max(total_sales, total_expenses)
    if max_val == 0:
        max_val = 1
    BAR_MAX_WIDTH = 360
    sales_width = int((total_sales / max_val) * BAR_MAX_WIDTH)
    expenses_width = int((total_expenses / max_val) * BAR_MAX_WIDTH)

    # Animate each bar
    animate_bar(chart_canvas, "Total Sales", x=120, y=50, target_width=sales_width,
                bar_color="green", value_text=f"₱{total_sales:,.0f}")
    animate_bar(chart_canvas, "Expenses", x=120, y=130, target_width=expenses_width,
                bar_color="red", value_text=f"₱{total_expenses:,.0f}")


def animate_bar(canvas, label_text, x, y, target_width, bar_color, value_text):
    BAR_HEIGHT = 40
    steps = 60  # total animation frames
    delay = 10  # milliseconds between frames

    def draw_frame(step):
        current_width = int((step / steps) * target_width)
        canvas.delete(f"{label_text}_bar")  # remove previous bar/text

        # Label
        canvas.create_text(20, y + BAR_HEIGHT / 2, text=label_text, anchor="w",
                           font=("Arial", 12, "bold"), fill="black", tags=f"{label_text}_bar")

        # Bar
        canvas.create_rectangle(x, y, x + current_width, y + BAR_HEIGHT,
                                fill=bar_color, outline="", tags=f"{label_text}_bar")

        # Centered Value Text
        value_x = x + current_width / 2
        canvas.create_text(value_x, y + BAR_HEIGHT / 2,
                           text=value_text, fill="white", font=("Arial", 12, "bold"), tags=f"{label_text}_bar")

        if step < steps:
            canvas.after(delay, lambda: draw_frame(step + 1))

    draw_frame(0)


# ------------------ INVENTORY ------------------
def inventory():
    global inv_treeview, item_name_entry, quantity_entry, category_entry, price_entry, unit_combobox, expiry_entry, best_before_entry, nutrition_entry
    inventory_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    inventory_frame.place(x=450, y=100)

    # Undo Button
    undo_icon_img = Image.open(r"D:\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    headlabel = Label(inventory_frame, text="Inventory Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)
    undolabel = Button(inventory_frame, image=undo_icon, compound=RIGHT, borderwidth=0, bg='#7aabd4',
                       cursor='hand2', command=lambda: inventory_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    # Data Entry Frame
    entry_frame = Frame(inventory_frame, bg='#f0f0f0')
    entry_frame.place(x=100, y=80)
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
    # EXPIRY DATE, BEST BEFORE, NUTRITION — Fixed Grid Placement

    # Row 2 — Expiry Date and Best Before
    Label(entry_frame, text='Expiry Date (YYYY-MM-DD):', font=('times new roman', 15)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    expiry_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    expiry_entry.grid(row=2, column=1, padx=10, pady=10)

    Label(entry_frame, text='Best Before Date (YYYY-MM-DD):', font=('times new roman', 15)).grid(row=2, column=2, padx=10, pady=10, sticky='e')
    best_before_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    best_before_entry.grid(row=2, column=3, padx=10, pady=10)

    # Row 3 — Nutrition Info
    Label(entry_frame, text='Nutrition Info:', font=('times new roman', 15)).grid(row=3, column=0, padx=10, pady=10, sticky='ne')
    nutrition_entry = Entry(entry_frame, font=('times new roman', 15), width=60)
    nutrition_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky='w')

    # Row 4 — Buttons aligned across full row
    Button(entry_frame, text="Add", font=('times new roman', 20), bg="#32d9dc", fg='white',
        command=add_inventory).grid(row=4, column=0, pady=20, padx=10)
    Button(entry_frame, text="Update", font=('times new roman', 20), bg="#F6D51A", fg='white',
        command=update_inventory).grid(row=4, column=1, pady=20, padx=10)
    Button(entry_frame, text="Clear", font=('times new roman', 20), bg="#9ba09d", fg='white',
        command=clear_inventory_fields).grid(row=4, column=2, pady=20, padx=10)
    Button(entry_frame, text="Delete", font=('times new roman', 20), bg="#D90B11", fg='white',
        command=delete_inventory).grid(row=4, column=3, pady=20, padx=10)

    # Inventory Table
    tree_frame = Frame(inventory_frame, bg='white')
    tree_frame.place(x=50, y=350, width=1350, height=450)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=30, borderwidth=2, relief="solid")
    style.configure("Treeview.Heading", font=('Times New Roman', 13, 'bold'),
                    borderwidth=2, relief="solid")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    inv_treeview = ttk.Treeview(tree_frame, columns=('Name', 'Qty', 'Unit', 'Category', 'Price', 'ExpiryDate', 'BestBeforeDate', 'Nutrition'), show='headings')

    # Fix headings and columns to match the column names exactly:
    inv_treeview.heading('Name', text='Item Name')
    inv_treeview.heading('Qty', text='Quantity')
    inv_treeview.heading('Unit', text='Unit')
    inv_treeview.heading('Category', text='Category')
    inv_treeview.heading('Price', text='Price')
    inv_treeview.heading('ExpiryDate', text='Expiry Date')
    inv_treeview.heading('BestBeforeDate', text='Best Before')
    inv_treeview.heading('Nutrition', text='Nutrition Info')

    inv_treeview.column('Name', width=200)
    inv_treeview.column('Qty', width=100)
    inv_treeview.column('Unit', width=100)
    inv_treeview.column('Category', width=150)
    inv_treeview.column('Price', width=100)
    inv_treeview.column('ExpiryDate', width=120)
    inv_treeview.column('BestBeforeDate', width=120)
    inv_treeview.column('Nutrition', width=200)

    inv_treeview.pack(fill='both', expand=True)
    inv_treeview.bind('<<TreeviewSelect>>', fill_inventory_fields)
    load_inventory_data()


def add_inventory():
    global item_name_entry, quantity_entry, category_entry, price_entry, unit_combobox, inv_treeview, expiry_entry, best_before_entry, nutrition_entry
    item = item_name_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    unit = unit_combobox.get()

    if item and quantity and category and price:
        try:
            quantity = int(quantity)
            price = float(price)
            total_cost = price * quantity
        except ValueError:
            # Optionally show warning on invalid input
            messagebox.showwarning("Warning", "Invalid price or quantity format.")
            return

        cursor, conn = connect_database()
        if cursor:
            try:
                # Include expiry, best_before, nutrition info in INSERT if your DB has these columns
                expiry = expiry_entry.get() if expiry_entry else None
                best_before = best_before_entry.get() if best_before_entry else None
                nutrition = nutrition_entry.get() if nutrition_entry else None

                cursor.execute("""
                    INSERT INTO inventory (item_name, quantity, unit, category, price, expiry_date, best_before_date, nutrition_info)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (item, quantity, unit, category, price, expiry, best_before, nutrition))

                cursor.execute("""
                    INSERT INTO expenses (description, amount, date)
                    VALUES (%s, %s, CURDATE())
                """, (f"Purchased {quantity} {unit} of {item}", total_cost))

                conn.commit()
                messagebox.showinfo("Success", f"{item} added to inventory. ₱{total_cost:.2f} recorded as expense.")
                add_notification(f"Inventory added and expense recorded: {item}")
                load_inventory_data()
                clear_inventory_fields()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")



def load_inventory_data():
    global inv_treeview
    cursor, conn = connect_database()
    if cursor:
        # Ensure all columns (expiry_date, best_before_date, nutrition_info) exist in DB and selected here
        cursor.execute("SELECT item_name, quantity, unit, category, price, expiry_date, best_before_date, nutrition_info FROM inventory")
        rows = cursor.fetchall()
        inv_treeview.delete(*inv_treeview.get_children())
        for row in rows:
            inv_treeview.insert('', 'end', values=row)
        conn.close()



def update_inventory():
    global inv_treeview, item_name_entry, quantity_entry, category_entry, price_entry, expiry_entry, best_before_entry, nutrition_entry
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
    if not new_item or not new_quantity or not new_category or not new_price:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    cursor, conn = connect_database()
    if cursor:
        try:
            cursor.execute(
                "UPDATE inventory SET item_name=%s, quantity=%s, category=%s, price=%s WHERE item_name=%s",
                (new_item, new_quantity, new_category, new_price, old_item)
            )
            conn.commit()
            messagebox.showinfo("Success", "Item updated successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")
        finally:
            conn.close()
        load_inventory_data()
        clear_inventory_fields()


def delete_inventory():
    global inv_treeview
    selected = inv_treeview.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select an item to delete.")
        return
    data = inv_treeview.item(selected, 'values')
    item = data[0]
    cursor, conn = connect_database()
    if cursor:
        cursor.execute("DELETE FROM inventory WHERE item_name = %s", (item,))
        conn.commit()
        conn.close()
        load_inventory_data()
        clear_inventory_fields()
        messagebox.showinfo("Deleted", f"{item} has been deleted.")


def clear_inventory_fields():
    global item_name_entry, quantity_entry, category_entry, price_entry, unit_combobox, expiry_entry, best_before_entry, nutrition_entry
    item_name_entry.delete(0, END)
    quantity_entry.delete(0, END)
    category_entry.delete(0, END)
    price_entry.delete(0, END)
    unit_combobox.set("pcs")
    expiry_entry.delete(0, END)
    best_before_entry.delete(0, END)
    nutrition_entry.delete(0, END)


def fill_inventory_fields(event):
    global inv_treeview, item_name_entry, quantity_entry, category_entry, price_entry, unit_combobox, expiry_entry, best_before_entry, nutrition_entry
    selected = inv_treeview.focus()
    if selected:
        values = inv_treeview.item(selected, 'values')
        if values:
            item_name_entry.delete(0, END)
            item_name_entry.insert(0, values[0])
            quantity_entry.delete(0, END)
            quantity_entry.insert(0, values[1])
            unit_combobox.set(values[2])
            category_entry.delete(0, END)
            category_entry.insert(0, values[3])
            price_entry.delete(0, END)
            price_entry.insert(0, values[4])

            # Safely insert expiry date if not None
            expiry_entry.delete(0, END)
            if len(values) > 5 and values[5] is not None:
                expiry_entry.insert(0, values[5])

            best_before_entry.delete(0, END)
            if len(values) > 6 and values[6] is not None:
                best_before_entry.insert(0, values[6])

            nutrition_entry.delete(0, END)
            if len(values) > 7 and values[7] is not None:
                nutrition_entry.insert(0, values[7])


# ------------------ PRODUCT MANAGEMENT ------------------
def product_management():
    global product_treeview, product_name_entry, customers_entry, price_entry, quantity_entry, product_category_entry, order_date_entry
    product_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    product_frame.place(x=450, y=100)

    headlabel = Label(product_frame, text="Product Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    # Undo Button
    undo_icon_img = Image.open(r"D:\Downloads\undo.png")
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
    customers_entry = Entry(entry_frame, font=('times new roman', 15), width=10)
    customers_entry.grid(row=0, column=3, padx=10)
    Label(entry_frame, text='Price:', font=('times new roman', 15)).grid(row=1, column=0, padx=10, pady=10)
    price_entry = Entry(entry_frame, font=('times new roman', 15), width=10)
    price_entry.grid(row=1, column=1, padx=10)
    Label(entry_frame, text='Quantity:', font=('times new roman', 15)).grid(row=1, column=2, padx=10, pady=10)
    quantity_entry = Entry(entry_frame, font=('times new roman', 15), width=10)
    quantity_entry.grid(row=1, column=3, padx=10)
    Label(entry_frame, text='Category:', font=('times new roman', 15)).grid(row=2, column=0, padx=10, pady=10)
    product_category_entry = Entry(entry_frame, font=('times new roman', 15), width=20)
    product_category_entry.grid(row=2, column=1, padx=10)
    Label(entry_frame, text='Order Date (YYYY-MM-DD):', font=('times new roman', 15)).grid(row=2, column=2, padx=10, pady=10)
    order_date_entry = Entry(entry_frame, font=('times new roman', 15), width=15)
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
    style.theme_use("default")
    style.configure("Treeview", rowheight=30, borderwidth=2, relief="solid")
    style.configure("Treeview.Heading", font=('Times New Roman', 13, 'bold'),
                    borderwidth=2, relief="solid")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
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
        for row in rows:
            product_treeview.insert('', 'end', values=row)
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
    global supplier_treeview, name_entry_supp, contact_entry_supp, email_entry_supp, address_entry_supp, product_entry_supp
    supplier_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    supplier_frame.place(x=450, y=100)

    headlabel = Label(supplier_frame, text="Supplier Management", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    undo_icon_img = Image.open(r"D:\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    undolabel = Button(supplier_frame, image=undo_icon, borderwidth=0, bg='#7aabd4', cursor='hand2',
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

    Button(entry_frame, text="Add Supplier", font=('times new roman', 20), bg='#0b8fcb', fg='white',
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
    style.theme_use("default")
    style.configure("Treeview", rowheight=30, borderwidth=2, relief="solid")
    style.configure("Treeview.Heading", font=('Times New Roman', 13, 'bold'),
                    borderwidth=2, relief="solid")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    supplier_treeview = ttk.Treeview(tree_frame, columns=('Name', 'Contact', 'Email', 'Address', 'Product'),
                                     show='headings')
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
    global name_entry_supp, contact_entry_supp, email_entry_supp, address_entry_supp, product_entry_supp
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
            add_notification(f"Supplier added: {name}")
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()


def load_supplier_data():
    global supplier_treeview
    cursor, conn = connect_database()
    if cursor:
        supplier_treeview.delete(*supplier_treeview.get_children())
        cursor.execute("SELECT name, contact, email, address, product FROM suppliers")
        for row in cursor.fetchall():
            supplier_treeview.insert('', 'end', values=row)
        conn.close()


def clear_supplier_fields():
    global name_entry_supp, contact_entry_supp, email_entry_supp, address_entry_supp, product_entry_supp
    name_entry_supp.delete(0, END)
    contact_entry_supp.delete(0, END)
    email_entry_supp.delete(0, END)
    address_entry_supp.delete(0, END)
    product_entry_supp.delete(0, END)


def fill_supplier_fields(event):
    global supplier_treeview, name_entry_supp, contact_entry_supp, email_entry_supp, address_entry_supp, product_entry_supp
    selected = supplier_treeview.focus()
    if selected:
        values = supplier_treeview.item(selected, 'values')
        if values:
            name_entry_supp.delete(0, END)
            name_entry_supp.insert(0, values[0])
            contact_entry_supp.delete(0, END)
            contact_entry_supp.insert(0, values[1])
            email_entry_supp.delete(0, END)
            email_entry_supp.insert(0, values[2])
            address_entry_supp.delete(0, END)
            address_entry_supp.insert(0, values[3])
            product_entry_supp.delete(0, END)
            product_entry_supp.insert(0, values[4])


def update_supplier():
    global name_entry_supp, contact_entry_supp, email_entry_supp, address_entry_supp, product_entry_supp
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
            cursor.execute(
                "UPDATE suppliers SET name=%s, contact=%s, email=%s, address=%s, product=%s WHERE name=%s",
                (new_name, new_contact, new_email, new_address, new_product, old_name)
            )
            conn.commit()
            messagebox.showinfo("Success", "Supplier updated successfully!")
            add_notification(f"Supplier updated: {new_name}")
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


def delete_supplier():
    global supplier_treeview
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
            add_notification(f"Supplier deleted: {supplier_name}")
            load_supplier_data()
            clear_supplier_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


# ------------------ NOTIFICATIONS ------------------
def notification_df():
    notif_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    notif_frame.place(x=450, y=100)
    
    # Header
    headlabel = Label(notif_frame, text="Notifications", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)
    
    # Undo button
    try:
        undo_icon_img = Image.open(r"D:\Downloads\undo.png")
        undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
        undo_icon = ImageTk.PhotoImage(undo_icon_resized)
        undolabel = Button(notif_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                          bg='#7aabd4', cursor='hand2', command=lambda: notif_frame.place_forget())
        undolabel.image = undo_icon
    except:
        # Fallback if image not found
        undolabel = Button(notif_frame, text="←", font=('Arial', 16, 'bold'), borderwidth=0,
                          bg='#7aabd4', cursor='hand2', command=lambda: notif_frame.place_forget())
    
    undolabel.place(x=5, y=2)
    
    # Create scrollable frame for notifications
    canvas = Canvas(notif_frame, width=1600, height=700, bg='#f0f0f0', highlightthickness=0)
    scrollbar = Scrollbar(notif_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#f0f0f0')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.place(x=100, y=100)
    scrollbar.place(x=1700, y=100, height=700)
    
    def refresh_notifications():
        # Clear existing notification widgets
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        if not notifications_list:
            # Show empty state
            empty_frame = Frame(scrollable_frame, bg='#f0f0f0')
            empty_frame.pack(fill=X, pady=50)
            
            Label(empty_frame, text="📭", font=('Arial', 48), bg='#f0f0f0', fg='#999').pack()
            Label(empty_frame, text="No notifications yet", 
                  font=('times new roman', 16), bg='#f0f0f0', fg='#666').pack(pady=10)
            return
        
        # Display notifications as cards
        for i, notif in enumerate(reversed(notifications_list)):  # Show newest first
            create_notification_card(scrollable_frame, notif, i)
    
    def create_notification_card(parent, notif_data, index):
        # Main card frame
        card_frame = Frame(parent, bg='white', relief='raised', bd=1)
        card_frame.pack(fill=X, padx=20, pady=8)
        
        # Add subtle shadow effect with another frame
        shadow_frame = Frame(parent, bg='#d0d0d0', height=2)
        shadow_frame.pack(fill=X, padx=22)
        
        # Card content
        content_frame = Frame(card_frame, bg='white')
        content_frame.pack(fill=X, padx=15, pady=12)
        
        # Notification icon and content
        top_frame = Frame(content_frame, bg='white')
        top_frame.pack(fill=X)
        
        # Notification icon
        icon_label = Label(top_frame, text="🔔", font=('Arial', 18), bg='white')
        icon_label.pack(side=LEFT, padx=(0, 10))
        
        # Message content
        message_frame = Frame(top_frame, bg='white')
        message_frame.pack(side=LEFT, fill=X, expand=True)
        
        # Message text
        message_label = Label(message_frame, text=notif_data['message'], 
                             font=('times new roman', 13), bg='white', 
                             wraplength=1200, justify=LEFT, anchor='w')
        message_label.pack(anchor='w')
        
        # Timestamp
        timestamp_label = Label(message_frame, text=notif_data['timestamp'], 
                               font=('Arial', 10), bg='white', fg='#666')
        timestamp_label.pack(anchor='w', pady=(5, 0))
        
        # Delete button for individual notification
        delete_btn = Button(top_frame, text="✕", font=('Arial', 12, 'bold'), 
                           bg='white', fg='#999', borderwidth=0, cursor='hand2',
                           command=lambda idx=len(notifications_list)-1-index: delete_notification(idx))
        delete_btn.pack(side=RIGHT)
        
        # Hover effects
        def on_enter(e):
            card_frame.config(bg='#f8f9fa', relief='raised', bd=2)
            content_frame.config(bg='#f8f9fa')
            top_frame.config(bg='#f8f9fa')
            message_frame.config(bg='#f8f9fa')
            icon_label.config(bg='#f8f9fa')
            message_label.config(bg='#f8f9fa')
            timestamp_label.config(bg='#f8f9fa')
            delete_btn.config(bg='#f8f9fa', fg='#666')
        
        def on_leave(e):
            card_frame.config(bg='white', relief='raised', bd=1)
            content_frame.config(bg='white')
            top_frame.config(bg='white')
            message_frame.config(bg='white')
            icon_label.config(bg='white')
            message_label.config(bg='white')
            timestamp_label.config(bg='white')
            delete_btn.config(bg='white', fg='#999')
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        for child in card_frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
    
    def delete_notification(index):
        if 0 <= index < len(notifications_list):
            notifications_list.pop(index)
            refresh_notifications()
    
    def clear_all_notifications():
        notifications_list.clear()
        refresh_notifications()
    
    # Control buttons frame
    buttons_frame = Frame(notif_frame, bg='#f0f0f0')
    buttons_frame.place(x=100, y=820)
    
    # Clear all button
    clear_btn = Button(buttons_frame, text="Clear All Notifications", 
                      font=('times new roman', 12, 'bold'), bg='#dc3545', fg='white',
                      padx=20, pady=8, cursor='hand2', command=clear_all_notifications)
    clear_btn.pack(side=LEFT, padx=(0, 10))
    
    # Refresh button
    refresh_btn = Button(buttons_frame, text="🔄 Refresh", 
                        font=('times new roman', 12), bg='#28a745', fg='white',
                        padx=20, pady=8, cursor='hand2', command=refresh_notifications)
    refresh_btn.pack(side=LEFT)
    
    # Notification count
    count_label = Label(buttons_frame, 
                       text=f"Total: {len(notifications_list)} notification(s)",
                       font=('Arial', 11), bg='#f0f0f0', fg='#666')
    count_label.pack(side=RIGHT, padx=20)
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", on_mousewheel)
    
    # Initial load
    refresh_notifications()

# ------------------ PLACEHOLDER FUNCTIONS FOR USER MANAGEMENT ------------------
def treeview_data():
    global employee_treeview
    try:
        employee_treeview.delete(*employee_treeview.get_children())
    except Exception:
        pass
    # Dummy employee data
    sample_data = [
        ("Alice Smith", "alice@example.com", "0123456789", "25", "Street A", "Female"),
        ("Bob Johnson", "bob@example.com", "9876543210", "30", "Street B", "Male")
    ]
    for row in sample_data:
        employee_treeview.insert("", "end", values=row)


def add_employee():
    # Dummy function for adding an employee
    messagebox.showinfo("Add Employee", "Employee added (placeholder).")


def update(employee_name, email, contact, age, address, gender):
    # Dummy function for updating an employee
    messagebox.showinfo("Update Employee", "Employee updated (placeholder).")


def clear(*args):
    # Generic clear function to clear the given Entry widgets
    for widget in args:
        widget.delete(0, END)


def delete_details(*args):
    # Dummy function to delete an employee
    messagebox.showinfo("Delete Employee", "Employee deleted (placeholder).")


# ------------------ USER MANAGEMENT ------------------
def usermanage():
    global employee_treeview, name_entry, email_entry, contact_entry, age_entry, address_entry, gender_entry

    usermanage_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    usermanage_frame.place(x=450, y=100)

    undo_icon_img = Image.open(r"D:\Downloads\undo.png")
    undo_icon_resized = undo_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
    undo_icon = ImageTk.PhotoImage(undo_icon_resized)
    usermanage_frame = Frame(root, width=1800, height=1000, bg='#f0f0f0')
    usermanage_frame.place(x=450, y=100)

    headlabel = Label(usermanage_frame, text="Employee Details", font=('times new roman', 20, 'bold'),
                      bg='#7aabd4', fg='black', padx=680, pady=15)
    headlabel.place(x=0, y=0)

    undolabel = Button(usermanage_frame, image=undo_icon, compound=RIGHT, borderwidth=0,
                       bg='#7aabd4', cursor='hand2', command=lambda: usermanage_frame.place_forget())
    undolabel.place(x=5, y=2)
    undolabel.image = undo_icon

    employee_frame = Frame(usermanage_frame)
    employee_frame.place(x=0, y=79, relwidth=1, height=235)
    search_frame = Frame(employee_frame)
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Name', 'Email', 'Contact', 'Gender', 'Address', 'Age'),
                                   font=('times new roman', 12), state='readonly', justify=CENTER)
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0)
    search_entry = Entry(search_frame, font=('times new roman', 12))
    search_entry.grid(row=0, column=2)
    search_button = Button(search_frame, text='Search', font=('times new roman', 12))
    search_button.grid(row=0, column=3)
    
    employee_treeview = ttk.Treeview(employee_frame, columns=('Name', 'Email', 'Contact', 'Age', 'Address', 'Gender'),
                                     show='headings')
    employee_treeview.place(x=20, y=50)

    employee_treeview.heading('Name', text='Name')
    employee_treeview.heading('Email', text='Email')
    employee_treeview.heading('Contact', text='Contact')
    employee_treeview.heading('Age', text='Age')
    employee_treeview.heading('Address', text='Address')
    employee_treeview.heading('Gender', text='Gender')

    employee_treeview.column('Name', width=210)
    employee_treeview.column('Contact', width=170)
    employee_treeview.column('Age', width=70)
    employee_treeview.column('Address', width=270)
    employee_treeview.column('Gender', width=70)

    treeview_data()

    detail_frame = Frame(usermanage_frame)
    detail_frame.place(x=0, y=320)

    emp_name = Label(detail_frame, text='Name:', font=('times new roman', 15))
    emp_name.grid(row=0, column=0, padx=20, pady=10)
    name_entry = Entry(detail_frame, font=('times new roman', 12), width=20)
    name_entry.grid(row=0, column=1, padx=40)
    
    emp_email = Label(detail_frame, text='Email:', font=('times new roman', 15))
    emp_email.grid(row=1, column=0, padx=20, pady=10)
    email_entry = Entry(detail_frame, font=('times new roman', 12), width=20)
    email_entry.grid(row=1, column=1, padx=20, pady=10)

    emp_contact = Label(detail_frame, text='Contact:', font=('times new roman', 15))
    emp_contact.grid(row=0, column=3, padx=20, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), width=20)
    contact_entry.grid(row=0, column=4)

    emp_age = Label(detail_frame, text='Age:', font=('times new roman', 15))
    emp_age.grid(row=1, column=3, padx=20, pady=10, sticky='w')
    age_entry = Entry(detail_frame, font=('times new roman', 12), width=20)
    age_entry.grid(row=1, column=4)

    emp_address = Label(detail_frame, text='Address:', font=('times new roman', 15))
    emp_address.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    address_entry = Entry(detail_frame, font=('times new roman', 12), width=20)
    address_entry.grid(row=2, column=1)

    emp_gender = Label(detail_frame, text='Gender:', font=('times new roman', 15))
    emp_gender.grid(row=2, column=3, padx=10, pady=10, sticky='w')
    gender_entry = Entry(detail_frame, font=('times new roman', 12), width=20)
    gender_entry.grid(row=2, column=4)

    save_button = Button(detail_frame, text='Update', font=('Helvetica', 15),
                         command=lambda: update(name_entry.get(), email_entry.get(), contact_entry.get(), 
                                                  age_entry.get(), address_entry.get(), gender_entry.get()),
                         bg='#0b8fcb', padx=20, fg='white')
    save_button.grid(row=0, column=5, padx=50)

    add_button = Button(detail_frame, text='Add', font=('Helvetica', 15), bg='#0b8fcb', padx=20, pady=3,
                        command=add_employee, fg='white')
    add_button.grid(row=0, column=6, padx=15)

    clear_button = Button(detail_frame, text='Clear', font=('Helvetica', 15), bg='#0b8fcb',
                          command=lambda: clear(name_entry, email_entry, contact_entry, age_entry, gender_entry, address_entry),
                          padx=20, fg='white')
    clear_button.grid(row=1, column=5, padx=50, pady=10)

    delete_button = Button(detail_frame, text='Delete', font=('Helvetica', 15),
                           command=lambda: delete_details(name_entry, email_entry, contact_entry, age_entry, gender_entry, address_entry),
                           bg='#0b8fcb', padx=20, fg='white')
    delete_button.grid(row=1, column=6, padx=15)


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