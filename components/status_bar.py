# components/status_bar.py
import tkinter as tk

class StatusBar(tk.Label):
    def __init__(self, master, bg_color, fg_color):
        super().__init__(
            master, 
            text="就绪",
            bg="#1e1e1e", 
            fg=fg_color, 
            height=1,
            anchor=tk.W,
            padx=10
        )
        self.status_var = tk.StringVar(value="就绪")
        self.config(textvariable=self.status_var)
    
    def set_status(self, text):
        self.status_var.set(text)
    
    def get_status(self):
        return self.status_var.get()