import cv2

class Calculator:
    def __init__(self, origin=(800, 50), button_size=100,
                 font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=2, font_color=(50, 50, 50),
                 alpha=0.6):
        self.origin = origin  # 左上角起点
        self.delay_counter = 0  # 防抖计数器
        self.button_size = button_size
        self.font = font
        self.font_scale = font_scale
        self.font_color = font_color
        self.alpha = alpha  # 透明度（0-1）
        self.myEquation = ''
        self.buttonListvalues = [['7', '8', '9', '*'],
                                 ['4', '5', '6', '-'],
                                 ['1', '2', '3', '+'],
                                 ['0', '/', '.', '=']]
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        ox, oy = self.origin
        for y in range(4):
            for x in range(4):
                xpos = ox + x * self.button_size
                ypos = oy + 100 + y * self.button_size
                value = self.buttonListvalues[y][x]
                self.buttons.append({
                    'pos': (xpos, ypos),
                    'value': value
                })

    def draw(self, img):
        """在原始图像上绘制带透明背景的计算器"""
        overlay = img.copy()
        ox, oy = self.origin

        # 绘制表达式区域
        cv2.rectangle(overlay, (ox, oy), (ox + 4 * self.button_size, oy + 100), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(overlay, (ox, oy), (ox + 4 * self.button_size, oy + 100), (50, 50, 50), 3)
        cv2.putText(overlay, self.myEquation, (ox + 10, oy + 80),
                    self.font, 3, (0, 0, 0), 3)

        # 绘制所有按键
        for button in self.buttons:
            x, y = button['pos']
            value = button['value']
            cv2.rectangle(overlay, (x, y), (x + self.button_size, y + self.button_size),
                          (225, 225, 225), cv2.FILLED)
            cv2.rectangle(overlay, (x, y), (x + self.button_size, y + self.button_size),
                          (50, 50, 50), 3)
            text_size = cv2.getTextSize(value, self.font, self.font_scale, 2)[0]
            text_x = x + (self.button_size - text_size[0]) // 2
            text_y = y + (self.button_size + text_size[1]) // 2
            cv2.putText(overlay, value, (text_x, text_y),
                        self.font, self.font_scale, self.font_color, 2)

        # 将 overlay 合成回原图
        cv2.addWeighted(overlay, self.alpha, img, 1 - self.alpha, 0, img)

    def set_equation(self, eq):
        self.myEquation = eq

    def get_button_regions(self):
        regions = []
        for button in self.buttons:
            x, y = button['pos']
            regions.append({
                'value': button['value'],
                'x1': x,
                'y1': y,
                'x2': x + self.button_size,
                'y2': y + self.button_size
            })
        return regions

    def check_hand_input(self, palm_pos, hand_status):
        """
        根据掌心坐标和状态，判断是否点击了某个按钮。
        启用防抖机制，处理表达式计算，支持结果后自动清空。
        """
        if self.delay_counter > 0:
            self.delay_counter -= 1
            return

        if hand_status != "fist":
            return

        px, py = palm_pos
        for region in self.get_button_regions():
            if region['x1'] <= px <= region['x2'] and region['y1'] <= py <= region['y2']:
                value = region['value']

                # 如果已经是计算结果，下一次按键清空
                if hasattr(self, 'calculated') and self.calculated:
                    self.myEquation = ''
                    self.calculated = False

                if value == '=':
                    try:
                        result = str(eval(self.myEquation))
                        self.myEquation = result
                    except:
                        self.myEquation = "Error"
                    self.calculated = True  # 标记为“已计算”，等待清空
                else:
                    self.myEquation += value

                self.delay_counter = 20
                break


