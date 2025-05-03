import unittest
from backend.app.logic.routes import Routes

class TestRoutes(unittest.TestCase):

    def test_initialization_with_route_dict_and_id(self):
        route_data = {"route_id": "RUT001", "name": "Ruta A"}
        route_instance = Routes(route=route_data, route_id="EXTERNAL_ID")
        self.assertEqual(route_instance.route, route_data)
        self.assertEqual(route_instance.route_id, "EXTERNAL_ID")

    def test_initialization_with_route_dict_only(self):
        route_data = {"route_id": "RUT002", "origin": "Inicio", "destination": "Fin"}
        route_instance = Routes(route=route_data)
        self.assertEqual(route_instance.route, route_data)
        self.assertEqual(route_instance.route_id, "RUT002")

    def test_initialization_with_route_dict_without_id(self):
        route_data = {"name": "Ruta B", "stops": ["S1", "S2"]}
        route_instance = Routes(route=route_data)
        self.assertEqual(route_instance.route, route_data)
        self.assertIsNone(route_instance.route_id)

    def test_set_route_updates_route_id_if_present(self):
        route_instance = Routes(route={"route_id": "OLD_ID", "name": "Vieja"})
        new_route_data = {"route_id": "NEW_ID", "description": "Nueva"}
        route_instance.route = new_route_data
        self.assertEqual(route_instance.route, new_route_data)
        self.assertEqual(route_instance.route_id, "NEW_ID")

    def test_set_route_does_not_update_route_id_if_absent(self):
        route_instance = Routes(route={"route_id": "OLD_ID", "name": "Vieja"})
        new_route_data = {"description": "Nueva parada", "location": "Centro"}
        route_instance.route = new_route_data
        self.assertEqual(route_instance.route, new_route_data)
        self.assertEqual(route_instance.route_id, "OLD_ID")

    def test_set_route_id_updates_route_dict(self):
        route_instance = Routes(route={"name": "Sin ID"})
        route_instance.route_id = "ASSIGNED_ID"
        self.assertEqual(route_instance.route['route_id'], "ASSIGNED_ID")
        self.assertEqual(route_instance.route_id, "ASSIGNED_ID")

    def test_set_route_id_overwrites_existing_id_in_route_dict(self):
        route_instance = Routes(route={"route_id": "INITIAL_ID", "name": "Con ID"})
        route_instance.route_id = "OVERWRITTEN_ID"
        self.assertEqual(route_instance.route['route_id'], "OVERWRITTEN_ID")
        self.assertEqual(route_instance.route_id, "OVERWRITTEN_ID")

if __name__ == '__main__':
    unittest.main()