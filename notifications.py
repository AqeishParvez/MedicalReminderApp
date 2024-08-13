# Description: This file contains the code to display the notifications form in the application.
from tkinter import Label, Entry, Button, Checkbutton, BooleanVar

def open_notifications_form(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Notifications Options
    Label(content_frame, text="Select Notification Methods:", font=("Arial", 12)).pack(pady=10)

    notification_methods = {
        "Text": BooleanVar(),
        "Phone Call": BooleanVar(),
        "Email": BooleanVar(),
        "System Notification": BooleanVar()
    }

    for method, var in notification_methods.items():
        Checkbutton(content_frame, text=method, variable=var, font=("Arial", 12)).pack(anchor="w")

    # Phone Number Entry
    Label(content_frame, text="Phone Number:", font=("Arial", 12)).pack(pady=10)
    phone_entry = Entry(content_frame, font=("Arial", 12))
    phone_entry.pack(pady=5)

    # Email Entry
    Label(content_frame, text="Email Address:", font=("Arial", 12)).pack(pady=10)
    email_entry = Entry(content_frame, font=("Arial", 12))
    email_entry.pack(pady=5)

    # Submit Button
    def submit_notifications():
        selected_methods = [method for method, var in notification_methods.items() if var.get()]
        phone = phone_entry.get()
        email = email_entry.get()

        if selected_methods:
            # Logic to handle notifications
            pass

    submit_button = Button(content_frame, text="Submit", font=("Arial", 12), command=submit_notifications)
    submit_button.pack(pady=20)
