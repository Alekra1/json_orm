JSON ORM SIMULATOR

For my course project, I will build an orm simulator. It will be something similar to sqlalchemy; however, instead of working with a real database, it will save and read data from json file.

Main functionality:

    Convert Python objects to a dictionary and save to json file
    Read data from json file and convert it to Python objects
    Manipulate the data: basic CRUD operations - create, read, update, delete, as well as search, filter, sort, and aggregate data (for example, counting the total number of users or total number of admin users, etc.)

Meeting the criteria:

    I will use separate files/directories for my project. Such as: models.py - for data classes; main.py as the main program itself, and a separate directory tests/ for test and, etc.
    Three-level hierarchy: BaseModel -> User -> AdminUser
    Data will be accessed using getters and setters, and the setters will validate the data before saving it (e.g., checking if a username is long enough).
    There will be an overloaded operator that will check if two records have the same id
    There will be a get_permissions() - polymorphic method that will return the permissions that a certain user has
    I will get the path to a JSON (DB) file from argparse
    After loading data from a file, I will provide functionality to sort and filter records.

All other project requirements, including pep8 formatting, Google-style docstrings, and test coverage, will be strictly followed by me.
