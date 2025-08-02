# components/progress_bar.py
import tkinter as tk
from tkinter import ttk

class ProgressBar(tk.Frame):
    def __init__(self, master, bg_color, fg_color, accent_color):
        super().__init__(master, bg=bg_color)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.accent = accent_color
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self, 
            variable=self.progress_var, 
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, padx=10)
        
        # 进度文本
        self.progress_text = tk.StringVar(value="等待开始...")
        progress_label = tk.Label(
            self,
            textvariable=self.progress_text,
            bg=bg_color,
            fg=fg_color,
            font=("微软雅黑", 9)
        )
        progress_label.pack(pady=(5, 0))
    
    def set_progress(self, value):
        self.progress_var.set(value)
    
    def set_progress_text(self, text):
        self.progress_text.set(text)
    
    def reset(self):
        self.progress_var.set(0)
        self.progress_text.set("等待开始...")