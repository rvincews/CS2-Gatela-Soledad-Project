#Hezekiah C. Gatela & Rile Vince W. Soledad
#Fresh Tracker!
 
import os
from datetime import datetime, timedelta
from common_items import SHELF_LIFE_DAYS, REFRIGERATED
 
DATA_FILE = "fresh_tracker_data.txt"
 
expiryProducts = []
expiryProductsDate = []
expiredProducts = []
expiredProductsDate = []
groceryList = []
 
 
def save_data():
    # saves everything to the text file
    f = open(DATA_FILE, "w")
    f.write("EXPIRY\n")
    for i in range(len(expiryProducts)):
        f.write(expiryProducts[i] + "|" + expiryProductsDate[i] + "\n")
    f.write("EXPIRED\n")
    for i in range(len(expiredProducts)):
        f.write(expiredProducts[i] + "|" + expiredProductsDate[i] + "\n")
    f.write("GROCERY\n")
    for i in range(len(groceryList)):
        f.write(groceryList[i] + "\n")
    f.close()
 
 
def load_data():
    # loads saved data from the text file when the program starts
    if not os.path.exists(DATA_FILE):
        return
    f = open(DATA_FILE, "r")
    lines = f.readlines()
    f.close()
    section = ""
    for line in lines:
        line = line.strip()
        if line == "EXPIRY":
            section = "expiry"
        elif line == "EXPIRED":
            section = "expired"
        elif line == "GROCERY":
            section = "grocery"
        elif line != "" and "|" in line and section == "expiry":
            parts = line.split("|")
            expiryProducts.append(parts[0])
            expiryProductsDate.append(parts[1])
        elif line != "" and "|" in line and section == "expired":
            parts = line.split("|")
            expiredProducts.append(parts[0])
            expiredProductsDate.append(parts[1])
        elif line != "" and section == "grocery":
            groceryList.append(line)
 
 
def get_valid_manual_expiry_date():
    # asks the user to type in an expiry date and checks if its valid
    attempts = 0
    while attempts < 3:
        expiry_date = input("Enter the expiry date (YYYY-MM-DD): ")
        try:
            expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            days_diff = (expiry_date_obj - today).days
            if days_diff > 365:
                years_diff = days_diff / 365.25
                confirm = input("WARNING: This item expires in " + str(round(years_diff, 1)) + " years. Is this correct? (y/n): ")
                if confirm.startswith("y"):
                    return expiry_date
                else:
                    print("Please enter a different date.")
                    attempts += 1
                    continue
            return expiry_date
        except ValueError:
            attempts += 1
            print("ERROR: Invalid date format. Please use YYYY-MM-DD.")
            if attempts < 3:
                print("Please try again (" + str(3 - attempts) + " attempts left).")
    print("Too many invalid entries. Returning to Expiry Tracker menu.")
    return None
 
 
def get_expiry_date_from_user(productName):
    name_lower = productName.lower().strip()
    attempts = 0
    answer = ""
    while attempts < 3:
        answer = input("Would you like an estimate based on typical shelf life? (y/n): ").lower().strip()
        if answer.startswith("y") or answer.startswith("n"):
            break
        attempts += 1
        print("ERROR: Please enter 'y' for yes or 'n' for no.")
        if attempts < 3:
            print("Please try again (" + str(3 - attempts) + " attempts left).")
    if attempts == 3:
        print("Too many invalid entries. Proceeding to manual entry.")
        return get_valid_manual_expiry_date()
 
    if answer.startswith("y"):
        if name_lower in SHELF_LIFE_DAYS:
            shelf_days = SHELF_LIFE_DAYS[name_lower]
            if name_lower in REFRIGERATED:
                attempts = 0
                refrigerate = "n"
                while attempts < 3:
                    refrigerate = input("Will this item be refrigerated? (y/n): ").lower().strip()
                    if refrigerate.startswith("y") or refrigerate.startswith("n"):
                        break
                    attempts += 1
                    print("ERROR: Please enter 'y' for yes or 'n' for no.")
                    if attempts < 3:
                        print("Please try again (" + str(3 - attempts) + " attempts left).")
                if refrigerate.startswith("y"):
                    shelf_days = int(shelf_days * 1.5)
                    print("INFO: Refrigerated items last longer; adjusting estimated life to " + str(shelf_days) + " days.")
            estimated_date = (datetime.now().date() + timedelta(days=shelf_days)).strftime("%Y-%m-%d")
            print("ESTIMATED DATE: Estimated expiry date for " + productName + " is " + estimated_date + ".")
            return estimated_date
        else:
            print("ERROR: No shelf life data for this item. Please enter manually.")
            return get_valid_manual_expiry_date()
    return get_valid_manual_expiry_date()
 
 
def move_expired_items_to_display():
    today = datetime.now().date()
    i = 0
    while i < len(expiryProducts):
        expiryDateObj = datetime.strptime(expiryProductsDate[i], "%Y-%m-%d").date()
        if expiryDateObj < today:
            expiredProducts.append(expiryProducts[i])
            expiredProductsDate.append(expiryProductsDate[i])
            expiryProducts.pop(i)
            expiryProductsDate.pop(i)
        else:
            i += 1
    save_data()
 
 
def expiryTracker():
    while True:
        dateNow = datetime.now().date()
        print("\n=== Expiry Tracker ===")
        print("Date Today: " + str(dateNow) + "\n")
 
        move_expired_items_to_display()
 
        if len(expiryProducts) == 0 and len(expiredProducts) == 0:
            print("No products in the expiry tracker.")
            print("\nAdd Items [1]")
            print("Back to Main Menu [2]")
            choice = input("Choose an option: ")
            if choice == "1":
                productName = input("Enter the product name: ")
                expiryDate = get_expiry_date_from_user(productName)
                if expiryDate:
                    expiryProducts.append(productName)
                    expiryProductsDate.append(expiryDate)
                    print("ADDED " + productName + " with expiry date " + expiryDate + " to the tracker.")
                    save_data()
            elif choice == "2":
                mainMenu()
                return
            else:
                print("ERROR: Invalid choice. Please try again.")
        else:
            if len(expiryProducts) > 0:
                print("Fresh Products:")
                for i in range(len(expiryProducts)):
                    expiryDateObj = datetime.strptime(expiryProductsDate[i], "%Y-%m-%d").date()
                    daysLeft = (expiryDateObj - dateNow).days
                    if daysLeft > 3:
                        status = "OK"
                    else:
                        status = "WARNING"
                    print(status + " " + str(i + 1) + ". " + expiryProducts[i] + " - Expiry: " + expiryProductsDate[i] + " (" + str(daysLeft) + " days)")
 
            if len(expiredProducts) > 0:
                print("\nExpired Products:")
                for i in range(len(expiredProducts)):
                    expiryDateObj = datetime.strptime(expiredProductsDate[i], "%Y-%m-%d").date()
                    daysExpired = (dateNow - expiryDateObj).days
                    print("EXPIRED " + str(i + 1) + ". " + expiredProducts[i] + " - Expired: " + expiredProductsDate[i] + " (" + str(daysExpired) + " days ago)")
 
            print("\nAdd Items [1]")
            print("Remove Item [2]")
            print("Back to Main Menu [3]")
            choice = input("Choose an option: ")
 
            if choice == "1":
                productName = input("Enter the product name: ")
                expiryDate = get_expiry_date_from_user(productName)
                if expiryDate:
                    expiryProducts.append(productName)
                    expiryProductsDate.append(expiryDate)
                    print("ADDED " + productName + " with expiry date " + expiryDate + " to the tracker.")
                    save_data()
            elif choice == "2":
                try:
                    itemNum = int(input("Enter item number to remove (use Fresh or Expired number): ")) - 1
                    if 0 <= itemNum < len(expiryProducts):
                        removed = expiryProducts[itemNum]
                        expiryProducts.pop(itemNum)
                        expiryProductsDate.pop(itemNum)
                        print("REMOVED " + removed + " from the tracker.")
                        save_data()
                    elif 0 <= itemNum - len(expiryProducts) < len(expiredProducts):
                        idx = itemNum - len(expiryProducts)
                        removed = expiredProducts[idx]
                        expiredProducts.pop(idx)
                        expiredProductsDate.pop(idx)
                        print("REMOVED " + removed + " from the tracker.")
                        save_data()
                    else:
                        print("ERROR: Invalid item number.")
                except ValueError:
                    print("ERROR: Please enter a valid number.")
            elif choice == "3":
                mainMenu()
                return
            else:
                print("ERROR: Invalid choice. Please try again.")
 
 
def shoppingList():
    while True:
        print("\n=== Shopping List ===")
 
        if len(groceryList) == 0:
            print("Your shopping list is empty.")
            print("\nAdd Item [1]")
            print("Back to Main Menu [2]")
            choice = input("Choose an option: ")
            if choice == "1":
                item = input("Enter item to add: ")
                groceryList.append(item)
                print("ADDED " + item + " to shopping list.")
                save_data()
            elif choice == "2":
                mainMenu()
                return
            else:
                print("ERROR: Invalid choice. Please try again.")
        else:
            print("Shopping List:")
            for i in range(len(groceryList)):
                print(str(i + 1) + ". " + groceryList[i])
            print("\nAdd Item [1]")
            print("Remove Item [2]")
            print("Clear List [3]")
            print("Back to Main Menu [4]")
            choice = input("Choose an option: ")
            if choice == "1":
                item = input("Enter item to add: ")
                groceryList.append(item)
                print("ADDED " + item + " to shopping list.")
                save_data()
            elif choice == "2":
                try:
                    itemNum = int(input("Enter item number to remove: ")) - 1
                    if 0 <= itemNum < len(groceryList):
                        removed = groceryList[itemNum]
                        groceryList.pop(itemNum)
                        print("REMOVED " + removed + " from shopping list.")
                        save_data()
                    else:
                        print("ERROR: Invalid item number.")
                except ValueError:
                    print("ERROR: Please enter a valid number.")
            elif choice == "3":
                groceryList.clear()
                print("CLEARED Shopping list cleared.")
                save_data()
            elif choice == "4":
                mainMenu()
                return
            else:
                print("ERROR: Invalid choice. Please try again.")
 
 
def mainMenu():
    print(""" ███████╗██████╗ ███████╗███████╗██╗  ██╗
 ██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║
 █████╗  ██████╔╝█████╗  ███████╗███████║
 ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║
 ██║     ██║  ██║███████╗███████║██║  ██║
 ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
 
 ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
 ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
    ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
 
        🌱  Fresh Tracker!  🌱
   "May all your food be fresh!"
""")
    print("Expiry Date [1]")
    print("Shopping List [2]")
    print("Exit [3]")
    choice = input("Choose an option: ")
    if choice == "1":
        expiryTracker()
    elif choice == "2":
        shoppingList()
    elif choice == "3":
        print("Thank you for using Fresh Tracker! Goodbye! Fresh")
        exit()
    else:
        print("Invalid choice. Please try again.")
        mainMenu()
 
 
load_data()
mainMenu()