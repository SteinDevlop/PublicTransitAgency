from locust import HttpUser, task, between

class IncidenceUser(HttpUser):
    wait_time = between(1, 4)  # Espera entre 1 y 2 segundos entre tareas

    @task
    def listar_incidencias(self):
        self.client.get("/incidences/")

    @task
    def detalle_incidencia(self):
        self.client.get("/incidences/1")

    @task
    def crear_actualizar_eliminar_incidencia(self):
        # Cambia el ID en cada iteración para evitar conflictos
        import random
        incidencia_id = random.randint(100000, 999999)
        data = {
            "ID": incidencia_id,
            "IDTicket": 1,
            "Descripcion": "Incidencia de prueba",
            "Tipo": "Test",
            "IDUnidad": 1
        }
        # Crear
        self.client.post("/incidences/create", data=data)
        # Actualizar
        data["Descripcion"] = "Incidencia actualizada"
        self.client.post("/incidences/update", data=data)
        # Eliminar
        self.client.post("/incidences/delete", data={"ID": incidencia_id})