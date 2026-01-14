# models.py

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.items = []        # Items user has listed
        self.reviews = []      # Reviews by this user

class Item:
    def __init__(self, name, description, owner, image_url=None):
        self.name = name
        self.description = description
        self.owner = owner
        self.image_url = image_url
        self.reviews = []      # List of Review objects

class Review:
    def __init__(self, reviewer, rating, comment):
        self.reviewer = reviewer
        self.rating = rating   # 1-5
        self.comment = comment
