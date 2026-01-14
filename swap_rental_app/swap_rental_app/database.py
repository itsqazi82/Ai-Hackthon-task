# database.py

from models import User, Item

users = {}
items = []

# Example item
if "alice" not in users:
    from models import User
    users["alice"] = User("alice", "alice@example.com")

from models import Item
items.append(Item("Camera", "DSLR camera for photography", users["alice"], "static/images/camera.jpg"))
