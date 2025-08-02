# components/file_selector.py
import tkinter as tk
from tkinter import filedialog
from custom_widgets import RoundedButton, ModernEntry

class FileSelector(tk.Frame):
    def __init__(self, master, bg_color, fg_color, accent_color, 
                 input_label="输入文件:", output_label="输出文件:"):
        super().__init__(master, bg=bg_color)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.accent = accent_color
        
        # 输入文件选择
        input_frame = tk.Frame(self, bg=bg_color)
        input_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            input_frame, 
            text=input_label, 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 2))
        
        self.input_entry = ModernEntry(
            input_frame, 
            width=480, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        RoundedButton(
            input_frame, 
            text="浏览...", 
            command=self._select_input,
            width=70, 
            height=26, 
            radius=4,
            button_color="#333333", 
            hover_color="#555555",
            text_color=fg_color
        ).pack(side=tk.LEFT)

        # 输出文件选择
        output_frame = tk.Frame(self, bg=bg_color)
        output_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            output_frame, 
            text=output_label, 
            bg=bg_color, 
            fg=fg_color
        ).pack(side=tk.LEFT, padx=(0, 2))
        
        self.output_entry = ModernEntry(
            output_frame, 
            width=480, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=accent_color, 
            text_color=fg_color
        )
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        RoundedButton(
            output_frame, 
            text="浏览...", 
            command=self._select_output,
            width=70, 
            height=26, 
            radius=4,
            button_color="#333333", 
            hover_color="#555555",
            text_color=fg_color
        ).pack(side=tk.LEFT)
    
    def _select_input(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)
        return path
    
    def _select_output(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)
        return path
    
    def get_input_path(self):
        return self.input_entry.get()
    
    def get_output_path(self):
        return self.output_entry.get()
    
    def set_input_path(self, path):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, path)
    
    def set_output_path(self, path):
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, path)