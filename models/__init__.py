#!/usr/bin/python3
"""Initialize the FileStorage engine and load data if available."""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
