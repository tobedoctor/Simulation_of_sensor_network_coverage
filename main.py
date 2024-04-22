import tkinter as tk
import random
import win32gui
import cv2
import time
import math
from PIL import Image, ImageGrab


class Window:
    def __init__(self, master):
        self.root = master
        self.createpage()
        self.run()

    def createpage(self):
        self.root.geometry('910x510')
        # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
        self.root.resizable(width=False, height=False)

        tk.LabelFrame(self.root, text='|参数|', fg='black', padx=10, pady=10,
                      font='Verdana 10 bold').place(x=10, y=10, height=180, width=290)
        tk.Label(self.root, text='传感器数量：', fg='black').place(x=15, y=45)
        tk.Label(self.root, text='传感器探测半径：', fg='black').place(x=15, y=115)
        # 创建一个输入框，以输入内容
        self.inputnum_text = tk.StringVar()
        self.inputnum = tk.Entry(self.root, textvariable=self.inputnum_text)
        self.inputnum.place(x=120, y=50)

        self.inputradius_text = tk.StringVar()
        self.inputradius = tk.Entry(
            self.root, textvariable=self.inputradius_text)
        self.inputradius.place(x=120, y=120)

        tk.LabelFrame(self.root, text='|结果|', fg='black', padx=10, pady=10,
                      font='Verdana 10 bold').place(x=10, y=215, height=180, width=290)
        tk.Label(self.root, text='理论覆盖率(%)：', fg='black').place(x=15, y=250)
        tk.Label(self.root, text='实际覆盖率(%)：', fg='black').place(x=15, y=320)

        self.theoryoutput = tk.Text(self.root, width=20, height=1)
        self.theoryoutput.place(x=120, y=255)  # 先创建对象再放置位置，否则会报错

        self.actualoutput = tk.Text(self.root, height=1, width=20)
        self.actualoutput.place(x=120, y=325)

        self.cv = tk.Canvas(self.root, bg='white', height=500, width=600)
        self.cv.place(x=300)
        # 创建按钮
        tk.Button(self.root, text='传感器布置', command=self.circle_create).place(
            x=100, y=400, width=100)
        tk.Button(self.root, text='计算', command=self.Calculation_Area).place(
            x=100, y=460, width=100)

    def Wipe_Data(self):
        # 清空文本框内的内容
        self.theoryoutput.delete(0.0, 'end')
        self.actualoutput.delete(0.0, 'end')

    def CaptureScreen(self):
        # print('执行截图函数')
        HWND = win32gui.GetFocus()  # 获取当前窗口句柄
        self.rect = win32gui.GetWindowRect(HWND)  # 获取当前窗口坐标
        x = self.rect[0] + 300
        x1 = x + self.cv.winfo_width()
        y = self.rect[1]
        y1 = y + self.cv.winfo_height()
        image = ImageGrab.grab((x, y, x1, y1))
        image.save("second.jpeg", 'jpeg')  # 前面一个参数是保存路径，后面一个参数是保存格式

    def Calculation_Area(self):
        self.CaptureScreen()
        # print('执行计算函数')
        self.Wipe_Data()
        img = cv2.imread("second.jpeg")  # 图片读取
        pictue_size = img.shape
        picture_height = pictue_size[0]
        picture_width = pictue_size[1]
        # 输出长和宽
        # print(picture_height,picture_width)
        All_area = 304416.0
        Proportion_area_white = 0
        Proportion_area_blue = 0
        for a in range(picture_height):
            for b in range(picture_width):
                if img[a, b].all() > 0:
                    Proportion_area_white = Proportion_area_white + 1

        Proportion_area_blue = float(All_area - Proportion_area_white)
        # 计算实际输出
        # print(Proportion_area_blue)
        Occupancy_actual = Proportion_area_blue / All_area
        Occupancy_actual = ('%.12f' % Occupancy_actual)
        Occupancy_actual = float(Occupancy_actual)
        Occupancy_actual = Occupancy_actual * 100
        # 计算理论输出
        # 𝑅 = 1 − 𝑒^−𝑛𝜋𝑟2/𝐴 理论值计算公式
        i = float(self.sensor_num * math.pi *
                  self.sensor_radius * self.sensor_radius)
        Occupancy_theory = (1 - math.exp((i * -1.0) / All_area)) * 100
        # 将得到的值输入到文本框里
        self.theoryoutput.insert('end', Occupancy_theory)
        self.actualoutput.insert('end', Occupancy_actual)

    def circle_create(self):
        # print('执行绘图函数')
        # 清空画图的内容
        self.cv.delete(tk.ALL)
        # 获取在参数里输入的值
        self.sensor_num = self.inputnum.get()
        self.sensor_radius = self.inputradius.get()
        # 转int
        self.sensor_num = int(self.sensor_num)
        self.sensor_radius = int(self.sensor_radius)
        # 做循环开始绘图
        for num in range(1, (self.sensor_num + 1)):
            circle_center_x = random.randint(10, 590)
            circle_center_y = random.randint(10, 490)
            self.cv.create_oval((circle_center_x - self.sensor_radius, circle_center_y - self.sensor_radius,
                                 circle_center_x + self.sensor_radius, circle_center_y + self.sensor_radius),
                                outline='blue',
                                fill='blue'
                                )

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print("*** exception:\n".format(e))


def main():
    window = tk.Tk()
    window.title('SensorHomework Design By HJK')
    Window(window).run()


if __name__ == '__main__':
    main()
