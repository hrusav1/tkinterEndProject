#/views/prediction_page.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PredictionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a frame for the content
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add title
        title_label = ttk.Label(self.content_frame, text="Predictions", font=("Helvetica", 24))
        title_label.pack(pady=20)

        # Create tabs for different predictions
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Honey Production Prediction tab
        honey_frame = ttk.Frame(self.notebook)
        self.notebook.add(honey_frame, text="Honey Production")
        self.create_honey_prediction_chart(honey_frame)

        # Hive Health Prediction tab
        health_frame = ttk.Frame(self.notebook)
        self.notebook.add(health_frame, text="Hive Health")
        self.create_hive_health_prediction(health_frame)

    def create_honey_prediction_chart(self, parent):
        # Placeholder data for the chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        production = [10, 15, 25, 40, 60, 80, 100, 90, 70, 50, 30, 20]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(months, production)
        ax.set_title('Predicted Honey Production')
        ax.set_xlabel('Month')
        ax.set_ylabel('Production (kg)')

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    def create_hive_health_prediction(self, parent):
        # Placeholder text for hive health prediction
        health_text = ("Based on current data and historical trends, the overall hive health "
                       "is predicted to be GOOD for the next 3 months.\n\n"
                       "Factors contributing to this prediction:\n"
                       "- Stable temperature and humidity levels\n"
                       "- Consistent weight gain\n"
                       "- No signs of disease or pest infestation\n\n"
                       "Recommendations:\n"
                       "- Continue regular inspections\n"
                       "- Monitor for any sudden changes in weight or temperature\n"
                       "- Prepare for potential honey harvest in the coming months")

        text_widget = tk.Text(parent, wrap=tk.WORD, font=("Helvetica", 12))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert(tk.END, health_text)
        text_widget.config(state=tk.DISABLED)  # Make the text read-only