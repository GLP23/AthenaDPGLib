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

# premade SQL statements
TRANSLATION_CREATE_TABLE="CREATE TABLE `translation` (`tag` VARCHAR(255),`english` LONGTEXT,PRIMARY KEY (`tag`));"
TRANSLATION_SELECT_LANGUAGE= lambda language: f"SELECT `tag`,`{language}` FROM `translation`;"
