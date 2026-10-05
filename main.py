import tkinter as tk
import sqlite3

from datetime import datetime

# DATABASE

conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    price REAL
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone TEXT
)
""")

conn.commit()

# ORDERS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    item_name TEXT,
    quantity INTEGER,
    total REAL
)
""")

conn.commit()

# ADD ORDER DATE COLUMN

try:
    cursor.execute(
        "ALTER TABLE orders ADD COLUMN order_date TEXT"
    )
    conn.commit()
except sqlite3.OperationalError:
    pass

# INVENTORY TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    stock INTEGER
)
""")

conn.commit()

# MAIN WINDOW


window = tk.Tk()

window.title("Cafe Management System")
window.geometry("500x500")



# MENU MANAGEMENT FUNCTION

def menu_management():

    menu_window = tk.Toplevel(window)

    menu_window.title("Menu Management")
    menu_window.geometry("800x600")


    # Heading

    title = tk.Label(
        menu_window,
        text="MENU MANAGEMENT",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=30)


    # Item Name

    item_label = tk.Label(
        menu_window,
        text="Item Name",
        font=("Arial", 14)
    )

    item_label.pack()

    item_entry = tk.Entry(
        menu_window,
        font=("Arial", 14),
        width=25
    )

    item_entry.pack(pady=10)


    # Price

    price_label = tk.Label(
        menu_window,
        text="Price",
        font=("Arial", 14)
    )

    price_label.pack()

    price_entry = tk.Entry(
        menu_window,
        font=("Arial", 14),
        width=25
    )

    price_entry.pack(pady=10)
    # Search Item

    search_entry = tk.Entry(
        menu_window,
        font=("Arial", 14),
        width=25
    )

    search_entry.pack(pady=10)

    
    # MENU TABLE
    

    table = tk.Listbox(
        menu_window,
        width=50,
        height=10,
        font=("Arial", 12)
    )

    table.pack(pady=20)


   
    # ADD ITEM FUNCTION
   

    def add_item():

        item_name = item_entry.get()
        price = price_entry.get()

        if item_name == "" or price == "":

            print("Please enter Item Name and Price")

        else:

            cursor.execute(
                "INSERT INTO menu (item_name, price) VALUES (?, ?)",
                (item_name, price)
            )

            conn.commit()

            print("Item Added Successfully")

            # Refresh table

            table.delete(0, tk.END)

            cursor.execute("SELECT * FROM menu")

            items = cursor.fetchall()

            for item in items:

                table.insert(
                    tk.END,
                    f"ID: {item[0]}   {item[1]}   ₹{item[2]}"
                )

            item_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)


   
    # UPDATE ITEM FUNCTION
    

    def update_item():

        selected = table.curselection()

        if selected:

            item = table.get(selected[0])

            item_id = item.split()[1]

            new_name = item_entry.get()
            new_price = price_entry.get()

            if new_name == "" or new_price == "":

                print("Please enter new Item Name and Price")

            else:

                cursor.execute(
                    "UPDATE menu SET item_name = ?, price = ? WHERE id = ?",
                    (new_name, new_price, item_id)
                )

                conn.commit()

                print("Item Updated Successfully")

                # Refresh table

                table.delete(0, tk.END)

                cursor.execute("SELECT * FROM menu")

                items = cursor.fetchall()

                for item in items:

                    table.insert(
                        tk.END,
                        f"ID: {item[0]}   {item[1]}   ₹{item[2]}"
                    )

                item_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)

        else:

            print("Please select an item")


    
    # DELETE ITEM FUNCTION
    
    def delete_item():

        selected = table.curselection()

        if selected:

            item = table.get(selected[0])

            item_id = item.split()[1]

            cursor.execute(
                "DELETE FROM menu WHERE id = ?",
                (item_id,)
            )

            conn.commit()

            print("Item Deleted Successfully")

            # Refresh Table

            table.delete(0, tk.END)

            cursor.execute("SELECT * FROM menu")

            items = cursor.fetchall()

            for item in items:

                table.insert(
                    tk.END,
                    f"ID: {item[0]}   {item[1]}   ₹{item[2]}"
                )

        else:

            print("Please select an item")

    
    # SEARCH ITEM FUNCTION
   

    def search_item():

        search_name = search_entry.get()

        table.delete(0, tk.END)

        cursor.execute(
            "SELECT * FROM menu WHERE item_name LIKE ?",
            ('%' + search_name + '%',)
        )

        items = cursor.fetchall()

        for item in items:

            table.insert(
                tk.END,
                f"ID: {item[0]}   {item[1]}   ₹{item[2]}"
            )
     
      
    # SHOW ALL ITEMS FUNCTION
    

    def show_all_items():

        table.delete(0, tk.END)

        cursor.execute("SELECT * FROM menu")

        items = cursor.fetchall()

        for item in items:

            table.insert(
                tk.END,
                f"ID: {item[0]}   {item[1]}   ₹{item[2]}"
            ) 
    
    # ADD ITEM BUTTON
    

    add_button = tk.Button(
        menu_window,
        text="ADD ITEM",
        font=("Arial", 14, "bold"),
        width=15,
        command=add_item
    )

    add_button.pack(pady=10)


    
    # UPDATE ITEM BUTTON
   

    update_button = tk.Button(
        menu_window,
        text="UPDATE ITEM",
        font=("Arial", 14, "bold"),
        width=15,
        command=update_item
    )

    update_button.pack(pady=10)


   
    # DELETE ITEM BUTTON
    

    delete_button = tk.Button(
        menu_window,
        text="DELETE ITEM",
        font=("Arial", 14, "bold"),
        width=15,
        command=delete_item
    )

    delete_button.pack(pady=10)

    
    # SEARCH ITEM BUTTON
    

    search_button = tk.Button(
        menu_window,
        text="SEARCH ITEM",
        font=("Arial", 14, "bold"),
        width=15,
        command=search_item
    )

    search_button.pack(pady=10)
 
    
    # SHOW ALL ITEMS BUTTON
    

    show_all_button = tk.Button(
        menu_window,
        text="SHOW ALL ITEMS",
        font=("Arial", 14, "bold"),
        width=15,
        command=show_all_items
    )

    show_all_button.pack(pady=10)
    
    # SHOW SAVED ITEMS
    

    cursor.execute("SELECT * FROM menu")

    items = cursor.fetchall()

    for item in items:

        table.insert(
            tk.END,
            f"ID: {item[0]}   {item[1]}   ₹{item[2]}"
        )


# CUSTOMER MANAGEMENT

def customer_management():

    customer_window = tk.Toplevel(window)

    customer_window.title("Customer Management")
    customer_window.geometry("800x600")


    # Heading

    title = tk.Label(
        customer_window,
        text="CUSTOMER MANAGEMENT",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=30)


    # Customer Name

    name_label = tk.Label(
        customer_window,
        text="Customer Name",
        font=("Arial", 14)
    )

    name_label.pack()


    name_entry = tk.Entry(
        customer_window,
        font=("Arial", 14),
        width=25
    )

    name_entry.pack(pady=10)


    # Phone Number

    phone_label = tk.Label(
        customer_window,
        text="Phone Number",
        font=("Arial", 14)
    )

    phone_label.pack()


    phone_entry = tk.Entry(
        customer_window,
        font=("Arial", 14),
        width=25
    )

    phone_entry.pack(pady=10)
    
    
    # ADD CUSTOMER FUNCTION
    

    def add_customer():

        customer_name = name_entry.get()
        phone = phone_entry.get()

        if customer_name == "" or phone == "":

            print("Please enter Customer Name and Phone Number")

        else:

            cursor.execute(
                "INSERT INTO customers (customer_name, phone) VALUES (?, ?)",
                (customer_name, phone)
            )

            conn.commit()

            print("Customer Added Successfully")
           
            # Refresh Customer List

            customer_table.delete(0, tk.END)

            cursor.execute("SELECT * FROM customers")

            customers = cursor.fetchall()

            for customer in customers:

                customer_table.insert(
                    tk.END,
                    f"ID: {customer[0]}   {customer[1]}   {customer[2]}"
                )
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
    
    # ADD CUSTOMER BUTTON
   

    add_customer_button = tk.Button(
        customer_window,
        text="ADD CUSTOMER",
        font=("Arial", 14, "bold"),
        width=18,
        command=add_customer
    )

    add_customer_button.pack(pady=20)   
    
    # CUSTOMER LIST
    

    customer_table = tk.Listbox(
        customer_window,
        width=50,
        height=10,
        font=("Arial", 12)
    )

    customer_table.pack(pady=20)
    
    # UPDATE CUSTOMER FUNCTION
    

    def update_customer():

        selected = customer_table.curselection()

        if selected:

            customer = customer_table.get(selected[0])

            customer_id = customer.split()[1]

            new_name = name_entry.get()
            new_phone = phone_entry.get()

            if new_name == "" or new_phone == "":

                print("Please enter new Customer Name and Phone Number")

            else:

                cursor.execute(
                    "UPDATE customers SET customer_name = ?, phone = ? WHERE id = ?",
                    (new_name, new_phone, customer_id)
                )

                conn.commit()

                print("Customer Updated Successfully")

                # Refresh Customer List

                customer_table.delete(0, tk.END)

                cursor.execute("SELECT * FROM customers")

                customers = cursor.fetchall()

                for customer in customers:

                    customer_table.insert(
                        tk.END,
                        f"ID: {customer[0]}   {customer[1]}   {customer[2]}"
                    )

                name_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)

        else:

            print("Please select a customer")
   
    # UPDATE CUSTOMER BUTTON
   

    update_customer_button = tk.Button(
        customer_window,
        text="UPDATE CUSTOMER",
        font=("Arial", 14, "bold"),
        width=18,
        command=update_customer
    )

    update_customer_button.pack(pady=10)
    
    # DELETE CUSTOMER FUNCTION
    

    def delete_customer():

        selected = customer_table.curselection()

        if selected:

            customer = customer_table.get(selected[0])

            customer_id = customer.split()[1]

            cursor.execute(
                "DELETE FROM customers WHERE id = ?",
                (customer_id,)
            )

            conn.commit()

            print("Customer Deleted Successfully")

            # Refresh Customer List

            customer_table.delete(0, tk.END)

            cursor.execute("SELECT * FROM customers")

            customers = cursor.fetchall()

            for customer in customers:

                customer_table.insert(
                    tk.END,
                    f"ID: {customer[0]}   {customer[1]}   {customer[2]}"
                )

        else:

            print("Please select a customer") 
            
    
    # DELETE CUSTOMER BUTTON
    

    delete_customer_button = tk.Button(
        customer_window,
        text="DELETE CUSTOMER",
        font=("Arial", 14, "bold"),
        width=18,
        command=delete_customer
    )

    delete_customer_button.pack(pady=10) 
    
    
    # SEARCH CUSTOMER BOX
    
    search_label = tk.Label(
        customer_window,
        text="Search Customer",
        font=("Arial", 14)
    )

    search_label.pack(pady=5)

    search_entry = tk.Entry(
        customer_window,
        font=("Arial", 14),
        width=25
    )

    search_entry.pack(pady=5)    
   
    # SEARCH CUSTOMER FUNCTION
    

    def search_customer():

        search_text = search_entry.get()

        customer_table.delete(0, tk.END)

        cursor.execute(
            "SELECT * FROM customers WHERE customer_name LIKE ? OR phone LIKE ?",
            ('%' + search_text + '%', '%' + search_text + '%')
        )

        customers = cursor.fetchall()

        for customer in customers:

            customer_table.insert(
                tk.END,
                f"ID: {customer[0]}   {customer[1]}   {customer[2]}"
            )    
  
    
    # SEARCH CUSTOMER BUTTON
   

    search_customer_button = tk.Button(
        customer_window,
        text="SEARCH CUSTOMER",
        font=("Arial", 14, "bold"),
        width=18,
        command=search_customer
    )

    search_customer_button.pack(pady=10) 
           
   
    # SHOW ALL CUSTOMERS FUNCTION
    

    def show_all_customers():

        customer_table.delete(0, tk.END)

        cursor.execute("SELECT * FROM customers")

        customers = cursor.fetchall()

        for customer in customers:

            customer_table.insert(
                tk.END,
                f"ID: {customer[0]}   {customer[1]}   {customer[2]}"
            )
    
    # SHOW ALL CUSTOMERS BUTTON
    

    show_all_customers_button = tk.Button(
        customer_window,
        text="SHOW ALL CUSTOMERS",
        font=("Arial", 14, "bold"),
        width=18,
        command=show_all_customers
    )

    show_all_customers_button.pack(pady=10)            
            
    # SHOW SAVED CUSTOMERS
    

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    for customer in customers:

        customer_table.insert(
            tk.END,
            f"ID: {customer[0]}   {customer[1]}   {customer[2]}"
        )  
        

# ORDER MANAGEMENT FUNCTION


def order_management():

    order_window = tk.Toplevel(window)

    order_window.title("Order Management")

    order_window.geometry("800x600")


    # Heading

    title = tk.Label(
        order_window,
        text="ORDER MANAGEMENT",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=30)


    # Customer Name

    customer_label = tk.Label(
        order_window,
        text="Customer Name",
        font=("Arial", 14)
    )

    customer_label.pack()


    customer_entry = tk.Entry(
        order_window,
        font=("Arial", 14),
        width=25
    )

    customer_entry.pack(pady=10)


    # Item Name

    item_label = tk.Label(
        order_window,
        text="Item Name",
        font=("Arial", 14)
    )

    item_label.pack()


    item_entry = tk.Entry(
        order_window,
        font=("Arial", 14),
        width=25
    )

    item_entry.pack(pady=10)


    # Quantity

    quantity_label = tk.Label(
        order_window,
        text="Quantity",
        font=("Arial", 14)
    )

    quantity_label.pack()


    quantity_entry = tk.Entry(
        order_window,
        font=("Arial", 14),
        width=25
    )

    quantity_entry.pack(pady=10)   
    
    # CALCULATE TOTAL FUNCTION

    def calculate_total():

        item_name = item_entry.get()
        quantity = quantity_entry.get()

        if item_name == "" or quantity == "":
            print("Please enter Item Name and Quantity")
            return

        cursor.execute(
            "SELECT price FROM menu WHERE item_name = ?",
            (item_name,)
        )

        result = cursor.fetchone()

        if result:

            price = result[0]
            total = price * int(quantity)

            total_label.config(
                text=f"Total: ₹{total}"
            )

        else:

            total_label.config(
                text="Item Not Found"
            )


    # CALCULATE BUTTON

    total_button = tk.Button(
        order_window,
        text="CALCULATE TOTAL",
        font=("Arial", 14, "bold"),
        width=20,
        command=calculate_total
    )

    total_button.pack(pady=15)


    # TOTAL LABEL

    total_label = tk.Label(
        order_window,
        text="Total: ₹0",
        font=("Arial", 16, "bold")
    )

    total_label.pack(pady=10)
    
    # SAVE ORDER FUNCTION

    # SAVE MULTIPLE ITEMS ORDER

    def save_order():
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        customer_name = customer_entry.get()

        if customer_name == "":
            print("Please enter Customer Name")
            return

        if order_list.size() == 0:
            print("Please add at least one item")
            return

        for item in order_list.get(0, tk.END):

            parts = item.split("   ")

            item_name = parts[0]
            quantity = int(parts[1].replace("x ", ""))
            total = float(parts[2].replace("= ₹", ""))

            cursor.execute(
    """
    INSERT INTO orders
    (customer_name, item_name, quantity, total, order_date)
    VALUES (?, ?, ?, ?, ?)
    """,
    (customer_name, item_name, quantity, total, order_date)
)

        conn.commit()

        print("Order Saved Successfully")

        customer_entry.delete(0, tk.END)
        order_list.delete(0, tk.END)

        grand_total_label.config(
            text="Grand Total: ₹0"
        )   

    # SAVE ORDER BUTTON

    save_order_button = tk.Button(
        order_window,
        text="SAVE ORDER",
        font=("Arial", 14, "bold"),
        width=20,
        command=save_order
    )

    save_order_button.pack(pady=15)    
 
    # ORDER LIST

    order_list = tk.Listbox(
        order_window,
        width=50,
        height=8,
        font=("Arial", 12)
    )

    order_list.pack(pady=20) 
    
    # ADD ITEM TO ORDER FUNCTION

    def add_item_to_order():

        item_name = item_entry.get()
        quantity = quantity_entry.get()

        if item_name == "" or quantity == "":
            print("Please enter Item Name and Quantity")
            return

        cursor.execute(
            "SELECT price FROM menu WHERE item_name = ?",
            (item_name,)
        )

        result = cursor.fetchone()

        if result:

            price = result[0]
            total = price * int(quantity)

            order_list.insert(
                tk.END,
                f"{item_name}   x {quantity}   = ₹{total}"
            )

            item_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)

        else:

            print("Item Not Found")


    # ADD ITEM BUTTON

    add_order_item_button = tk.Button(
        order_window,
        text="ADD ITEM",
        font=("Arial", 14, "bold"),
        width=20,
        command=add_item_to_order
    )

    add_order_item_button.pack(pady=10)  
    
    # GRAND TOTAL FUNCTION

    def calculate_grand_total():

        grand_total = 0

        for item in order_list.get(0, tk.END):

            total_part = item.split("₹")[-1]

            grand_total = grand_total + float(total_part)

        grand_total_label.config(
            text=f"Grand Total: ₹{grand_total}"
        )


    # GRAND TOTAL BUTTON

    grand_total_button = tk.Button(
        order_window,
        text="GRAND TOTAL",
        font=("Arial", 14, "bold"),
        width=20,
        command=calculate_grand_total
    )

    grand_total_button.pack(pady=10)


    # GRAND TOTAL LABEL

    grand_total_label = tk.Label(
        order_window,
        text="Grand Total: ₹0",
        font=("Arial", 16, "bold")
    )

    grand_total_label.pack(pady=10)  
    
# BILLING MANAGEMENT FUNCTION

def billing_management():

    billing_window = tk.Toplevel(window)

    billing_window.title("Billing")

    billing_window.geometry("800x600")

    title = tk.Label(
        billing_window,
        text="BILLING",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=30)  
    
    # CUSTOMER NAME

    customer_label = tk.Label(
        billing_window,
        text="Customer Name",
        font=("Arial", 14)
    )

    customer_label.pack()

    customer_entry = tk.Entry(
        billing_window,
        font=("Arial", 14),
        width=25
    )

    customer_entry.pack(pady=10)


    # SUBTOTAL

    subtotal_label = tk.Label(
        billing_window,
        text="Subtotal: ₹0",
        font=("Arial", 16, "bold")
    )

    subtotal_label.pack(pady=20) 
    
    # CALCULATE SUBTOTAL

    def calculate_subtotal():

        customer_name = customer_entry.get()

        if customer_name == "":
            print("Please enter Customer Name")
            return

        cursor.execute(
            "SELECT SUM(total) FROM orders WHERE customer_name = ?",
            (customer_name,)
        )

        result = cursor.fetchone()

        if result[0] is not None:

            subtotal = result[0]

            subtotal_label.config(
                text=f"Subtotal: ₹{subtotal}"
            )

        else:

            subtotal_label.config(
                text="No Orders Found"
            )


    subtotal_button = tk.Button(
        billing_window,
        text="CALCULATE SUBTOTAL",
        font=("Arial", 13, "bold"),
        width=20,
        command=calculate_subtotal
    )

    subtotal_button.pack(pady=10)    
  
    # TAX

    tax_label = tk.Label(
        billing_window,
        text="Tax (5%): ₹0",
        font=("Arial", 16, "bold")
    )

    tax_label.pack(pady=10)   

    # FINAL TOTAL

    total_label = tk.Label(
        billing_window,
        text="Total Amount: ₹0",
        font=("Arial", 18, "bold")
    )

    total_label.pack(pady=15)   
    
    # DISCOUNT

    discount_label = tk.Label(
        billing_window,
        text="Discount: ₹0",
        font=("Arial", 16, "bold")
    )

    discount_label.pack(pady=10)   
    
    discount_entry = tk.Entry(
        billing_window,
        font=("Arial", 14),
        width=15
    )

    discount_entry.pack(pady=5)

    discount_info = tk.Label(
        billing_window,
        text="Enter Discount (%)",
        font=("Arial", 12)
    )

    discount_info.pack() 
    
    # CALCULATE FINAL BILL

    def calculate_final_bill():

        customer_name = customer_entry.get()

        if customer_name == "":
            print("Please enter Customer Name")
            return

        cursor.execute(
            "SELECT SUM(total) FROM orders WHERE customer_name = ?",
            (customer_name,)
        )

        result = cursor.fetchone()

        if result[0] is not None:

            subtotal = result[0]

            # 5% Tax
            tax = subtotal * 0.05

            # Get Discount
            discount_text = discount_entry.get()

            if discount_text == "":
                discount_percent = 0
            else:
                discount_percent = float(discount_text)

            discount = subtotal * discount_percent / 100

            # Final Amount
            final_amount = subtotal + tax - discount

            subtotal_label.config(
                text=f"Subtotal: ₹{subtotal:.2f}"
            )

            tax_label.config(
                text=f"Tax (5%): ₹{tax:.2f}"
            )

            discount_label.config(
                text=f"Discount ({discount_percent}%): ₹{discount:.2f}"
            )

            total_label.config(
                text=f"Total Amount: ₹{final_amount:.2f}"
            )

        else:

            print("No Orders Found")  
            
    calculate_final_button = tk.Button(
        billing_window,
        text="CALCULATE FINAL BILL",
        font=("Arial", 14, "bold"),
        width=22,
        command=calculate_final_bill
    )

    calculate_final_button.pack(pady=15)  

    # PAYMENT METHOD

    payment_label = tk.Label(
        billing_window,
        text="Payment Method",
        font=("Arial", 14, "bold")
    )

    payment_label.pack(pady=10)

    payment_method = tk.StringVar()

    cash_button = tk.Radiobutton(
        billing_window,
        text="Cash",
        variable=payment_method,
        value="Cash",
        font=("Arial", 12)
    )

    cash_button.pack()

    upi_button = tk.Radiobutton(
        billing_window,
        text="UPI",
        variable=payment_method,
        value="UPI",
        font=("Arial", 12)
    )

    upi_button.pack()

    card_button = tk.Radiobutton(
        billing_window,
        text="Card",
        variable=payment_method,
        value="Card",
        font=("Arial", 12)
    )

    card_button.pack()          
    
    # GENERATE BILL

    def generate_bill():

        customer_name = customer_entry.get()
        payment = payment_method.get()

        if customer_name == "":
            print("Please enter Customer Name")
            return

        if payment == "":
            print("Please select Payment Method")
            return

        cursor.execute(
            "SELECT SUM(total) FROM orders WHERE customer_name = ?",
            (customer_name,)
        )

        result = cursor.fetchone()

        if result[0] is None:
            print("No Orders Found")
            return

        subtotal = result[0]

        # Tax
        tax = subtotal * 0.05

        # Discount
        discount_text = discount_entry.get()

        if discount_text == "":
            discount_percent = 0
        else:
            discount_percent = float(discount_text)

        discount = subtotal * discount_percent / 100

        # Final Amount
        final_amount = subtotal + tax - discount

        # Bill Window
        bill_window = tk.Toplevel(billing_window)

        bill_window.title("Generated Bill")

        bill_window.geometry("500x600")

        bill_title = tk.Label(
            bill_window,
            text="☕ CAFE BILL",
            font=("Arial", 22, "bold")
        )

        bill_title.pack(pady=20)

        bill_text = tk.Label(
            bill_window,
            text=(
                f"Customer Name: {customer_name}\n\n"
                f"Subtotal: ₹{subtotal:.2f}\n"
                f"Tax (5%): ₹{tax:.2f}\n"
                f"Discount: ₹{discount:.2f}\n"
                f"--------------------------\n"
                f"TOTAL: ₹{final_amount:.2f}\n\n"
                f"Payment Method: {payment}"
            ),
            font=("Arial", 14),
            justify="left"
        )

        bill_text.pack(pady=20)   
    generate_button = tk.Button(
        billing_window,
        text="GENERATE BILL",
        font=("Arial", 14, "bold"),
        width=20,
        command=generate_bill
    )

    generate_button.pack(pady=15)  
    
# INVENTORY MANAGEMENT FUNCTION

def inventory_management():

    inventory_window = tk.Toplevel(window)

    inventory_window.title("Inventory Management")

    inventory_window.geometry("800x600")


    # Heading

    title = tk.Label(
        inventory_window,
        text="INVENTORY MANAGEMENT",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=30)

    # Item Name

    item_label = tk.Label(
        inventory_window,
        text="Item Name",
        font=("Arial", 14)
    )

    item_label.pack()

    item_entry = tk.Entry(
        inventory_window,
        font=("Arial", 14),
        width=25
    )

    item_entry.pack(pady=10)


    # Stock Quantity

    stock_label = tk.Label(
        inventory_window,
        text="Stock Quantity",
        font=("Arial", 14)
    )

    stock_label.pack()

    stock_entry = tk.Entry(
        inventory_window,
        font=("Arial", 14),
        width=25
    )

    stock_entry.pack(pady=10)       

    # ADD STOCK FUNCTION

    def add_stock():

        item_name = item_entry.get()
        stock = stock_entry.get()

        if item_name == "" or stock == "":

            print("Please enter Item Name and Stock Quantity")

        else:

            cursor.execute(
                "INSERT INTO inventory (item_name, stock) VALUES (?, ?)",
                (item_name, stock)
            )

            conn.commit()

            print("Stock Added Successfully")

            item_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)


    # ADD STOCK BUTTON

    add_stock_button = tk.Button(
        inventory_window,
        text="ADD STOCK",
        font=("Arial", 14, "bold"),
        width=18,
        command=add_stock
    )

    add_stock_button.pack(pady=15)
    
    # INVENTORY LIST

    inventory_table = tk.Listbox(
        inventory_window,
        width=50,
        height=10,
        font=("Arial", 12)
    )

    inventory_table.pack(pady=20) 
    
    
    # SHOW SAVED INVENTORY

    cursor.execute("SELECT * FROM inventory")

    inventory_items = cursor.fetchall()

    for item in inventory_items:

        inventory_table.insert(
            tk.END,
            f"ID: {item[0]}   {item[1]}   Stock: {item[2]}"
        )  
        
    # UPDATE STOCK FUNCTION

    def update_stock():

        selected = inventory_table.curselection()

        if selected:

            item = inventory_table.get(selected[0])

            item_id = item.split()[1]

            new_stock = stock_entry.get()

            if new_stock == "":

                print("Please enter new Stock Quantity")

            else:

                cursor.execute(
                    "UPDATE inventory SET stock = ? WHERE id = ?",
                    (new_stock, item_id)
                )

                conn.commit()

                print("Stock Updated Successfully")

                stock_entry.delete(0, tk.END)

                inventory_table.delete(0, tk.END)

                cursor.execute("SELECT * FROM inventory")

                inventory_items = cursor.fetchall()

                for item in inventory_items:

                    inventory_table.insert(
                        tk.END,
                        f"ID: {item[0]}   {item[1]}   Stock: {item[2]}"
                    )

        else:

            print("Please select an item") 
            
 # UPDATE STOCK BUTTON

    update_stock_button = tk.Button(
        inventory_window,
        text="UPDATE STOCK",
        font=("Arial", 14, "bold"),
        width=18,
        command=update_stock
    )

    update_stock_button.pack(pady=10) 

    # DELETE STOCK FUNCTION

    def delete_stock():

        selected = inventory_table.curselection()

        if selected:

            item = inventory_table.get(selected[0])

            item_id = item.split()[1]

            cursor.execute(
                "DELETE FROM inventory WHERE id = ?",
                (item_id,)
            )

            conn.commit()

            print("Stock Deleted Successfully")

            inventory_table.delete(selected[0])

        else:

            print("Please select an item")


    # DELETE STOCK BUTTON

    delete_stock_button = tk.Button(
        inventory_window,
        text="DELETE STOCK",
        font=("Arial", 14, "bold"),
        width=18,
        command=delete_stock
    )

    delete_stock_button.pack(pady=10)

    # LOW STOCK ALERT FUNCTION

    def low_stock_alert():

        cursor.execute(
            "SELECT * FROM inventory WHERE stock <= 5"
        )

        low_items = cursor.fetchall()

        if low_items:

            print("LOW STOCK ITEMS:")

            for item in low_items:
                print(
                    f"{item[1]} - Stock: {item[2]}"
                )

        else:

            print("No Low Stock Items")


    # LOW STOCK ALERT BUTTON

    low_stock_button = tk.Button(
        inventory_window,
        text="LOW STOCK ALERT",
        font=("Arial", 14, "bold"),
        width=18,
        command=low_stock_alert
    )

    low_stock_button.pack(pady=10)   

# REPORTS MANAGEMENT FUNCTION

def reports_management():

    reports_window = tk.Toplevel(window)

    reports_window.title("Reports")

    reports_window.geometry("800x600")


    # Heading

    title = tk.Label(
        reports_window,
        text="REPORTS",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=30)


    # DAILY SALES

    def daily_sales():

        cursor.execute(
            "SELECT SUM(total) FROM orders"
        )

        result = cursor.fetchone()

        if result[0] is None:

            print("No Sales Available")

        else:

            print("Total Sales:", result[0])
            
    # DAILY SALES BUTTON

    daily_button = tk.Button(
        reports_window,
        text="DAILY SALES",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=daily_sales
    )

    daily_button.pack(pady=20) 
    
    # MONTHLY SALES

    def monthly_sales():

        cursor.execute(
            "SELECT SUM(total) FROM orders"
        )

        result = cursor.fetchone()

        if result[0] is None:

            print("No Monthly Sales Available")

        else:

            print("Total Monthly Sales:", result[0])


    # MONTHLY SALES BUTTON

    monthly_button = tk.Button(
        reports_window,
        text="MONTHLY SALES",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=monthly_sales
    )

    monthly_button.pack(pady=10) 
    
    # BEST SELLING ITEMS

    def best_selling_items():

        cursor.execute("""
            SELECT item_name, SUM(quantity)
            FROM orders
            GROUP BY item_name
            ORDER BY SUM(quantity) DESC
        """)

        items = cursor.fetchall()
        if items:

            reports_table.delete(0, tk.END)

            reports_table.insert(
                tk.END,
                "BEST SELLING ITEMS"
            )

            for item in items:

                reports_table.insert(
                    tk.END,
                    f"{item[0]} - Quantity Sold: {item[1]}"
                )

        else:

            reports_table.delete(0, tk.END)

            reports_table.insert(
                tk.END,
                "No Sales Available"
            )       
       

    # BEST SELLING ITEMS BUTTON

    best_selling_button = tk.Button(
        reports_window,
        text="BEST SELLING ITEMS",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=best_selling_items
    )

    best_selling_button.pack(pady=10)  
    
    # REPORTS TABLE

    reports_table = tk.Listbox(
        reports_window,
        width=50,
        height=10,
        font=("Arial", 12)
    )

    reports_table.pack(pady=20)    
     

# DASHBOARD FUNCTION


def dashboard():

    dashboard_window = tk.Toplevel(window)

    dashboard_window.title("Cafe Management System - Dashboard")
    dashboard_window.geometry("1000x600")


    # Dashboard Heading

    title = tk.Label(
        dashboard_window,
        text="CAFE MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=30)


    # Button Frame

    button_frame = tk.Frame(dashboard_window)

    button_frame.pack(pady=20)


    # Menu Button

    menu_button = tk.Button(
        button_frame,
        text="MENU",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=menu_management
    )

    menu_button.grid(
        row=0,
        column=0,
        padx=20,
        pady=15
    )


        # Customer Button

    customer_button = tk.Button(
        button_frame,
        text="CUSTOMERS",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=customer_management
    )

    customer_button.grid(
        row=0,
        column=1,
        padx=20,
        pady=15
    )


    # Order Button

    order_button = tk.Button(
        button_frame,
        text="ORDERS",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=order_management
    )

    order_button.grid(
        row=1,
        column=0,
        padx=20,
        pady=15
    )


    # Billing Button

    billing_button = tk.Button(
        button_frame,
        text="BILLING",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=billing_management
    )

    billing_button.grid(
        row=1,
        column=1,
        padx=20,
        pady=15
    )


    # Inventory Button

    inventory_button = tk.Button(
        button_frame,
        text="INVENTORY",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=inventory_management
    )

    inventory_button.grid(
        row=2,
        column=0,
        padx=20,
        pady=15
    )


    # Reports Button

    report_button = tk.Button(
        button_frame,
        text="REPORTS",
        font=("Arial", 14, "bold"),
        width=20,
        height=2,
        command=reports_management
    )

    report_button.grid(
        row=2,
        column=1,
        padx=20,
        pady=15
    )


    # Logout Button

    logout_button = tk.Button(
        dashboard_window,
        text="LOGOUT",
        font=("Arial", 14, "bold"),
        width=20
    )

    logout_button.pack(pady=20)



# LOGIN FUNCTION

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":

        print("Login Successful")

        dashboard()

        window.withdraw()

    else:

        print("Invalid Username or Password")



# LOGIN PAGE


title = tk.Label(
    window,
    text="CAFE MANAGEMENT",
    font=("Arial", 24, "bold")
)

title.pack(pady=40)


# Username

username_label = tk.Label(
    window,
    text="Username",
    font=("Arial", 14)
)

username_label.pack()


username_entry = tk.Entry(
    window,
    font=("Arial", 14),
    width=25
)

username_entry.pack(pady=10)


# Password

password_label = tk.Label(
    window,
    text="Password",
    font=("Arial", 14)
)

password_label.pack()


password_entry = tk.Entry(
    window,
    font=("Arial", 14),
    width=25,
    show="*"
)

password_entry.pack(pady=10)


# Login Button

login_button = tk.Button(
    window,
    text="LOGIN",
    font=("Arial", 14, "bold"),
    width=15,
    command=login
)

login_button.pack(pady=30)


import sqlite3

conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM orders")
print(cursor.fetchall())

# START PROGRAM


window.mainloop()

