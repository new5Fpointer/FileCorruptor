# components/replace_selector.py
import tkinter as tk
from tkinter import ttk
from custom_widgets import ModernEntry

class ReplaceSelector(ttk.LabelFrame):
    def __init__(self, master, bg_color, fg_color, accent_color):
        super().__init__(master, text=" 替换值设置 ", padding=(10, 10), style="Custom.TLabelframe")
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.accent = accent_color
        
        # 替换模式选择
        replace_mode_frame = tk.Frame(self, bg=bg_color)
        replace_mode_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            replace_mode_frame, 
            text="替换方式:", 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.replace_mode = tk.StringVar(value="random")
        
        # 替换模式单选按钮
        modes = [
            ("随机字节", "random"),
            ("替换为 0x00", "zero"),
            ("替换为 0xFF", "ff"),
            ("自定义值", "custom")
        ]
        
        for i, (text, value) in enumerate(modes):
            rb = tk.Radiobutton(
                replace_mode_frame, 
                text=text, 
                variable=self.replace_mode, 
                value=value,
                bg=bg_color, 
                fg=fg_color, 
                selectcolor=bg_color,
                command=self._update_replace_mode
            )
            rb.pack(side=tk.LEFT, padx=(0, 10))
        
        # 自定义值输入框
        custom_frame = tk.Frame(self, bg=bg_color)
        custom_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            custom_frame, 
            text="自定义值:", 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.custom_entry = ModernEntry(
            custom_frame, 
            width=100, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.custom_entry.pack(side=tk.LEFT)
        self.custom_entry.insert(0, "0x55")
        
        # 提示标签
        tk.Label(
            custom_frame, 
            text="(格式: 0xXX 或 十进制数)", 
            bg=bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # 初始更新替换模式显示
        self._update_replace_mode()
    
    def _update_replace_mode(self):
        mode = self.replace_mode.get()
        if mode == "custom":
            self.custom_entry.configure(state="normal")
        else:
            self.custom_entry.configure(state="disabled")
    
    def get_replace_value(self):
        mode = self.replace_mode.get()
        if mode == "random":
            return "random"
        elif mode == "zero":
            return "0x00"
        elif mode == "ff":
            return "0xFF"
        else:  # custom
            return self.custom_entry.get()