# EnrichAI 

> An AI-Driven Data Enhancement Platform for intelligent data enrichment and processing

## Overview

EnrichAI is a powerful tool built using Streamlit that enhances tabular data by fetching relevant information from online sources and using AI language models for data enrichment. The platform supports input from both CSV files and Google Sheets and provides batch processing, error reporting, and downloadable results.

## Features

- **Data Input**: Upload a CSV file or fetch data from Google Sheets
- **Validation**: Validate files and data for integrity and correctness
- **Search & Query**: Fetch information using Google Search API (SerpAPI)
  - Define dynamic queries with placeholders like `{entity}` for flexibility
- **AI Enrichment**: Process search results using a Groq-powered LLM to generate detailed responses
- **Batch Processing**: Handles data in batches for efficient processing
- **Results and Exports**: Display enriched data in the app
  - Export results in CSV format
- **Error Reporting**: Provides a detailed error log for debugging and review

## Project Structure

```
project/
│
├── main.py                       # Main Streamlit app
├── utils/
│   ├── data_processor.py         # Handles data validation and processing
│   ├── sheets.py                 # Manages Google Sheets integration
│   ├── search.py                 # Implements SerpAPI-based search
│   ├── llm.py                    # LLM integration for enrichment
├── .env                          # Stores environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## Installation

### Prerequisites

- **Python Version**: Python 3.8 or above
- **API Credentials**:
  - Google Sheets: A service account key in JSON format
  - SerpAPI: API key for search functionality
  - Groq: API key for language model integration

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/raneshrk02/EnrichAI.git
   cd EnrichAI
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project directory and add:
   ```
   GOOGLE_SHEETS_CREDENTIALS=<path_to_service_account_key>
   SERPAPI_API_KEY=<your_serpapi_key>
   GROQ_API_KEY=<your_groq_api_key>
   ```

4. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

## Usage

1. **Data Input**: 
   - Select the data source: Upload a CSV file or provide a Google Sheets URL
   - If using Google Sheets, ensure your credentials are properly set up

2. **Configure Search**: 
   - Select the column containing the entities to search
   - Input a query template, using `{entity}` as a placeholder for dynamic entity insertion

3. **Start Processing**: 
   - Click 'Start Processing' to fetch data and process with the AI model
   - Results will be displayed in the app

4. **Export Results**: 
   - Download the enriched data as a CSV file

5. **Error Report**: 
   - If any errors occur during processing, view a detailed error report in the app

## API Integrations

- **Google Sheets API**: Used to fetch tabular data from a given Google Sheets URL
- **SerpAPI**: Retrieves search results for each entity using a dynamic query
- **Groq LLM API**: Processes search results and generates relevant enriched data

## Future Enhancements

- Add support for more file formats
- Implement parallel processing for faster batch execution
- Enhance error reporting with more granular details
- Integrate additional AI models for improved data enrichment

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributors

- Ranesh RK
