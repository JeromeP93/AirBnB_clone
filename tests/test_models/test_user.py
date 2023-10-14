#!/usr/bin/python3
"""This module defines unit tests for the 'user' module.

Defines three unittest classes for testing the User model:
- TestUserInstantiation: Test User class instantiation and its attributes.
- TestUserSave: Test the save method of the User class.
- TestUserToDict: Test the to_dict method of the User class.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Test User class instantiation and attributes."""

    def test_no_args_instantiates(self):
        """Test if User class can be instantiated with no arguments."""
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        """Test if a new User instance is stored in the objects dictionary."""
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test if User.id is a public attribute of type str."""
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        """Test if User.created_at is a public attribute of type datetime."""
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test if User.updated_at is a public attribute of type datetime."""
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        """Test if User.email is a public attribute of type str."""
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        """Test if User.password is a public attribute of type str."""
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        """Test if User.first_name is a public attribute of type str."""
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        """Test if User.last_name is a public attribute of type str."""
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        """Test uniqueness of User IDs for two different User instances."""
        us1 = User()
        us2 = User()
        self.assertNotEqual(us1.id, us2.id)

    def test_different_created_at_for_two_users(self):
        """Test if the created_at attribute is different for two User instances."""
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def test_different_updated_at_for_two_users(self):
        """Test if the updated_at attribute is different for two User instances."""
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a User instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        usstr = us.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def test_args_unused(self):
        """Test instantiation of User with None as arguments."""
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of User with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Tests for the save method of the User class."""

    @classmethod
    def setUp(self):
        """Set up for testing the save method."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Clean up after testing the save method."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test that calling `save()` once updates the `updated_at` attribute."""
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def test_two_saves(self):
        """Test that calling `save()` twice updates the `updated_at` attribute."""
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def test_save_with_arg(self):
        """Test that calling `save()` with an argument raises a TypeError."""
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_save_updates_file(self):
        """Test if calling `save()` updates the data in the JSON file."""
        us = User()
        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUserToDict(unittest.TestCase):
    """Tests for the to_dict method of the User class."""

    def test_to_dict_type(self):
        """Test if the to_dict method returns a dictionary."""
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the dictionary contains the correct keys."""
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that the dictionary contains added attributes."""
        us = User()
        us.middle_name = "Holberton"
        us.my_number = 98
        self.assertEqual("Holberton", us.middle_name)
        self.assertIn("my_number", us.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that datetime attributes in the dictionary are strings."""
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the content of the dictionary."""
        dt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the `to_dict` method does not return the object's __dict__."""
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def test_to_dict_with_arg(self):
        """Test calling to_dict method with an argument."""
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
