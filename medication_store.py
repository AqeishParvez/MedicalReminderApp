# This file contains the MedicationStore class which is responsible for storing the medications in a dictionary
import json
from datetime import datetime

class MedicationStore:
    grouped_medications = {}

    @classmethod
    def load_data_from_file(cls):
        try:
            with open('medications.json', 'r') as file:
                cls.grouped_medications = json.load(file)
            cls.update_missed_medications()  # Update status of missed medications
            print("Loaded medications:", cls.grouped_medications)
        except FileNotFoundError:
            cls.grouped_medications = {}

    @classmethod
    def save_data_to_file(cls):
        with open('medications.json', 'w') as file:
            json.dump(cls.grouped_medications, file)

    @classmethod
    def update_missed_medications(cls):
        today = datetime.today().strftime("%m-%d-%Y")
        current_time = datetime.now().strftime("%H:%M %p")

        for date, meds in cls.grouped_medications.items():
            for med in meds:
                # For medications on today or future dates
                if date >= today:
                    # If the medication is in the future, ensure it's set to pending
                    if date > today or (date == today and med["time"] > current_time):
                        med["status"] = "Pending"
                    # If the medication is today and time has passed, mark as missed
                    elif date == today and med["time"] < current_time and med["status"] == "Pending":
                        med["status"] = "Missed"
        
        cls.save_data_to_file()  # Save updated status
