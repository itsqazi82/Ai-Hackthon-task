# utils.py

from database import resources
from models import Booking

def search_resources(keyword=None, resource_type=None):
    results = resources
    if keyword:
        results = [r for r in results if keyword.lower() in r.name.lower()]
    if resource_type:
        results = [r for r in results if r.type.lower() == resource_type.lower()]
    return results

def is_available(resource, date, time_slot):
    for b in resource.bookings:
        if b.date == date and b.time_slot == time_slot and b.status=="Approved":
            return False
    return True

def create_booking(user, resource, date, time_slot):
    if not is_available(resource, date, time_slot):
        return None
    booking = Booking(user, resource, date, time_slot)
    resource.bookings.append(booking)
    return booking
