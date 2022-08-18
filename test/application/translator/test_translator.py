# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest

# Custom Library
from AthenaDPGLib.models.application.cogs.translation.translator import Translator
from AthenaDPGLib.data.sql import TRANSLATION_CREATE_EMPTY_TABLES, SHOW_TABLES

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestTranslator(unittest.TestCase):
    sqlite_filepath = "application/translator/test_translation.sqlite"

    def get_translator(self) -> Translator:
        """Will create the sqlite file if it doesn't exist with the proper tables installed"""
        return Translator(sqlite_filepath=self.sqlite_filepath)

    def test_tables(self):
        with  self.get_translator().cursor() as cur:
            self.assertEqual(
                # Found tables
                {table for table, in cur.execute(SHOW_TABLES)},
                # The keys of the dict hold the names of the expected tables
                TRANSLATION_CREATE_EMPTY_TABLES.keys()
            )


