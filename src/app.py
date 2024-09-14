import tkinter as tk
from gui import ApplicationGUI

def main():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
