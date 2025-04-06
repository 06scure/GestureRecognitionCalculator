from HandDetector import HandDetector
import cv2

detector = HandDetector()

while True:
    frame = detector.update()
    if frame is None:
        break

    positions = detector.get_hand_positions()
    for hand in positions:
        for pid, x, y in hand:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

detector.release()