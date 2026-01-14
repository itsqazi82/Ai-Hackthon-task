import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# ---- Models ----
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.items = []

class Review:
    def __init__(self, reviewer, rating, comment):
        self.reviewer = User(reviewer, f"{reviewer}@example.com")
        self.rating = rating
        self.comment = comment

class Item:
    def __init__(self, name, description, owner, image_url=None):
        self.name = name
        self.description = description
        self.owner = owner
        self.image_url = image_url
        self.reviews = []

# ---- In-memory DB ----
users = {}
items = []

# ---- Flask App ----
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ---- Routes ----
@app.route("/")
def index():
    return redirect(url_for("admin_dashboard"))

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    message = ""
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            name = request.form["name"]
            desc = request.form["description"]
            owner_name = request.form["owner"]

            image_file = request.files.get("image_file")
            image_filename = None
            if image_file and allowed_file(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            if owner_name not in users:
                users[owner_name] = User(owner_name, f"{owner_name}@example.com")
            owner = users[owner_name]

            new_item = Item(name, desc, owner, image_filename)
            items.append(new_item)
            owner.items.append(new_item)
            message = "Item added successfully."

        elif action == "delete":
            name = request.form["item_name"]
            item = next((i for i in items if i.name==name), None)
            if item:
                items.remove(item)
                message = "Item deleted successfully."

    return render_template("admin.html", items=items, message=message)

@app.route("/item/<name>", methods=["GET", "POST"])
def item_detail(name):
    item = next((i for i in items if i.name==name), None)
    message = ""
    if not item:
        return "Item not found", 404

    if request.method == "POST":
        reviewer = request.form["reviewer"]
        rating = int(request.form["rating"])
        comment = request.form["comment"]
        item.reviews.append(Review(reviewer, rating, comment))
        message = "Review added!"

    # Suggestions: other items not owned by same owner
    suggestions = [i for i in items if i.owner != item.owner and i != item][:3]

    return render_template("item_detail.html", item=item, suggestions=suggestions, message=message)

# ---- Run Server ----
if __name__ == "__main__":
    app.run(debug=True)
