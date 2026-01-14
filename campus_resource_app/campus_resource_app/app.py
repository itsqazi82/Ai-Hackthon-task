# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import User
from database import users, resources
from utils import search_resources, create_booking, is_available

app = Flask(__name__)

# -----------------
# Routes
# -----------------

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.args.get("keyword")
    resource_type = request.args.get("type")
    results = search_resources(keyword, resource_type)
    return render_template("index.html", resources=results)

@app.route("/resource/<name>", methods=["GET", "POST"])
def resource_detail(name):
    resource = next((r for r in resources if r.name==name), None)
    if not resource:
        return "Resource not found"

    message = ""
    if request.method=="POST":
        username = request.form["username"]
        email = request.form["email"]
        date = request.form["date"]
        time_slot = request.form["time_slot"]

        # Create or get user
        if username not in users:
            users[username] = User(username, email)
        user = users[username]

        # Create booking
        booking = create_booking(user, resource, date, time_slot)
        if booking:
            message = "Booking created! Pending approval."
        else:
            message = "Time slot already booked."

    return render_template("resource_detail.html", resource=resource, message=message)

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    message = ""
    if request.method=="POST":
        resource_name = request.form["resource_name"]
        action = request.form["action"]
        booking_index = int(request.form["booking_index"])
        resource = next((r for r in resources if r.name==resource_name), None)
        if resource:
            booking = resource.bookings[booking_index]
            booking.status = "Approved" if action=="approve" else "Declined"
            message = f"Booking {booking.status}."
    return render_template("admin.html", resources=resources, message=message)

if __name__=="__main__":
    app.run(debug=True)
    