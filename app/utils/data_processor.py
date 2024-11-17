import os
import pandas as pd
from typing import List, Dict, Union, Tuple
from .search import search_entity
from .llm import process_with_llm

errors = []

def validate_file(file) -> Tuple[bool, str]:
    if file is None:
        return False, "No file uploaded"
        
    #File size
    file_size = file.size / (1024 * 1024)  # Convert to MB
    if file_size > 10:
        return False, "File size should be less than 10MB"
        
    #File extension(CSV)
    if not file.name.endswith('.csv'):
        return False, "Only CSV files are allowed"
        
    return True, "File is valid"

def process_batch(data: pd.DataFrame, entity_column: str, query_template: str, batch_size: int = 5) -> List[Dict]:
    results = []
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        
        for _, row in batch.iterrows():
            entity = row[entity_column]
            try:
                #Search for entity
                search_results = search_entity(entity, query_template)
                
                #Process with LLM
                extracted_info = process_with_llm(search_results, entity, query_template)
                
                result = {}

                for col in data.columns:
                    result[col] = row[col]

                result['extracted_info'] = extracted_info
                result['status'] = 'success'

                results.append(result)
            
            except Exception as e:
                result = {}
                for col in data.columns:
                    result[col] = row[col]

                result['extracted_info'] = str(e)
                result['status'] = 'error'

                errors.append(f"Error processing {entity}: {str(e)}")
                results.append(result)
            
    return results

def validate_data(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, str]:
    if df.empty:
        return False, "DataFrame is empty"
        
    #Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
        
    #Check for empty values in required columns
    for col in required_columns:
        if df[col].isnull().any():
            return False, f"Column '{col}' contains empty values"
            
    return True, "Data is valid"

def export_results(results: List[Dict], 
                   output_format: str = 'csv',
                   output_path: str = None) -> Union[str, pd.DataFrame]:

    df = pd.DataFrame(results)
    
    if output_format == 'csv':
        if output_path:
            df.to_csv(output_path, index=False)
            return output_path
        return df.to_csv(index=False)
        
    elif output_format == 'json':
        if output_path:
            df.to_json(output_path, orient='records')
            return output_path
        return df.to_json(orient='records')
        
    elif output_format == 'excel':
        if output_path:
            df.to_excel(output_path, index=False)
            return output_path
        raise ValueError("Output path is required for Excel format")
        
    return df

def get_error_report() -> Dict:
    return {
        'total_errors': len(errors),
        'error_messages': errors
    }