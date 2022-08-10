# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg
import dearpygui._dearpygui as internal_dpg
from typing import Any, Union, List, Tuple, Callable

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDPGLib.models.dpg_component import DpgComponent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class Window(DpgComponent):
    label: str =None
    user_data: Any =None
    use_internal_label: bool =True
    tag: Union[int, str] =0
    width: int =0
    height: int =0
    indent: int =-1
    show: bool =True
    pos: Union[list[int], tuple[int, ...]] = field(default_factory=list)
    delay_search: bool =False
    min_size: Union[list[int], tuple[int, ...]] =field(default_factory=lambda: [100, 100])
    max_size: Union[list[int], tuple[int, ...]] =field(default_factory=lambda: [30000, 30000])
    menubar: bool =False
    collapsed: bool =False
    autosize: bool =False
    no_resize: bool =False
    no_title_bar: bool =False
    no_move: bool =False
    no_scrollbar: bool =False
    no_collapse: bool =False
    horizontal_scrollbar: bool =False
    no_focus_on_appearing: bool =False
    no_bring_to_front_on_focus: bool =False
    no_close: bool =False
    no_background: bool =False
    modal: bool =False
    popup: bool =False
    no_saved_settings: bool =False
    no_open_over_existing_popup: bool =True
    on_close: Callable =None

    # non init
    children:list = field(init=False, default_factory=list)

    def __post_init__(self):
        with dpg.stage() as stage:
            self.id = internal_dpg.add_window(
                label=self.label,
                user_data=self.user_data,
                use_internal_label=self.use_internal_label,
                tag=self.tag,
                width=self.width,
                height=self.height,
                indent=self.indent,
                show=self.show,
                pos=self.pos,
                delay_search=self.delay_search,
                min_size=self.min_size,
                max_size=self.max_size,
                menubar=self.menubar,
                collapsed=self.collapsed,
                autosize=self.autosize,
                no_resize=self.no_resize,
                no_title_bar=self.no_title_bar,
                no_move=self.no_move,
                no_scrollbar=self.no_scrollbar,
                no_collapse=self.no_collapse,
                horizontal_scrollbar=self.horizontal_scrollbar,
                no_focus_on_appearing=self.no_focus_on_appearing,
                no_bring_to_front_on_focus=self.no_bring_to_front_on_focus,
                no_close=self.no_close,
                no_background=self.no_background,
                modal=self.modal,
                popup=self.popup,
                no_saved_settings=self.no_saved_settings,
                no_open_over_existing_popup=self.no_open_over_existing_popup,
                on_close=self.on_close,
            )
        self.stage = stage

    def add_child(self, child:DpgComponent):
        dpg.move_item(
            child.id,
            parent=self.id
        )
        self.children.append(child)

