``` plantuml

RootWidget --> ControlWidget
RootWidget --> FileWidget
RootWidget --> PreviewWidget
RootWidget --> SliderWidget

class RootWidget{
    preview_window : PreviewWidget
    control_window : ControlWidget
    file_window    : FileWidget
    update_all()
}

class FileWidget{
    load_path      : str
    save_path      : str
    files_abs_path : List[str]
    get_files_abs_path() -> List[str]
}

class ControlWidget{
    valA : float
    valB : float
    valC : float
    valD : float
    
    get_values() -> (valA, valB, valC, valD)
}

class SliderWidget{
    current_val : int
    start_val   : int
    end_val     : int
}

class PreviewWidget{
    render_image()  
}


```
