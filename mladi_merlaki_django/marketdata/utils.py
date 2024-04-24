import os
import json

from django.utils.timezone import datetime


def load_last_update_date():
    # Load the last update date from a file or database
    if os.path.exists("last_update_date.json"):
        with open("last_update_date.json", "r") as f:
            return datetime.fromisoformat(json.load(f))
    else:
        return None


def save_last_update_date(date):
    # Save the last update date to a file or database
    with open("last_update_date.json", "w") as f:
        json.dump(date.isoformat(), f)