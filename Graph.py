import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# Sample data
data = [
    {"name": "HARIKA", "admission_number": "21BCE9067", "date": "2023-08-01", "duration": 55},
    {"name": "HARIKA", "admission_number": "21BCE9067", "date": "2023-08-02", "duration": 36},
    {"name": "HARIKA", "admission_number": "21BCE9067", "date": "2023-08-03", "duration": 77},
    {"name": "HARIKA", "admission_number": "21BCE9067", "date": "2023-08-04", "duration": 46},
    {"name": "RAM", "admission_number": "21BCE9789", "date": "2023-08-01", "duration": 56},
    {"name": "RAM", "admission_number": "21BCE9789", "date": "2023-08-02", "duration": 34},
    {"name": "RAM", "admission_number": "21BCE9789", "date": "2023-08-03", "duration": 65},
    {"name": "RAM", "admission_number": "21BCE9789", "date": "2023-08-04", "duration": 56},
    {"name": "SATYA", "admission_number": "21BCE7559", "date": "2023-08-01", "duration": 52},
    {"name": "SATYA", "admission_number": "21BCE7559", "date": "2023-08-02", "duration": 25},
    {"name": "SATYA", "admission_number": "21BCE7559", "date": "2023-08-03", "duration": 74},
    {"name": "SATYA", "admission_number": "21BCE7559", "date": "2023-08-04", "duration": 20},
    {"name": "PREETHI", "admission_number": "21BCE9767", "date": "2023-08-01", "duration": 70},
    {"name": "PREETHI", "admission_number": "21BCE9767", "date": "2023-08-02", "duration": 10},
    {"name": "PREETHI", "admission_number": "21BCE9767", "date": "2023-08-03", "duration": 10},
    {"name": "PREETHI", "admission_number": "21BCE9767", "date": "2023-08-04", "duration": 20},
    {"name": "SHRUTHI", "admission_number": "21BCE9167", "date": "2023-08-01", "duration": 65},
    {"name": "SHRUTHI", "admission_number": "21BCE9167", "date": "2023-08-02", "duration": 75},
    {"name": "SHRUTHI", "admission_number": "21BCE9167", "date": "2023-08-03", "duration": 87},
    {"name": "SHRUTHI", "admission_number": "21BCE9167", "date": "2023-08-04", "duration": 36},
    {"name": "KEERTHI", "admission_number": "21BCE9260", "date": "2023-08-01", "duration": 74},
    {"name": "KEERTHI", "admission_number": "21BCE9260", "date": "2023-08-02", "duration": 86},
    {"name": "KEERTHI", "admission_number": "21BCE9260", "date": "2023-08-04", "duration": 68},
    {"name": "KEERTHI", "admission_number": "21BCE9260", "date": "2023-08-01", "duration": 54},
    # ... more data ...
]


# Create a Tkinter window
root = tk.Tk()
root.title("Attendance Visualizer")

# Dropdown for admission numbers
admission_numbers = list(set(entry["admission_number"] for entry in data))
admission_number_var = tk.StringVar(value=admission_numbers[0])
admission_number_dropdown = ttk.Combobox(root, textvariable=admission_number_var, values=admission_numbers)
admission_number_dropdown.pack()

canvas = None  # Define canvas variable

def plot_graph():
    global canvas  # Declare canvas as global
    
    selected_admission_number = admission_number_var.get()
    selected_data = [entry for entry in data if entry["admission_number"] == selected_admission_number]
    
    if selected_data:
        df = pd.DataFrame(selected_data)
        df["date"] = pd.to_datetime(df["date"])
        
        plt.figure(figsize=(10, 6))
        
        plt.plot(df["date"], df["duration"], marker='o')
        
        plt.xlabel("Date")
        plt.ylabel("Duration")
        plt.title(f'Attendance Duration for {selected_admission_number}')
        plt.xticks(rotation=45)
        plt.grid()
        
        if canvas is not None:
            canvas.get_tk_widget().destroy()
            
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Function to close the graph and quit the program
def close_graph(event):
    plt.close()
    root.quit()

# Bind the close_graph function to the 'q' key press event
root.bind('<Key>', close_graph)

# Button to plot the graph
plot_button = tk.Button(root, text="Plot Graph", command=plot_graph)
plot_button.pack()

root.mainloop()
