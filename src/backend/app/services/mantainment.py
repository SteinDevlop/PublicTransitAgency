from datetime import datetime

class Maintenance:
    def __init__(self, id: int, unit: str, date: datetime, type: str, status: str):
        self.id = id
        self.unit = unit
        self.date = date
        self.type = type
        self.status = status

    def schedule_maintenance(self, new_date: datetime):
        self.date = new_date

    def update_status(self, new_status: str):
        self.status = new_status