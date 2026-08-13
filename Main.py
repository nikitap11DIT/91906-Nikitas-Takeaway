"""Nikita's Takeaway ( Takeaway food ordering system )
    Author: Nikita Patel
    Starting : 8th June started 
    Purpose: Creating A Takeaway ordering system"""

# -------- Retrieve the Libraries

import tkinter as tk # Import tkinter and shorten it to tk.
from tkinter import messagebox, ttk # Import GUI widgets and message boxes.
from tkmacosx import Button # Import the third party styled button.

# Store the items currently included in the customer's order.
current_order = []

# Store fixed values used throughout the program.
DELIVERY_FEE = 5.00
NO_DELIVERY_FEE = 0.00
MAX_QUANTITY = 20
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 30

# Store the available food items and their prices.
food_prices = {
    "Butter Chicken": 10.00,
    "Chicken Biryani": 14.00,
    "Garlic Naan":3.00,
    "Samosa":2.00,
    "Mango Lassi": 5.00

    }

# ---------------Functions

def add_to_order(
    food_dropdown, quantity_dropdown, table_frame, summary_area,
    subtotal_label, delivery_fee_label, total_label,
    order_type, address_entry, customer_entry

    ):
    """Validate and add a selected food item to the current order."""

    # This helps retrieve the current values entered or selected by the operator.
    customer = customer_entry.get()
    food = food_dropdown.get()
    quantity = quantity_dropdown.get()
    order = order_type.get()
    address = address_entry.get()
 
    # Check whether all required order fields have been left blank.
    if food =="" and quantity == "" and order =="":
            messagebox.showerror( "Error", "Before clicking 'Add to Order', please fill in all fields.")
            return 

    
    # Delivery address cannot start or end with spaces 
    if order == "Delivery" and address != address.strip():
        messagebox.showerror("Error", "Delivery address cannot start or end with spaces.")
        return

    # Remove spaces after validation 
    address = address.strip()
    
    # Delivery address cannot be blank or contain only spaces 
    if order == "Delivery" and address == "":
        messagebox.showerror("Error", "Delivery address is required.")
        return
    
    # Check that the delivery address contains only allowed address characters.
    if order == "Delivery":
        if not address.replace(" ", "").replace(",", "").replace(".", "").replace("'", "").replace("-", "").replace("’", "").isalnum():
            messagebox.showerror("Error","Please enter a valid delivery address")
            return

    # Check that the customer name is not empty or only spaces. 
    if customer.strip() =="":
        messagebox.showerror("Error", "Customer name is required.")
        return

    # Check that the customer name does not contain consecutive spaces.
    if customer != customer.strip():
        messagebox.showerror("Error", "Customer name cannot start or end with spaces.")
        return

    # Customer name cannot contain two spaces together.
    if "  " in customer:
        messagebox.showerror("Error", "Please use only one space between names.")
        return

    # Check that the customer name contains only letters and spaces.
    if not customer.replace(" ","").isalpha():
        messagebox.showerror("Error","Customer name cannot contain special characters or numbers.")
        return

    # Check that the customer name contains at least two letters.
    if len(customer.replace(" ",""))< MIN_NAME_LENGTH:
        messagebox.showerror("Error", "Customer name must be at least 2 letters long.")
        return
    
    # Check that the customer name does not exceed the maximum length.
    if len(customer)> MAX_NAME_LENGTH:
        messagebox.showerror("Error", "Customer name cannot go over 30 letters.")
        return
    
    # Remove unnecessary spaces after validation.
    customer = customer.strip()

    # Check that all required order selections have been completed.
    
    if food =="":
        messagebox.showerror("Error","Please select a food item.")
        return

    if quantity =="":
        messagebox.showerror("Error","Please select a quantity.")
        return

    if order == "":
        messagebox.showerror("Error","Please select Takeaway or Delivery.")
        return
    
    # This calculates the total price for the selected food and quantity.
    price = food_prices[food]
    item_total = price * int(quantity)
    order_line = f"{food} x {quantity} - ${item_total:.2f}"

    # Calculates the total quantity already included in the current order. 
    total_quantity = 0

    # Checks that adding new quantity does not exceed the maximum order limit.
    for item in current_order:
        total_quantity += int(item.split(" x ")[1].split(" - ")[0])

    if total_quantity + int(quantity) > MAX_QUANTITY:
        messagebox.showerror("Error", f"Unfortunately you can only order a maximum of {MAX_QUANTITY} food items.")
        return
        
    # Add the validated item to the current order.
    current_order.append(order_line)

    row = len(current_order)
    
    # Display the new item, quantity and the price in the order summary.
    item_name = tk.Label(table_frame,text=food, font=("Georgia",13), bg="white", relief="solid", bd=1)
    item_name.grid(row=row, column=0, sticky="nsew")

    item_quantity = tk.Label(table_frame, text=quantity,font=("Georgia",13),bg="white", relief="solid",bd=1)
    item_quantity.grid(row=row,column=1,sticky="nsew")

    item_price = tk.Label(table_frame,text=f"${item_total:.2f}",font=("Georgia",13),bg="white",relief="solid",bd=1)
    item_price.grid(row=row,column=2,sticky="nsew")


    # Updates the scroll bar area so all order items can be seen in the order summary.
    summary_area.config(scrollregion=(0,0,800,(len(current_order) + 1) *25))
    
    # Clears the food and quantity selections after adding the item.  
    food_dropdown.set("")
    quantity_dropdown.set("")


    # Calculates the subtotal by adding the price of every item in the order.
    subtotal = 0

    # Applies the delivery fee based on the selected order type chosen.
    for item in current_order:
        parts = item.split("$")
        subtotal += float(parts[1])

    if order_type.get() == "Delivery":
        delivery_fee = DELIVERY_FEE
    else:
        delivery_fee = NO_DELIVERY_FEE

    # Calculates the final order total.
    total = subtotal + delivery_fee

    # Updates the subtotal displayed along with delivery fee and total.
    subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
    delivery_fee_label.config(text=f"Delivery Fee: ${delivery_fee:.2f}")
    total_label.config(text=f"Total: ${total:.2f}")

    # Updates the scrollable region to make sure it fits the current order contents.
    summary_area.config(scrollregion=summary_area.bbox("all"))


def clear_order(table_frame, subtotal_label, delivery_fee_label, total_label, food_dropdown, quantity_dropdown, address_entry, order_type):

    """Clear all items and rest the current order fields."""

    answer = messagebox.askyesno("Clear Order", "Are you sure you want to clear the order?")
    if not answer:
        return

    current_order.clear()

    # This removes all order rows while keeping the table headings.
    for widget in table_frame.winfo_children():
        if int(widget.grid_info()["row"])>0:
            widget.destroy()
            
    # This resets the order input and disables the delivery address.
    food_dropdown.set("")
    quantity_dropdown.set("")
    address_entry.delete(0, tk.END)
    address_entry.config(state="disabled")

    order_type.set("")

    # This resets all order totals to zero.
    subtotal_label.config(text="Subtotal: $0.00")
    delivery_fee_label.config(text="Delivery Fee: $0.00")
    total_label.config(text="Total: $0.00")

def show_login_help():
    """Display instructions for logging into the program."""
    
    messagebox.showinfo(
                        "Login Help",
                          "Welcome to Nikita's Takeaway!\n\n"
                          "To Login in: \n\n"
                          "1. Enter your username.\n\n"
                          "2. Enter your password.\n\n"
                          "3. Click Continue.\n\n"
                          "4. If your login credentials are correct, the ordering window will open!\n\n"
                        )

    

def show_main_help():
    """Display instructions for using the main ordering window."""
    messagebox.showinfo(
                         "Help",
                         "Please read below:\n\n"
                         "1. Enter Customer Name.\n\n"
                         "2. Select either takeaway or Delivery. \n\n"
                         "3. If Delivery is selected, enter a valid delivery address.\n\n"
                         "4. Choose a food item and quantity from the dropdown list.\n\n"
                         "5. Click Add to Order to add the selected item to Your Order.\n\n"
                         "6. Repeat this step to add more items.\n\n"
                         "7. Check your order summary and total before continuing.\n\n"
                         "8. Click place order to confirm your order.\n\n"
                         "9. To remove all items and start your order again, click the clear order.\n\n"
                         "10. To view your receipt go to your file that stores the program and click Order receipt.txt.\n\n"
                         "11. Click Quit to close the ordering window and back to the login window."
                        ) 

def save_receipt(customer, order, address, subtotal, delivery_fee, total):
    """Save the completed order information to a text receipt file."""
    
    # Opens the receipt file and writes the completed order details.
    try:
        with open("Order Receipt.txt", mode="w", encoding="utf-8") as output_file:

            output_file.write("Nikita's Takeaway\n\n")
            output_file.write(f"Customer: {customer}\n")
            output_file.write(f"Order Type: {order}\n")

            # This includes the delivery address only for delivery orders.   
            if order == "Delivery":
                output_file.write(f"Address: {address}\n")

            output_file.write("\nOrder:\n")

            # Writes each item fron the current order to the receipt.
            for item in current_order:
                    output_file.write(item + "\n")

            output_file.write(f"\nSubtotal: ${subtotal:.2f}\n")
            output_file.write(f"Delivery Fee: ${delivery_fee:.2f}\n")
            output_file.write(f"Total: ${total:.2f}\n\n")
            
    # Handles errors that prevents the receipt from being saved.
    except OSError:
        messagebox.showerror("Receipt Error", "The Receipt could not be saved. Please try again.")
        return False

    return True


def place_order(order_type, address_entry, table_frame, subtotal_label,delivery_fee_label,
                total_label, food_dropdown, quantity_dropdown, customer_entry):
    """Validate and save the customer's completed order."""

    customer = customer_entry.get().strip()
    order = order_type.get()
    address = address_entry.get().strip()

    # Checks whether all required fields are empty.
    if customer == "" and len(current_order) ==0 and order == "":
        messagebox.showerror(
           "Error",
            "Please fill in all fields."
            )
        return
    
    # Checks that a customer name has been entered.
    if customer == "":
        messagebox.showerror("Error", "Please enter your name.")
        return 

    if len(current_order) ==0:
        messagebox.showerror("Error", "Before placing your order, please click 'Add to Order' to add at least one item.")
        return
    
    if order == "":
        messagebox.showerror("Error","Please select an order type.")
        return

    # This retrieves the displayed subtotal, delivery fee and total as numbers.
    subtotal= float(subtotal_label.cget("text").replace("Subtotal: $", ""))
    delivery_fee = float( delivery_fee_label.cget("text").replace("Delivery Fee: $", ""))
    total = float(total_label.cget("text").replace("Total: $",""))

    # Saves the completed order and checks whether the receipt was saved successfully. 
    receipt_saved = save_receipt(customer, order, address, subtotal, delivery_fee, total)

    if not receipt_saved:
        return
    
    
    messagebox.showinfo("Order Confirmed",f"Thank you, {customer}!\n\n"
                        f"Your {order} order has been placed successfully.\n"
                        f"Total: ${total:.2f}\n\n"
                        "Your receipt has been saved to Order receipt.txt.")

    reset_order(table_frame,subtotal_label,delivery_fee_label, total_label,
                food_dropdown, quantity_dropdown,address_entry,order_type, customer_entry)

def reset_order(table_frame, subtotal_label, delivery_fee_label,total_label,food_dropdown,quantity_dropdown,address_entry, order_type, customer_entry):
    """Reset the ordering window after an order is completed."""

    current_order.clear()

    # This removes all order rows while keeping the table headings.
    for widget in table_frame.winfo_children():
        if int(widget.grid_info()["row"])>0:
            widget.destroy()
   
    # Clears all customer and order input fields.
    customer_entry.delete(0, tk.END)
    food_dropdown.set("")
    quantity_dropdown.set("")
    address_entry.delete(0, tk.END)
    order_type.set("")

    address_entry.config(state="disabled")

    # Resets all order totals back to zero.
    subtotal_label.config(text="Subtotal: $0.00")
    delivery_fee_label.config(text="Delivery Fee: $0.00")
    total_label.config(text="Total: $0.00")
                 
   
def select_takeaway(address_entry):
    """Disable and clear the address field for takeaway orders."""
    
    address_entry.delete(0, tk.END)
    address_entry.config(state="disabled")

def select_delivery(address_entry):
    """Enable the address field for delivery orders."""
    
    address_entry.config(state="normal")

def quit_main_window(main_window):
    """Close the ordering window and return to the login window."""
    main_window.destroy()

    # Clears the login username and password.
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    # Shows the hidden login window again.
    root.deiconify() 
        

def open_main_window():
    """Create and display the main takeaway ordering window."""
    
    main_window = tk.Toplevel()
    
    # -----------------Main window styling 

    main_window.title("Nikita's Takeaway - Main Window")
    main_window.geometry ("800x650")
    main_window.resizable (False,False)
    main_window.configure (bg="#FFC067")

   # ------------------Main window widgets

    # Business name label
    business_name_label = tk.Label(main_window,text="Nikita's Takeaway",font=("Apple Chancery", 32, "bold"),bg="#2E7D32",fg="white")
    business_name_label.pack(fill="x", padx=40, pady=(20,15))
    
    # Top frame
    top_frame = tk.Frame(main_window, bg="#FFC067")
    top_frame.pack(fill="x", padx=40, pady=(5,10))
    
    # Left frame
    left_frame = tk.Frame(top_frame, bg="#FFC067")
    left_frame.pack(side="left", fill="both", expand=True)

    # Creates a fixed sized frame for the logo.
    right_frame = tk.Frame(top_frame, bg="#FFC067",width=200, height=180)
    right_frame.pack(side="right", padx=(25, 0), pady=(0,15))
    right_frame.pack_propagate(False)

    # Logo label
    logo_label = tk.Label(right_frame,image=Nikitas_logo,bg="white")
    logo_label.pack(expand=True)
    
    # Customer name label
    customer_label = tk.Label(left_frame, text="Customer Name:", font=("Georgia", 13), fg="#283593", bg="#FFF3E0")
    customer_label.pack(anchor="w")

    # Customer name entry box
    customer_entry = tk.Entry(left_frame, font=("Arial", 12), width=35)
    customer_entry.pack(anchor="w", pady=(5,10))

    # Order type label
    order_label = tk.Label(left_frame, text="Order Type:", font=("Georgia",13),  bg="#FFF3E0", fg="#283593")
    order_label.pack(anchor="w")

    # Variable to store the order type.
    order_type = tk.StringVar(value="")

    # Creates a frame to keep the order type radio buttons together.
    radio_frame= tk.Frame(left_frame, bg="#FFF3E0")
    radio_frame.pack(anchor="w", pady=(5,15))

    # Delivery address label
    address_label = tk.Label(left_frame, text="Delivery Address:", font=("Georgia", 13), bg="#FFF3E0",fg="#283593")
    address_label.pack(anchor="w")

    address_entry = tk.Entry(left_frame,font=("Georgia",13), width=35)
    address_entry.pack(anchor="w", pady=(5,15))
    address_entry.config(state="disabled")


    # Takeaway button
    takeaway_button = tk.Radiobutton (radio_frame, text="Takeaway",font=("Georgia",13), variable=order_type, value="Takeaway",bg="#FFF3E0",fg="#283593",
                                      command=lambda: select_takeaway(address_entry))

    takeaway_button.pack(side="left", padx=20)

    # Delivery button
    delivery_button = tk.Radiobutton(radio_frame, text="Delivery",font=("Georgia",13), variable=order_type, value="Delivery",bg="#FFF3E0",fg="#283593",
                                     command=lambda: select_delivery(address_entry))

    delivery_button.pack(side="left", padx=20)
 
    # Food and quantity frame
    item_frame = tk.Frame(left_frame,bg="#FFF3E0")
    item_frame.pack(anchor="w", pady=10)

    # Food item label
    food_label = tk.Label(item_frame, text="Food Item:", font=("Georgia",13),bg="#FFF3E0", fg="#283593")
    food_label.grid(row=0, column=0, padx=(0,8))
    
    # Food options list
    food_list = list(food_prices.keys())

    # Food dropdown menu
    food_dropdown = ttk.Combobox(item_frame, values=food_list, width=25, state="readonly")
    food_dropdown.grid(row=0, column=1, padx=(0, 20))
  

    # Quantity label
    quantity_label = tk.Label(item_frame, text="Quantity:", font=("Georgia",13), bg="#FFF3E0", fg="#283593")
    quantity_label.grid(row=0, column=2, padx=(0,8))

    
    # Quantity options
    quantity_list = [1,2,3,4,5,6,7,8,9,10]

    # Quantity dropdown
    quantity_dropdown = ttk.Combobox(item_frame, values=quantity_list, width=8, state="readonly")
    quantity_dropdown.grid(row=0, column=3)

    # Add to order button
    add_button = Button(left_frame, text="Add to Order",bg="#2E7D32",fg="white",activebackground="#1B5E20",activeforeground="white",relief="raised",
                        command=lambda: add_to_order(food_dropdown, quantity_dropdown,table_frame,summary_area,subtotal_label,delivery_fee_label,
                                                     total_label,order_type,address_entry, customer_entry))
    
    add_button.pack(anchor = "w", pady=(5,10))

    # Order summary label
    summary_label = tk.Label(main_window, text="Your Order", font=("Georgia", 13, "bold"),bg="#283593", fg="white")
    summary_label.pack(fill="x", padx=40, pady=(5,5))

    # Order summary frame
    summary_frame = tk.Frame(main_window, bg="#FFF3E0")
    summary_frame.pack(fill="x", padx=40)


    # Scroll frame 
    scroll_frame = tk.Frame(summary_frame, bg="white")
    scroll_frame.pack(fill="x")

    # Area that allows the order to scroll.
    summary_area = tk.Canvas(scroll_frame,height=130,bg="white")
    summary_area.pack(side="left",fill="both",expand=True)


    # This creates a scrollable area for displaying the summary order.
    summary_scrollbar = tk.Scrollbar(scroll_frame, orient="vertical",command=summary_area.yview)
    summary_scrollbar.pack(side="right", fill="y")

    summary_area.config(yscrollcommand=summary_scrollbar.set)

    # Table containing the order
    table_frame = tk.Frame(summary_area, bg="#FFF3E0", width=705)
    summary_area.create_window((0,0),window=table_frame,anchor="nw",width=705)
    
    # Item heading
    item_heading=tk.Label(table_frame,text="Item",font=("Georgia",13,"bold"),bg="#FFC067",fg="#283593",relief="solid",bd=1)
    item_heading.grid(row=0,column=0,sticky="nsew")

    # Quantity heading
    quantity_heading = tk.Label(table_frame,text="Qty",font=("Georgia", 13, "bold"),bg="#FFC067",fg="#283593",relief="solid",bd=1)
    quantity_heading.grid(row=0,column=1,sticky="nsew")
 
    # Price heading 
    price_heading = tk.Label(table_frame, text="Price", font=("", 13, "bold"), bg="#FFC067",fg="#283593", relief="solid", bd=1)
    price_heading.grid(row=0, column=2, sticky="nsew")

    # Sets column weights so the item column is wider than the quantity and price columns.
    table_frame.columnconfigure(0,weight=3)
    table_frame.columnconfigure(1,weight=1)
    table_frame.columnconfigure(2,weight=1)

    # -------------------- Order Totals

    totals_frame = tk.Frame(main_window, bg="#FFF3E0")
    totals_frame.pack(pady=8)

    subtotal_label = tk.Label(totals_frame, text="Subtotal: $0.00", bg="#FFF3E0",fg="#283593", font=("Georgia",13))
    subtotal_label.grid(row=0, column=0, padx=25)

    delivery_fee_label = tk.Label(totals_frame, text="Delivery Fee: $0.00", bg="#FFF4E6",fg="#283593", font=("Georgia", 13))
    delivery_fee_label.grid(row=0, column=1, padx=25)

    total_label = tk.Label(totals_frame, text="Total: $0.00", bg="#FFF3E0",fg="#283593",font=("Georgia",13,"bold"))
    total_label.grid(row=0, column=2, padx=25)

    # ------------------- Buttons

    # Bottom buttons frame
    bottom_frame = tk.Frame(main_window,  bg="#FFF3E0")
    bottom_frame.pack(pady=10)

    # Clear order button
    clear_button = Button(bottom_frame,text="Clear Order",bg="#2E7D32",fg="white",activebackground="#1B5E20",activeforeground="white",relief="raised",
                          command=lambda: clear_order(table_frame,subtotal_label,delivery_fee_label,
                                                      total_label,food_dropdown,quantity_dropdown,address_entry,order_type))

    clear_button.pack(side="left", padx=10)

    # Place order button
    place_order_button =Button(bottom_frame, text="Place Order",bg="#2E7D32",fg="white",activebackground="#1B5E20",activeforeground="white",
                               command=lambda: place_order(order_type,address_entry, table_frame, subtotal_label, delivery_fee_label,
                                                           total_label, food_dropdown, quantity_dropdown, customer_entry))
    place_order_button.pack(side="left",padx=10)

    # Help button for main window 
    help_button = Button(bottom_frame, text="Help",bg="#2E7D32",fg="white",activebackground="#1B5E20",activeforeground="white", command=show_main_help)
                            
    help_button.pack(side="left",padx=10)

    # Quit button for main window 
    quit_button = Button(bottom_frame, text="Quit",bg="#2E7D32",fg="white",activebackground="#1B5E20",activeforeground="white",
                         command=lambda: quit_main_window(main_window))
    
    quit_button.pack(side="left", padx=10)


def check_login():
    """Validate login credentials and open the main ordering window."""
    username= username_entry.get()
    password= password_entry.get()

    # Checking if both login fields are empty. 
    if username == "" and password == "":
        messagebox.showerror("Login Error", "Please fill in all fields.")
        return
 
    # Checking is username is empty.
    if username =="":
        messagebox.showerror("Login Error", "Please enter your username")
        return

    # Checking if password is empty.
    if password == "":
        messagebox.showerror("Login Error", "Please Enter your password")
        return

    # Checking if username contains spaces.
    if " " in username:
        messagebox.showerror("Login Error", "Username cannot contain spaces.")
        return

    # Checking if password contains spaces.
    if " " in password:
        messagebox.showerror("Login Error", "Password cannot contain spaces.")
        return
    
    # Checking that the username contains only letters and numbers.
    if not username.isalnum():
        messagebox.showerror("Login Error", "Your username can only contain letters and numbers.")
        return
    
    # Checking that the password contains only letters.
    if not password.isalpha():
        messagebox.showerror("Login Error", "Your password can only contain letters.")
        return

    # Checking the required username and password.
    if username == "hungry123" and password == "ilovetakeaways":
        root.withdraw()
        open_main_window()

    # Username is incorrect and password is correct.
    elif username != "hungry123" and password == "ilovetakeaways":
        messagebox.showerror( "Login Error", "You have entered your username incorrectly.")

    # Username is correct but password is incorrect 
    elif username == "hungry123" and password != "ilovetakeaways":
        messagebox.showerror("Login Error", "You have entered your password incorrectly.")
        
    # Both the username and password are incorrect.
    else:
        messagebox.showerror("Login Error", "You have entered incorrect username and password") 

# -------------- Login window


# Creates the main application window and load the logo.
root = tk.Tk()
Nikitas_logo= tk.PhotoImage(file="Nikitas_logo.png").subsample(3,3)


# -------------- Login window styling


# Configure the login window.
root.title ("Nikita's Takeaway")
root.geometry("600x400")
root.configure(bg="#FFC067")
root.resizable(False, False)


# Login window widgets


# Main heading
title_label = tk.Label(root, text="Nikita's Takeaway", font=("Apple Chancery", 28, "bold"), bg="#2E7D32", fg="white")
title_label.pack(pady=(70,10))

# Sub heading
sub_label = tk.Label(root, text="TAKEAWAY AND DELIVERY", font=("Georgia", 13),bg="#FFF3E0", fg="#1d4ed8")
sub_label.pack(pady=(0,35))

# Username field
username_entry = tk.Entry(root, font=("Georgia", 13), width=35,relief="solid", bd=1)
username_entry.pack(pady=(0,20))

# Password Field
password_entry = tk.Entry(root, font=("Georgia", 13), width=35,relief="solid", bd=1, show="*")
password_entry.pack(pady=(0,30))

# Buttons 
button_frame = tk.Frame(root, bg="#FFF3E0")
button_frame.pack(pady=20)

# Continue button
continue_btn = Button(button_frame, text="Continue",font=("Georgia", 13), bg="#2E7D32",fg="white",activebackground="#1B5E20",
                      activeforeground="white",relief="raised",command=check_login)

continue_btn.pack(side="left", padx=15)

# Help button for login window
help_btn = Button(button_frame, text="Help",font=("Georgia", 13),bg="#2E7D32",fg="white",
                  activebackground="#1B5E20",activeforeground="white",relief="raised", command=show_login_help)

help_btn.pack(side="left",padx=15)


# Quit button
quit_btn = Button(button_frame, text="Quit",font=("Georgia", 13),bg="#2E7D32",fg="white",activebackground="#1B5E20",
                  activeforeground="white",relief="raised",command=root.destroy)

quit_btn.pack(side="left", padx=15 )

# Start the application
root.mainloop()

