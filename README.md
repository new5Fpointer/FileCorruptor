# FileCorruptor
## 项目结构
```
FileCorruptor/
├── main.py                      # 程序入口
├── gui.py                       # 主窗口界面
├── file_corruptor.py            # 文件处理核心逻辑
├── custom_widgets/              # 自定义UI控件
│   ├── __init__.py              # 导出RoundedButton和ModernEntry
│   ├── button.py                # 圆角按钮控件
│   ├── cursor.py                # 光标控件
│   └── entry.py                 # 现代化输入框控件
└── components/                  # GUI功能组件
    ├── __init__.py              # 导出所有组件
    ├── file_selector.py         # 文件选择组件（输入框宽度480）
    ├── mode_selector.py         # 处理模式选择组件
    ├── replace_selector.py      # 替换值设置组件
    ├── progress_bar.py          # 进度条组件
    └── status_bar.py            # 状态栏组件
```