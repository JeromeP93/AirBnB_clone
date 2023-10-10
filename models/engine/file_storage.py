#!/usr/bin/python3
"""Defines the FileStorage class for handling data storage."""
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Representation of an abstracted storage engine.

    Attributes:
        __file_path (str): The file name used to save objects.
        __objects (dict): A dictionary storing instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects stored in the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add an object to __objects using <obj_class_name>.id as the key."""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """Serialize the objects in __objects to the JSON file specified by __file_path."""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize objects from the JSON file __file_path into __objects, if the file exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
