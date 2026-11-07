# ==============================================================
#            TECHHUB MOBILE ACCESSORIES BILLING SYSTEM
#                     MINI PROJECT - PART 1 & 2
#
# Developed Using Python
# Concepts Used:
# • Functions
# • Dictionary
# • Loops
# • Exception Handling
# • File Handling
# • Date & Time
# • Random Module
# ==============================================================

import random
import sys
from datetime import datetime

# Set console output encoding to UTF-8 for Indian Rupee symbol (₹) on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# -------------------- CONSTANTS --------------------

GST_RATE = 18          # GST Percentage
DISCOUNT_RATE = 5      # Discount Percentage

# ---------------- PRODUCT CATALOGUE ----------------

# Dictionary Format:
# Product ID : [Product Name, Price]

products = {
    1: ["Phone Case", 299],
    2: ["Fast Charger", 899],
    3: ["USB Cable", 199],
    4: ["Wireless Earbuds", 2499],
    5: ["Power Bank", 1599],
    6: ["Screen Protector", 249],
    7: ["Bluetooth Speaker", 1899],
    8: ["Memory Card 64GB", 799]
}

# ---------------- INPUT VALIDATION FUNCTIONS ----------------


def get_customer_name():

    while True:

        name = input("Enter Customer Name : ").strip()

        if name == "":
            print("Customer name cannot be empty.\n")

        elif not all(ch.isalpha() or ch.isspace() for ch in name):
            print("Name should contain only alphabets.\n")

        else:
            return name.title()


def get_positive_integer(message):

    while True:

        try:

            number = int(input(message))

            if number <= 0:
                print("Please enter a value greater than zero.\n")

            else:
                return number

        except ValueError:
            print("Invalid input! Enter a whole number.\n")


def get_choice(message, minimum, maximum):

    while True:

        try:

            choice = int(input(message))

            if minimum <= choice <= maximum:
                return choice

            else:
                print("Choose between", minimum, "and", maximum)

        except ValueError:
            print("Invalid choice.\n")


# ---------------- DISPLAY PRODUCT MENU ----------------


def display_products():

    print("\n")
    print("=" * 60)
    print("               AVAILABLE PRODUCTS")
    print("=" * 60)

    print("{:<8}{:<28}{:<10}".format(
        "ID", "Product", "Price (₹)"
    ))

    print("-" * 60)

    for product_id in products:

        print("{:<8}{:<28}₹{:<10}".format(
            product_id,
            products[product_id][0],
            products[product_id][1]
        ))

    print("=" * 60)


# ---------------- PAYMENT METHOD ----------------


def payment_method():

    while True:

        print("\nChoose Payment Method")

        print("1. Cash")
        print("2. UPI")
        print("3. Debit/Credit Card")

        option = input("Enter Choice : ")

        if option == "1":
            return "Cash"

        elif option == "2":
            return "UPI"

        elif option == "3":
            return "Card"

        else:
            print("Invalid Choice.\n")


# ---------------- ADD PRODUCTS ----------------


def add_products():

    cart = []

    while True:

        display_products()

        product_id = get_choice(
            "Enter Product ID : ",
            1,
            len(products)
        )

        quantity = get_positive_integer(
            "Enter Quantity : "
        )

        name = products[product_id][0]
        price = products[product_id][1]
        total = quantity * price

        cart.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": total
        })

        while True:

            choice = input(
                "\nAdd another product? (Y/N) : "
            ).upper()

            if choice == "Y":
                break

            elif choice == "N":
                return cart

            else:
                print("Enter Y or N only.")


# ---------------- CALCULATE BILL ----------------


def calculate_bill(cart):

    subtotal = 0

    for item in cart:
        subtotal += item["total"]

    if subtotal >= 5000:
        discount = subtotal * DISCOUNT_RATE / 100
    else:
        discount = 0

    taxable_amount = subtotal - discount

    gst = taxable_amount * GST_RATE / 100

    grand_total = taxable_amount + gst

    return subtotal, discount, gst, grand_total


# ---------------- BILL GENERATION ----------------


def print_bill(bill_number, current_date, current_time, customer_name, payment, cart, subtotal, discount, gst, grand_total):

    print("\n")
    print("=" * 75)
    print("                 TECHHUB MOBILE ACCESSORIES STORE")
    print("                          CUSTOMER BILL")
    print("=" * 75)

    print(f"Bill Number      : {bill_number}")
    print(f"Date             : {current_date}")
    print(f"Time             : {current_time}")
    print(f"Customer Name    : {customer_name}")
    print(f"Payment Method   : {payment}")

    print("-" * 75)

    print("{:<5}{:<25}{:>10}{:>15}{:>15}".format(
        "No",
        "Product",
        "Qty",
        "Price",
        "Total"
    ))

    print("-" * 75)

    for i, item in enumerate(cart, start=1):

        print("{:<5}{:<25}{:>10}{:>15.2f}{:>15.2f}".format(
            i,
            item["name"],
            item["quantity"],
            item["price"],
            item["total"]
        ))

    print("-" * 75)

    print("{:>60} ₹{:>10.2f}".format("Subtotal :", subtotal))
    print("{:>60} ₹{:>10.2f}".format("Discount :", discount))
    print("{:>60} ₹{:>10.2f}".format(f"GST ({GST_RATE}%) :", gst))
    print("{:>60} ₹{:>10.2f}".format("Grand Total :", grand_total))

    print("=" * 75)
    print("              Thank You For Shopping With Us!")
    print("                    Visit Again!")
    print("=" * 75)


def save_bill(bill_number, current_date, current_time, customer_name, payment, cart, subtotal, discount, gst, grand_total):

    filename = f"receipt_{bill_number}.txt"

    with open(filename, "w", encoding="utf-8") as file:

        file.write("=" * 75 + "\n")
        file.write("TECHHUB MOBILE ACCESSORIES STORE\n")
        file.write("CUSTOMER BILL\n")
        file.write("=" * 75 + "\n\n")

        file.write(f"Bill Number    : {bill_number}\n")
        file.write(f"Date           : {current_date}\n")
        file.write(f"Time           : {current_time}\n")
        file.write(f"Customer Name  : {customer_name}\n")
        file.write(f"Payment Method : {payment}\n\n")

        file.write("{:<5}{:<25}{:>10}{:>15}{:>15}\n".format(
            "No",
            "Product",
            "Qty",
            "Price",
            "Total"
        ))

        file.write("-" * 75 + "\n")

        for i, item in enumerate(cart, start=1):

            file.write("{:<5}{:<25}{:>10}{:>15.2f}{:>15.2f}\n".format(
                i,
                item["name"],
                item["quantity"],
                item["price"],
                item["total"]
            ))

        file.write("-" * 75 + "\n")

        file.write("{:>60} ₹{:>10.2f}\n".format("Subtotal :", subtotal))
        file.write("{:>60} ₹{:>10.2f}\n".format("Discount :", discount))
        file.write("{:>60} ₹{:>10.2f}\n".format(f"GST ({GST_RATE}%) :", gst))
        file.write("{:>60} ₹{:>10.2f}\n".format("Grand Total :", grand_total))

        file.write("=" * 75 + "\n")
        file.write("Thank You For Shopping With Us!\n")
        file.write("Visit Again!\n")
        file.write("=" * 75 + "\n")

    print(f"\nReceipt has been saved successfully as '{filename}'")


# ---------------- MAIN EXECUTION ----------------

def main():
    print("=" * 65)
    print("        TECHHUB MOBILE ACCESSORIES STORE")
    print("              BILLING SYSTEM")
    print("=" * 65)

    customer_name = get_customer_name()
    cart = add_products()
    subtotal, discount, gst, grand_total = calculate_bill(cart)
    payment = payment_method()

    bill_number = random.randint(1000, 9999)
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")

    print_bill(bill_number, current_date, current_time, customer_name, payment, cart, subtotal, discount, gst, grand_total)
    save_bill(bill_number, current_date, current_time, customer_name, payment, cart, subtotal, discount, gst, grand_total)

if __name__ == "__main__":
    main()
