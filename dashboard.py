import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from datetime import datetime
import os

filepath = r'exported\Merged File 20250731_134520.csv'
export_path = r'exported'

def create_dashboard(filepath):
    data = pd.read_csv(filepath,encoding='latin-1', low_memory=False)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    data.to_excel(os.path.join(export_path,f'exported_excel_{timestamp}.xlsx'))
    
create_dashboard(filepath=filepath)