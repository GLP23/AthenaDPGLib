# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest
import json

# Custom Library
from AthenaGuiLib.Applications.Application import Application
from AthenaGuiLib.Applications.ApplicationInfo import AppVersion


# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class test_Application(unittest.TestCase):
    def test_Application_Empty(self):
        app = Application()

        # test the info of an application
        self.assertEqual(
            "Undefined Application",
            app.info.name
        )
        self.assertEqual(
            AppVersion(0,0,0),
            app.info.version
        )

    def test_Application_PremadeInfo(self):
        app = Application(app_info_path="Data/AppInfo_Example.json")

        # test the info of an application
        self.assertEqual(
            "Test Application",
            app.info.name
        )
        self.assertEqual(
            AppVersion(0,1,2),
            app.info.version
        )