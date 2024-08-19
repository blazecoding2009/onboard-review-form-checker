import os
from dotenv import load_dotenv
from airtable import Airtable

load_dotenv()

AIRTABLE_ACCESS_TOKEN = os.getenv('AIRTABLE_ACCESS_TOKEN')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
COLUMN_NAME = os.getenv('COLUMN_NAME')

airtable = Airtable(BASE_ID, TABLE_NAME, api_key=AIRTABLE_ACCESS_TOKEN)

def find_row_by_name(name):
    formula = f"{{{COLUMN_NAME}}}='{name}'"
    records = airtable.get_all(formula=formula)
    
    if records:
        for record in records:
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
            print("-" * 40)
    else:
        print(f"No records found for name: {name}")

if __name__ == "__main__":
    name_to_find = 'anirudh12032008'
    find_row_by_name(name_to_find)
