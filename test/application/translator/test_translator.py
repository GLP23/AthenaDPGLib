# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest

# Custom Library
from AthenaDPGLib.models.application.cogs.translation.translator import Translator

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestTranslator(unittest.TestCase):
    sqlite_filepath = "application/translator/test_translation.sqlite"

    def get_translator(self) -> Translator:
        return Translator(sqlite_filepath=self.sqlite_filepath)

    def test_connection(self):
        translator = self.get_translator()

