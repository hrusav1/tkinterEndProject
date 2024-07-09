# views/dashboard_page.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_layout()

    def create_layout(self):
        # Create left sidebar
        sidebar = ttk.Frame(self, width=200)
        sidebar.pack(side="left", fill="y")

        dashboard_button = ttk.Button(sidebar, text="Dashboard", command=self.show_dashboard)
        dashboard_button.pack(pady=10)

        apiary_button = ttk.Button(sidebar, text="Apiary", command=self.show_apiary)
        apiary_button.pack(pady=10)

        prediction_button = ttk.Button(sidebar, text="Prediction", command=self.show_prediction)
        prediction_button.pack(pady=10)

        logout_button = ttk.Button(sidebar, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

        # Create right content area
        self.content_area = ttk.Frame(self)
        self.content_area.pack(side="right", expand=True, fill="both")

        # Initially show dashboard content
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_content()
        self.create_charts()

    def show_apiary(self):
        self.controller.show_frame("ApiaryPage")

    def show_prediction(self):
        self.clear_content()
        # Placeholder for prediction content
        label = ttk.Label(self.content_area, text="Prediction charts will be shown here")
        label.pack(pady=20)

    def logout(self):
        if tk.messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.controller.show_frame("HomePage")

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def create_charts(self):
        # Create temperature chart
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.plot([1, 2, 3, 4], [20, 22, 21, 23])  # Placeholder data
        ax1.set_title("Temperature (°C)")
        canvas1 = FigureCanvasTkAgg(fig1, master=self.content_area)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

        # Create humidity chart
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.plot([1, 2, 3, 4], [60, 65, 62, 58])  # Placeholder data
        ax2.set_title("Humidity (%)")
        canvas2 = FigureCanvasTkAgg(fig2, master=self.content_area)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

        # Create weight chart
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.plot([1, 2, 3, 4], [50, 52, 53, 55])  # Placeholder data
        ax3.set_title("Weight (kg)")
        canvas3 = FigureCanvasTkAgg(fig3, master=self.content_area)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)