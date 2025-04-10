import cv2
from HandDetector import HandDetector
from Calculator import Calculator


def process_hand_input(calc: Calculator, hand_info: tuple) -> str:
    """
    处理手部输入并返回按钮值
    :param hand_info: 包含手掌坐标和状态的元组 (palm_position, status)
    :return: 检测到的按钮值 (空字符串表示无输入)
    """
    palm_pos, status = hand_info
    return calc.check_hand_input(palm_pos, status)


def draw_hand_landmarks(frame, positions: list) -> None:
    """在图像上绘制手部关键点"""
    for hand in positions:
        for pid, x, y in hand:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), cv2.FILLED)


def draw_status_info(frame, status: str) -> None:
    """在图像上绘制状态信息"""
    cv2.putText(frame,
                f'Status: {status}',
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2)


def main():
    # 初始化模块
    detector = HandDetector()
    calc = Calculator()

    while True:
        # 读取摄像头帧
        frame = detector.update()
        if frame is None:
            print("无法读取摄像头输入")
            break

        # 获取手部信息
        positions = detector.get_hand_positions()
        hand_info = detector.get_hand_info()

        # 处理手部输入
        current_input = ""
        if hand_info:
            # 绘制掌心位置
            palm_pos, status = hand_info
            cv2.circle(frame, palm_pos, 10, (0, 0, 255), -1)

            # 处理输入并显示状态
            current_input = process_hand_input(calc, hand_info)
            draw_status_info(frame, status)

        # 绘制手部关键点
        if positions:
            draw_hand_landmarks(frame, positions)

        # 更新计算器显示
        if current_input:
            calc.set_equation(calc.myEquation + current_input)
        calc.draw(frame)

        # 显示画面
        cv2.imshow("GestureRecognitionCalculator", frame)

        # ESC键退出
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 释放资源
    detector.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()