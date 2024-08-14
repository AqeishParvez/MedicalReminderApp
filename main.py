# Description: The main entry point of the application. It initializes the UI components and starts the Tkinter event loop.
import tkinter as tk
from ui import initialize_ui, show_dashboard, show_login_form
from data import load_data_from_file, notify_today_medications, MedicationStore


# Initialize the main window
root = tk.Tk()
root.title("Medical Reminder App")
root.geometry("900x700")

# Load data from file at the start
MedicationStore.load_data_from_file()

# Initialize UI components
initialize_ui(root)

# Show the login form initially
show_login_form(root)

# Notify about today's medications
# notify_today_medications()

# Display the dashboard after loading data
# show_dashboard()

# Start the Tkinter event loop
root.mainloop()
