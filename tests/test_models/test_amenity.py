#!/usr/bin/python3
"""This module defines unit tests for the 'amenity' module.

Defines three unittest classes for testing the Amenity model:
- TestAmenityInstantiation: Test the instantiation of the Amenity class.
- TestAmenitySave: Test the 'save' method of the Amenity class.
- TestAmenityToDict: Test the 'to_dict' method of the Amenity class.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity

class TestAmenity_instantiation(unittest.TestCase):
    """Unit tests for instantiating the Amenity class."""

    def test_no_args_instantiates(self):
        """Test that an Amenity instance can be created without arguments."""
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        """Test that a newly created Amenity instance is stored in the 'objects' attribute."""
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test that the 'id' attribute of Amenity is a public string."""
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        """Test that the 'created_at' attribute of Amenity is a public datetime object."""
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test that the 'updated_at' attribute of Amenity is a public datetime object."""
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        """Test that 'name' is a public class attribute of Amenity."""
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_two_amenities_unique_ids(self):
        """Test that two Amenity instances have unique 'id' values."""
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_different_created_at_for_two_amenities(self):
        """Test that two Amenity instances have different 'created_at' values."""
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_different_updated_at_for_two_amenities(self):
        """Test that two Amenity instances have different 'updated_at' values."""
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_representation(self):
        """Test the string representation of an Amenity instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        """Test that unused arguments do not affect the Amenity instance."""
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that instantiation with None as kwargs raises a TypeError."""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """Unit tests for the 'save' method of the Amenity class."""

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
        """Test saving an Amenity instance once and check if 'updated_at' has changed."""
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(self):
        """Test saving an Amenity instance twice and check if 'updated_at' has changed both times."""
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_save_with_arg(self):
        """Test saving an Amenity instance with an argument and check if it raises a TypeError."""
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def test_save_updates_file(self):
        """Test saving an Amenity instance and check if the 'file.json' file is updated with its ID."""
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenityToDict(unittest.TestCase):
    """Unit tests for the 'to_dict' method of the Amenity class."""

    def test_to_dict_type(self):
        """Test the type of the output of the 'to_dict' method."""
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the output of 'to_dict' contains the correct keys."""
        am = Amenity()
        self.assertIn("id", am.to_dict())
        self.assertIn("created_at", am.to_dict())
        self.assertIn("updated_at", am.to_dict())
        self.assertIn("__class__", am.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that 'to_dict' includes attributes added to an Amenity instance."""
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 98
        self.assertEqual("Holberton", am.middle_name)
        self.assertIn("my_number", am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that datetime attributes in 'to_dict' are represented as strings."""
        am = Amenity()
        am_dict = am.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of 'to_dict' for an Amenity instance."""
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that 'to_dict' and '__dict__' are not the same for an Amenity instance."""
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to 'to_dict' raises a TypeError."""
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)

if __name__ == "__main__":
    unittest.main()
