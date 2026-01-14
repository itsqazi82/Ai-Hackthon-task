# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import User, Post
from database import users, posts

app = Flask(__name__)

# Helper function
def create_user(username):
    if username in users:
        return users[username]
    user = User(username)
    users[username] = user
    return user

# -------------------
# Routes
# -------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        content = request.form["content"]
        user = create_user(username)
        post = Post(user, content)
        posts.insert(0, post)  # newest first
        user.posts.append(post)
        return redirect(url_for("index"))
    return render_template("index.html", posts=posts)

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    user = users.get(username)
    if not user:
        return "User not found"
    
    if request.method == "POST":
        action = request.form.get("action")
        post_index = int(request.form.get("post_index", -1))
        if post_index >= 0 and post_index < len(posts):
            target_post = posts[post_index]
            if action == "like":
                target_post.like_post(user)
            elif action == "comment":
                comment_text = request.form.get("comment_text")
                target_post.comment_post(user, comment_text)
        elif action == "follow":
            target_user = users.get(request.form.get("target_user"))
            if target_user:
                user.follow(target_user)
        return redirect(url_for("profile", username=username))
    
    return render_template("profile.html", user=user, posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
