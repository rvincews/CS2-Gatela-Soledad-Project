#common_items.py
#Shelf life data for common items
SHELF_LIFE_DAYS = {
    "apple": 30,
    "banana": 7,
    "orange": 20,
    "strawberry": 5,
    "lettuce": 7,
    "milk": 7,
    "bread": 5,
    "cheese": 21,
    "tomato": 10,
    "potato": 60,
    "carrot": 60,
}

REFRIGERATED = {
    "milk": True,
    "cheese": True,
    "lettuce": True,
    "strawberry": True,
    "tomato": False,
    "potato": False,
    "carrot": False,
    "apple": False,
    "banana": False,
    "orange": False,
    "bread": False,
}
#refs: FoodShare, FoodSafety.gov, Purdue, U.S. Dairy, Virginia Tech
