from tkinter import Frame, Label, Entry, Button, Radiobutton, StringVar
from data import search_medications
from medication_store import MedicationStore

def open_search_form(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Medication Name Entry
    Label(content_frame, text="Search by Medication Name:", font=("Arial", 12)).pack(pady=5)
    med_name_entry = Entry(content_frame, font=("Arial", 12))
    med_name_entry.pack(pady=5)

    # Status Selection
    Label(content_frame, text="Search by Status:", font=("Arial", 12)).pack(pady=5)
    status_var = StringVar(value="All")  # Default to "All"
    statuses = ["All", "Taken", "Pending", "Missed"]
    for status in statuses:
        Radiobutton(content_frame, text=status, variable=status_var, value=status, font=("Arial", 12)).pack(anchor="w")

    # Submit Button
    def submit_search():
        med_name = med_name_entry.get().strip().lower()
        selected_status = status_var.get()
        search_results = search_medications(med_name, selected_status)
        display_search_results(content_frame, search_results)

    submit_button = Button(content_frame, text="Search", font=("Arial", 12), command=submit_search)
    submit_button.pack(pady=20)

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

def display_search_results(content_frame, results):
    for widget in content_frame.winfo_children():
        widget.destroy()

    if not results:
        Label(content_frame, text="No results found.", font=("Arial", 14)).pack(pady=20)
    else:
        for date, med in results:
            result_frame = Frame(content_frame, bg="lightyellow", padx=10, pady=5)
            result_frame.pack(fill="x", pady=2)

            date_label = Label(result_frame, text=date, font=("Arial", 14), width=15, anchor="w")
            date_label.pack(side="left", padx=5)

            time_label = Label(result_frame, text=med["time"], font=("Arial", 14), width=10)
            time_label.pack(side="left")

            name_label = Label(result_frame, text=med["name"], font=("Arial", 14), width=15)
            name_label.pack(side="left")

            status_label = Label(result_frame, text=med["status"], font=("Arial", 14), width=10)
            status_label.pack(side="left")

            # Additional buttons can be added here
