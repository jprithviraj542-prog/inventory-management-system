import json
import os

FILE = "inventory.json"
LOW_STOCK_LIMIT = 5
items = []

def load_items():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            items.extend(json.load(f))

def save_items():
    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)

def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None

def get_number(message, number_type=int):
    while True:
        try:
            value = number_type(input(message))
            if value < 0:
                print("Value cannot be negative")
            else:
                return value
        except ValueError:
            print("Please enter a valid number")

def add_item():
    item_id = input("Enter item ID: ")
    if find_item(item_id):
        print("This ID already exists!")
        return
    name = input("Enter item name: ")
    quantity = get_number("Enter quantity: ")
    price = get_number("Enter price per unit: ", float)
    items.append({"id": item_id, "name": name,
                  "quantity": quantity, "price": price})
    save_items()
    print("Item added successfully!")

def view_items():
    if not items:
        print("Inventory is empty.")
        return
    print("\nID | Name | Quantity | Price | Value")
    for item in items:
        value = item["quantity"] * item["price"]
        print(item["id"], "|", item["name"], "|", item["quantity"], "|",
              item["price"], "|", round(value, 2))

def search_item():
    keyword = input("Enter item name to search: ").lower()
    found = False
    for item in items:
        if keyword in item["name"].lower():
            print(item["id"], "|", item["name"], "|",
                  item["quantity"], "|", item["price"])
            found = True
    if not found:
        print("No item found.")

def add_stock():
    item = find_item(input("Enter item ID: "))
    if item is None:
        print("Item not found.")
        return
    qty = get_number("Quantity to add: ")
    item["quantity"] += qty
    save_items()
    print("Stock updated! New quantity:", item["quantity"])

def sell_item():
    item = find_item(input("Enter item ID: "))
    if item is None:
        print("Item not found.")
        return
    qty = get_number("Quantity to sell: ")
    if qty > item["quantity"]:
        print("Not enough stock! Available:", item["quantity"])
        return
    item["quantity"] -= qty
    save_items()
    print("Sold! Bill amount:", round(qty * item["price"], 2))
    if item["quantity"] <= LOW_STOCK_LIMIT:
        print("WARNING: Low stock for", item["name"])

def low_stock_report():
    low = [i for i in items if i["quantity"] <= LOW_STOCK_LIMIT]
    if not low:
        print("No low stock items.")
        return
    print("\n--- Low Stock Items ---")
    for item in low:
        print(item["id"], "|", item["name"], "| Qty:", item["quantity"])

def total_value():
    total = sum(i["quantity"] * i["price"] for i in items)
    print("Total inventory value: Rs.", round(total, 2))

def delete_item():
    item = find_item(input("Enter item ID to delete: "))
    if item is None:
        print("Item not found.")
    else:
        items.remove(item)
        save_items()
        print("Item deleted!")

load_items()

while True:
    print("\n--- Inventory Menu ---")
    print("1. Add Item")
    print("2. View Items")
    print("3. Search Item")
    print("4. Add Stock")
    print("5. Sell Item")
    print("6. Low Stock Report")
    print("7. Total Inventory Value")
    print("8. Delete Item")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_item()
    elif choice == "2":
        view_items()
    elif choice == "3":
        search_item()
    elif choice == "4":
        add_stock()
    elif choice == "5":
        sell_item()
    elif choice == "6":
        low_stock_report()
    elif choice == "7":
        total_value()
    elif choice == "8":
        delete_item()
    elif choice == "9":
        print("Goodbye!")
        break
    else:
        print("Invalid choice")