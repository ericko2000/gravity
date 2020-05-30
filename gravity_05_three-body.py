
import numpy as np
import random
from tkinter import *
import time


# 畢氏定理求斜邊長度公式
def norm(a):
    return (a[0] ** 2 + a[1] ** 2) ** 0.5


# 計算兩物件的重力轉換成步幅函數
def step_by_gravity(obj1, obj2):
    norm_of_normal = norm([obj1.center[0] - obj2.center[0], obj1.center[1] - obj2.center[1]])  # 法線向量長度，
    normal12 = [(obj2.center[0] - obj1.center[0]) / norm_of_normal,
                (obj2.center[1] - obj1.center[1]) / norm_of_normal]  # obj1 射向 obj2 的法線單位向量
    normal21 = [(obj1.center[0] - obj2.center[0]) / norm_of_normal,
                (obj1.center[1] - obj2.center[1]) / norm_of_normal]  # obj2 射向 obj1 的法線單位向量
    g_constant = 0.0000000002

    r_square = norm_of_normal * norm_of_normal
    temp_v1_delta = g_constant * obj2.mass / r_square / 2
    temp_v1_step = [normal12[0] * temp_v1_delta, normal12[1] * temp_v1_delta]
    temp_v2_delta = g_constant * obj1.mass / r_square / 2
    temp_v2_step = [normal21[0] * temp_v2_delta, normal21[1] * temp_v2_delta]

    # 計算加速度作用後的速度（單位時間之位移）
    obj1.step_x += temp_v1_step[0]
    obj1.step_y += temp_v1_step[1]
    obj1.step = norm([obj1.step_x, obj1.step_y])
    obj2.step_x += temp_v2_step[0]
    obj2.step_y += temp_v2_step[1]
    obj2.step = norm([obj2.step_x, obj2.step_y])

    if obj1.step_x != 0:  # 計算加速度作用後 obj1 的位移角度
        obj1.theta = ((np.arctan(obj1.step_y / obj1.step_x) if obj1.step_x > 0 else np.pi + np.arctan(
            obj1.step_y / obj1.step_x)) * 180 / np.pi) % 360  # 計算角度
    else:
        obj1.theta = 90 if obj1.step_y >= 0 else 270

    if obj2.step_x != 0:  # 計算加速度作用後 obj2 的位移角度
        obj2.theta = ((np.arctan(obj2.step_y / obj2.step_x) if obj2.step_x > 0 else np.pi + np.arctan(
            obj2.step_y / obj2.step_x)) * 180 / np.pi) % 360  # 計算角度
    else:
        obj2.theta = 90 if obj2.step_y >= 0 else 270


class Ball:
    cid = 0

    def __new__(cls, *args, **kwargs):
        cls.cid += 1
        return object.__new__(cls)

    def __init__(self, canvas, width, height, sid, radius=5, theta=random.randint(0, 360), step=random.randint(2, 7),
                 color='blue', position=None):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.radius = radius  # 小球徑大小
        self.mass = (self.radius * 100) ** 4  # 小球質量
        self.theta = theta  # 隨機產生小球移動的角度
        self.step = step  # 隨機產生小球的步幅 預設 (2, 3)
        self.step_x = np.cos(self.theta / 180 * np.pi) * self.step  # x 的位移幅度
        self.step_y = np.sin(self.theta / 180 * np.pi) * self.step  # y 的位移幅度
        self.color = color
        self.tag = str(sid) + str(self.cid)  # 刪除 canvas 物件時需用到的標籤
        self.canvas_id = self.canvas.create_oval(0, 0, self.radius * 2, self.radius * 2, fill=self.color,
                                                 outline=self.color, tag=self.tag)  # 產生小球物件
        if position:
            self.canvas.move(self.canvas_id, position[0], position[1])  # 預設出生點位
            self.position = self.canvas.coords(self.canvas_id)  # 呼叫小球的位置
        else:
            self.canvas.move(self.canvas_id, random.randint(840, self.width - 40 - self.radius),
                             random.randint(40, self.height - 40 - self.radius))  # 隨機安排出生點位
            self.position = self.canvas.coords(self.canvas_id)  # 呼叫小球的位置
        self.center = [(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]  # 球心位置

    def moveAction(self):  # 移動之執行函數
        self.canvas.move(self.canvas_id, self.step_x, self.step_y)  # 固定的步幅和角度
        self.position = self.canvas.coords(self.canvas_id)  # 呼叫小球的位置
        self.center = [(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]  # 更新小球的球心


def main():
    ball_n = 6  # 粒子總數
    width = 1280  # 視窗寬度
    height = 768  # 視窗高度
    root = Tk()  # 根視窗
    root.title('Eric\'s Elastic Collision')  # 視窗標題
    canvas = Canvas(root, width=width, height=height, bg='grey')  # 設定畫布
    canvas.grid(row=0, column=0, rowspan=3)  # 畫布定位

    canvas.create_line(20, 20, 1260, 20, 1260, 748, 20, 748, 20, 20, width=10, fill='black', tag='base')  # 四邊的框

    ball = []  # 粒子物件串列初始化
    rr1 = 250
    ss1 = 0.75
    mm1 = 6.8
    for i in range(0, 1):  # 建構粒子物件迴圈
        temp_radius = 10  # random.randint(10, 10)  # 粒子半徑
        temp_position = [width / 2 + rr1, height / 2 + rr1 * np.tan(np.pi / 6)]  # 粒子出生位置
        temp_step = ss1  # random.randint(2, 10)  # 粒子出生步幅
        ball.append(Ball(canvas, width=width, height=height, sid='ball', radius=temp_radius,
                         theta=random.randint(150, 150), step=temp_step, color='yellow',
                         position=[temp_position[0] - temp_radius, temp_position[1] - temp_radius,
                                   temp_position[0], temp_position[1]]))  # 建構粒子物件
        ball[i].mass *= mm1

    for i in range(1, 2):  # 建構粒子物件迴圈
        temp_radius = 10  # random.randint(10, 10)  # 粒子半徑
        temp_position = [width / 2 - rr1, height / 2 + rr1 * np.tan(np.pi / 6)]  # 粒子出生位置
        temp_step = ss1  # random.randint(2, 10)  # 粒子出生步幅
        ball.append(Ball(canvas, width=width, height=height, sid='ball', radius=temp_radius,
                         theta=random.randint(270, 270), step=temp_step, color='red',
                         position=[temp_position[0] - temp_radius, temp_position[1] - temp_radius,
                                   temp_position[0], temp_position[1]]))  # 建構粒子物件
        ball[i].mass *= mm1

    for i in range(2, 3):  # 建構粒子物件迴圈
        temp_radius = 10  # random.randint(10, 10)  # 粒子半徑
        temp_position = [width / 2, height / 2 - rr1 * 2 * np.tan(np.pi / 6)]  # 粒子出生位置
        temp_step = ss1  # random.randint(2, 10)  # 粒子出生步幅
        ball.append(Ball(canvas, width=width, height=height, sid='ball', radius=temp_radius,
                         theta=random.randint(30, 30), step=temp_step, color='green',
                         position=[temp_position[0] - temp_radius, temp_position[1] - temp_radius,
                                   temp_position[0], temp_position[1]]))  # 建構粒子物件
        ball[i].mass *= mm1

    rr2 = 38
    ss2 = 3.315
    mm2 = 0.12
    for i in range(3, 4):  # 建構粒子物件迴圈
        temp_radius = 3  # random.randint(10, 10)  # 粒子半徑
        temp_position = [width / 2 + rr1 + rr2 * np.cos(120 / 180 * np.pi), height / 2 + rr1 * np.tan(np.pi / 6) + rr2 * np.sin(120 / 180 * np.pi)]  # 粒子出生位置
        temp_step = ss2  # random.randint(2, 10)  # 粒子出生步幅
        ball.append(Ball(canvas, width=width, height=height, sid='ball', radius=temp_radius,
                         theta=random.randint(210, 210), step=temp_step, color='yellow',
                         position=[temp_position[0] - temp_radius, temp_position[1] - temp_radius,
                                   temp_position[0], temp_position[1]]))  # 建構粒子物件
        ball[i].mass *= mm2

    for i in range(4, 5):  # 建構粒子物件迴圈
        temp_radius = 3  # random.randint(10, 10)  # 粒子半徑
        temp_position = [width / 2 - rr1 + rr2 * np.cos(240 / 180 * np.pi), height / 2 + rr1 * np.tan(np.pi / 6) + rr2 * np.sin(240 / 180 * np.pi)]  # 粒子出生位置
        temp_step = ss2  # random.randint(2, 10)  # 粒子出生步幅
        ball.append(Ball(canvas, width=width, height=height, sid='ball', radius=temp_radius,
                         theta=random.randint(330, 330), step=temp_step, color='red',
                         position=[temp_position[0] - temp_radius, temp_position[1] - temp_radius,
                                   temp_position[0], temp_position[1]]))  # 建構粒子物件
        ball[i].mass *= mm2

    for i in range(5, 6):  # 建構粒子物件迴圈
        temp_radius = 3  # random.randint(10, 10)  # 粒子半徑
        temp_position = [width / 2 + rr2, height / 2 - rr1 * 2 * np.tan(np.pi / 6)]  # 粒子出生位置
        temp_step = ss2  # random.randint(2, 10)  # 粒子出生步幅
        ball.append(Ball(canvas, width=width, height=height, sid='ball', radius=temp_radius,
                         theta=random.randint(90, 90), step=temp_step, color='green',
                         position=[temp_position[0] - temp_radius, temp_position[1] - temp_radius,
                                   temp_position[0], temp_position[1]]))  # 建構粒子物件
        ball[i].mass *= mm2

    root.update()  # 初始視窗展現
    time.sleep(1)  # 迴圈之前的等待時間

    run = 0  # 回合數
    track = []
    for i in range(ball_n):
        track.append([ball[i].center[0], ball[i].center[1]])  # 軌跡起始值

    # 開始主迴圈
    while True:
        run += 1
        for i in range(ball_n):  # 遍例所有的球
            ball[i].moveAction()  # 執行位移函數

        # 執行重力函數
        for i in range(ball_n):
            for j in range(i + 1, ball_n):
                if run > 5:  # 啟動重力的 run 數
                    step_by_gravity(ball[i], ball[j])  # 呼叫重力函數

        canvas.delete('track')  # 清除上一次的軌跡
        for i in range(ball_n):  # 插入新軌跡座標
            track[i].insert(0, ball[i].center[1])
            track[i].insert(0, ball[i].center[0])

            if len(track[i]) > 300:  # 軌跡長度
                del track[i][-2:]  # 刪除末二筆（一對座標）
            canvas.create_line(*track[i], width=2, fill=ball[i].color, tag='track')  # 新繪製軌跡

        root.update()  # 視窗更新
        time.sleep(0.000)  # 調整間隔時間


if __name__ == '__main__':
    main()






