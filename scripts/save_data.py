from google.oauth2.service_account import Credentials  # type: ignore
import gspread  # type: ignore
from datetime import datetime
import os
from dotenv import load_dotenv  # type: ignore
import os

# Load .env from the project's root directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")

# Authenticate Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

# **** Define a fixed header order for consistency ****
HEADER_ORDER = [
    "name", 
    "start_time", 
    "end_time", 
    "total_hours", 
    "meeting_date", 
    "note", 
    "transcript", 
    "creation_date"
]

def check_and_add_headers(sheet, data):
    """
    Check if headers exist in the Google Sheet and update them using a fixed header order.
    Instead of deleting the existing header row, we update cell A1 with the HEADER_ORDER.
    """
    first_row = sheet.row_values(1)  # Read the first row

    # If headers are missing or do not match the fixed order, update them
    if not first_row or first_row != HEADER_ORDER:
        print("Headers missing or incorrect. Updating headers...")
        sheet.update('A1', [HEADER_ORDER])  # Overwrite the header row with HEADER_ORDER
        print("Headers updated successfully!")

# Save the result to Google Sheets using the API with creation date
def save_to_google_sheets(data):
    if "error" in data:
        print("Error: Invalid data, skipping Google Sheets update.")
        return
    
    check_and_add_headers(sheet, data)
    
    # **** Add creation_date if not provided ****
    data['creation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # **** Construct row based on fixed header order ****
    row = [data.get(key, "") for key in HEADER_ORDER]
    
    sheet.append_row(row)
    print("Data saved to Google Sheets successfully!")
