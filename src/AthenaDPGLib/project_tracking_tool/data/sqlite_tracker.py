# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
SQLITE_CREATE_FILE_QUERIES:str = """
    /* Create the Admin table. this stores values like the version numbering, etc... */
    CREATE TABLE IF NOT EXISTS Admin (
        head varchar(255),
        val varchar(255)
    );
    INSERT INTO Admin 
        (head, val) 
    VALUES 
        ("version", "0.0.0")
    ;
    
    /* Because of relational behaviour, create all the sub tabel */
    CREATE TABLE IF NOT EXISTS TABLE Projects(
        id int,
        name varchar(255)
    );

    """
