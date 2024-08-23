import os
from dotenv import load_dotenv
from airtable import Airtable

load_dotenv()

# .env file vars
AIRTABLE_ACCESS_TOKEN = os.getenv('AIRTABLE_ACCESS_TOKEN')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
COLUMN_NAME = os.getenv('COLUMN_NAME')

# start the Airtable client
airtable = Airtable(BASE_ID, TABLE_NAME, api_key=AIRTABLE_ACCESS_TOKEN)

def find_row_by_name(name):
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
            
            print(f"Name: {name}")
            print(f"Date of Birth: {dob}")
            print(f"Email: {email}")
            print(f"Proof of Enrollment Images: {', '.join(proof_image_links) if proof_image_links else 'None'}")
            
            # set 'Action: Find PR link' to true
            if not fields.get('Action: Find PR link', False):
                airtable.update(record_id, {'Action: Find PR link': True})
                print("Updated Action Find PR link to True")
            else:
                print("Action Find PR link is already set to True")
            
            print("-" * 40)
    else:
        print(f"No records found for Github Username: {name}")

if __name__ == "__main__":
    name_to_find = input("Enter the Github Username you want to search for: ")
    find_row_by_name(name_to_find)
