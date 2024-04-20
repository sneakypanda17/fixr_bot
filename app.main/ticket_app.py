import tkinter as tk
from tkinter import ttk, messagebox
import json

import sys

# Add the path of your script to sys.path
module_path = '../web_scraper'
if module_path not in sys.path:
    sys.path.append(module_path)
print(module_path)

# Import the script as a module
import get_events

# Call the function from the script
get_events.main()


class TicketApp(tk.Tk):
    def __init__(self, json_path):
        super().__init__()

        self.title("Ticket Purchase App")
        self.geometry("300x200")

        # Read dates from JSON at a given path
        self.ticket_types = self.read_ticket_types(json_path)
        self.ticket_quantity = tk.IntVar(value=1)

        # Widgets
        self.create_widgets()

    def read_ticket_types(self, filepath):
        """Reads dates from the 'date' key in a JSON file and returns a list of dates."""
        types = []
        try:
            with open(filepath, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                types = [item['date'] for item in data if 'date' in item]
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file at {filepath} was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "The JSON file is malformed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        return types

    def create_widgets(self):
        # Ticket Type Dropdown
        ttk.Label(self, text="Select Date:").pack(pady=10)
        self.ticket_type_combo = ttk.Combobox(self, values=self.ticket_types, state="readonly")
        self.ticket_type_combo.pack()
        self.ticket_type_combo.current(0)

        # Ticket Quantity Entry
        ttk.Label(self, text="Enter Quantity:").pack(pady=10)
        self.quantity_entry = ttk.Entry(self, textvariable=self.ticket_quantity)
        self.quantity_entry.pack()

        # Purchase Button
        ttk.Button(self, text="Purchase", command=self.purchase_tickets).pack(pady=20)

    def purchase_tickets(self):
        ticket_type = self.ticket_type_combo.get()
        quantity = self.ticket_quantity.get()
        message = f"You have purchased {quantity} tickets for the date {ticket_type}."
        messagebox.showinfo("Purchase Confirmation", message)

# Run the application with a path to the JSON
if __name__ == "__main__":
    json_file_path = "../web_scraper/events.json"  # Adjust this path as needed
    app = TicketApp(json_file_path)
    app.mainloop()
