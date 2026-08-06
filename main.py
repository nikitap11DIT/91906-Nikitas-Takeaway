''' Nikita's Takout ( Takeaway food ordering system )
    Author: Nikita Patel
    Starting : 8th June
    Purpose: Creating A Takeaway ordering system'''

#---------------------------- RETRIEVE THE LIBRARIES

import tkinter as tk #imported the library of tkinter (shortens "tkinter" to "tk"
from tkinter import ttk, messagebox #Widgets that come with gui application
current_order = []
food_prices = {"Butter Chicken": 18.50, "Chicken Biryani": 16.00, "Garlic Naan":4.50, "Samosa":6.00, "Mango Lassi": 5.50}

#------------------------------ FUNCTIONS
    
def start_order():
    """Validate customer name and proceed to main window."""
    name = name_entry.get().strip()
    
    if name == "":
        messagebox.showerror("Error", "Please enter your name before contintuing.")
        return
    
    messagebox.showinfo("Success", f"Welcome, {name}! (Main window coming soon)")

def add_to_order(food_dropdown,quantity_dropdown,summary_box,
                 subtotal_label,delivery_fee_label,total_label,
                 order_type,address_entry,customer_entry):

    customer = customer_entry.get()
    food= food_dropdown.get()
    quantity = quantity_dropdown.get()
    order = order_type.get()
    address = address_entry.get()
    
    # Delivery address cannot start or end with spaces 
    if order == "Delivery" and address != address.strip():
        messagebox.showerror("Error", "Delivery address cannot start or end with spaces.")
        return

    # Remove spaces after validation 
    address = address.strip()
    
    # Delivery addres cannot be blank or contain only spaces 
    if order == "Delivery" and address == "":
        messagebox.showerror("Error", "Delivery address is required.")
        return

    # Customer name cannot be entered empty or spaces only 
    if customer.strip() =="":
        messagebox.showerror("Error", "Customer name is required.")
        return

    # Customer name caanot start or even end with spaces
    if customer != customer.strip():
        messagebox.showerror("Error", "Customer name cannot start or end with spaces.")
        return

    # Customer name cannot contain two sapces together
    if "  " in customer:
        messagebox.showerror("Error", "Please use only one space between names.")
        return

    #Remove spaces after validation
    customer = customer.strip()

    if food =="" and quantity == "" and order =="":
        messagebox.showerror( "Error", "Before clicking 'Add to Order', please fill in all fields.")
        return 

    if food =="":
        messagebox.showerror("Error","Please select a food item.")
        return

    if quantity =="":
        messagebox.showerror("Error","Please select a quantity.")
        return

    if order_type.get() == "":
        messagebox.showerror("Error","Please select Takeaway or Delivery.")
        return

    price = food_prices[food]
    item_total = price * int(quantity)
    order_line = f"{food} x {quantity} - ${item_total:.2f}"
    current_order.append(order_line)
    
    food_dropdown.set("")
    quantity_dropdown.set("")
    
    summary_box.config(state="normal")
    summary_box.delete("1.0", tk.END)

    for item in current_order:
        summary_box.insert(tk.END, item + "\n")

    subtotal = 0

    for item in current_order:
        parts = item.split("$")
        subtotal += float(parts[1])

    if order_type.get() == "Delivery":
        delivery_fee = 5.00
    else:
        delivery_fee = 0.00

    total = subtotal + delivery_fee

    summary_box.insert(tk.END, "\n..............................................\n")
    summary_box.insert(tk.END, f"Subtotal: ${subtotal:.2f}\n")

    if delivery_fee > 0:
        summary_box.insert(tk.END, f"Delivery Fee: ${delivery_fee:.2f}\n")

    summary_box.insert(tk.END, f"Total: ${total:.2f}")
    summary_box.config(state="disabled")

    subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
    delivery_fee_label.config(text=f"Delivery Fee: ${delivery_fee:.2f}")
    total_label.config(text=f"Total: ${total:.2f}")

def clear_order(summary_box, subtotal_label, delivery_fee_label,total_label,food_dropdown,quantity_dropdown,address_entry, order_type):

    answer = messagebox.askyesno("Clear Order", "Are you sure you want to clear the order?")
    if not answer:
        return

    current_order.clear()
    
    summary_box.config(state="normal")
    summary_box.delete("1.0",tk.END)
    summary_box.config(state="disabled")

    food_dropdown.set("")
    quantity_dropdown.set("")
    address_entry.delete(0, tk.END)

    order_type.set("")
    
    subtotal_label.config(text="Subtotal: $0.00")
    delivery_fee_label.config(text="Delivery Fee: $0.00")
    total_label.config(text="Total: $0.00")

def show_login_help():
    messagebox.showinfo(
                        "Login Help",
                          "Welcome to Nikita's Takeaway!\n\n"
                          "To Login In: \n\n"
                          "1.Enter your username.\n\n"
                          "2.Enter your password.\n\n"
                          "3.Click Continue.\n\n"
                          "4.If your login credentials are correct, the ordering window will open!\n\n"
                          )
    

      

def show_main_help():
    messagebox.showinfo(
                         "Help",
                         "Please read below:\n\n"
                         "1.Enter Customer Name.\n\n"
                         "2.Select either takeeaway or Delivery. \n\n"
                         "3.If Delivery is selected, enter a valid delivery address.\n\n"
                         "4.Choose a food item and quantity from the dropw down list.\n\n"
                         "5.Click Add to Order to add the selected item to Your Oder.\n\n"
                         "6.Repeat this step to add more items.\n\n"
                         "7.Check your order summary and total before continuing.\n\n"
                         "8.Click place order to confirm your order.\n\n"
                         "9.To remove all items and start your order again, click the clear order.\n\n"
                         "10. Click Quit to close the ordering window wihtout placing an order."
                        ) 

def place_order(order_type, address_entry, summary_box, subtotal_label,delivery_fee_label,
                total_label, food_dropdown, quantity_dropdown, customer_entry):

    customer = customer_entry.get().strip()
    order = order_type.get()

    #If all fields are empty then send this error message
    if customer == "" and len(current_order) ==0 and order == "":
        messagebox.showerror(
            "Error",
            "Please fill in all fields."
            )
        return
    
    #Check if customer name is entered
    if customer == "":
        messagebox.showerror("Error", "Please enter your name.")
        return 

    if len(current_order) ==0:
        messagebox.showerror("Error", "Before placing your order, please click 'Add to Order' to add at least one item.")
        return
    
    if order_type.get() == "":
        messagebox.showerror("Error","Please select an order type.")
        return
    
    messagebox.showinfo("Success",
                        "Your order has been placed"
                        )

    reset_order(summary_box,subtotal_label,delivery_fee_label, total_label,
                food_dropdown, quantity_dropdown,address_entry,order_type, customer_entry)

def reset_order(summary_box, subtotal_label, delivery_fee_label,total_label,food_dropdown,quantity_dropdown,address_entry, order_type, customer_entry):

    current_order.clear()
    
    summary_box.config(state="normal")
    summary_box.delete("1.0",tk.END)
    summary_box.config(state="disabled")

    customer_entry.delete(0, tk.END)

    food_dropdown.set("")
    quantity_dropdown.set("")
    address_entry.delete(0, tk.END)

    order_type.set("")

    address_entry.config(state="disabled")
    
    subtotal_label.config(text="Subtotal: $0.00")
    delivery_fee_label.config(text="Delivery Fee: $0.00")
    total_label.config(text="Total: $0.00")
                 
   
def select_takeaway(address_entry):
    address_entry.delete(0, tk.END)
    address_entry.config(state="disabled")

def select_delivery(address_entry):
    address_entry.config(state="normal")

def quit_main_window(main_window):
    main_window.destroy()

    #Clear the Login Username and password
    username_entry.delete(0, tk.END)
    password_entry. delete(0, tk.END)
    
    root.deiconify() # This will show the hidden login window again
        

def open_main_window():

    main_window = tk.Toplevel()
    
#------------------------------ Main window - STYLING 

    main_window.title("Nikita's Takeaway - Main Window")
    main_window.geometry ("800x600")
    main_window.resizable (False,False)
    main_window.configure (bg="white")

#------------------------------ Main window - WIDGETS

    #Title Label
    title_label = tk.Label( main_window, text="Nikita's Takeaway", font=("Arial", 28, "bold"), bg="pink",fg="black")
    title_label.pack(pady=(20,15))

    #Customer Name Label
    customer_label = tk.Label(main_window, text="Customer Name:", font=("Arial", 12), fg="black", bg="pink")
    customer_label.pack()

    #Customer Name Entry Box
    customer_entry = tk.Entry(main_window, font=("Arial", 12), width=35)
    customer_entry.pack(pady=(5,10))

    #Order Type Label
    order_label = tk.Label(main_window, text="Order Type:", font=("Arial",12), bg="pink")
    order_label.pack()


    #Variable to store the order type
    order_type = tk.StringVar(value="")

    #Frame to keep the radio buttons together
    radio_frame= tk.Frame(main_window, bg="light pink")
    radio_frame.pack(pady=(5,10))

    #Takeaway button
    takeaway_button = tk.Radiobutton (radio_frame, text="Takeaway", variable=order_type, value="Takeaway",bg="pink", command=lambda: select_takeaway(address_entry))
    takeaway_button.pack(side="left", padx=20)

    #Delivery button
    delivery_button = tk.Radiobutton(radio_frame, text="Delivery", variable=order_type, value="Delivery",bg="pink", command=lambda: select_delivery(address_entry))
    delivery_button.pack(side="left", padx=20)

    #Delivery Address Label
    address_label = tk.Label(main_window, text="Delivery Address:", font=("arial", 12), bg="pink")
    address_label.pack()

    #Delivery Address Entry Box
    address_entry = tk.Entry(main_window,font=("Arial",12), width=35)
    address_entry.pack(pady=(5,10))
    address_entry.config(state="disabled")

    #Food and Quantity Frame
    item_frame = tk.Frame(main_window, bg="white")
    item_frame.pack(pady=10)

    #Food Item label
    food_label = tk.Label(item_frame, text="Food Item:", font=("Arial",12), bg="pink")
    food_label.grid(row=0, column=0, padx=10)
    
    #Food options list
    food_list = ["Butter Chicken", "Chicken Biryani", "Garlic Naan", "Samosa", "Mango Lassi"]

    #Food dropdown menu
    food_dropdown = ttk.Combobox(item_frame, values=food_list, width=25, state="readonly")
    food_dropdown.grid(row=0, column=1, padx=10)
  

    #Quantity Label
    quantity_label = tk.Label(item_frame, text="Quantity:", font=("Arial", 12), bg="pink")
    quantity_label.grid(row=0, column=2, padx=10)


    #Quantity options
    quantity_list = [1,2,3,4,5,6,7,8,9,10]

    #Quantity dropdown
    quantity_dropdown = ttk.Combobox(item_frame, values=quantity_list, width=8, state="readonly")
    quantity_dropdown.grid(row=0, column=3, padx=10)
 

    #Add to order button
    add_button = tk.Button(main_window, text="Add to Order", width=15, command=lambda: add_to_order(food_dropdown, quantity_dropdown,summary_box,subtotal_label,delivery_fee_label,
                                                                                                    total_label,order_type,address_entry, customer_entry))
    
    add_button.pack(pady=(5,10))

    #Order Summary Label
    summary_label = tk.Label(main_window, text="Your Order", font=("Arial", 14, "bold"),bg="pink")
    summary_label.pack()

    summary_frame = tk.Frame(main_window)
    summary_frame.pack(pady=(5,15))

    scrollbar = tk.Scrollbar(summary_frame)

    summary_box = tk.Text(summary_frame, width=60, height=8, font=("Arial",11), yscrollcommand=scrollbar.set)
    scrollbar.config(command=summary_box.yview)

    scrollbar.pack(side="right", fill="y")
    summary_box.pack(side="left")

    summary_box.config(state="disabled")

    totals_frame = tk.Frame(main_window, bg="white")
    totals_frame.pack(pady=10)

    subtotal_label = tk.Label(totals_frame, text="Subtotal: $0.00", bg="white", font=("Arial",11))
    subtotal_label.grid(row=0, column=0, padx=30)

    delivery_fee_label = tk.Label(totals_frame, text="Delivery Fee: $0.00", bg="white", font=("Arial", 11))
    delivery_fee_label.grid(row=0, column=1, padx=30)

    total_label = tk.Label(totals_frame, text="Total: $0.00", bg="white",font=("Arial",11,"bold"))
    total_label.grid(row=0, column=2, padx=30)

    #Bottom buttons frame
    bottom_frame = tk.Frame(main_window, bg="white")
    bottom_frame.pack(pady=20)

    #Clear order button
    clear_button = tk.Button(bottom_frame,text="Clear Order",width=12, command=lambda: clear_order(summary_box,subtotal_label,delivery_fee_label,total_label,food_dropdown, quantity_dropdown,address_entry,order_type))
    clear_button.pack(side="left", padx=10)

    #Place order button
    place_order_button = tk.Button(bottom_frame, text="Place Order", width=12, command=lambda: place_order(order_type,address_entry, summary_box, subtotal_label, delivery_fee_label, total_label, food_dropdown, quantity_dropdown, customer_entry))
    place_order_button.pack(side="left",padx=10)

    #Help Button for Main Window 
    help_button = tk.Button(bottom_frame, text="Help",width=12, command=show_main_help
                            )
    help_button.pack(side="left",padx=10)

    #Quit Button for main Window 
    quit_button = tk.Button(bottom_frame, text="Quit", width=12, command=lambda: quit_main_window(main_window))
    quit_button.pack(side="left", padx=10)


def check_login():
    username= username_entry.get()
    password= password_entry.get()

    # checking if both fields are empty 
    if username == "" and password == "":
        messagebox.showerror("Login Error", "Please fill in all fields.")
        return
 
    #Checking is username is empty
    if username =="":
        messagebox.showerror("Login Error", "Please enter your username")
        return

    # Check if password is empty
    if password == "":
        messagebox.showerror("Login Error", "Please Enter your password")
        return

    # Check if username contains spaces

    if " " in username:
        messagebox.showerror("Login Error", "Username cannot contain spaces.")
        return

    # Check if password contains spaces 

    if " " in password:
        messagebox.showerror("Login Error", "Password cannot contain spaces.")
        return 

    # The requierd username and password
    if username == "hungry123" and password == "ilovetakeaways":
        root.withdraw()
        open_main_window()

    # Username is incorrect and password is correct
    elif username != "hungry123" and password == "ilovetakeaways":
        messagebox.showerror( "Login Error", "You have entered your username incorrectly.")

    elif username == "hungry123" and password != "ilovetakeaways":
        messagebox.showerror("Login Error", "You have entered you password incorrectly.")
        

    else:
        messagebox.showerror("Login Error", " You have entered incorrect username and password") 

# ------------------------------- Login Window
root = tk.Tk()

# -------------------------------- Login Window - STYLING 

root.title ("Nikita's Takeaway")
root.geometry("600x400")
root.configure(bg="white")
root.resizable(False, False)

# --------------------------------- Login window - WIDGETS

# Main Heading
title_label = tk.Label(root, text="Nikita's Takeaway", font=("Poppins", 28, "bold"), bg="pink", fg="#1d4ed8")
title_label.pack(pady=(70,10))

# Sub heading
sub_label = tk.Label(root, text="TAKEAWAY AND DELIVERY", font=("Poppins", 10),bg="pink", fg="#93c5fd")
sub_label.pack(pady=(0,35))

# Username field
username_entry = tk.Entry(root, font=("Poppins", 12), width=35,relief="solid", bd=1)
username_entry.pack(pady=(0,20))

# Password Field
password_entry = tk.Entry(root, font=("Poppins", 12), width=35,relief="solid", bd=1, show="*")
password_entry.pack(pady=(0,30))

# Buttons----------------------------
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

# Continue button
continue_btn = tk.Button(button_frame, text="Continue", width=10, command=check_login)
continue_btn.pack(side="left", padx=15)

# Help button for login window
help_btn = tk.Button(button_frame, text="Help", width=10, command=show_login_help)
help_btn.pack(side="left",padx=15)


#Quit Button
quit_btn = tk.Button(button_frame, text="Quit", width=10, command=root.destroy)
quit_btn.pack(side="left", padx=15 )



# -------------------Mainloop
root.mainloop()


