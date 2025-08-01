# cursor.py
import tkinter as tk

class PureCursor:
    """光标控件"""
    def __init__(self, canvas, x=0, y=0, height=14, width=1, 
                 color="#ffffff", blink_speed=450):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.blink_speed = blink_speed
        self.visible = True
        self.blink_id = None
        self.last_blink_time = 0
        
        # 创建光标主体
        self.cursor_id = canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=color, outline="", width=0
        )
    
    def move(self, x, y):
        """平滑移动光标到新位置"""
        # 记录当前可见状态
        was_visible = self.visible
        
        # 取消当前闪烁计时
        if self.blink_id:
            self.canvas.after_cancel(self.blink_id)
            self.blink_id = None
        
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
        
        # 保持原有可见状态
        if was_visible:
            self.canvas.itemconfig(self.cursor_id, fill=self.color)
        
        # 重新开始闪烁计时
        self.start_blinking()
    
    def blink(self):
        """优化后的闪烁动画"""
        self.visible = not self.visible
        
        # 只更新可见性，不改变位置
        if self.visible:
            self.canvas.itemconfig(self.cursor_id, fill=self.color)
        else:
            self.canvas.itemconfig(self.cursor_id, fill="")
        
        # 安排下一次闪烁
        self.blink_id = self.canvas.after(self.blink_speed, self.blink)
    
    def start_blinking(self):
        """开始/恢复闪烁动画"""
        if self.blink_id is not None:
            self.canvas.after_cancel(self.blink_id)
        
        # 立即显示光标
        self.visible = True
        self.canvas.itemconfig(self.cursor_id, fill=self.color)
        
        # 开始闪烁循环
        self.blink_id = self.canvas.after(self.blink_speed, self.blink)
    
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