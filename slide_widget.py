import PySide6.QtWidgets as wid
import PySide6.QtCore as core

class SlideWidget(wid.QDockWidget):

    def update_frame(self):
        # フレームを更新
        self.movie_slider.setValue(self.current_frame)
        self.current_frame_display.display(self.current_frame)
        self.update()

    def on_timer_timeout(self):
        # タイマーがタイムアウトしたときの処理
        self.current_frame += 1
        if self.current_frame > self.spn_end_frame.value():
            self.on_btn_stop_click()

        # スライダーの値を更新
        self.update_frame()

    def on_btn_play_click(self):
        # 再生ボタンがクリックされたときの処理
        self.timer = core.QTimer()
        self.fps = self.doubleSpinBox_fps.value()
        self.timer.setInterval(int(1/self.fps*1000))
        self.current_frame = self.movie_slider.value()    
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start()
    
    def on_btn_stop_click(self):
        # 停止ボタンがクリックされたときの処理
        self.timer.stop()

    def on_btn_step_next_click(self):
        # 次のステップボタンがクリックされたときの処理
        self.current_frame += 1
        if self.current_frame > self.spn_end_frame.value():
            return
        self.update_frame()

    def on_btn_step_prev_click(self):
        # 前のステップボタンがクリックされたときの処理
        self.current_frame -= 1
        if self.current_frame < self.spn_start_frame.value():
            return
        self.update_frame()

    def on_movie_slider_value_changed(self, value):
        # スライダーの値が変更されたときの処理
        self.current_frame = value
        self.update_frame()

    def on_btn_back_click(self):
        # バックボタンがクリックされたときの処理
        self.current_frame = self.spn_start_frame.value()
        self.update_frame()

    def on_start_frame_value_changed(self, value):
        # 開始フレームの値が変更されたときの処理
        self.movie_slider.setRange(value, self.spn_end_frame.value())

    def on_end_frame_value_changed(self, value):
        # 終了フレームの値が変更されたときの処理
        self.movie_slider.setRange(self.spn_start_frame.value(), value)

    def __init__(self, parent=None):
        super(SlideWidget, self).__init__(parent)

        # currentFrame
        self.current_frame = 0

        # create -------------------------------------------
        # play slider
        self.movie_slider = wid.QSlider(core.Qt.Horizontal)

        # play control 
        self.spn_start_frame = wid.QSpinBox()
        self.spn_end_frame = wid.QSpinBox()
        self.btn_play = wid.QPushButton('Play')
        self.btn_stop = wid.QPushButton('Stop')
        self.btn_back = wid.QPushButton('Back')
        self.btn_step_next = wid.QPushButton('Next')
        self.btn_step_prev = wid.QPushButton('Prev')

        # fps control
        self.dobuleSpinBox_fps_label = wid.QLabel("FPS")
        self.doubleSpinBox_fps = wid.QDoubleSpinBox()

        # current frame display
        self.current_frame_label = wid.QLabel('Current Frame')
        self.current_frame_display = wid.QLCDNumber()

        # event -------------------------------------------

        # btn_event
        self.btn_play.clicked.connect(self.on_btn_play_click)
        self.btn_stop.clicked.connect(self.on_btn_stop_click)
        self.btn_step_next.clicked.connect(self.on_btn_step_next_click)
        self.btn_step_prev.clicked.connect(self.on_btn_step_prev_click)
        self.btn_back.clicked.connect(self.on_btn_back_click)
        # slider_event
        self.movie_slider.valueChanged.connect(self.on_movie_slider_value_changed)
        
        self.spn_start_frame.valueChanged.connect(self.on_start_frame_value_changed)
        self.spn_end_frame.valueChanged.connect(self.on_end_frame_value_changed)    

        # propety -------------------------------------------
        MAX_FRAME = 10000
        MIN_FRAME = 0
        DEFAULT_FRAME = 100
        # frame range   
        self.spn_start_frame.setRange(MIN_FRAME,MAX_FRAME)
        self.spn_start_frame.setValue(MIN_FRAME)
        self.spn_end_frame.setRange(MIN_FRAME,MAX_FRAME)
        self.spn_end_frame.setValue(DEFAULT_FRAME)

        # slider
        self.movie_slider.setRange(MIN_FRAME,DEFAULT_FRAME)

        # fps
        self.doubleSpinBox_fps.setRange(1, 60)
        self.doubleSpinBox_fps.setValue(30)

        # layout -------------------------------------------
        contena = wid.QWidget()

        # frame range
        layout_frame_range = wid.QHBoxLayout()
        layout_frame_range.addWidget(wid.QLabel('Start Frame'))
        layout_frame_range.addWidget(self.spn_start_frame)
        layout_frame_range.addWidget(wid.QLabel('End Frame'))
        layout_frame_range.addWidget(self.spn_end_frame)

        # play controls
        layout_play_controls =  wid.QHBoxLayout()
        layout_play_controls.addWidget(self.btn_play)
        layout_play_controls.addWidget(self.btn_stop)
        layout_play_controls.addWidget(self.btn_back)
        layout_play_controls.addWidget(self.btn_step_prev)
        layout_play_controls.addWidget(self.btn_step_next)

        # fps controls & current frame display
        layout_fps = wid.QHBoxLayout()
        layout_fps.addWidget(self.dobuleSpinBox_fps_label)
        layout_fps.addWidget(self.doubleSpinBox_fps)
        layout_fps.addWidget(self.current_frame_label)
        layout_fps.addWidget(self.current_frame_display)

        # master layout
        layout_master = wid.QVBoxLayout()
        layout_master.addWidget(self.movie_slider)
        layout_master.addLayout(layout_frame_range)
        layout_master.addLayout(layout_play_controls)
        layout_master.addLayout(layout_fps)
        contena.setLayout(layout_master)
        
        # set layout
        self.setWidget(contena)

if __name__ == '__main__':
    app = wid.QApplication([])
    slide_widget = SlideWidget()
    slide_widget.show()
    app.exec_()







