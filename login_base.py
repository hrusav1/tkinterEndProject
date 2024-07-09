# File: login_base.py

import tkinter as tk
from pathlib import Path

class CustomButton(tk.Button):
    def __init__(self, master, **kwargs):
        self.bg = kwargs.pop('bg', '#FFFFFF')
        self.fg = kwargs.pop('fg', '#000000')
        self.hover_bg = kwargs.pop('hover_bg', '#CCCCCC')
        self.hover_fg = kwargs.pop('hover_fg', '#000000')

        super().__init__(master, **kwargs)

        self.config(
            bg=self.bg,
            fg=self.fg,
            activebackground=self.hover_bg,
            activeforeground=self.hover_fg,
            relief=tk.FLAT,
            bd=0
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.hover_bg, fg=self.hover_fg)

    def on_leave(self, e):
        self.config(bg=self.bg, fg=self.fg)

class BaseApplication(tk.Tk):
    def __init__(self, title, geometry, bg="#252525"):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.configure(bg=bg)


        self.canvas = tk.Canvas(
            self,
            bg=bg,
            height=int(geometry.split("x")[1]),
            width=int(geometry.split("x")[0]),
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

    def add_frame(self, frame, name):
        self.frames[name] = frame
        frame.place(x=0, y=0, relwidth=1, relheight=1)

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[name].place(x=0, y=0, relwidth=1, relheight=1)

    def create_custom_button(self, x, y, text, command, width, height, **kwargs):
        button = CustomButton(
            self.canvas,
            text=text,
            command=command,
            **kwargs
        )
        return self.canvas.create_window(x, y, anchor='nw', width=width, height=height, window=button)

    def create_entry(self, x, y, width, height, **kwargs):
        entry = tk.Entry(self, **kwargs)
        entry.place(x=x, y=y, width=width, height=height)
        return entry

    def create_text(self, x, y, **kwargs):
        return self.canvas.create_text(x, y, **kwargs)

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        return self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

def relative_to_assets(assets_path: Path, path: str) -> Path:
    return assets_path / Path(path)
