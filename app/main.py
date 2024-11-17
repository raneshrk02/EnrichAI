import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from utils.data_processor import validate_file, process_batch, validate_data, export_results, get_error_report, errors
from utils.sheets import get_sheet_data

#Load environment variables
load_dotenv()

def main():
    st.markdown("<h1 style='text-align: center;'>AI-Driven Data Enhancement Platform</h1>", unsafe_allow_html=True)
    
    #File upload section
    st.header("1. Data Input")
    data_source = st.radio(
        "Choose your data source:",
        ("Upload CSV", "Google Sheets")
    )
    
    df = None
    
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            valid, message = validate_file(uploaded_file)
            if not valid:
                st.error(message)
                return
            df = pd.read_csv(uploaded_file)
    else:
        sheet_url = st.text_input("Enter Google Sheet URL")
        if sheet_url:
            df = get_sheet_data(sheet_url)
    
    if df is not None:
        st.write("Preview of your data:")
        st.dataframe(df.head())
        
        #Column selection
        st.header("2. Configure Search")
        selected_column = st.selectbox(
            "Select the column containing entities:",
            df.columns.tolist()
        )
        
        #Query input from user
        query_input = st.text_input(
            "Enter your query:",
            "Give details about {entity}"  
        )
        st.caption("Use {entity} as a placeholder for each item in your selected column")

        #Validate data
        required_columns = [selected_column]  
        valid, message = validate_data(df, required_columns)
        if not valid:
            st.error(message)
            return
        
        #Process button
        if st.button("Start Processing"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            entity_from_query = query_input.split("{")[1].split("}")[0].strip()  # Extract entity in curly braces
            st.write(f"Processing entity: {entity_from_query}")

            entity_lower = entity_from_query.lower()
            column_values_lower = df[selected_column].str.lower()
            
            matching_rows = df[column_values_lower.str.contains(entity_lower, na=False)] # Wildcard matching

            if matching_rows.empty:
                st.error(f"No results found for the entity '{entity_from_query}' in the selected column.")
                return

            results = process_batch(matching_rows, selected_column, query_input, batch_size=5)

            #Display results
            st.header("3. Results")
            result_df = pd.DataFrame(results)
            st.dataframe(result_df)

            #Export results
            st.header("4. Export Results")

            csv = export_results(results, output_format='csv')
            st.download_button(
                label="Download Results",
                data=csv,
                file_name="enriched_data.csv",
                mime="text/csv"
            )

            #Display error report
            if errors:
                st.header("5. Error Report")
                error_report = get_error_report()
                st.write(error_report)

if __name__ == "__main__":
    main()