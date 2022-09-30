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
class SQLQueries:
    # ------------------------------------------------------------------------------------------------------------------
    # - Static sql queries -
    # ------------------------------------------------------------------------------------------------------------------
    create_db:str = """
/* Create the Admin table. this stores values like the version numbering, etc... */
CREATE TABLE IF NOT EXISTS 'Admin' (
    'head' Text not Null,
    'val' Text not Null
);
INSERT INTO 'Admin' 
    ('head', 'val') 
VALUES 
    ('version', '0.0.0')
;

/* Because of relational behaviour, create all the sub tabel */
CREATE TABLE IF NOT EXISTS 'Projects'(
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' TEXT not Null,
    'info' TEXT 
);
"""
    query_get_all_projects: str = "SELECT * FROM Projects;"

    # ------------------------------------------------------------------------------------------------------------------
    # - Dynamic sql queries -
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def insert_new_project(name:str, info:str|None):
        return f"""
INSERT INTO 'PROJECTS' 
    ('name', 'info') 
VALUES 
    ({f"'{name}'"}, {f"'{info}'" if isinstance(info, str) else "Null"});
"""

