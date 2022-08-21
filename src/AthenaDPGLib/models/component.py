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
class Component:
    def component_startup(self, *args, **kwargs):
        """Ran at Application startup"""
        pass

    def component_closedown(self, *args, **kwargs):
        """Ran at Application closedown"""
        pass