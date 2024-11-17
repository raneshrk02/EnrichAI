import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

def setup_sheets_connection():
    creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service
        
    except Exception as e:
        print(f"Error setting up Google Sheets connection: {str(e)}")
        return None

def get_sheet_data(sheet_url: str) -> pd.DataFrame:
    try:
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        
        service = setup_sheets_connection()
        if not service:
            return None
            
        #Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range='A1:Z1000'  
        ).execute()
        
        values = result.get('values', [])
        if not values:
            return None
            
        #Convert to DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
        
    except Exception as e:
        print(f"Error getting sheet data: {str(e)}")
        return None