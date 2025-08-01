# main.py
import tkinter as tk
from gui import AdvancedFileCorruptor

def main():
    root = tk.Tk()
    app = AdvancedFileCorruptor(root)
    root.mainloop()

if __name__ == "__main__":
    main()