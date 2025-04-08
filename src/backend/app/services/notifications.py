class Notifications():
    def __init__ (self, id_notification: str, id_user: str, message: str): ##id usuario mejor que destinatario, ya que puede ser un grupo de usuarios.
        self.id_notification = id_notification
        self.id_user = id_user
        self.message = message

    def send_notification(self):
        # Aquí iría la lógica para enviar la notificación al usuario
        #Ni idea pero, mensaje de exito xq si.
        print(f"Notification sent to user {self.id_user}: {self.message}")
        return True