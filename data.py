import json
from datetime import datetime, timedelta
import os
from tkinter import messagebox
from medication_store import MedicationStore
import bcrypt

# File path for storing user credentials
USERS_FILE = 'users.json'

def add_or_update_medication(date, med_name, time, recurring=False, frequency="daily", end_date=None, old_date=None, old_time=None):
    if old_date and old_time:  
        # If updating an existing reminder
        meds = MedicationStore.grouped_medications.get(old_date, [])
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
                        del MedicationStore.grouped_medications[old_date]
                    add_medication(date, med_name, time, recurring, frequency, end_date)
                break
    else:
        # Create the first instance of the medication
        add_medication(date, med_name, time, recurring, frequency, end_date)

        if recurring and end_date:
            # Generate future instances based on the recurrence frequency
            generate_future_instances(date, med_name, time, frequency, end_date)

    MedicationStore.save_data_to_file()  # Save data after any modification

def add_medication(date, med_name, time, recurring=False, frequency="daily", end_date=None):
    if date not in MedicationStore.grouped_medications:
        MedicationStore.grouped_medications[date] = []
    MedicationStore.grouped_medications[date].append({
        "time": time, 
        "name": med_name, 
        "status": "Pending", 
        "recurring": recurring, 
        "recurrence_frequency": frequency, 
        "end_date": end_date
    })

def generate_future_instances(start_date, med_name, time, frequency, end_date):
    current_date = datetime.strptime(start_date, "%m-%d-%Y")
    end_date = datetime.strptime(end_date, "%m-%d-%Y")

    while current_date < end_date:
        if frequency == "daily":
            current_date += timedelta(days=1)
        elif frequency == "weekly":
            current_date += timedelta(weeks=1)
        elif frequency == "monthly":
            current_date = add_months(current_date, 1)

        # Add the next instance to grouped_medications
        formatted_date = current_date.strftime("%m-%d-%Y")
        add_medication(formatted_date, med_name, time, recurring=True, frequency=frequency, end_date=end_date.strftime("%m-%d-%Y"))

def add_months(source_date, months):
    # Utility function to handle month-end overflow
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, [31, 29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return source_date.replace(year=year, month=month, day=day)

def delete_medication(date, time):
    grouped_medications = MedicationStore.grouped_medications  # Access the stored medications directly

    meds = grouped_medications.get(date, [])
    for med in meds:
        if med["time"] == time:
            meds.remove(med)
            if not meds:
                del grouped_medications[date]
            break
    save_data_to_file()

def save_data_to_file():
    MedicationStore.save_data_to_file()

def load_data_from_file():
    MedicationStore.load_data_from_file()

def notify_today_medications():
    grouped_medications = MedicationStore.grouped_medications  # Access the stored medications directly

    today = datetime.today().strftime("%m-%d-%Y")
    notifications = []

    print(f"Checking for medications on {today}")  # Debugging line

    if today in grouped_medications:
        print(f"Found medications for today: {grouped_medications[today]}")  # Debugging line
        for med in grouped_medications[today]:
            if med["status"] == "Pending":
                notifications.append(f"{med['name']} at {med['time']} - Status: {med['status']}")
    else:
        print("No medications found for today")  # Debugging line

    if notifications:
        message = "Today's Pending Medications:\n\n" + "\n".join(notifications)
        print("Displaying notification box")  # Debugging line
        messagebox.showinfo("Medication Reminder", message)
    else:
        print("No pending notifications for today")  # Debugging line


def search_medications(med_name, status):
    grouped_medications = MedicationStore.grouped_medications  # Access the stored medications directly

    results = []
    for date, meds in grouped_medications.items():
        for med in meds:
            name_match = med_name in med["name"].lower()
            status_match = (status == "All" or med["status"] == status)
            if name_match and status_match:
                results.append((date, med))
    return results

def mark_as_taken(date, time):
    grouped_medications = MedicationStore.grouped_medications  # Access the stored medications directly

    meds = grouped_medications.get(date, [])
    for med in meds:
        if med["time"] == time:
            med["status"] = "Taken"
            save_data_to_file()
            return True  # Indicate that the status was updated
    return False  # Indicate no update was made

def mark_as_pending(date, time):
    grouped_medications = MedicationStore.grouped_medications  # Access the stored medications directly

    meds = grouped_medications.get(date, [])
    for med in meds:
        if med["time"] == time:
            med["status"] = "Pending"
            save_data_to_file()
            return True  # Indicate that the status was updated
    return False  # Indicate no update was made

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_password
    save_users(users)
    return True, "Registration successful."

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."

    stored_password = users[username].encode()
    if bcrypt.checkpw(password.encode(), stored_password):
        return True, "Login successful."
    else:
        return False, "Incorrect password."