# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest

# Custom Library
from AthenaDPGLib.track_attack.models.data_tracker import DataTracker
import AthenaDPGLib.track_attack.functions.sql_dynamic as SQL
# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestTracker(unittest.TestCase):
    @staticmethod
    def _get_tracker() -> DataTracker:
        tracker = DataTracker(db="project_tracking.db")
        tracker.db_reset()
        return tracker

    def test_new_project(self):
        self.assertEqual(
            1,
            self._get_tracker().new_project(name="test_project", info="This is a test project")
        )

    def test_get_all_projects(self):
        tracker:DataTracker = self._get_tracker()

        test_projects = [
            (1,"test_project_0", "This is a test project, v0"),
            (2,"test_project_1", "This is a test project, v1")
        ]

        with tracker.connector.get_cursor(commit=True) as cursor:
            for _, name, info in test_projects:
                cursor.execute(SQL.insert_new_project(name, info))

        self.assertEqual(
            test_projects,
            tracker.get_all_projects()
        )