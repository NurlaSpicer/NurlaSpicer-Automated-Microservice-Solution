# Project Overview

This project involves three microservices, two of which are interconnected. These microservices assist in automating processes on a platform specializing in the creation and management of bots. Below is a detailed description of each microservice and its functionality.

## Microservices

### 1. `excelToGoogleSheet.py` and `OutputFromBP.py`

These microservices handle the following tasks:

- **Data Collection and Analysis**: They gather and process analytics and data related to bots. This involves organizing, filtering, and preparing data using APIs.
- **Export to Google Sheets**: The processed data is then exported to Google Sheets for further analysis and reporting.

### 2. `DownloadAudio.py`

This microservice is responsible for:

- **Audio Export**: It facilitates the export of bot audio recordings to a local directory. This process is managed via API, including handling authorization to the platform.

## Project Structure

The project relies on several libraries and modules:

- **`os`**: For interacting with the operating system, such as file and directory management.
- **`json`**: For handling JSON data.
- **`requests`**: For making HTTP requests to APIs.
- **`pandas`**: For data manipulation and analysis.
- **`googleapiclient`**: For interacting with Google APIs, specifically Google Sheets.
- **`google.oauth2`**: For handling authentication and authorization.

## Setup Instructions

1. **Install Required Libraries**

   Make sure to install the necessary Python libraries by running:

   ```bash
   pip install pandas google-api-python-client google-auth
