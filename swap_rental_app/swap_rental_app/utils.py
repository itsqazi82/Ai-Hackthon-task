# utils.py

from database import items

def search_items(keyword=None):
    results = items
    if keyword:
        results = [i for i in items if keyword.lower() in i.name.lower() or keyword.lower() in i.description.lower()]
    return results

def suggest_swap(user_item):
    # Simple matching: suggest items not owned by user
    matches = [i for i in items if i.owner != user_item.owner]
    return matches
