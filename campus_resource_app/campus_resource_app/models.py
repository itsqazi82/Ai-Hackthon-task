# models.py

class User:
    def __init__(self, username, email, is_admin=False):
        self.username = username
        self.email = email
        self.is_admin = is_admin

class Resource:
    def __init__(self, name, resource_type):
        self.name = name
        self.type = resource_type  # lab, hall, equipment
        self.bookings = []         # list of Booking objects

class Booking:
    def __init__(self, user, resource, date, time_slot):
        self.user = user
        self.resource = resource
        self.date = date            # string YYYY-MM-DD
        self.time_slot = time_slot  # string "09:00-11:00"
        self.status = "Pending"     # Pending / Approved / Declined
