import tkinter as tk
from ui.vacuum_ui import VacuumCleanerUI


if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumCleanerUI(root)
    root.mainloop()
