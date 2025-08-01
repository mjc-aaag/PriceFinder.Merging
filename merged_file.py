import pandas as pd 
import os
from datetime import datetime

folder_path = r'dataset\rockhampton_qld'
default_template = r'template\default_template.csv'
export_path = r'exported'

columns_to_keep = ['Street Address', 'Suburb', 'State', 'Postcode', 'Property Type', 
                   'Bed', 'Bath', 'Car', 'Land Size (m²)', 'Floor Size (m²)',
                   'Year Built', 'Sale Price','Sale Date', 'Settlement Date', 'Sale Type','Agency','Agent',
                   'Land Use', 'Development Zone', 'Parcel Details', 'Owner 1 Name','Owner 2 Name' ,'Owner 3 Name', 'Owner Type', 'Vendor 1 Name' ,'Vendor 2 Name', 
                   'Vendor 3 Name', 'Open in RPData']

column_mapping = {'Street Display' : 'Street Address', 'Locality' : 'Suburb', 'Postcode' : 'Postcode', 'Legal Description' : 'Parcel Details', 
                   'Vendor Names' : 'Vendor 1 Name', 'Purchaser Names' : 'Owner 1 Name', 'Office Name' : 'Agency', 'Agent Name' : 'Agent', 'Build Year' :'Year Built',
                   'Area' : 'Land Size (m²)', 'Building Area' : 'Floor Size (m²)', 
                   'Bedrooms': 'Bed', 'Bathrooms' : 'Bath', 'Car Parks' : 'Car' ,
                   'PDS ID' : 'Open in RPData'}

#CHANGE THIS TO NECESSARY STATE
state = 'QLD'

def merged_file(folder_path):
    
    os.makedirs(folder_path,exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dataframes = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path,file)
        
        if not file.lower().endswith(('.csv', '.xlsx', '.xls')):
            continue
        
        try:
            if file.endswith('.csv'):
                data = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
            elif file.endswith('.xlsx'):
                data = pd.read_excel(file_path, engine='openpyxl')
            elif file.endswith('.xls'):
                data = pd.read_excel(file_path,engine='xlrd')
        except Exception as e:  
            print(f'Reading Error {file} : {e}')
            continue
        
        data = data.drop(columns='Disclaimer')
        
        data = data.dropna(how='all')
        
        if 'Sale Date' in data.columns:
            data['Sale Date'] = pd.to_datetime(data['Sale Date'], errors='coerce')
            data['Sale Date'] = data['Sale Date'].dt.strftime('%d/%m/%Y')

        if 'Settlement Date' in data.columns:
            data['Settlement Date'] = pd.to_datetime(data['Settlement Date'], errors='coerce')
            data['Settlement Date'] = data['Settlement Date'].dt.strftime('%d/%m/%Y')
            
        if 'State' not in data.columns:
            data['State'] = state
            
            
        additional_columns = ['Owner 2 Name' ,'Owner 3 Name', 'Owner Type', 'Vendor 2 Name', 
                   'Vendor 3 Name', 'Development Zone']
        
        for col in additional_columns:
            if col not in data.columns:
                data[col] = ''
                
        data.rename(columns=column_mapping, inplace = True)
        
        #THIS MIGHT CAUSE AN ERROR IN IMPORTING TO THE RP DATA
        #if 'lotplan' not in data.columns:
            #data['lotplan'] = data['Parcel Details'].apply(lambda x : x.split('&')[0].strip()
                                                           #if isinstance(x, str) else '')
        
        
        url_text = 'https://app.pricefinder.com.au/v4/app?page=property/PropertyLink&service=external&action=property&propertyid='
        data['Open in RPData'] = data['Open in RPData'].apply(lambda x : url_text + str(int(x)))
        
        filtered_columns = [col for col in columns_to_keep if col in data.columns]
        data_filtered = data[filtered_columns]
        
    
        if not data.empty:
            dataframes.append(data_filtered)
        else:
            print(f"Skipped empty/invalid after cleaning: {file}")
                      
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        output_file = os.path.join(export_path, f'Merged File {timestamp}.csv')
        output_file_xlsx = os.path.join(export_path, f'Merged File {timestamp}.xlsx')
        merged_df.to_csv(output_file, encoding='utf-8', index=False)
        merged_df.to_excel(output_file_xlsx,index=False)
        print(f"Merged file saved: {output_file}")
        print(f'Merged file saved: {output_file_xlsx}')
        return output_file
    else:
        print("No valid data after cleaning.")
        return None       
        
merged_file(folder_path=folder_path)

