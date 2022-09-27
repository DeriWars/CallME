from object.color import Color
from datetime import datetime

def get_date():
    return "[ {0:02}:{1:02}:{2:02} ]".format(datetime.now().hour, datetime.now().minute, datetime.now().second)

def log(message):
    print(f"{Color.GREY}{get_date()}{Color.END} [INFO] {message}")

def warn(message):
    print(f"{Color.GREY}{get_date()}{Color.END} {Color.YELLOW2}[WARN] {message}{Color.END}")

def error(message):
    print(f"{Color.GREY}{get_date()}{Color.END} {Color.RED2}[ERROR] {message}{Color.END}")

def debug(message):
    print(f"{Color.GREY}{get_date()}{Color.END} {Color.VIOLET2}[DEBUG] {message}{Color.END}")