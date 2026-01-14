# models.py

class User:
    def __init__(self, username):
        self.username = username
        self.followers = set()
        self.following = set()
        self.posts = []

    def follow(self, other_user):
        if other_user != self:
            self.following.add(other_user)
            other_user.followers.add(self)

class Post:
    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.likes = set()
        self.comments = []

    def like_post(self, user):
        self.likes.add(user)

    def comment_post(self, user, comment_text):
        self.comments.append((user, comment_text))
