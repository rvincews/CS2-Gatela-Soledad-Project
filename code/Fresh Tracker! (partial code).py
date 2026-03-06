# Hezekiah C. Gatela & Rile Vince W. Soledad
# Fresh Tracker!

from datetime import datetime, timedelta
from common_items import SHELF_LIFE_DAYS, REFRIGERATED

expiryProducts = []
expiryProductsDate = []
order = []
orderNum = 0
groceryList = []


def get_expiry_date_from_user(productName: str) -> str:
    """Ask the user for an expiry date, using predefined library for estimates."""
    name_lower = productName.lower().strip()
    answer = input("Would you like an estimate based on typical shelf life? (y/n): ")
    if answer.lower().startswith("y"):
        if name_lower in SHELF_LIFE_DAYS:
            shelf_days = SHELF_LIFE_DAYS[name_lower]
            if name_lower in REFRIGERATED:
                refrigerate = input("Will this item be refrigerated? (y/n): ")
                if refrigerate.lower().startswith("y"):
                    shelf_days = int(shelf_days * 1.5)
                    print(f"INFO: Refrigerated items last longer; adjusting estimated life to {shelf_days} days.")
            estimated_date = (datetime.now().date() + timedelta(days=shelf_days)).strftime("%Y-%m-%d")
            print(f"ESTIMATED DATE: Estimated expiry date for {productName} is {estimated_date}.")
            return estimated_date
        else:
            print("ERROR: No shelf life data for this item. Please enter manually.")
    # manual entry
    return input("Enter the expiry date (YYYY-MM-DD): ")

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

def checkExpiryStatus(dateNow):
    print("\n=== Expiry Status Check ===")
    hasWarnings = False
    
    for i in range(len(expiryProducts)):
        expiryDateObj = datetime.strptime(expiryProductsDate[i], "%Y-%m-%d").date()
        daysLeft = (expiryDateObj - dateNow).days
        
        if daysLeft < 0:
            print(f"WARNING:  {expiryProducts[i]} has expired {abs(daysLeft)} days ago!")
            hasWarnings = True
        elif daysLeft == 0:
            print(f"WARNING:  {expiryProducts[i]} expires today!")
            hasWarnings = True
        elif daysLeft <= 3:
            print(f"WARNING:  {expiryProducts[i]} is about to expire in {daysLeft} days.")
            hasWarnings = True
        else:
            print(f"OK {expiryProducts[i]} is fresh ({daysLeft} days remaining)")
    
    if not hasWarnings:
        print("All products are fresh! Fresh")
    print()

def expiryTracker():
    while True:
        dateNow = datetime.now().date()
        print(f"\n=== Expiry Tracker ===")
        print(f"Date Today: {dateNow}\n")
        
        if expiryProducts == []:
            print("No products in the expiry tracker.")
            print("\nAdd Items [1]")
            print("Back to Main Menu [2]")
            choice = input("Choose an option: ")
            
            if choice == "1":
                productName = input("Enter the product name: ")
                expiryDate = get_expiry_date_from_user(productName)
                try:
                    datetime.strptime(expiryDate, "%Y-%m-%d")
                    expiryProducts.append(productName)
                    expiryProductsDate.append(expiryDate)
                    print(f"ADDED {productName} with expiry date {expiryDate} to the tracker.")
                except ValueError:
                    print("ERROR: Invalid date format. Please use YYYY-MM-DD.")
            elif choice == "2":
                mainMenu()
                return
        else:
            print("Expiry Products:")
            for position in range(len(expiryProducts)):
                expiryDateObj = datetime.strptime(expiryProductsDate[position], "%Y-%m-%d").date()
                daysLeft = (expiryDateObj - dateNow).days
                status = "OK" if daysLeft > 3 else "WARNING"
                print(f"{status} {position + 1}. {expiryProducts[position]} - Expiry: {expiryProductsDate[position]} ({daysLeft} days)")
            
            print("\nAdd Items [1]")
            print("Check Expiry Status [2]")
            print("Remove Item [3]")
            print("Back to Main Menu [4]")
            choice = input("Choose an option: ")
            
            if choice == "1":
                productName = input("Enter the product name: ")
                expiryDate = get_expiry_date_from_user(productName)
                try:
                    datetime.strptime(expiryDate, "%Y-%m-%d")
                    expiryProducts.append(productName)
                    expiryProductsDate.append(expiryDate)
                    print(f"ADDED {productName} with expiry date {expiryDate} to the tracker.")
                except ValueError:
                    print("ERROR: Invalid date format. Please use YYYY-MM-DD.")
            elif choice == "2":
                checkExpiryStatus(dateNow)
            elif choice == "3":
                try:
                    itemNum = int(input("Enter item number to remove: ")) - 1
                    if 0 <= itemNum < len(expiryProducts):
                        removed = expiryProducts.pop(itemNum)
                        expiryProductsDate.pop(itemNum)
                        print(f"ADDED {removed} from the tracker.")
                    else:
                        print("ERROR: Invalid item number.")
                except ValueError:
                    print("ERROR: Please enter a valid number.")
            elif choice == "4":
                mainMenu()
                return
            else:
                print("ERROR: Invalid choice. Please try again.")

def shoppingList():
    while True:
        print("\n=== Shopping List ===")
        
        if groceryList == []:
            print("Your shopping list is empty.")
            print("\nAdd Item [1]")
            print("Back to Main Menu [2]")
            choice = input("Choose an option: ")
            
            if choice == "1":
                item = input("Enter item to add: ")
                groceryList.append(item)
                print(f"ADDED {item} to shopping list.")
            elif choice == "2":
                mainMenu()
                return
        else:
            print("Shopping List:")
            for i, item in enumerate(groceryList):
                print(f"{i + 1}. {item}")
            
            print("\nAdd Item [1]")
            print("Remove Item [2]")
            print("Clear List [3]")
            print("Back to Main Menu [4]")
            choice = input("Choose an option: ")
            
            if choice == "1":
                item = input("Enter item to add: ")
                groceryList.append(item)
                print(f"ADDED {item} to shopping list.")
            elif choice == "2":
                try:
                    itemNum = int(input("Enter item number to remove: ")) - 1
                    if 0 <= itemNum < len(groceryList):
                        removed = groceryList.pop(itemNum)
                        print(f"REMOVED {removed} from shopping list.")
                    else:
                        print("ERROR: Invalid item number.")
                except ValueError:
                    print("ERROR: Please enter a valid number.")
            elif choice == "3":
                groceryList.clear()
                print("CLEARED Shopping list cleared.")
            elif choice == "4":
                mainMenu()
                return
            else:
                print("ERROR: Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    mainMenu()