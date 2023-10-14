#!/usr/bin/python3
"""This module defines unit tests for the 'state' module.

Defines three unittest classes for testing the State model:
- TestStateInstantiation: Test the instantiation of the State class.
- TestStateSave: Test the 'save' method of the State class.
- TestStateToDict: Test the 'to_dict' method of the State class.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unit tests for testing the instantiation of the State class."""

    def test_no_args_instantiates(self):
        """Test that a State instance can be created with no arguments."""
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        """Test that a newly created State instance is stored in objects."""
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test that the 'id' attribute of State is a public string."""
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        """Test that the 'created_at' attribute of State is a public datetime."""
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test that the 'updated_at' attribute of State is a public datetime."""
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        """Test that 'name' is a public class attribute of State."""
        st = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)

    def test_unique_ids_for_two_states(self):
        """Test that two instances of State have unique 'id' values."""
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_different_created_at_for_two_states(self):
        """Test that two instances of State have different 'created_at' values."""
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_different_updated_at_for_two_states(self):
        """Test that two instances of State have different 'updated_at' values."""
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a State instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        ststr = st.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(self):
        """Test that unused arguments are not stored in the State instance."""
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation of State with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at, dt)
        self.assertEqual(st.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that instantiation with None as kwargs raises a TypeError."""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unit tests for testing the 'save' method of the State class."""

    @classmethod
    def setUp(self):
        """Set up for test cases by renaming 'file.json' to 'tmp' if it exists."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Clean up after test cases by removing 'file.json' and restoring 'tmp'."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test that the 'save' method updates the 'updated_at' attribute."""
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)

    def test_two_saves(self):
        """Test that consecutive 'save' calls update the 'updated_at' attribute."""
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        self.assertLess(second_updated_at, st.updated_at)

    def test_save_with_arg(self):
        """Test that passing an argument to 'save' raises a TypeError."""
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def test_save_updates_file(self):
        """Test that the 'save' method updates the 'file.json' file."""
        st = State()
        st.save()
        stid = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestStateToDict(unittest.TestCase):
    """Unit tests for testing the 'to_dict' method of the State class."""

    def test_to_dict_type(self):
        """Test that the 'to_dict' method returns a dictionary."""
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the 'to_dict' method contains the correct keys."""
        st = State()
        self.assertIn("id", st.to_dict())
        self.assertIn("created_at", st.to_dict())
        self.assertIn("updated_at", st.to_dict())
        self.assertIn("__class__", st.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that 'to_dict' includes added attributes in the dictionary."""
        st = State()
        st.middle_name = "Holberton"
        st.my_number = 98
        self.assertEqual("Holberton", st.middle_name)
        self.assertIn("my_number", st.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that datetime attributes in 'to_dict' are represented as strings."""
        st = State()
        st_dict = st.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of 'to_dict' for a State instance."""
        dt = datetime.today()
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(st.to_dict(), tdict)

    def test_contrast_to_dict_and_dunder_dict(self):
        """Test that 'to_dict' and '__dict__' are not the same for a State instance."""
        st = State()
        self.assertNotEqual(st.to_dict(), st.__dict__)

    def test_to_dict_with_arg(self):
        """Test that passing an argument to 'to_dict' raises a TypeError."""
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
