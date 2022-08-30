# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def create_new_input():
    item = dpg.add_input_text(parent="window")
    input_items:list[int|str] = dpg.get_item_user_data("button")
    input_items.append(item)
    dpg.set_item_user_data("button", input_items)

def main():
    dpg.create_context()
    dpg.create_viewport(title='Input with generated items')

    with dpg.window(tag="window",label="Test Window"):
        dpg.add_text("Hello world!")
        dpg.add_button(
            label="Press me, to create a new item",
            callback=create_new_input
        )
        dpg.add_button(
            tag="button",
            label="Press me, to output all inputs",
            user_data=[],
            callback=(lambda sender,app_data, user_data: print(dpg.get_values(user_data)))
        )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()