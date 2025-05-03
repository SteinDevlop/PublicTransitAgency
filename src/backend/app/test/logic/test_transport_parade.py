import unittest
from datetime import datetime
from backend.app.logic.transport_parade import Parade
class TestParade(unittest.TestCase):
    def setUp(self):
        self.parade = Parade(location='Main Street', id=101, name='Spring Festival')

    def test_parade_attributes(self):
        self.assertEqual(self.parade.location, 'Main Street')
        self.assertEqual(self.parade.id, 101)
        self.assertEqual(self.parade.name, 'Spring Festival')

if __name__ == '__main__':
    unittest.main()