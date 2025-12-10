# client/postgres/models/user_info.py

class EmployeeInfo:
    def __init__(self, id=None, name=None, status=None, date=None):
        self.id = id
        self.name = name
        self.status = status
        self.date = date
