"""A program that will tell you your eventual fate.

Usage:
    timeuntil <person> <event>...
"""

import datetime
import hashlib
import json
import random

from docopt import docopt

DAYS_IN_YEAR = 365
DAYS_IN_WEEK = 7
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60
MAX_YEARS = 100
MAX_HOURS = 23
MAX_MINUTES = 59
MAX_SECONDS = 59
SAVED_EVENTS_FILE = "events.json"

def load_data(filename=SAVED_EVENTS_FILE):
    with open(filename, 'r', encoding='utf-8') as reader:
        return json.load(reader)

def write_data(data, filename=SAVED_EVENTS_FILE):
    with open(filename, 'w', encoding='utf-8') as writer:
        return json.dump(data, writer)

def create_dateobj(datetime):
    dateobj = {
        "year": datetime.year,
        "day": datetime.day,
        "hour": datetime.hour,
        "month": datetime.month,
        "minute": datetime.minute,
        "second": datetime.second,
    }
    return dateobj

def load_datetime(dateobj):
    target_date = datetime.datetime(
        year=dateobj["year"],
        day=dateobj["day"],
        hour=dateobj["hour"],
        month=dateobj["month"],
        minute=dateobj["minute"],
        second=dateobj["second"],
    )
    return target_date

def print_time_betwen(date1, date2):
    delta = date2 - date1
    year = abs(delta.days // DAYS_IN_YEAR)
    day = abs(delta.days % DAYS_IN_YEAR)
    hour = abs(delta.seconds // SECONDS_IN_MINUTE // MINUTES_IN_HOUR % MAX_HOURS)
    minute = abs(delta.seconds // SECONDS_IN_MINUTE % MAX_MINUTES)
    second = abs(delta.seconds % MAX_SECONDS)
    
    print(
        f"{name} has {year} years, {day} days, {hour} hours, {minute} minutes, and {second} seconds until {event}"
    )


if __name__ == "__main__":
    args = docopt(__doc__)
    name = args["<person>"]
    event = " ".join(args["<event>"])
    key = (name.lower() + event.lower()).encode("utf-8", errors="strict")
    dahash = hashlib.sha256(key).hexdigest()
    random.seed(dahash)
    hoy = datetime.datetime.today()
    jsondata = load_data()
    target_date = None
    if dahash in jsondata:
        target_date = load_datetime(jsondata[dahash])
    else:
        deltadays = random.randint(0, MAX_YEARS * DAYS_IN_YEAR)
        deltahours = random.randint(0, MAX_HOURS)
        deltaminutes = random.randint(0, MAX_MINUTES)
        deltaseconds = random.randint(0, MAX_SECONDS)
        delta = datetime.timedelta(
            days=deltadays,
            hours=deltahours,
            minutes=deltaminutes,
            seconds=deltaseconds,
        )
        target_date = hoy + delta
    jsondata[dahash] = create_dateobj(target_date)
    write_data(jsondata)
    print_time_betwen(hoy, target_date)
    
