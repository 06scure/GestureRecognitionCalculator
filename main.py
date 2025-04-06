import cv2
from HandDetector import HandDetector
from Calculator import Calculator


detector = HandDetector()
calc = Calculator()

detector.cap.set(3, 1280)
detector.cap.set(4, 720)

while True:
    frame = detector.update()
    if frame is None:
        # 读取不到摄像头
        break

    positions = detector.get_hand_positions()
    info = detector.get_hand_info()
    button_value = 0

    for hand in positions:
        for pid, x, y in hand:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), cv2.FILLED)

    if info:
        palm, status = info
        # 获取手掌坐标和状态
        button_value = calc.check_hand_input(palm, status)
        # 绘制掌心位置
        cv2.circle(frame, palm, 10, (0, 0, 255), -1)  # 红色大圆表示掌心
        # 显示状态文字
        cv2.putText(frame, f'Status: {status}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    if button_value:
        calc.set_equation(calc.myEquation + button_value)
    calc.draw(frame)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

detector.release()