# Description: This file contains the code for the user interface of the medication management system.
from datetime import datetime, timedelta
import json
import tkinter as tk
from tkinter import VERTICAL, Canvas, Frame, Label, Scrollbar, messagebox
from tkinter import filedialog
from data import add_or_update_medication, delete_medication, search_medications, mark_as_taken, mark_as_pending
from medication_store import MedicationStore
from tkcalendar import DateEntry

# Initialize UI components
def initialize_ui(root):
    global content_frame

    # Frame for the top section (User's Name)
    top_frame = tk.Frame(root, bg="lightblue", height=100)
    top_frame.pack(fill="x")

    user_name_label = tk.Label(top_frame, text="Medical Reminder App", font=("Arial", 20), bg="lightblue")
    user_name_label.pack(pady=20)

    # Frame for the left-side navigation bar
    nav_frame = tk.Frame(root, bg="gray", width=80)
    nav_frame.pack(side="left", fill="y")

    # Navigation icons
    icons = [
        "Dashboard", "Search", "Schedule", 
        "History", "Payment", 
        "Settings"
    ]

    for icon in icons:
        if icon == "Schedule":
            button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: open_schedule_form(content_frame))
        # elif icon == "Notifications":
        #     button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: open_notifications_form(content_frame))
        elif icon == "Search":
            button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: open_search_form(content_frame))
        elif icon == "History":
            button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: open_history_form(content_frame))
        elif icon == "Payment":
            button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: open_payment_form(content_frame))
        elif icon == "Settings":
            button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: open_settings_form(content_frame))
        else:
            button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=lambda: show_dashboard())
        button.pack(pady=10)

    # Frame for the content area (dashboard or form)
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Display the initial dashboard
    show_dashboard()


# Function to clear the frame and display the dashboard
def show_dashboard():
    for widget in content_frame.winfo_children():
        widget.destroy()
    display_dashboard()

# Function to display the dashboard
def display_dashboard():
    # Get today's date
    today = datetime.today().date()

    # Calculate the date 3 days from now
    three_days_from_now = today + timedelta(days=3)

    grouped_medications = MedicationStore.grouped_medications

    # Create a canvas widget for scrollable content
    canvas = tk.Canvas(content_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    for date_str, meds in grouped_medications.items():
        # Convert the date string to a datetime object for comparison
        date = datetime.strptime(date_str, "%m-%d-%Y").date()

        # Only display dates from today up to 3 days from now
        if today <= date <= three_days_from_now:
            date_label = tk.Label(scrollable_frame, text=date_str, font=("Arial", 16, "bold"), bg="lightgray")
            date_label.pack(fill="x", pady=(10, 0))

            for med in meds:
                med_frame = tk.Frame(scrollable_frame, bg="lightyellow", padx=10, pady=5)
                med_frame.pack(fill="x", pady=2)

                time_label = tk.Label(med_frame, text=med["time"], font=("Arial", 14), width=10)
                time_label.pack(side="left")

                name_label = tk.Label(med_frame, text=med["name"], font=("Arial", 14), width=15)
                name_label.pack(side="left")

                status_label = tk.Label(med_frame, text=med["status"], font=("Arial", 14), width=10)
                status_label.pack(side="left")

                edit_button = tk.Button(med_frame, text="Edit", font=("Arial", 10), command=lambda d=date_str, t=med["time"], n=med["name"]: open_schedule_form(d, n, t))
                edit_button.pack(side="left", padx=5)

                delete_button = tk.Button(med_frame, text="Del", font=("Arial", 10), command=lambda d=date_str, t=med["time"]: delete_medication(d, t))
                delete_button.pack(side="left", padx=5)

                # Add "Mark as Taken" button
                taken_button = tk.Button(med_frame, text="Mark as Taken", font=("Arial", 10), command=lambda d=date_str, t=med["time"]: handle_mark_as_taken(d, t))
                taken_button.pack(side="left", padx=5)

                # Add "Mark as Pending" button
                pending_button = tk.Button(med_frame, text="Mark as Pending", font=("Arial", 10), command=lambda d=date_str, t=med["time"]: handle_mark_as_pending(d, t))
                pending_button.pack(side="left", padx=5)


def handle_mark_as_taken(date, time):
    if mark_as_taken(date, time):
        show_dashboard()

def handle_mark_as_pending(date, time):
    if mark_as_pending(date, time):
        show_dashboard()

def open_schedule_form(content_frame, date=None, med_name=None, time=None, recurring=False, recurrence_frequency="daily", end_date=None):
    for widget in content_frame.winfo_children():
        widget.destroy()

    today = datetime.today().date()

    # Start Date Picker
    tk.Label(content_frame, text="Start Date (MM-DD-YYYY):", font=("Arial", 12)).pack(pady=5)
    start_date_entry = DateEntry(content_frame, font=("Arial", 12), date_pattern="mm-dd-yyyy", mindate=today)
    start_date_entry.pack(pady=5)
    if date:
        start_date_entry.set_date(datetime.strptime(date, "%m-%d-%Y"))

    # End Date Picker
    tk.Label(content_frame, text="End Date (MM-DD-YYYY):", font=("Arial", 12)).pack(pady=5)
    end_date_entry = DateEntry(content_frame, font=("Arial", 12), date_pattern="mm-dd-yyyy", mindate=today, maxdate=today + timedelta(days=30))
    end_date_entry.pack(pady=5)
    if end_date:
        end_date_entry.set_date(datetime.strptime(end_date, "%m-%d-%Y"))

    # Medication Name Entry
    tk.Label(content_frame, text="Medication Name:", font=("Arial", 12)).pack(pady=5)
    med_name_entry = tk.Entry(content_frame, font=("Arial", 12))
    med_name_entry.pack(pady=5)
    if med_name:
        med_name_entry.insert(0, med_name)

    # Time Entry
    tk.Label(content_frame, text="Time (HH:MM AM/PM):", font=("Arial", 12)).pack(pady=5)
    time_entry = tk.Entry(content_frame, font=("Arial", 12))
    time_entry.pack(pady=5)
    if time:
        time_entry.insert(0, time)

    recurring_var = tk.BooleanVar(value=recurring)
    tk.Checkbutton(content_frame, text="Recurring", variable=recurring_var, font=("Arial", 12)).pack(anchor="w")

    tk.Label(content_frame, text="Recurrence Frequency:", font=("Arial", 12)).pack(pady=5)
    frequency_var = tk.StringVar(value=recurrence_frequency)
    frequencies = ["daily", "weekly", "monthly"]
    for freq in frequencies:
        tk.Radiobutton(content_frame, text=freq.capitalize(), variable=frequency_var, value=freq, font=("Arial", 12)).pack(anchor="w")

    def submit_form():
        new_date = start_date_entry.get_date().strftime("%m-%d-%Y")
        new_end_date = end_date_entry.get_date().strftime("%m-%d-%Y")
        new_med_name = med_name_entry.get()
        new_time = time_entry.get()
        recurring = recurring_var.get()
        frequency = frequency_var.get()

        if not new_med_name or not new_time:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        # Validation for date range
        if datetime.strptime(new_end_date, "%m-%d-%Y") > datetime.strptime(new_date, "%m-%d-%Y") + timedelta(days=30):
            messagebox.showwarning("Input Error", "End date cannot be more than 30 days away from the start date.")
            return

        add_or_update_medication(new_date, new_med_name, new_time, recurring, frequency, new_end_date, old_date=date, old_time=time)
        
        # Success message and redirect to dashboard
        messagebox.showinfo("Success", f"Medication '{new_med_name}' successfully added!")
        show_dashboard()

    submit_button = tk.Button(content_frame, text="Submit", font=("Arial", 12), command=submit_form)
    submit_button.pack(pady=20)

# def open_notifications_form(content_frame):
#     for widget in content_frame.winfo_children():
#         widget.destroy()

#     # Notifications Options
#     tk.Label(content_frame, text="Select Notification Methods:", font=("Arial", 12)).pack(pady=10)

#     notification_methods = {
#         "Text": tk.BooleanVar(),
#         "Phone Call": tk.BooleanVar(),
#         "Email": tk.BooleanVar(),
#         "System Notification": tk.BooleanVar()
#     }

#     checkboxes = {}
#     for method, var in notification_methods.items():
#         check = tk.Checkbutton(content_frame, text=method, variable=var, font=("Arial", 12))
#         check.pack(anchor="w")
#         checkboxes[method] = check

#     phone_label = tk.Label(content_frame, text="Phone Number:", font=("Arial", 12))
#     phone_entry = tk.Entry(content_frame, font=("Arial", 12))
#     phone_label.pack(pady=10)
#     phone_entry.pack(pady=5)

#     email_label = tk.Label(content_frame, text="Email Address:", font=("Arial", 12))
#     email_entry = tk.Entry(content_frame, font=("Arial", 12))
#     email_label.pack(pady=10)
#     email_entry.pack(pady=5)

#     def submit_notifications():
#         selected_methods = [method for method, var in notification_methods.items() if var.get()]
#         phone = phone_entry.get()
#         email = email_entry.get()

#         if selected_methods:
#             message = f"Notifications will be sent via: {', '.join(selected_methods)}"
#             if "Phone Call" in selected_methods or "Text" in selected_methods:
#                 if not phone:
#                     messagebox.showwarning("Input Error", "Please enter a phone number.")
#                     return
#                 message += f"\nPhone: {phone}"
#             if "Email" in selected_methods:
#                 if not email:
#                     messagebox.showwarning("Input Error", "Please enter an email address.")
#                     return
#                 message += f"\nEmail: {email}"
#             messagebox.showinfo("Notifications Set", message)
#             show_dashboard()
#         else:
#             messagebox.showwarning("Input Error", "Please select at least one notification method.")

#     submit_button = tk.Button(content_frame, text="Submit", font=("Arial", 12), command=submit_notifications)
#     submit_button.pack(pady=20)


def open_search_form(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Medication Name Entry
    tk.Label(content_frame, text="Search by Medication Name:", font=("Arial", 12)).pack(pady=5)
    med_name_entry = tk.Entry(content_frame, font=("Arial", 12))
    med_name_entry.pack(pady=5)

    # Status Selection
    tk.Label(content_frame, text="Search by Status:", font=("Arial", 12)).pack(pady=5)
    status_var = tk.StringVar(value="All")  # Default to "All"
    statuses = ["All", "Taken", "Pending", "Missed"]
    for status in statuses:
        tk.Radiobutton(content_frame, text=status, variable=status_var, value=status, font=("Arial", 12)).pack(anchor="w")

    # Submit Button
    def submit_search():
        med_name = med_name_entry.get().strip().lower()
        selected_status = status_var.get()
        search_results = search_medications(med_name, selected_status)
        display_search_results(content_frame, search_results)

    submit_button = tk.Button(content_frame, text="Search", font=("Arial", 12), command=submit_search)
    submit_button.pack(pady=20)


def display_search_results(content_frame, results):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a canvas widget for scrollable content
    canvas = tk.Canvas(content_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    if not results:
        tk.Label(scrollable_frame, text="No results found.", font=("Arial", 14)).pack(pady=20)
    else:
        for date, med in results:
            result_frame = tk.Frame(scrollable_frame, bg="lightyellow", padx=10, pady=5)
            result_frame.pack(fill="x", pady=2)

            date_label = tk.Label(result_frame, text=date, font=("Arial", 14), width=15, anchor="w")
            date_label.pack(side="left", padx=5)

            time_label = tk.Label(result_frame, text=med["time"], font=("Arial", 14), width=10)
            time_label.pack(side="left")

            name_label = tk.Label(result_frame, text=med["name"], font=("Arial", 14), width=15)
            name_label.pack(side="left")

            status_label = tk.Label(result_frame, text=med["status"], font=("Arial", 14), width=10)
            status_label.pack(side="left")



def open_history_form(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a canvas widget
    canvas = Canvas(content_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = Scrollbar(content_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Add the scrollable frame to the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Populate the scrollable frame with history data
    grouped_medications = MedicationStore.grouped_medications
    for date, meds in grouped_medications.items():
        if date < datetime.today().strftime("%m-%d-%Y"):  # Show only past dates
            date_label = Label(scrollable_frame, text=date, font=("Arial", 16, "bold"), bg="lightgray")
            date_label.pack(fill="x", pady=(10, 0))

            for med in meds:
                med_frame = Frame(scrollable_frame, bg="lightyellow", padx=10, pady=5)
                med_frame.pack(fill="x", pady=2)

                time_label = Label(med_frame, text=med["time"], font=("Arial", 14), width=10)
                time_label.pack(side="left")

                name_label = Label(med_frame, text=med["name"], font=("Arial", 14), width=15)
                name_label.pack(side="left")

                status_label = Label(med_frame, text=med["status"], font=("Arial", 14), width=10)
                status_label.pack(side="left")

                # No Edit or Delete buttons in history view

def open_payment_form(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Credit Card Number Entry
    tk.Label(content_frame, text="Credit Card Number:", font=("Arial", 12)).pack(pady=5)
    card_number_entry = tk.Entry(content_frame, font=("Arial", 12))
    card_number_entry.pack(pady=5)

    # Expiration Date Entry
    tk.Label(content_frame, text="Expiration Date (MM/YY):", font=("Arial", 12)).pack(pady=5)
    expiration_entry = tk.Entry(content_frame, font=("Arial", 12))
    expiration_entry.pack(pady=5)

    # CVV Entry
    tk.Label(content_frame, text="CVV:", font=("Arial", 12)).pack(pady=5)
    cvv_entry = tk.Entry(content_frame, font=("Arial", 12))
    cvv_entry.pack(pady=5)

    # Submit Button
    def submit_payment_info():
        # Display a message indicating that this is a mock page
        messagebox.showinfo("Payment Info", "This is a mock payment info page.")

    submit_button = tk.Button(content_frame, text="Submit", font=("Arial", 12), command=submit_payment_info)
    submit_button.pack(pady=20)

def open_settings_form(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Settings", font=("Arial", 16, "bold")).pack(pady=10)

    # Notification Preferences
    tk.Label(content_frame, text="Notification Preferences:", font=("Arial", 12)).pack(pady=10)

    notification_methods = {
        "Text": tk.BooleanVar(),
        "Phone Call": tk.BooleanVar(),
        "Email": tk.BooleanVar(),
        "System Notification": tk.BooleanVar()
    }

    for method, var in notification_methods.items():
        check = tk.Checkbutton(content_frame, text=method, variable=var, font=("Arial", 12))
        check.pack(anchor="w")

    # Contact Information
    phone_label = tk.Label(content_frame, text="Phone Number:", font=("Arial", 12))
    phone_entry = tk.Entry(content_frame, font=("Arial", 12))
    phone_label.pack(pady=10)
    phone_entry.pack(pady=5)

    email_label = tk.Label(content_frame, text="Email Address:", font=("Arial", 12))
    email_entry = tk.Entry(content_frame, font=("Arial", 12))
    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    # Theme Selection
    tk.Label(content_frame, text="Theme Selection:", font=("Arial", 12)).pack(pady=10)
    theme_var = tk.StringVar(value="Light")
    themes = ["Light", "Dark", "Blue"]
    for theme in themes:
        tk.Radiobutton(content_frame, text=theme, variable=theme_var, value=theme, font=("Arial", 12)).pack(anchor="w")

    # Data Backup and Restore
    tk.Label(content_frame, text="Data Backup and Restore:", font=("Arial", 12)).pack(pady=10)

    def backup_data():
        file = filedialog.asksaveasfile(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file:
            json.dump(MedicationStore.grouped_medications, file)
            file.close()
            messagebox.showinfo("Backup", "Data backed up successfully!")

    def restore_data():
        file = filedialog.askopenfile(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file:
            MedicationStore.grouped_medications = json.load(file)
            file.close()
            messagebox.showinfo("Restore", "Data restored successfully!")
            show_dashboard()

    backup_button = tk.Button(content_frame, text="Backup Data", font=("Arial", 12), command=backup_data)
    backup_button.pack(pady=5)

    restore_button = tk.Button(content_frame, text="Restore Data", font=("Arial", 12), command=restore_data)
    restore_button.pack(pady=5)

    # Save Settings Button
    def save_settings():
        selected_methods = [method for method, var in notification_methods.items() if var.get()]
        phone = phone_entry.get()
        email = email_entry.get()
        theme = theme_var.get()

        if selected_methods:
            message = f"Settings saved!\nNotifications will be sent via: {', '.join(selected_methods)}"
            if "Phone Call" in selected_methods or "Text" in selected_methods:
                if not phone:
                    messagebox.showwarning("Input Error", "Please enter a phone number.")
                    return
                message += f"\nPhone: {phone}"
            if "Email" in selected_methods:
                if not email:
                    messagebox.showwarning("Input Error", "Please enter an email address.")
                    return
                message += f"\nEmail: {email}"
            messagebox.showinfo("Settings Saved", message)
        else:
            messagebox.showwarning("Input Error", "Please select at least one notification method.")

        # Apply the selected theme
        apply_theme(theme, content_frame)

    save_button = tk.Button(content_frame, text="Save Settings", font=("Arial", 12), command=save_settings)
    save_button.pack(pady=20)

def apply_theme(theme, content_frame):
    if theme == "Light":
        content_frame.config(bg="white")
    elif theme == "Dark":
        content_frame.config(bg="black")
    elif theme == "Blue":
        content_frame.config(bg="lightblue")