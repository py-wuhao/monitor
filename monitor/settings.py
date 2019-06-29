import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "statics": os.path.join(BASE_DIR, "statics"),
}
