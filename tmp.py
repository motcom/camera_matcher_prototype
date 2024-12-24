
import cv2

# ビデオキャプチャ（カメラを使用する場合は引数を0に設定）
video = cv2.VideoCapture(0)  # カメラ
# video = cv2.VideoCapture('video.mp4')  # 動画ファイルの場合

# CSRTトラッカーを作成
tracker = cv2.TrackerCSRT_create()

# 最初のフレームを読み込む
ret, frame = video.read()
if not ret:
    print("ビデオの読み込みに失敗しました。")
    video.release()
    exit()

# トラッキングするオブジェクトの領域を手動で選択
bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)

# トラッカーを初期化
tracker.init(frame, bbox)

while True:
    # フレームを取得
    ret, frame = video.read()
    if not ret:
        print("ビデオの最後に到達しました。")
        break

    # トラッカーを更新
    success, bbox = tracker.update(frame)

    if success:
        # トラッキング成功: バウンディングボックスを描画
        x, y, w, h = map(int, bbox)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        # トラッキング失敗
        cv2.putText(frame, "Lost Tracking", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # フレームを表示
    cv2.imshow("CSRT Tracker", frame)

    # ESCキーで終了
    if cv2.waitKey(1) & 0xFF == 27:
        break

# リソースを解放
video.release()
cv2.destroyAllWindows()
