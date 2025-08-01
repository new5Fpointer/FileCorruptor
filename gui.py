# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from custom_widgets import RoundedButton, ModernEntry
from file_corruptor import FileCorruptor

class AdvancedFileCorruptor:
    """文件熵增器GUI界面"""
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        """窗口基本设置"""
        self.root.title("文件熵增器")
        self.root.geometry("600x500")
        self.root.minsize(500, 450)
        self.bg_color = "#252526"
        self.fg_color = "#ffffff"
        self.accent = "#4ec9b0"
        self.root.configure(bg=self.bg_color)

    def _create_widgets(self):
        """创建界面控件"""
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self._create_file_selectors(main_frame)
        self._create_mode_selectors(main_frame)
        self._create_action_button(main_frame)

    def _create_file_selectors(self, parent):
        """创建文件选择区域"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=10, padx=20)

        # 输入文件选择
        tk.Label(frame, text="输入文件:", bg=self.bg_color, fg=self.fg_color
                ).grid(row=0, column=0, sticky="w")
        self.input_entry = ModernEntry(
            frame, width=382, height=26, radius=4,
            bg_color="#333333", border_normal="#404040",
            border_focus=self.accent, text_color=self.fg_color
        )
        self.input_entry.grid(row=0, column=1, sticky="ew", padx=5)
        RoundedButton(frame, text="浏览", command=self._select_input,
                     width=80, height=26, radius=4,
                     button_color="#333333", hover_color="#555555",
                     text_color=self.fg_color
                    ).grid(row=0, column=2, padx=5)

        # 输出文件选择
        tk.Label(frame, text="输出文件:", bg=self.bg_color, fg=self.fg_color
                ).grid(row=1, column=0, sticky="w", pady=10)
        self.output_entry = ModernEntry(
            frame, width=382, height=26, radius=4,
            bg_color="#333333", border_normal="#404040",
            border_focus=self.accent, text_color=self.fg_color
        )
        self.output_entry.grid(row=1, column=1, sticky="ew", padx=5)
        RoundedButton(frame, text="浏览", command=self._select_output,
                     width=80, height=26, radius=4,
                     button_color="#333333", hover_color="#555555",
                     text_color=self.fg_color
                    ).grid(row=1, column=2, padx=5)
        frame.columnconfigure(1, weight=1)

    def _create_mode_selectors(self, parent):
        """创建模式选择区域"""
        # 模式选择
        self.mode_var = tk.StringVar(value="interval")
        tk.Radiobutton(parent, text="固定间隔", variable=self.mode_var, value="interval",
                      bg=self.bg_color, fg=self.fg_color, selectcolor=self.bg_color
                      ).pack(anchor="w", padx=20, pady=(5, 0))
        tk.Radiobutton(parent, text="随机比例", variable=self.mode_var, value="rate",
                      bg=self.bg_color, fg=self.fg_color, selectcolor=self.bg_color
                      ).pack(anchor="w", padx=20)

        # 参数设置
        params = [
            ("间隔字节数:", "interval_spin", "100"),
            ("损坏比例:", "rate_entry", "10"),
            ("头部保护:", "head_spin", "1024"),
            ("尾部保护:", "tail_spin", "1024")
        ]
        
        for i, (label, name, default) in enumerate(params):
            if i == 1:  # 比例输入框特殊处理
                frame = tk.Frame(parent, bg=self.bg_color)
                frame.pack(anchor="w", padx=20, pady=(2, 5))
                tk.Label(frame, text=label, bg=self.bg_color, fg=self.fg_color
                        ).pack(side=tk.LEFT)
                entry = ModernEntry(
                    frame, width=80, height=28, radius=3,
                    bg_color="#333333", border_normal="#404040",
                    border_focus=self.accent, text_color=self.fg_color
                )
                entry.insert(0, default)
                entry.pack(side=tk.LEFT)
                tk.Label(frame, text="%", bg=self.bg_color, fg=self.fg_color
                        ).pack(side=tk.LEFT, padx=4)
                setattr(self, name, entry)
            else:
                tk.Label(parent, text=label, bg=self.bg_color, fg=self.fg_color
                        ).pack(anchor="w", padx=20, pady=(10, 0) if i != 3 else (0, 0))
                entry = ModernEntry(
                    parent, width=100, height=28, radius=3,
                    bg_color="#333333", border_normal="#404040",
                    border_focus=self.accent, text_color=self.fg_color
                )
                entry.insert(0, default)
                entry.pack(anchor="w", padx=20, pady=(2, 5))
                setattr(self, name, entry)

    def _create_action_button(self, parent):
        """创建操作按钮"""
        RoundedButton(parent, text="开始熵增", command=self._start_corrupt,
                     width=120, height=32, radius=4,
                     button_color=self.accent, hover_color="#6bd8c9",
                     press_color="#3aa08f", text_color="#000000",
                     font_size=11, font_weight="bold"
                    ).pack(pady=20)

    def _select_input(self):
        """选择输入文件"""
        path = filedialog.askopenfilename()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def _select_output(self):
        """选择输出文件"""
        path = filedialog.asksaveasfilename()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def _start_corrupt(self):
        """执行文件损坏操作"""
        inp = self.input_entry.get()
        out = self.output_entry.get()
        if not inp or not out:
            messagebox.showwarning("错误", "请选择输入和输出文件！")
            return
        
        try:
            corruptor = FileCorruptor()
            mode = self.mode_var.get()
            head = int(self.head_spin.get())
            tail = int(self.tail_spin.get())
            
            if mode == "interval":
                interval = int(self.interval_spin.get())
                corruptor.corrupt_fixed_interval(inp, out, interval, head, tail)
            else:
                rate = float(self.rate_entry.get()) / 100
                corruptor.corrupt_random_rate(inp, out, rate, head, tail)
            
            messagebox.showinfo("完成", "文件损坏操作已完成！")
        except Exception as e:
            messagebox.showerror("错误", f"操作失败: {str(e)}")
