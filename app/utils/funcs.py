"""
Module containing useful functions for the website
"""
import datetime as dt
import re
import json
from flask import abort
from flask_login import current_user
from functools import wraps


def time_ago(time: str) -> str:
    """
    Returns a string showing how long ago the inputted time string was.
    """
    formatted_dt = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    time_ago = re.split(r"[:\.\,]+", str(dt.datetime.utcnow() - formatted_dt))

    if len(time_ago) > 4:
        return f"{time_ago[0]} ago"

    if int(time_ago[-4]) > 0:
        if int(time_ago[-4]) == 1:
            return f"{int(time_ago[-4])} hour ago"
        return f"{int(time_ago[-4])} hours ago"

    if int(time_ago[-3]) > 0:
        if int(time_ago[-3]) == 1:
            return f"{int(time_ago[-3])} minute ago"
        return f"{int(time_ago[-3])} minutes ago"

    return "Just now"


def load_projects():
    with open("static/pw/resources/projects.json",
              "r", encoding="utf-8") as file:
        projects = json.load(file)
    return projects


def split_into_groups(lst, group_size=3):
    groups = [lst[i:i + group_size] for i in range(0, len(lst), group_size)]
    for i in groups:
        while len(i) < 3:
            i.append({"name": "hidden"})
    return groups


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if current_user.id == 1:
                return func(*args, **kwargs)
            return abort(403)
        except AttributeError:
            return abort(403)
    return wrapper


if __name__ == '__main__':
    class Obj:
        def __init__(self) -> None:
            self.date_created = "2023-09-18 19:00:20.448339"
    obj = Obj()
    print(time_ago(object.date_created))
