# Leveraging Historical Data in Digital Forensic & Open Source Intelligence for Football Match-Fixing Investigations

## Abstract

Match-fixing incidents in football cause significant damage to the integrity of the sport. This project aims to detect various anomalies for the purpose of match-fixing investigation using open source intelligence and digital forensic intelligence. The study focuses on betfair.com, one of the most important online betting exchange platforms, and its historical data.

The project analyzes datasets from May 2020 and July 2020, processing data from approximately 3,723 football matches across various world leagues. Using automated methods, the data is converted, processed, and visualized to detect anomalies based on predefined criteria.

## Project Structure

### 0_Login_ApiKey.py
This script handles the authentication process for accessing the Betfair API. It manages the login credentials and API key required for data retrieval.

### 1_Event_Files_Collection.py
This script finds the largest .bz2 files in a directory structure and copies them to appropriate destination folders. It separates large files (>5MB) from smaller ones.

### 2_Convert_and_Process_Event.py
This script converts the .bz2 files to CSV format. It includes a function to open files in the system's default application.

### 3_Convert_and_Process_All_Events.py
This script likely handles the bulk conversion of files and uses pandas for data manipulation and analysis.

### 4_Event_Timeline.py
This script probably creates a timeline of events based on the processed data, helping to visualize the sequence of betting activities.

### 5_Data_Visualisation (Graphs).py
This script generates various graphs and visualizations based on the analyzed data, aiding in the identification of patterns and anomalies.

### 6_Anomalie_Detection.py
This script implements the core anomaly detection logic. It applies various criteria to identify potential match-fixing incidents, including:

1. High percentage of money on market with high odds and significant total matched
2. Unusual betting patterns in small leagues
3. High percentage of money on market during specific time periods
4. Sharp increases in betting activity
5. Sudden changes in odds and market liquidity
6. Disproportionate bets in the early stages of a match
7. Disproportion of bets 
8. Win rate anomalies

The detected anomalies are stored in an SQLite database for further analysis.

## Usage

To use this project:
1. Ensure you have the necessary Python libraries installed.
2. Run the scripts in numerical order, starting with 0_Login_ApiKey.py.
3. The final output will be a database of detected anomalies, which can be further analyzed for potential match-fixing incidents.

## Note

This project is designed for research and investigative purposes. Always comply with legal and ethical standards when using this tool.
