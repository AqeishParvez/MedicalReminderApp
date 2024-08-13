import tkinter as tk
from tkinter import messagebox
import json
import random
from datetime import datetime, timedelta

# ----------------------------
# Main Window Initialization
# ----------------------------

# Initialize the main window
root = tk.Tk()
root.title("Medical Reminder App")
root.geometry("618x700")  # Size for a mobile device mockup

# ----------------------------
# Functions for Data Management
# ----------------------------

# Function to add or update medication on the dashboard
def add_or_update_medication(date, med_name, time, recurring=False, frequency="daily", end_date=None, old_date=None, old_time=None):
    if old_date and old_time:  # If we are updating an existing reminder
        # Find and update the existing reminder
        meds = grouped_medications.get(old_date, [])
        for med in meds:
            if med["time"] == old_time:
                med["name"] = med_name
                med["time"] = time
                med["recurring"] = recurring
                med["recurrence_frequency"] = frequency
                med["end_date"] = end_date
                if date != old_date:  # If the date is changed, move the reminder to the new date
                    meds.remove(med)
                    if not meds:
                        del grouped_medications[old_date]
                    add_medication(date, med_name, time, recurring, frequency, end_date)
                break
    else:  # If we are adding a new reminder
        add_medication(date, med_name, time, recurring, frequency, end_date)
    save_data_to_file()  # Save data after any modification
    show_dashboard()  # Update the dashboard after adding/updating the medication

def add_medication(date, med_name, time, recurring=False, frequency="daily", end_date=None):
    if date not in grouped_medications:
        grouped_medications[date] = []
    grouped_medications[date].append({
        "time": time, 
        "name": med_name, 
        "status": "Pending", 
        "recurring": recurring, 
        "recurrence_frequency": frequency, 
        "end_date": end_date
    })
    save_data_to_file()  # Save data after adding medication

# Function to delete a medication reminder
def delete_medication(date, time):
    meds = grouped_medications.get(date, [])
    for med in meds:
        if med["time"] == time:
            meds.remove(med)
            if not meds:
                del grouped_medications[date]
            break
    save_data_to_file()  # Save data after deleting medication
    show_dashboard()  # Update the dashboard after deleting the medication

# Function to simulate device input (optional)
def simulate_device_input():
    # Simulate device input by randomly marking doses as "Taken" or "Missed"
    current_time = datetime.now().strftime("%H:%M %p")
    for date, meds in grouped_medications.items():
        for med in meds:
            if med["time"] == current_time:
                med["status"] = random.choice(["Taken", "Missed"])
    show_dashboard()  # Update the dashboard to reflect changes

# Function to save data to a JSON file
def save_data_to_file():
    with open('medications.json', 'w') as file:
        json.dump(grouped_medications, file)

# Function to load data from a JSON file
def load_data_from_file():
    global grouped_medications
    try:
        with open('medications.json', 'r') as file:
            grouped_medications = json.load(file)
        show_dashboard()  # Update the dashboard with loaded data
        notify_today_medications()  # Check and notify about medications
    except FileNotFoundError:
        grouped_medications = {}

# Function to notify about today's medications
def notify_today_medications():
    today = datetime.today().strftime("%d-%m-%Y")
    print(f"Checking for medications on {today}")
    notifications = []

    if today in grouped_medications:
        print(f"Found medications for today: {grouped_medications[today]}")
        for med in grouped_medications[today]:
            if med["status"] == "Pending":
                notifications.append(f"{med['name']} at {med['time']} - Status: {med['status']}")
    else:
        print("No medications found for today")

    if notifications:
        message = "Today's Pending Medications:\n\n" + "\n".join(notifications)
        messagebox.showinfo("Medication Reminder", message)
    else:
        print("No pending notifications for today")

# Function to search medications based on name and/or status
def search_medications(med_name, status):
    results = []
    for date, meds in grouped_medications.items():
        for med in meds:
            name_match = med_name in med["name"].lower()
            status_match = (status == "All" or med["status"] == status)
            if name_match and status_match:
                results.append((date, med))
    return results


# ----------------------------
# Functions for UI Management
# ----------------------------

# Function to clear the frame and display the dashboard
def show_dashboard():
    for widget in content_frame.winfo_children():
        widget.destroy()
    display_dashboard()

# Function to handle the Schedule button click
def open_schedule_form(date=None, med_name=None, time=None, recurring=False, recurrence_frequency="daily", end_date=None):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Date Entry
    tk.Label(content_frame, text="Date (DD-MM-YYYY):", font=("Arial", 12)).pack(pady=5)
    date_entry = tk.Entry(content_frame, font=("Arial", 12))
    date_entry.pack(pady=5)
    if date:
        date_entry.insert(0, date)

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

    # Recurrence Options
    recurring_var = tk.BooleanVar(value=recurring)
    tk.Checkbutton(content_frame, text="Recurring", variable=recurring_var, font=("Arial", 12)).pack(anchor="w")

    tk.Label(content_frame, text="Recurrence Frequency:", font=("Arial", 12)).pack(pady=5)
    frequency_var = tk.StringVar(value=recurrence_frequency)
    frequencies = ["daily", "weekly", "monthly"]
    for freq in frequencies:
        tk.Radiobutton(content_frame, text=freq.capitalize(), variable=frequency_var, value=freq, font=("Arial", 12)).pack(anchor="w")

    tk.Label(content_frame, text="End Date (DD-MM-YYYY):", font=("Arial", 12)).pack(pady=5)
    end_date_entry = tk.Entry(content_frame, font=("Arial", 12))
    end_date_entry.pack(pady=5)
    if end_date:
        end_date_entry.insert(0, end_date)

    # Submit Button
    def submit_form():
        new_date = date_entry.get()
        new_med_name = med_name_entry.get()
        new_time = time_entry.get()
        recurring = recurring_var.get()
        frequency = frequency_var.get()
        new_end_date = end_date_entry.get()

        if new_date and new_med_name and new_time:
            add_or_update_medication(new_date, new_med_name, new_time, recurring, frequency, new_end_date, old_date=date, old_time=time)
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    submit_button = tk.Button(content_frame, text="Submit", font=("Arial", 12), command=submit_form)
    submit_button.pack(pady=20)


# Function to display the dashboard
def display_dashboard():
    # Loop through the grouped medications and display them by date
    for date, meds in grouped_medications.items():
        date_label = tk.Label(content_frame, text=date, font=("Arial", 16, "bold"), bg="lightgray")
        date_label.pack(fill="x", pady=(10, 0))
        
        for med in meds:
            med_frame = tk.Frame(content_frame, bg="lightyellow", padx=10, pady=5)
            med_frame.pack(fill="x", pady=2)
            
            time_label = tk.Label(med_frame, text=med["time"], font=("Arial", 14), width=10)
            time_label.pack(side="left")
            
            name_label = tk.Label(med_frame, text=med["name"], font=("Arial", 14), width=15)
            name_label.pack(side="left")
            
            status_label = tk.Label(med_frame, text=med["status"], font=("Arial", 14), width=10)
            status_label.pack(side="left")
            
            edit_button = tk.Button(med_frame, text="Edit", font=("Arial", 10), command=lambda d=date, t=med["time"], n=med["name"]: open_schedule_form(d, n, t))
            edit_button.pack(side="left", padx=5)
            
            delete_button = tk.Button(med_frame, text="Del", font=("Arial", 10), command=lambda d=date, t=med["time"]: delete_medication(d, t))
            delete_button.pack(side="left", padx=5)

            # Add "Mark as Taken" button
            taken_button = tk.Button(med_frame, text="Mark as Taken", font=("Arial", 10), command=lambda d=date, t=med["time"]: mark_as_taken(d, t))
            taken_button.pack(side="left", padx=5)

            # Add "Mark as Pending" button
            pending_button = tk.Button(med_frame, text="Mark as Pending", font=("Arial", 10), command=lambda d=date, t=med["time"]: mark_as_pending(d, t))
            pending_button.pack(side="left", padx=5)

# Function to mark a medication as taken
def mark_as_taken(date, time):
    meds = grouped_medications.get(date, [])
    for med in meds:
        if med["time"] == time:
            med["status"] = "Taken"
            break
    save_data_to_file()  # Save data after status update
    show_dashboard()  # Refresh the dashboard

# Function to mark a medication as pending
def mark_as_pending(date, time):
    meds = grouped_medications.get(date, [])
    for med in meds:
        if med["time"] == time:
            med["status"] = "Pending"
            break
    save_data_to_file()  # Save data after status update
    show_dashboard()  # Refresh the dashboard

# Function to handle the Notifications button click
def open_notifications_form():
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Notifications Options
    tk.Label(content_frame, text="Select Notification Methods:", font=("Arial", 12)).pack(pady=10)

    notification_methods = {
        "Text": tk.BooleanVar(),
        "Phone Call": tk.BooleanVar(),
        "Email": tk.BooleanVar(),
        "System Notification": tk.BooleanVar()
    }

    checkboxes = {}
    for method, var in notification_methods.items():
        check = tk.Checkbutton(content_frame, text=method, variable=var, font=("Arial", 12))
        check.pack(anchor="w")
        checkboxes[method] = check

    # Phone Number Entry
    phone_label = tk.Label(content_frame, text="Phone Number:", font=("Arial", 12))
    phone_entry = tk.Entry(content_frame, font=("Arial", 12))
    phone_label.pack(pady=10)
    phone_entry.pack(pady=5)

    # Email Entry
    email_label = tk.Label(content_frame, text="Email Address:", font=("Arial", 12))
    email_entry = tk.Entry(content_frame, font=("Arial", 12))
    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    # Submit Button
    def submit_notifications():
        selected_methods = [method for method, var in notification_methods.items() if var.get()]
        phone = phone_entry.get()
        email = email_entry.get()

        if selected_methods:
            message = f"Notifications will be sent via: {', '.join(selected_methods)}"
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
            messagebox.showinfo("Notifications Set", message)
            show_dashboard()  # Return to the dashboard
        else:
            messagebox.showwarning("Input Error", "Please select at least one notification method.")

    submit_button = tk.Button(content_frame, text="Submit", font=("Arial", 12), command=submit_notifications)
    submit_button.pack(pady=20)

# Function to open the search form
def open_search_form():
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
        display_search_results(search_results)

    submit_button = tk.Button(content_frame, text="Search", font=("Arial", 12), command=submit_search)
    submit_button.pack(pady=20)

# Function to display search results
def display_search_results(results):
    for widget in content_frame.winfo_children():
        widget.destroy()

    if not results:
        tk.Label(content_frame, text="No results found.", font=("Arial", 14)).pack(pady=20)
    else:
        for date, med in results:
            result_frame = tk.Frame(content_frame, bg="lightyellow", padx=10, pady=5)
            result_frame.pack(fill="x", pady=2)
            
            date_label = tk.Label(result_frame, text=date, font=("Arial", 14), width=15, anchor="w")
            date_label.pack(side="left", padx=5)
            
            time_label = tk.Label(result_frame, text=med["time"], font=("Arial", 14), width=10)
            time_label.pack(side="left")
            
            name_label = tk.Label(result_frame, text=med["name"], font=("Arial", 14), width=15)
            name_label.pack(side="left")
            
            status_label = tk.Label(result_frame, text=med["status"], font=("Arial", 14), width=10)
            status_label.pack(side="left")
            
            edit_button = tk.Button(result_frame, text="Edit", font=("Arial", 10), command=lambda d=date, t=med["time"], n=med["name"]: open_schedule_form(d, n, t))
            edit_button.pack(side="left", padx=5)
            
            delete_button = tk.Button(result_frame, text="Del", font=("Arial", 10), command=lambda d=date, t=med["time"]: delete_medication(d, t))
            delete_button.pack(side="left", padx=5)


# ----------------------------
# UI Initialization and Layout
# ----------------------------

# Frame for the top section (User's Name)
top_frame = tk.Frame(root, bg="lightblue", height=100)
top_frame.pack(fill="x")

user_name_label = tk.Label(top_frame, text="John Doe", font=("Arial", 20), bg="lightblue")
user_name_label.pack(pady=20)

# Frame for the left-side navigation bar
nav_frame = tk.Frame(root, bg="gray", width=80)
nav_frame.pack(side="left", fill="y")

# Navigation icons (These are represented by text for simplicity)
icons = [
    "Dashboard", "Search", "Schedule", 
    "History", "Notifications", "Payment", 
    "Preferences", "Settings"
]

for icon in icons:
    if icon == "Schedule":
        button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=open_schedule_form)
    elif icon == "Notifications":
        button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=open_notifications_form)
    elif icon == "Search":
        button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=open_search_form)
    else:
        button = tk.Button(nav_frame, text=icon, font=("Arial", 10), width=10, bg="lightgray", command=show_dashboard)
    button.pack(pady=10)

# Frame for the content area (dashboard or form)
content_frame = tk.Frame(root, bg="white")
content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Load data from file at the start
load_data_from_file()

# Display the initial dashboard
display_dashboard()

# ----------------------------
# Start the Tkinter event loop
# ----------------------------

root.mainloop()
