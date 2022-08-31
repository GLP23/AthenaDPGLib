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

def viewport_resize_callback():
    if dpg.does_item_exist("table"):
        child = dpg.get_item_children("table")
        vp_height = dpg.get_item_height("window")
        for x in child[1]:
            dpg.configure_item(x, height=vp_height / len(child[1]))

def main():
    dpg.create_context()
    dpg.create_viewport(title='Table redrawn with viewport_resize_callback')

    with dpg.window(tag="window"):
        with dpg.table(tag="table"):
            for _ in range(3):
                dpg.add_table_column()

            for _ in range(3):
                with dpg.table_row():
                    for _ in range(3):
                        dpg.add_text("test")

    with dpg.item_handler_registry(tag="registry"):
        dpg.add_item_resize_handler(
            callback=viewport_resize_callback
        )

    dpg.bind_item_handler_registry(
        item="window",
        handler_registry="registry"
    )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()