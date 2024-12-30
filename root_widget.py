import PySide6.QtWidgets as wid
import PySide6.QtGui as gui
import PySide6.QtCore as core
import preview_widget as pw
import control_widget as cw
import file_widget as fw
import slide_widget as sw
import file_list_loader as fl   
import progress_bar_widget as pb 
import cv2
import numpy as np

class RootWidget(wid.QMainWindow):

    # シグナル
    signal_send_image = core.Signal(np.ndarray)
    signal_send_frame_min_max = core.Signal(int,int)

    def __init__(self):
        super().__init__()

        # variable
        # 画像リスト
        self.tracking_flag = False
        self.img_lst = []
        self.akaze = cv2.AKAZE_create() # type: ignore
        
        # CSRTトラッカーを作成
        self.tracker = cv2.TrackerCSRT_create() # type: ignore

        # propety
        self.setWindowTitle("Movie Player")

        # crate
        self.preview_window = pw.PreviewWidget()
        self.controle_window = cw.ControleWidget()
        self.file_windows = fw.FileWidget()
        self.slide_window = sw.SlideWidget()

        # event start ---------------------------------------------------------------
        # ファイルをロードしたとき画像リストを更新
        self.file_windows.emmit_signal_getfiles_abs_path.connect(self.slot_load_image_start)

        # スライドウィンドウのフレームが変更されたとき画像を処理する
        self.slide_window.signal_frame_changed.connect(self.slot_update_frame)

        # プレビューウィンドウに画像を送信
        self.signal_send_image.connect(self.preview_window.slot_update_image)   

        # スライドウィンドウにフレームの最小値と最大値を送信
        self.signal_send_frame_min_max.connect(self.slide_window.slot_frame_min_max)

        # トラッカーを初期化
        self.preview_window.signal_tarcker_update.connect(self.slot_tracker_init)
        # event end -----------------------------------------------------------------
        
        # layout
        self.setCentralWidget(self.preview_window)
        self.addDockWidget(core.Qt.DockWidgetArea.RightDockWidgetArea, 
                           self.controle_window)
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea,
                           self.slide_window)
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea,
                           self.file_windows)

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

    # トラッカーを初期化
    def slot_tracker_init(self,rect:core.QRectF):
        self.tracking_flag = True

        img = self.img_lst[self.current_frame]
        img_height,img_width,channel = img.shape # type: ignore
        
        ratio_width = img_width / self.preview_window.contentsRect().width()
        ratio_height = img_height / self.preview_window.contentsRect().height()

        x      = int(rect.x() * ratio_width)
        y      = int(rect.y() * ratio_height)
        width  = int(rect.width() * ratio_width)
        height = int(rect.height() * ratio_height)

        self.tracker.init(img,(x,y,width,height))

    # プログレスばーを作製しファイルリストをロードマネージャに引き渡す--------------------- 
    def slot_load_image_start(self,files_abs_path:list):
        self.img_lst.clear()
        # プログレスバーを作成
        self.progress_bar = pb.ProgressBarWidget(0,len(files_abs_path))
        # ファイルリストをロードマネージャに引き渡す
        self.file_loader = fl.FileListLoader(files_abs_path)

    # ファイルリストをロードマネージャから受け取る---------------------------------------------
    def slot_file_load_progress(self,value:int):
        self.progress_bar.setValue(value)
        if self.progress_bar.max_val <= value:
            self.progress_bar.close()

    # プログレスバーを閉じる ------------------------------------------------------------------
    def slot_file_load_end(self):
        # スライドウィンドウにフレームの最小値と最大値を送信
        self.progress_bar.close()
        self.signal_send_frame_min_max.emit(0,len(self.img_lst)-1)

    # -----------------------------------------------------------------------------------------


    # スライドウィンドウのフレームが変更されたとき画像を処理する
    def slot_update_frame(self,frame:int):
        self.current_frame = frame
        img = self.img_lst[self.current_frame]

        # 特徴点を描画するかどうか
        if self.controle_window.checkBox_featurePoint.isChecked():
            # 特徴点抽出
            kp, des = self.akaze.detectAndCompute(img, None)
            # 特徴点を描画
            img = cv2.drawKeypoints(img, kp, None, color=(0, 0, 255))

        # トラッカーを更新frame
        if self.tracking_flag:
            # debug
            success, bbox = self.tracker.update(img)
            if success:
                # トラッキング成功: バウンディングボックスを描画
                x, y, w, h = map(int, bbox)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Tracking", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # トラッキング失敗
                cv2.putText(img, "Lost Tracking", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # 画像をリサイズ
        img_height, img_width,tmp  = img.shape
        pw_height = self.preview_window.contentsRect().height()
        pw_width = self.preview_window.contentsRect().width()
        img_ratio_height = pw_height / img_height
        img_ratio_width = pw_width / img_width
        img = cv2.resize(img, (int(img_width*img_ratio_width), int(img_height*img_ratio_height)))

        # 画像をピックスマップに変換
        img = self.ndarray_to_qpixmap(img)
        # プレビューウィンドウに画像を送信
        self.signal_send_image.emit(img) 

    # slot end ------------------------------------------------------------------

