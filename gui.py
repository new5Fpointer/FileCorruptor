# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from components.file_selector import FileSelector
from components.mode_selector import ModeSelector
from components.replace_selector import ReplaceSelector
from components.progress_bar import ProgressBar
from components.status_bar import StatusBar
from custom_widgets import RoundedButton
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
        self.root.geometry("650x600")
        self.root.minsize(500, 500)
        self.bg_color = "#252526"
        self.fg_color = "#e0e0e0"
        self.accent = "#4ec9b0"
        self.root.configure(bg=self.bg_color)
        
        # 设置窗口图标
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
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
        style.configure("TProgressbar", thickness=8)
        style.configure("TProgressbar.trough", background="#333333")
        style.configure("TProgressbar.pbar", background=self.accent)

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
        self.file_selector = FileSelector(
            main_frame, 
            self.bg_color, 
            self.fg_color, 
            self.accent
        )
        self.file_selector.pack(fill=tk.X, pady=5)
        
        # 处理模式区域
        self.mode_selector = ModeSelector(
            main_frame, 
            self.bg_color, 
            self.fg_color, 
            self.accent
        )
        self.mode_selector.pack(fill=tk.X, pady=10)
        
        # 替换值设置区域
        self.replace_selector = ReplaceSelector(
            main_frame, 
            self.bg_color, 
            self.fg_color, 
            self.accent
        )
        self.replace_selector.pack(fill=tk.X, pady=10)
        
        # 进度条区域
        self.progress_bar = ProgressBar(
            main_frame, 
            self.bg_color, 
            self.fg_color, 
            self.accent
        )
        self.progress_bar.pack(fill=tk.X, pady=(10, 5))
        
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
        
        # 状态栏
        self.status_bar = StatusBar(
            main_frame, 
            self.bg_color, 
            "#aaaaaa"
        )
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def _start_corrupt(self):
        """执行文件损坏操作"""
        if self.processing:
            return
            
        inp = self.file_selector.get_input_path()
        out = self.file_selector.get_output_path()
        
        if not inp or not out:
            messagebox.showwarning("缺少信息", "请选择源文件和输出位置")
            return
        
        try:
            # 禁用按钮防止重复点击
            self.process_btn.configure(state="disabled")
            self.processing = True
            
            # 获取参数
            mode = self.mode_selector.get_mode()
            head = self.mode_selector.get_head()
            tail = self.mode_selector.get_tail()
            replace_value = self.replace_selector.get_replace_value()
            
            # 重置进度
            self.progress_bar.reset()
            self.status_bar.set_status("正在处理，请稍候...")
            
            # 创建并启动处理线程
            thread = threading.Thread(
                target=self._process_file, 
                args=(inp, out, mode, head, tail, replace_value),
                daemon=True
            )
            thread.start()
            
        except ValueError as ve:
            self.status_bar.set_status("错误: " + str(ve))
            messagebox.showerror("输入错误", str(ve))
            self.process_btn.configure(state="normal")
            self.processing = False
        except Exception as e:
            self.status_bar.set_status("错误: " + str(e))
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
                self.progress_bar.set_progress(percent)
                self.progress_bar.set_progress_text(
                    f"处理中: {percent:.1f}% ({processed:,} / {total:,} 字节)"
                )
            
            # 根据模式调用
            if mode == "interval":
                interval = self.mode_selector.get_interval()
                if interval <= 0:
                    raise ValueError("间隔字节数必须大于0")
                corruptor.corrupt_fixed_interval(
                    inp, out, interval, head, tail, replace_value,
                    progress_callback=update_progress
                )
            else:
                rate = self.mode_selector.get_rate() / 100
                if rate <= 0 or rate > 1:
                    raise ValueError("损坏比例必须在0-100之间")
                corruptor.corrupt_random_rate(
                    inp, out, rate, head, tail, replace_value,
                    progress_callback=update_progress
                )
            
            # 完成处理
            self.progress_bar.set_progress(100)
            self.progress_bar.set_progress_text("处理完成!")
            self.status_bar.set_status("处理成功!")
            messagebox.showinfo("成功", "文件处理操作已完成")
            
        except ValueError as ve:
            self.status_bar.set_status("错误: " + str(ve))
            messagebox.showerror("输入错误", str(ve))
        except Exception as e:
            self.status_bar.set_status("错误: " + str(e))
            messagebox.showerror("处理失败", f"操作失败: {str(e)}")
        finally:
            # 恢复按钮状态
            self.process_btn.configure(state="normal")
            self.processing = False