import os
from dotenv import load_dotenv
from airtable import Airtable
import tkinter as tk
from tkinter import messagebox, scrolledtext

load_dotenv()

# .env file vars
AIRTABLE_ACCESS_TOKEN = os.getenv('AIRTABLE_ACCESS_TOKEN')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
COLUMN_NAME = os.getenv('COLUMN_NAME')

# Start the Airtable client
airtable = Airtable(BASE_ID, TABLE_NAME, api_key=AIRTABLE_ACCESS_TOKEN)

def find_row_by_name(name, output_text):
    formula = f"{{{COLUMN_NAME}}}='{name}'"
    records = airtable.get_all(formula=formula)
    
    if records:
        for record in records:
            record_id = record['id']
            fields = record['fields']
            dob = fields.get('Birthdate', 'N/A')
            email = fields.get('Email', 'N/A')
            name = fields.get('Full Name', 'N/A')
            
            proof_of_enrollment = fields.get('Proof of High School Enrollment', [])
            proof_image_links = [attachment['url'] for attachment in proof_of_enrollment if 'url' in attachment]
            
            output_text.insert(tk.END, f"Name: {name}\n")
            output_text.insert(tk.END, f"Date of Birth: {dob}\n")
            output_text.insert(tk.END, f"Email: {email}\n")
            output_text.insert(tk.END, f"Proof of Enrollment Images: {', '.join(proof_image_links) if proof_image_links else 'None'}\n")
            
            if not fields.get('Action: Find PR link', False):
                airtable.update(record_id, {'Action: Find PR link': True})
                output_text.insert(tk.END, "Updated Action Find PR link to True\n")
            else:
                output_text.insert(tk.END, "Action Find PR link is already set to True\n")
            
            output_text.insert(tk.END, "-" * 40 + "\n")
    else:
        messagebox.showinfo("Result", f"No records found for Github Username: {name}")

def on_search():
    name_to_find = name_entry.get()
    output_text.delete(1.0, tk.END)
    find_row_by_name(name_to_find, output_text)

root = tk.Tk()
root.title("Airtable Record Finder")

name_label = tk.Label(root, text="Enter the Github Username you want to search for:")
name_label.pack(pady=5)

name_entry = tk.Entry(root, width=50)
name_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=60, height=20)
output_text.pack(pady=10)

root.mainloop()
