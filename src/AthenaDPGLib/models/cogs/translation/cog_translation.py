# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Callable

# Custom Library

# Custom Packages
from AthenaDPGLib.models.cog import Cog
from AthenaDPGLib.models.cogs.translation.translator import Translator
from AthenaDPGLib.models.cogs.translation.languages import Languages
import AthenaDPGLib.data.sql as sql_fnc

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CogTranslation(Cog):
    translator:Translator
    _translation_mapping= [
        # Gather and apply all label texts
        {"sql":lambda language: sql_fnc.TRANSLATION_LABELS(language.value),"set_value":dpg.set_item_label},
        # Gather and apply  all value texts
        {"sql":lambda language: sql_fnc.TRANSLATION_VALUES(language.value),"set_value":dpg.set_value},
    ]

    def __init__(self, sqlite_filepath:str):
        self.translator = Translator(sqlite_filepath)

    def startup(self, translations_enabled:bool, language:Languages):
        if translations_enabled:
            self.translate_from_translator(language)

    def translate_from_translator(self, language:Languages):
        """
        Basic function to gather all records that have the corresponding language column filled in.
        If the Value of the language column is none, the text will be displayed in red
        """
        # create the theme for not found items
        #   TODO move this to a theme system
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255,0,0,255))

        for kwargs in self._translation_mapping:
            self._translate_from_translator_component(
                **kwargs,
                language=language,
                not_found_theme=item_theme
            )

    def _translate_from_translator_component(self, sql:Callable, language:Languages, set_value: Callable, not_found_theme:str|int):
        with self.translator.cursor() as cursor:
            for k, v in cursor.execute(sql(language)).fetchall():  # type: str, str|None
                if v is None:
                    set_value(k, k)
                    dpg.bind_item_theme(k, not_found_theme)
                else:
                    set_value(k, v)