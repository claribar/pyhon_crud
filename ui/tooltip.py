import tkinter as tk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if not self.tooltip:
            # Crear una ventana emergente de nivel superior sin bordes ni título
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.config(bg="yellow", padx=5, pady=5)
            label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1)
            label.pack()
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 25
            self.tooltip.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
