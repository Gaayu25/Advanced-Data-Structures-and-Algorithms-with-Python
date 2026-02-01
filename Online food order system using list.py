menu = ["Pizza", "Burger", "Pasta", "Sandwich", "Coffee"]
prices = [150, 80, 120, 60, 40]
cart = []

def show_menu():
    print("\n------ MENU ------")
    for i in range(len(menu)):
        print(f"{i+1}. {menu[i]} - ₹{prices[i]}")
    print("------------------")

def add_to_cart():
    show_menu()
    choice = int(input("Enter item number to add: ")) - 1
    if 0 <= choice < len(menu):
        cart.append(choice)
        print(menu[choice], "added to cart!\n")
    else:
        print("Invalid choice!\n")

def view_cart():
    print("\n------ CART ------")
    total = 0
    for i in cart:
        print(menu[i], "- ₹", prices[i])
        total += prices[i]
    print("Total Bill: ₹", total)
    print("------------------\n")

def remove_item():
    view_cart()
    idx = int(input("Enter cart item number to remove: ")) - 1
    if 0 <= idx < len(cart):
        removed = menu[cart[idx]]
        cart.pop(idx)
        print(removed, "removed!\n")
    else:
        print("Invalid choice!\n")

def checkout():
    view_cart()
    print("Order Placed! Thank you 😊")
    exit()

while True:
    print("1. Show Menu\n2. Add Item\n3. View Cart\n4. Remove Item\n5. Checkout")
    option = int(input("Choose option: "))

    if option == 1: show_menu()
    elif option == 2: add_to_cart()
    elif option == 3: view_cart()
    elif option == 4: remove_item()
    elif option == 5: checkout()
    else: print("Invalid option!")
