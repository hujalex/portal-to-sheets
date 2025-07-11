import gspread

class Gspread:
    def __init__(self):
        gc = gspread.service_account(filename = "./keys.json")