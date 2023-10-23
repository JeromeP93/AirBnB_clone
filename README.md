# 0x00. AirBnB clone - The console

## Description

This is the ALX AirBnB Clone project, focusing on creating a command-line interface (CLI) or console to manage AirBnB objects. The project will gradually evolve to encompass various aspects of web development, including HTML/CSS templating, database storage, APIs, and front-end integration.

### Key Tasks:

- Implement a parent class (BaseModel) for object initialization, serialization, and deserialization.
- Establish a flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file.
- Create classes representing AirBnB objects (e.g., User, State, City, Place) that inherit from BaseModel.
- Develop the first abstracted storage engine for the project: File storage.
- Create comprehensive unit tests to validate all classes and the storage engine.

## Command Interpreter

The command interpreter is a Python-based CLI that allows you to interact with the Airbnb objects. You can create, retrieve, update, and delete objects, as well as perform various operations on them.

## How to Start

To start the command interpreter, follow these steps:

1. Clone the project repository:

   ```shell
   git clone https://github.com/JeromeP93/AirBnB_clone.git
   ```
2. Change into the project directory:

   ```
   cd AirBnB_clone
   ```
3. Run the command interpreter:

   ```
   ./console.py
   ```

## How to Use

Once the command interpreter is running, you can use various commands to manage Airbnb objects. Here are some examples of commands you can use:

* `create <classname>`: Create a new instance of a class.
* `show <classname> <id>`: Show details of a specific instance.
* `update <classname> <id> <attribute> "<value>"`: Update an instance's attribute.
* `all <classname>`: List all instances of a class.
* `destroy <classname> <id>`: Delete a specific instance.
* `quit` or `EOF`: Exit the command interpreter.

For a full list of commands and their usage, type `help` in the command interpreter.

## Examples

Here are some usage examples:

```
(hbnb) create User
(hbnb) show User 12345
(hbnb) update User 12345 first_name "John"
(hbnb) all User
(hbnb) destroy User 12345
(hbnb) quit
```

## Authors

The following individuals have contributed to this project:

* [Jerome S. Patrick](https://github.com/JeromeP93 "@JeromeP93")
* [Jemima Aisha Okouya](https://github.com/Ash-beca "@Ash-beca")

Please refer to the [AUTHORS](https://github.com/JeromeP93/AirBnB_clone/blob/main/AUTHORS "Authors File") file for more details about authors.
