# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest
import json

# Custom Library
from AthenaGuiLib.Applications.ApplicationInfo import AppVersion, AppInfo


# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class test_Applicationinfo(unittest.TestCase):
    def test_ApplicationVersion(self):
        self.assertEqual(
            "AppVersion(Major=0, Minor=1, Patch=2)",
            repr(AppVersion(0, 1, 2))
        )

        self.assertEqual(
            {"Major": 0, "Minor": 1, "Patch": 2},
            AppVersion(0, 1, 2).to_dict()
        )

    def test_ApplicationInfo(self):
        app_info_file = "Data/AppInfo_Example.json"
        app_info = AppInfo(path=app_info_file)

        self.assertEqual(
            AppVersion(Major=0, Minor=1, Patch=2),
            app_info.version
        )

        self.assertEqual(
            "Test Application",
            app_info.name
        )
        with open(app_info_file, "r") as file:
            self.assertEqual(
                json.load(file),
                app_info.to_dict(),
            )


