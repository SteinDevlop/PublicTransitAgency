import unittest
from person import Person

class TestPerson(unittest.TestCase):
    def test_person_creation(self):
        p = Person("Alice", 30)
        self.assertEqual(p.name, "Alice")
        self.assertEqual(p.age, 30)
    
    def test_person_birthday(self):
        p = Person("Bob", 25)
        p.birthday()
        self.assertEqual(p.age, 26)
    
    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Person("", 20)
    
    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            Person("Charlie", -5)
    
    def test_person_str(self):
        p = Person("Diana", 40)
        self.assertEqual(str(p), "Diana, 40 years old")

if __name__ == "__main__":
    unittest.main()
