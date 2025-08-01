# entry.py
from tkinter import font as tkfont
import tkinter as tk
import math
from .cursor import PureCursor

class ModernEntry(tk.Canvas):
    """优化后的输入框，延迟创建光标"""
    _active_cursor = None  # 类变量，记录当前激活光标的输入框

    def __init__(self, master, width=180, height=30, radius=2,
                 bg_color="#1e1e1e", border_normal="#404040",
                 border_focus="#4ec9b0", text_color="#ffffff",
                 font_family="微软雅黑", font_size=10, **kwargs):
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bd=0, bg=bg_color)
        self.bg_color = bg_color
        self.border_normal = border_normal
        self.border_focus = border_focus
        self.text_color = text_color
        self._cursor_pos = 0
        self._text = ""
        self._font = tkfont.Font(family=font_family, size=font_size)
        
        # 使用固定光标高度
        self._cursor_height = 17
        
        # 绘制圆角边框
        self.rect_id = self._draw_rounded_rect(
            1, 1, width-1, height-1,
            fill=bg_color,
            outline=border_normal,
            radius=radius
        )

        # 文本显示 - 垂直居中
        font_height = self._font.metrics("linespace")
        self.text_x = 8
        self.text_y = (height - font_height) // 2
        
        # 计算光标垂直偏移量
        self.cursor_y_offset = (font_height - self._cursor_height) // 2
        if self.cursor_y_offset < 0:
            self.cursor_y_offset = 0
            
        self.text_id = self.create_text(
            self.text_x, self.text_y,
            text="",
            anchor="nw",
            fill=self.text_color,
            font=self._font
        )
        
        # 优化：延迟创建光标对象
        self.cursor = None  # 初始时不创建光标
        
        # 事件绑定
        self.bind("<Button-1>", self._on_click)
        self.bind("<Key>", self._on_key_press)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event=None):
        """获得焦点时激活光标"""
        # 优化：延迟创建光标
        if self.cursor is None:
            self._create_cursor()
        
        if ModernEntry._active_cursor:
            ModernEntry._active_cursor.cursor.stop_blinking()
        
        ModernEntry._active_cursor = self
        self.itemconfig(self.rect_id, outline=self.border_focus)
        
        if self.cursor:
            self.cursor.start_blinking()
    
    def _create_cursor(self):
        """在需要时创建光标"""
        if self.cursor is not None:
            return
            
        self.cursor = PureCursor(
            self,
            x=self.text_x,
            y=self.text_y + self.cursor_y_offset,
            height=self._cursor_height,
            width=1,
            color="#6bd8c9",
            blink_speed=450
        )
        # 初始不显示
        self.cursor.stop_blinking()
    
    def _on_focus_out(self, event=None):
        """失去焦点时隐藏光标"""
        if ModernEntry._active_cursor == self:
            if self.cursor:
                self.cursor.stop_blinking()
            ModernEntry._active_cursor = None
        self.itemconfig(self.rect_id, outline=self.border_normal)

    def _on_click(self, event):
        """点击时计算光标位置"""
        # 确保光标已创建
        if self.cursor is None:
            self._create_cursor()
        
        click_x = event.x
        text_width = self._font.measure(self._text)
        
        # 简单逻辑：如果点击在文本右侧，光标放末尾
        if click_x > self.text_x + text_width:
            self._cursor_pos = len(self._text)
        else:
            # 否则遍历字符，找到最近的光标位置
            for i in range(len(self._text) + 1):
                substr = self._text[:i]
                substr_width = self._font.measure(substr)
                if click_x <= self.text_x + substr_width:
                    self._cursor_pos = i
                    break
        
        self._update_cursor()
        self.focus_set()  # 确保点击后输入框获得焦点

    def _on_key_press(self, event):
        """处理键盘输入"""
        # 确保光标已创建
        if self.cursor is None:
            self._create_cursor()
        
        if event.keysym == "BackSpace":
            if self._cursor_pos > 0:
                self._text = self._text[:self._cursor_pos-1] + self._text[self._cursor_pos:]
                self._cursor_pos -= 1
        elif event.keysym == "Delete":
            if self._cursor_pos < len(self._text):
                self._text = self._text[:self._cursor_pos] + self._text[self._cursor_pos+1:]
        elif event.keysym == "Left":
            if self._cursor_pos > 0:
                self._cursor_pos -= 1
        elif event.keysym == "Right":
            if self._cursor_pos < len(self._text):
                self._cursor_pos += 1
        elif event.keysym == "Home":
            self._cursor_pos = 0
        elif event.keysym == "End":
            self._cursor_pos = len(self._text)
        elif len(event.char) > 0 and event.char.isprintable():
            self._text = self._text[:self._cursor_pos] + event.char + self._text[self._cursor_pos:]
            self._cursor_pos += 1
        
        self._update_text()
        self._update_cursor()

    def _update_text(self):
        """更新显示的文本"""
        self.itemconfig(self.text_id, text=self._text)
        
    def _update_cursor(self):
        """更新光标位置"""
        substr = self._text[:self._cursor_pos]
        cursor_x = self.text_x + self._font.measure(substr)
        cursor_y = self.text_y + self.cursor_y_offset
        
        # 如果光标存在，更新其位置
        if self.cursor:
            self.cursor.move(cursor_x, cursor_y)

    def get(self):
        """获取输入框内容"""
        return self._text

    def insert(self, idx, txt):
        """插入文本"""
        self._text = self._text[:idx] + txt + self._text[idx:]
        self._cursor_pos = idx + len(txt)
        self._update_text()
        self._update_cursor()

    def delete(self, fst, lst=None):
        """删除文本"""
        # 处理特殊索引值
        if fst == "end" or fst == tk.END:
            fst = len(self._text)
        
        if lst is None:
            lst = fst + 1
        elif lst == "end" or lst == tk.END:
            lst = len(self._text)
        
        # 确保索引是整数
        try:
            fst = int(fst)
            lst = int(lst)
        except (ValueError, TypeError):
            return  # 无效索引，不做处理
        
        # 边界检查
        if fst < 0:
            fst = 0
        if lst > len(self._text):
            lst = len(self._text)
        
        # 执行删除
        self._text = self._text[:fst] + self._text[lst:]
        self._cursor_pos = fst
        self._update_text()
        self._update_cursor()

    def _draw_rounded_rect(self, x1, y1, x2, y2, **kwargs):
        """绘制圆角矩形"""
        radius = kwargs.pop('radius', 2)
        points = []
        top = y1 + radius
        bottom = y2 - radius
        left = x1 + radius
        right = x2 - radius
        
        points.extend([x1, top])
        points.extend(self._get_arc_points(left, top, radius, math.pi, math.pi*1.5))
        points.extend([right, y1])
        points.extend(self._get_arc_points(right, top, radius, math.pi*1.5, math.pi*2))
        points.extend([x2, bottom])
        points.extend(self._get_arc_points(right, bottom, radius, 0, math.pi*0.5))
        points.extend([left, y2])
        points.extend(self._get_arc_points(left, bottom, radius, math.pi*0.5, math.pi))
        points.extend([x1, top])  # 闭合路径
        
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def _get_arc_points(self, cx, cy, radius, start_angle, end_angle, segments=8):
        """生成圆弧点集"""
        points = []
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * i / segments
            points.extend([cx + radius * math.cos(angle), cy + radius * math.sin(angle)])
        return points