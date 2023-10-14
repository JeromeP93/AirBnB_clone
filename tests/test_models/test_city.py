#!/usr/bin/python3
"""This module defines unit tests for the 'city' module.

Defines three unittest classes for testing the City model:
- TestCityInstantiation: Test the instantiation of the City class.
- TestCitySave: Test the 'save' method of the City class.
- TestCityToDict: Test the 'to_dict' method of the City class.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unit tests for instantiating the City class."""

    def test_no_args_instantiates(self):
        """Test that a City instance can be created without arguments."""
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        """Test that a newly created City instance is stored in the 'objects' attribute."""
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test that the 'id' attribute of City is a public string."""
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        """Test that the 'created_at' attribute of City is a public datetime object."""
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test that the 'updated_at' attribute of City is a public datetime object."""
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        """Test that 'state_id' is a public class attribute of City."""
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def test_name_is_public_class_attribute(self):
        """Test that 'name' is a public class attribute of City."""
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def test_two_cities_unique_ids(self):
        """Test that two City instances have unique 'id' values."""
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_different_created_at_for_two_cities(self):
        """Test that two City instances have different 'created_at' values."""
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_different_updated_at_for_two_cities(self):
        """Test that two City instances have different 'updated_at' values."""
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a City instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        """Test that unused arguments do not affect the City instance."""
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of City with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "345")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that instantiation with None as kwargs raises a TypeError."""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unit tests for the 'save' method of the City class."""

    @classmethod
    def setUp(self):
        """Set up for test cases by renaming 'file.json' to 'tmp' if it exists."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Clean up after test cases by removing 'file.json' and renaming 'tmp' to 'file.json'."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test saving a City instance once and check if 'updated_at' has changed."""
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_two_saves(self):
        """Test saving a City instance twice and check if 'updated_at' has changed both times."""
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_with_arg(self):
        """Test saving a City instance with an argument and check if it raises a TypeError."""
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates_file(self):
        """Test saving a City instance and check if the 'file.json' file is updated with its ID."""
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCityToDict(unittest.TestCase):
    """Unit tests for the 'to_dict' method of the City class."""

    def test_to_dict_type(self):
        """Test the type of the output of the 'to_dict' method."""
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the output of 'to_dict' contains the correct keys."""
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that 'to_dict' includes attributes added to a City instance."""
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 98
        self.assertEqual("Holberton", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that datetime attributes in 'to_dict' are represented as strings."""
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of 'to_dict' for a City instance."""
        dt = datetime.today()
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that 'to_dict' and '__dict__' are not the same for a City instance."""
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to 'to_dict' raises a TypeError."""
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
