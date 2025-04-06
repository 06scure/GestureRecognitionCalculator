import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=1,
                 model_complexity=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        # 初始化 MediaPipe Hands 模块
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode,
                                        max_num_hands,
                                        model_complexity,
                                        min_detection_confidence,
                                        min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)  # 默认从摄像头读取
        self.hand_landmarks = []  # 存储每帧手部关键点列表

    def update(self):
        """
        更新图像帧和手部关键点数据
        :return: 返回画好手部连接线的图像帧
        """
        success, img = self.cap.read()
        if not success:
            return None

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        self.hand_landmarks.clear()

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                # 将每只手的关键点坐标提取成列表，保存在 hand_landmarks 中
                single_hand = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    single_hand.append((id, cx, cy))
                self.hand_landmarks.append(single_hand)


        return img

    def get_hand_positions(self):
        """
        返回当前帧中所有手的关键点坐标
        :return: [[(id, x, y), ...], [(id, x, y), ...], ...]
        """
        return self.hand_landmarks

    def release(self):
        """
        释放视频流资源
        """
        self.cap.release()
        cv2.destroyAllWindows()
