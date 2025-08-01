import tkinter as tk
import math
import time
from tkinter import font

class PureCursor:
    """纯净极简的光标控件"""
    def __init__(self, canvas, x=0, y=0, height=14, width=1, 
                 color="#ffffff", blink_speed=450):
        """
        初始化光标
        
        参数:
            canvas: 父级Canvas控件
            x, y: 初始位置
            height: 光标高度
            width: 光标宽度
            color: 光标颜色
            blink_speed: 闪烁速度(毫秒)
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.blink_speed = blink_speed
        self.visible = True
        self.blink_id = None
        
        # 创建光标主体 - 简洁的矩形
        self.cursor_id = canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=color, outline="", width=0
        )
        
        # 开始闪烁动画
        self.start_blinking()
    
    def move(self, x, y):
        """移动光标到新位置"""
        # 更新位置
        self.x = x
        self.y = y
        
        # 移动光标主体
        self.canvas.coords(
            self.cursor_id, 
            x, y, 
            x + self.width, 
            y + self.height
        )
    
    def blink(self):
        """光标闪烁动画"""
        self.visible = not self.visible
        
        # 更新光标主体可见性
        if self.visible:
            self.canvas.itemconfig(self.cursor_id, fill=self.color)
        else:
            self.canvas.itemconfig(self.cursor_id, fill="")
        
        # 安排下一次闪烁
        self.blink_id = self.canvas.after(self.blink_speed, self.blink)
    
    def start_blinking(self):
        """开始光标闪烁动画"""
        if self.blink_id is not None:
            self.canvas.after_cancel(self.blink_id)
        self.visible = True  # 重置为可见状态
        self.canvas.itemconfig(self.cursor_id, fill=self.color)
        self.blink()
    
    def stop_blinking(self):
        """停止光标闪烁动画"""
        if self.blink_id is not None:
            self.canvas.after_cancel(self.blink_id)
            self.blink_id = None
        # 确保光标被隐藏
        self.visible = False
        self.canvas.itemconfig(self.cursor_id, fill="")
    
    def set_height(self, height):
        """设置光标高度"""
        self.height = height
        self.canvas.coords(
            self.cursor_id, 
            self.x, self.y, 
            self.x + self.width, 
            self.y + height
        )
    
    def set_color(self, color):
        """设置光标颜色"""
        self.color = color
        if self.visible:
            self.canvas.itemconfig(self.cursor_id, fill=color)
    
    def destroy(self):
        """销毁光标"""
        self.stop_blinking()
        self.canvas.delete(self.cursor_id)