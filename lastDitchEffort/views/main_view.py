# views/main_view.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainView:
    def __init__(self, master):
        self.master = master
        self.master.title("Apiary Management System")
        self.master.geometry("1280x1024")
        self.master.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Left navigation frame
        self.nav_frame = tk.Frame(self.master, width=256, bg="#252525")
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.nav_frame.pack_propagate(False)

        self.buttons = {}
        for text in ["Dashboard", "Apiary", "Prediction", "Logout"]:
            btn = tk.Button(self.nav_frame, text=text, bg="#464646", fg="white")
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#666666"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#464646"))
            self.buttons[text] = btn

        # Right content frame
        self.content_frame = tk.Frame(self.master, bg="#464646")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self, data):
        self.clear_content()

        canvas = tk.Canvas(self.content_frame, bg="#464646")
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for data_type, values in data.items():
            self.create_chart(scrollable_frame, data_type, values)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_chart(self, parent, data_type, data):
        dates = [d[0] for d in data]
        values = [d[1] for d in data]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(dates, values)
        ax.set_title(f"{data_type.capitalize()} over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel(data_type.capitalize())

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def show_prediction(self, honey_prediction, health_prediction, current_location):
        self.clear_content()

        predictions_frame = tk.Frame(self.content_frame, bg="#464646")
        predictions_frame.pack(padx=20, pady=20)

        # Location input
        tk.Label(predictions_frame, text="Location:", fg="white", bg="#464646", font=("Arial", 12)).pack(pady=5)
        self.location_entry = tk.Entry(predictions_frame, width=30)
        self.location_entry.pack(side=tk.LEFT, pady=5)
        self.location_entry.insert(0, current_location or "")

        self.location_submit = tk.Button(predictions_frame, text="Submit Location", bg="#666666", fg="white")
        self.location_submit.pack(side=tk.LEFT, padx=5, pady=5)

        # Honey production prediction
        tk.Label(predictions_frame, text="Honey Production Prediction", fg="#767676", bg="#464646", font=("Arial", 14)).pack(pady=10)
        honey_text = tk.Text(predictions_frame, height=5, width=50, bg="#666666", fg="white")
        honey_text.pack(pady=10)
        honey_text.insert(tk.END, honey_prediction)
        honey_text.config(state=tk.DISABLED)

        # Hive health prediction
        tk.Label(predictions_frame, text="Hive Health Prediction", fg="#767676", bg="#464646", font=("Arial", 14)).pack(pady=10)
        health_text = tk.Text(predictions_frame, height=5, width=50, bg="#666666", fg="white")
        health_text.pack(pady=10)
        health_text.insert(tk.END, health_prediction)
        health_text.config(state=tk.DISABLED)

    def show(self):
        print("MainView.show() called")  # Debug print
        self.master.deiconify()
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def hide(self):
        print("MainView.hide() called")  # Debug print
        self.nav_frame.pack_forget()
        self.content_frame.pack_forget()