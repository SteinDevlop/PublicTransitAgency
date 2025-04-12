from datetime import datetime
from logic import maintainance_status
class Maintenance:
    def __init__(self, id: int, unit: str, date: datetime, type: maintainance_status, status: str):
        self.id = id
        self.unit = unit
        self.date = date
        self.type = type
        self.status = status

    def schedule_maintenance(self, new_date: datetime):
        self.date = new_date

    def update_status(self, new_status: str):
        self.status = new_status