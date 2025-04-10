class Transport:
    def __init__(self, id, type, status, ubication, capacity):
        self.id = id
        self.type = type
        self.status = status
        self.ubication = ubication
        self.capacity = capacity
    def actualize_status(self, new_status):
        self.status = new_status

    def send_alert(self, message):
        print(f"Alert for Transport ID {self.id}: {message}")