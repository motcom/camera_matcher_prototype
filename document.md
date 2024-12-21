``` plantuml

RootWidget --> ControlWidget
RootWidget --> FileWidget
RootWidget --> PreviewWidget
RootWidget --> SliderWidget

class RootWidget{
    preview_window : PreviewWidget
    control_window : ControlWidget
    file_window    : FileWidget
    + slot_load_image_lst()
}

class FileWidget{
    load_path      : str
    save_path      : str
    files_abs_path : List[str]
    + signal_get_files_abs_path() -> List[str]
}

class ControlWidget{
    valA : float
    valB : float
    valC : float
    valD : float
    
    + get_values() -> (valA, valB, valC, valD)
}


class PreviewWidget{
    slot_update_image()  
}

class SliderWidget{
    current_frame:int
    
    - on_btn_play_click()
    - on_btn_stop_click()
    - on_btn_step_next_click()
    - on_btn_step_prev_click()
    - on_btn_back()
    - on_movie_slider_value_changed()
    - on_start_frame_value_changed()
    - on_end_frame_value_changed()
    + update_frame()
}

```
