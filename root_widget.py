import PySide6.QtWidgets as wid
import PySide6.QtGui as gui
import PySide6.QtCore as core
import preview_widget as pw
import control_widget as cw
import file_widget as fw
import slide_widget as sw
import cv2
import numpy as np

class RootWidget(wid.QMainWindow):
    # シグナル
    signal_send_image = core.Signal(np.ndarray)
    signal_send_frame_min_max = core.Signal(int,int)

    # utility start ---------------------------------------------------------------
    # ndarrayをQPixmapに変換
    def ndarray_to_qpixmap(self,array: np.ndarray) -> gui.QPixmap:
        # 配列の形状確認

        array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
        height, width, channels = array.shape

        if channels == 3:  # RGB
            format = gui.QImage.Format_RGB888
        elif channels == 4:  # RGBA
            format = gui.QImage.Format_RGBA8888
        else:
            raise ValueError("Invalid channels")

        # NumPy配列からQImageを作成
        image = gui.QImage(array.data, width, height, array.strides[0], format)
        return gui.QPixmap.fromImage(image)
    # utility end -----------------------------------------------------------------


    # slot start ----------------------------------------------------------------
    # ファイルをロードしたとき画像リストを更新
    def slot_load_image_list(self,files_abs_path:list):
        FILE_EXTENTION = [".jpg",".png"]

        self.img_lst.clear()
        for filePath in files_abs_path:
            if FILE_EXTENTION[0] in filePath or FILE_EXTENTION[1] in filePath:  
                self.img_lst.append(cv2.imread(filePath))

        # スライドウィンドウにフレームの最小値と最大値を送信
        self.signal_send_frame_min_max.emit(0,len(self.img_lst)-1)

    # スライドウィンドウのフレームが変更されたとき画像を処理する
    def slot_update_frame(self,frame:int):
        img = self.img_lst[frame]

        if self.controle_window.checkBox_featurePoint.isChecked():
            # 特徴点抽出
            kp, des = self.akaze.detectAndCompute(img, None)
            # 特徴点を描画
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255))

        # 画像をリサイズ
        img_height, img_width,tmp  = img.shape
        pw_height = self.preview_window.height()
        img_ratio = pw_height / img_height
        img = cv2.resize(img, (int(img_width*img_ratio), int(img_height*img_ratio)))


        # 画像をピックスマップに変換
        img = self.ndarray_to_qpixmap(img)
        # プレビューウィンドウに画像を送信
        self.signal_send_image.emit(img) 


    # slot end ------------------------------------------------------------------

    def __init__(self):
        super().__init__()

        # variable
        # 画像リスト
        self.img_lst = []
        self.akaze = cv2.AKAZE_create()
        

        # propety
        self.setWindowTitle("Movie Player")

        # crate
        self.preview_window = pw.PreviewWidget()
        self.controle_window = cw.ControleWidget()
        self.file_windows = fw.FileWidget()
        self.slide_window = sw.SlideWidget()

        # event start ---------------------------------------------------------------
        # ファイルをロードしたとき画像リストを更新
        self.file_windows.emmit_signal_getfiles_abs_path.connect(self.slot_load_image_list)

        # スライドウィンドウのフレームが変更されたとき画像を処理する
        self.slide_window.signal_frame_changed.connect(self.slot_update_frame)

        # プレビューウィンドウに画像を送信
        self.signal_send_image.connect(self.preview_window.slot_update_image)   

        # スライドウィンドウにフレームの最小値と最大値を送信
        self.signal_send_frame_min_max.connect(self.slide_window.slot_frame_min_max)
        # event end -----------------------------------------------------------------
        
        
        # layout
        self.setCentralWidget(self.preview_window)
        self.addDockWidget(core.Qt.DockWidgetArea.RightDockWidgetArea, 
                           self.controle_window)
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea,
                           self.slide_window)
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea,
                           self.file_windows)








