# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Callable, ClassVar
from dataclasses import dataclass, field, InitVar

# Custom Library

# Custom Packages
from AthenaDPGLib.models.component import Component
from AthenaDPGLib.models.components.translation.translator import Translator
from AthenaDPGLib.models.components.translation.languages import Languages
import AthenaDPGLib.data.sql as sql_fnc

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class ComponentTranslation(Component):
    sqlite_filepath:InitVar[str]
    not_found_theme:str

    # non init stuff
    translator:Translator = field(init=False)
    _translation_tables:ClassVar[list[dict]]= [
        # Gather and apply all label texts
        {"sql":sql_fnc.TRANSLATION_LABELS,"set_value":dpg.set_item_label},
        # Gather and apply all value texts
        {"sql":sql_fnc.TRANSLATION_VALUES,"set_value":dpg.set_value},
    ]

    def __post_init__(self,sqlite_filepath):
        self.translator = Translator(sqlite_filepath)

    def translate(self, language:Languages):
        """
        Basic function to gather all records that have the corresponding language column filled in.
        If the Value of the language column is none, the text will be displayed in red
        """
        for kwargs in self._translation_tables:
            self._translate_table(language=language, **kwargs)

    def _translate_table(self, *, sql:Callable, set_value: Callable, language:Languages):
        with self.translator.cursor() as cursor:
            for k, v in cursor.execute(sql(language.value)).fetchall():  # type: str, str|None
                if v is None:
                    set_value(k, k)
                    dpg.bind_item_theme(k, self.not_found_theme)
                else:
                    set_value(k, v)