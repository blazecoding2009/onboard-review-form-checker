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

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Draw a rounded rectangle on the canvas."""
    points = [
        x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

root = tk.Tk()
root.title("Airtable Record Finder")
root.configure(bg="#f0f0f0")
root.geometry("600x500")

main_frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
main_frame.pack(expand=True, fill=tk.BOTH)

name_label = tk.Label(main_frame, text="Enter the Github Username you want to search for:", bg="#f0f0f0", font=("Arial", 12))
name_label.pack(anchor="center", pady=(0, 10))

entry_canvas = tk.Canvas(main_frame, width=370, height=50, bg="#f0f0f0", highlightthickness=0)
entry_canvas.pack(anchor="center", pady=(0, 10))
create_rounded_rectangle(entry_canvas, 0, 0, 370, 30, radius=15, fill="white", outline="white")

name_entry = tk.Entry(entry_canvas, font=("Arial", 12), bd=0, highlightthickness=0, relief="flat", justify="center")
entry_canvas.create_window(185, 15, window=name_entry, width=350, height=30)

search_button = tk.Button(main_frame, text="Search", command=on_search, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
search_button.pack(anchor="center", pady=(0, 10))

output_canvas = tk.Canvas(main_frame, width=500, height=300, bg="#f0f0f0", highlightthickness=0)
output_canvas.pack(anchor="center", pady=(10, 0))
create_rounded_rectangle(output_canvas, 0, 0, 500, 300, radius=15, fill="white", outline="white")

text_frame = tk.Frame(output_canvas, bg="white", bd=0)
output_canvas.create_window((250, 150), window=text_frame, anchor="center")
output_text = scrolledtext.ScrolledText(text_frame, font=("Courier", 10), bd=0, highlightthickness=0, wrap=tk.WORD)
output_text.pack(fill="both", expand=True)

root.mainloop()
