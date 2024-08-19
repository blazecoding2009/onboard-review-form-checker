import os
from dotenv import load_dotenv
from airtable import Airtable

load_dotenv()

AIRTABLE_ACCESS_TOKEN = os.getenv('AIRTABLE_ACCESS_TOKEN')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
COLUMN_NAME = os.getenv('COLUMN_NAME')

airtable = Airtable(BASE_ID, TABLE_NAME, api_key=AIRTABLE_ACCESS_TOKEN)

def is_name_in_airtable(name):
    formula = f"{{{COLUMN_NAME}}}='{name}'"
    result = airtable.get_all(formula=formula)
    
    return len(result) > 0

name_to_check = 'Zacharie Morin'
if is_name_in_airtable(name_to_check):
    print(f"{name_to_check} is in Airtable.")
else:
    print(f"{name_to_check} is not in Airtable.")
