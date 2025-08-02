# components/mode_selector.py
import tkinter as tk
from tkinter import ttk
from custom_widgets import ModernEntry

class ModeSelector(ttk.LabelFrame):
    def __init__(self, master, bg_color, fg_color, accent_color):
        super().__init__(master, text=" 处理模式 ", padding=(10, 10), style="Custom.TLabelframe")
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.accent = accent_color
        
        # 模式选择
        mode_label = tk.Label(
            self, 
            text="选择处理方式:", 
            bg=bg_color, 
            fg=fg_color
        )
        mode_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.mode_var = tk.StringVar(value="interval")
        
        interval_btn = tk.Radiobutton(
            self, 
            text="固定间隔模式", 
            variable=self.mode_var, 
            value="interval",
            bg=bg_color, 
            fg=fg_color, 
            selectcolor=bg_color,
            command=self._update_mode_display
        )
        interval_btn.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        rate_btn = tk.Radiobutton(
            self, 
            text="随机比例模式", 
            variable=self.mode_var, 
            value="rate",
            bg=bg_color, 
            fg=fg_color, 
            selectcolor=bg_color,
            command=self._update_mode_display
        )
        rate_btn.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # 参数设置
        params_frame = tk.Frame(self, bg=bg_color)
        params_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        
        # 间隔参数
        interval_frame = tk.Frame(params_frame, bg=bg_color)
        interval_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            interval_frame, 
            text="间隔字节数:", 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.interval_entry = ModernEntry(
            interval_frame, 
            width=60, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.interval_entry.insert(0, "100")
        self.interval_entry.pack(side=tk.LEFT)
        tk.Label(
            interval_frame, 
            text="字节", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 15))
        
        # 比例参数
        rate_frame = tk.Frame(params_frame, bg=bg_color)
        rate_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            rate_frame, 
            text="损坏比例:", 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.rate_entry = ModernEntry(
            rate_frame, 
            width=60, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.rate_entry.insert(0, "10")
        self.rate_entry.pack(side=tk.LEFT)
        tk.Label(
            rate_frame, 
            text="%", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 15))
        
        # 保护区域
        protect_frame = tk.Frame(params_frame, bg=bg_color)
        protect_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            protect_frame, 
            text="保护区域:", 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            protect_frame, 
            text="头部", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.head_entry = ModernEntry(
            protect_frame, 
            width=50, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.head_entry.insert(0, "1024")
        self.head_entry.pack(side=tk.LEFT)
        
        tk.Label(
            protect_frame, 
            text="字节", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(
            protect_frame, 
            text="尾部", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.tail_entry = ModernEntry(
            protect_frame, 
            width=50, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.tail_entry.insert(0, "1024")
        self.tail_entry.pack(side=tk.LEFT)
        
        tk.Label(
            protect_frame, 
            text="字节", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # 初始显示模式
        self._update_mode_display()
    
    def _update_mode_display(self):
        mode = self.mode_var.get()
        if mode == "interval":
            self.interval_entry.configure(state="normal")
            self.rate_entry.configure(state="disabled")
        else:
            self.interval_entry.configure(state="disabled")
            self.rate_entry.configure(state="normal")
    
    def get_mode(self):
        return self.mode_var.get()
    
    def get_interval(self):
        return int(self.interval_entry.get())
    
    def get_rate(self):
        return float(self.rate_entry.get())
    
    def get_head(self):
        return int(self.head_entry.get())
    
    def get_tail(self):
        return int(self.tail_entry.get())