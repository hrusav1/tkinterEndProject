# utils/styling.py
from tkinter import ttk


def apply_style():
    style = ttk.Style()
    style.theme_use('clam')

    # Define colors
    bg_color = '#252525'
    fg_color = '#FFFFFF'
    button_bg = '#464646'
    button_fg = '#FFFFFF'
    hover_bg = '#666666'

    # Configure styles
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=fg_color)
    style.configure('TEntry', fieldbackground=bg_color, foreground=fg_color)
    style.configure('TButton', background=button_bg, foreground=button_fg)

    # Button hover effect
    style.map('TButton',
              background=[('active', hover_bg)],
              relief=[('pressed', 'sunken')]
              )


def create_main_frame(parent):
    frame = ttk.Frame(parent, padding="20")
    frame.pack(expand=True, fill="both")
    return frame


def create_centered_frame(parent, width, height):
    outer_frame = ttk.Frame(parent)
    outer_frame.pack(expand=True, fill="both")

    inner_frame = ttk.Frame(outer_frame, width=width, height=height)
    inner_frame.pack(expand=True)

    inner_frame.pack_propagate(False)
    return inner_frame