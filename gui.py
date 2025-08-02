# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from custom_widgets import RoundedButton, ModernEntry
from file_corruptor import FileCorruptor

class AdvancedFileCorruptor:
    """文件熵增器GUI界面"""
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_widgets()
        self.processing = False

    def _setup_window(self):
        """窗口基本设置"""
        self.root.title("文件熵增处理器")
        self.root.geometry("650x600")  # 增加高度以容纳进度条
        self.root.minsize(500, 500)
        self.bg_color = "#252526"
        self.fg_color = "#e0e0e0"
        self.accent = "#4ec9b0"
        self.root.configure(bg=self.bg_color)
        
        # 设置窗口图标
        try:
            self.root.iconbitmap("icon.ico")  # 如果有图标文件
        except:
            pass

    def _create_widgets(self):
        """创建界面控件"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="文件熵增处理器", 
            font=("微软雅黑", 14, "bold"),
            bg=self.bg_color, 
            fg=self.accent
        )
        title_label.pack(pady=(0, 15))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(
            main_frame, 
            text=" 文件设置 ", 
            padding=(10, 5),
            style="Custom.TLabelframe"
        )
        file_frame.pack(fill=tk.X, pady=5)
        
        # 输入文件选择
        input_frame = tk.Frame(file_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            input_frame, 
            text="输入文件:", 
            bg=self.bg_color, 
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=(0, 2))
        
        self.input_entry = ModernEntry(
            input_frame, 
            width=385, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
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
            text_color=self.fg_color
        ).pack(side=tk.LEFT)

        # 输出文件选择
        output_frame = tk.Frame(file_frame, bg=self.bg_color)
        output_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            output_frame, 
            text="输出文件:", 
            bg=self.bg_color, 
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=(0, 2))
        
        self.output_entry = ModernEntry(
            output_frame, 
            width=385, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
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
            text_color=self.fg_color
        ).pack(side=tk.LEFT)

        # 处理模式区域
        mode_frame = ttk.LabelFrame(
            main_frame, 
            text=" 处理模式 ", 
            padding=(10, 10),
            style="Custom.TLabelframe"
        )
        mode_frame.pack(fill=tk.X, pady=10)

        # 模式选择
        mode_label = tk.Label(
            mode_frame, 
            text="选择处理方式:", 
            bg=self.bg_color, 
            fg=self.fg_color
        )
        mode_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.mode_var = tk.StringVar(value="interval")
        
        interval_btn = tk.Radiobutton(
            mode_frame, 
            text="固定间隔模式", 
            variable=self.mode_var, 
            value="interval",
            bg=self.bg_color, 
            fg=self.fg_color, 
            selectcolor=self.bg_color,
            command=self._update_mode_display
        )
        interval_btn.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        rate_btn = tk.Radiobutton(
            mode_frame, 
            text="随机比例模式", 
            variable=self.mode_var, 
            value="rate",
            bg=self.bg_color, 
            fg=self.fg_color, 
            selectcolor=self.bg_color,
            command=self._update_mode_display
        )
        rate_btn.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # 参数设置
        params_frame = tk.Frame(mode_frame, bg=self.bg_color)
        params_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        
        # 间隔参数
        interval_frame = tk.Frame(params_frame, bg=self.bg_color)
        interval_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            interval_frame, 
            text="间隔字节数:", 
            bg=self.bg_color, 
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.interval_entry = ModernEntry(
            interval_frame, 
            width=60, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
        )
        self.interval_entry.insert(0, "100")
        self.interval_entry.pack(side=tk.LEFT)
        tk.Label(
            interval_frame, 
            text="字节", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 15))
        
        # 比例参数
        rate_frame = tk.Frame(params_frame, bg=self.bg_color)
        rate_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            rate_frame, 
            text="损坏比例:", 
            bg=self.bg_color, 
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.rate_entry = ModernEntry(
            rate_frame, 
            width=60, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
        )
        self.rate_entry.insert(0, "10")
        self.rate_entry.pack(side=tk.LEFT)
        tk.Label(
            rate_frame, 
            text="%", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 15))
        
        # 保护区域
        protect_frame = tk.Frame(params_frame, bg=self.bg_color)
        protect_frame.pack(fill=tk.X, pady=3)
        tk.Label(
            protect_frame, 
            text="保护区域:", 
            bg=self.bg_color, 
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            protect_frame, 
            text="头部", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.head_entry = ModernEntry(
            protect_frame, 
            width=50, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
        )
        self.head_entry.insert(0, "1024")
        self.head_entry.pack(side=tk.LEFT)
        
        tk.Label(
            protect_frame, 
            text="字节", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(
            protect_frame, 
            text="尾部", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.tail_entry = ModernEntry(
            protect_frame, 
            width=50, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
        )
        self.tail_entry.insert(0, "1024")
        self.tail_entry.pack(side=tk.LEFT)
        
        tk.Label(
            protect_frame, 
            text="字节", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # 初始显示模式
        self._update_mode_display()
        
        # 替换值设置区域
        replace_frame = ttk.LabelFrame(
            main_frame, 
            text=" 替换值设置 ", 
            padding=(10, 10),
            style="Custom.TLabelframe"
        )
        replace_frame.pack(fill=tk.X, pady=10)
        
        # 替换模式选择
        replace_mode_frame = tk.Frame(replace_frame, bg=self.bg_color)
        replace_mode_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            replace_mode_frame, 
            text="替换方式:", 
            bg=self.bg_color, 
            fg=self.fg_color
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
                bg=self.bg_color, 
                fg=self.fg_color, 
                selectcolor=self.bg_color,
                command=self._update_replace_mode
            )
            rb.pack(side=tk.LEFT, padx=(0, 10))
        
        # 自定义值输入框
        custom_frame = tk.Frame(replace_frame, bg=self.bg_color)
        custom_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            custom_frame, 
            text="自定义值:", 
            bg=self.bg_color, 
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.custom_entry = ModernEntry(
            custom_frame, 
            width=100, 
            height=26, 
            radius=4,
            bg_color="#333333", 
            border_normal="#404040",
            border_focus=self.accent, 
            text_color=self.fg_color
        )
        self.custom_entry.pack(side=tk.LEFT)
        self.custom_entry.insert(0, "0x55")
        
        # 提示标签
        tk.Label(
            custom_frame, 
            text="(格式: 0xXX 或 十进制数)", 
            bg=self.bg_color, 
            fg="#aaaaaa"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # 初始更新替换模式显示
        self._update_replace_mode()
        
        # 进度条区域
        progress_frame = tk.Frame(main_frame, bg=self.bg_color)
        progress_frame.pack(fill=tk.X, pady=(10, 5))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var, 
            maximum=100,
            length=500,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, padx=10)
        
        # 进度文本
        self.progress_text = tk.StringVar(value="等待开始...")
        progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_text,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("微软雅黑", 9)
        )
        progress_label.pack(pady=(5, 0))
        
        # 操作按钮区域
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=15)
        
        self.process_btn = RoundedButton(
            btn_frame, 
            text="开始处理", 
            command=self._start_corrupt,
            width=120, 
            height=35, 
            radius=5,
            button_color=self.accent, 
            hover_color="#6bd8c9",
            press_color="#3aa08f", 
            text_color="#000000",
            font_size=12, 
            font_weight="bold"
        )
        self.process_btn.pack()
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(
            main_frame, 
            textvariable=self.status_var,
            bg="#1e1e1e", 
            fg="#aaaaaa", 
            height=1,
            anchor=tk.W,
            padx=10
        )
        status_bar.pack(fill=tk.X, pady=(5, 0))
        
        # 创建自定义样式
        self._create_styles()
    
    def _create_styles(self):
        """创建自定义控件样式"""
        style = ttk.Style()
        style.configure(
            "Custom.TLabelframe", 
            background=self.bg_color,
            foreground=self.fg_color,
            bordercolor="#404040"
        )
        style.configure(
            "Custom.TLabelframe.Label", 
            background=self.bg_color,
            foreground=self.accent,
            font=("微软雅黑", 9, "bold")
        )
        
        # 进度条样式
        style.configure("TProgressbar", thickness=8)
        style.configure("TProgressbar.trough", background="#333333")
        style.configure("TProgressbar.pbar", background=self.accent)
    
    def _update_mode_display(self):
        """根据选择的模式更新显示"""
        mode = self.mode_var.get()
        
        if mode == "interval":
            self.interval_entry.configure(state="normal")
            self.rate_entry.configure(state="disabled")
        else:
            self.interval_entry.configure(state="disabled")
            self.rate_entry.configure(state="normal")
    
    def _update_replace_mode(self):
        """根据替换模式更新显示"""
        mode = self.replace_mode.get()
        if mode == "custom":
            self.custom_entry.configure(state="normal")
        else:
            self.custom_entry.configure(state="disabled")
    
    def _select_input(self):
        """选择输入文件"""
        self.status_var.set("选择源文件...")
        path = filedialog.askopenfilename()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)
            self.status_var.set(f"已选择源文件: {path}")
    
    def _select_output(self):
        """选择输出文件"""
        self.status_var.set("选择输出位置...")
        path = filedialog.asksaveasfilename()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)
            self.status_var.set(f"输出文件: {path}")
    
    def _start_corrupt(self):
        """执行文件损坏操作"""
        if self.processing:
            return
            
        inp = self.input_entry.get()
        out = self.output_entry.get()
        
        if not inp or not out:
            messagebox.showwarning("缺少信息", "请选择源文件和输出位置")
            return
        
        try:
            # 禁用按钮防止重复点击
            self.process_btn.configure(state="disabled")
            self.processing = True
            
            # 获取参数
            mode = self.mode_var.get()
            head = int(self.head_entry.get())
            tail = int(self.tail_entry.get())
            
            # 获取替换值
            replace_mode = self.replace_mode.get()
            if replace_mode == "random":
                replace_value = "random"
            elif replace_mode == "zero":
                replace_value = "0x00"
            elif replace_mode == "ff":
                replace_value = "0xFF"
            else:  # custom
                replace_value = self.custom_entry.get()
            
            # 重置进度
            self.progress_var.set(0)
            self.progress_text.set("准备处理...")
            self.status_var.set("正在处理，请稍候...")
            
            # 创建并启动处理线程
            thread = threading.Thread(
                target=self._process_file, 
                args=(inp, out, mode, head, tail, replace_value),
                daemon=True
            )
            thread.start()
            
        except ValueError as ve:
            self.status_var.set("错误: " + str(ve))
            messagebox.showerror("输入错误", str(ve))
            self.process_btn.configure(state="normal")
            self.processing = False
        except Exception as e:
            self.status_var.set("错误: " + str(e))
            messagebox.showerror("处理失败", f"操作失败: {str(e)}")
            self.process_btn.configure(state="normal")
            self.processing = False
    
    def _process_file(self, inp, out, mode, head, tail, replace_value):
        """在后台线程中处理文件"""
        try:
            # 创建损坏处理器
            corruptor = FileCorruptor()
            
            # 进度回调函数
            def update_progress(processed, total):
                percent = (processed / total) * 100
                self.progress_var.set(percent)
                self.progress_text.set(f"处理中: {percent:.1f}% ({processed:,} / {total:,} 字节)")
                self.root.update_idletasks()  # 安全更新UI
            
            # 根据模式调用
            if mode == "interval":
                interval = int(self.interval_entry.get())
                if interval <= 0:
                    raise ValueError("间隔字节数必须大于0")
                corruptor.corrupt_fixed_interval(
                    inp, out, interval, head, tail, replace_value,
                    progress_callback=update_progress
                )
            else:
                rate = float(self.rate_entry.get()) / 100
                if rate <= 0 or rate > 1:
                    raise ValueError("损坏比例必须在0-100之间")
                corruptor.corrupt_random_rate(
                    inp, out, rate, head, tail, replace_value,
                    progress_callback=update_progress
                )
            
            # 完成处理
            self.progress_var.set(100)
            self.progress_text.set("处理完成!")
            self.status_var.set("处理成功!")
            messagebox.showinfo("成功", "文件处理操作已完成")
            
        except ValueError as ve:
            self.status_var.set("错误: " + str(ve))
            messagebox.showerror("输入错误", str(ve))
        except Exception as e:
            self.status_var.set("错误: " + str(e))
            messagebox.showerror("处理失败", f"操作失败: {str(e)}")
        finally:
            # 恢复按钮状态
            self.process_btn.configure(state="normal")
            self.processing = False