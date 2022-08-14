# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import sqlite3
import functools
import pathlib
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
import AthenaDPGLib.data.sql as sql_fnc
from AthenaDPGLib.models.translation.languages import Languages


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def connected_to_db_file(fnc):
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        translation_obj, *_ =args
        if translation_obj.conn is None:
            raise ValueError("No connection has been made to a translation table")
        return fnc(*args, **kwargs)
    return wrapper

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Translation:
    sqlite_filepath:str
    conn: sqlite3.Connection = None

    def __init__(self, sqlite_filepath:str):
        if pathlib.Path(sqlite_filepath).exists():
            self.sqlite_filepath = sqlite_filepath
        else:
            raise ValueError(f"'{sqlite_filepath}' does not exist")

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.sqlite_filepath)
        except sqlite3.Error as e:
            print(e)

    @connected_to_db_file
    def close(self):
        self.conn.close()

    @connected_to_db_file
    def create_empty_table(self):
        self.conn.execute(sql_fnc.TRANSLATION_CREATE_TABLE)

    @connected_to_db_file
    def gather_translation(self, language:Languages) -> list[tuple]:
        return self.conn.execute(sql_fnc.TRANSLATION_SELECT_LANGUAGE(language.value)).fetchall()

    def apply_translation(self, language:Languages):
        for k,v in self.gather_translation(language):
            if dpg.get_item_type(k) == "mvAppItemType::mvText":
                dpg.set_value(k,v)
            else:
                dpg.set_item_label(k,v)