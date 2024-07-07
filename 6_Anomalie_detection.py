import sqlite3
import os
import pandas as pd
import numpy as np  # Import numpy for NaN values

# Create a new SQLite database file
conn = sqlite3.connect('anomaly_detection_errors.db')
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS anomaly_detections
             (id INTEGER PRIMARY KEY AUTOINCREMENT, criteria TEXT, market TEXT, bet TEXT, file_path TEXT, explanation TEXT, details TEXT)''')


# Define the folder path containing event folders
event_folders = "/Users/noahroni/Documents/Test/Event_Folders_errors/"
#print(event_folders)

# Get a list of all subdirectories in the event_folders directory
subdirectories = [os.path.join(event_folders, d) for d in os.listdir(event_folders) if os.path.isdir(os.path.join(event_folders, d))]
#print(subdirectories[0])

# Iterate over all subdirectories
for subdirectory in subdirectories:
    # Get a list of all files in the subdirectory
    files = [os.path.join(subdirectory, f) for f in os.listdir(subdirectory) if os.path.isfile(os.path.join(subdirectory, f)) and f.endswith('.csv')]

    # Iterate over all files in the subdirectory
    for file_path in files:
        # Print the filename
        #print(file_path) 
       
        file = pd.read_csv(file_path)
        #print(f"CSV file loaded successfully. Shape: {file.shape}")

        # 1. criteria: 

        # Filter the DataFrame based on the given conditions
        filtered_file = file[
            (file['percent_money_on_market'] > 95) & 
            (file['selection_ex.availableToBack.price'] > 4) & 
            (file['selection_totalMatched'] > 10000) 
        ]

        # Print the filtered DataFrame with related columns
        if not filtered_file.empty:
            #print(filtered_file)
            print("Anomalie alert: 1. criteria: ", {file_path})
            criteria = "1. criteria"
            market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
            bet = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
            explanation = "Anomaly detected based on criteria 1"
            details = "Percent of money on market is higher than 95%, total matched is higher than 10000, and selection price is higher than 4"
            c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                      (criteria, market, bet, file_path, explanation, detail))
            conn.commit()

            # check if there is a this criteria, as last time goal ??

        else:
            pass
            #print("No rows meet the criteria.")
        
        # 2. criteria  (only for small leagues!!)
        # For different leagues - different summ of bets. 
        #For example, for Indonesia 1 league 7,000 dollars in goal in a half, this is a small bets. 
        #For Brazil U-20 are already significant bets

        # Filter the DataFrame based on the given conditions
        filtered_file = file[
            (file['Minute'] < 40) &
            ((file['Minute'] > 50) & (file['Minute'] < (file['Minute'].max() - 4))) &
            (file['selection_ex.availableToBack.price'] > 1.3) &
            (file['selection_totalMatched'] > 15000)
        ]


        # Print the filtered DataFrame with related columns
        if not filtered_file.empty:
            #print(filtered_file)
            print("Anomalie alert: 2. criteria: ", {file_path})
            criteria = "2. criteria"
            market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
            bet = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
            explanation = "Anomaly detected based on criteria 2"
            datails = "During the match except the last 5 minutes,selection total matched is higher than 15000, and selection price is higher than 1.3"
            c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                      (criteria, market, bet, file_path, explanation))
            conn.commit()
        else:
            pass
            #print("No rows meet the criteria.")
        
        # 3. criteria: 

        # Filter the DataFrame based on the given conditions
        filtered_file = file[
            (file['percent_money_on_market'] > 90) &
            (file['Minute'] < 40) &
            ((file['Minute'] > 50) & (file['Minute'] < 85))
        ]

        # Print the filtered DataFrame with related columns
        if not filtered_file.empty:
            #print(filtered_file)
            print("Anomalie alert: 3. criteria: ", {file_path})
            criteria = "3. criteria"
            market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
            bet = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
            explanation = "Anomaly detected based on criteria 3"
            c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                      (criteria, market, bet, file_path, explanation))
            conn.commit()
        else:
            #print("No rows meet the criteria.")
            pass
        
        
        # 5. criteria: 

        # A special charm in games where there is a sharp increase in the summ of bets at the end of the game.

        # at least 20 percentage chance in last 10 minutes

        # Assuming 'publishTime' is in datetime format, if not convert it first
        file['publishTime'] = pd.to_datetime(file['publishTime'], format='%d.%m.%Y %H:%M:%S')

        # Split the DataFrame into two halves
        half_index = len(file) // 2
        file = file.iloc[:half_index]

        # Get unique options in the selection_md.name column
        unique_options = file['selection_md.name'].unique()

        # Define a function to check for 25% change in the "percent_money_on_market" column
        def check_percent_change(rows):
            # Check if the group has at least two rows
            if len(rows) < 2:
                return False

            # Get the first and last row for the 10-minute interval
            first_row = rows.iloc[0]
            last_row = rows.iloc[-1]
            
            # Check if any of the status is "Match ended" or totalMatched is 0
            if any(rows['status'] == 'Match ended') or any(rows['totalMatched'] == 0):
                return False
            
            # Check for zero or invalid values in the first row's percent_money_on_market
            if first_row['percent_money_on_market'] == 0 or np.isnan(first_row['percent_money_on_market']):
                return False
            
            # Calculate percent change in "percent_money_on_market" column
            try:
                percent_change = ((last_row['percent_money_on_market'] - first_row['percent_money_on_market']) / first_row['percent_money_on_market']) * 100
            except ZeroDivisionError:
                # Handle division by zero error
                return False
            
            # Return the percent change along with the row numbers
            if abs(percent_change) >= 20:   # Change threshold could be more than 20%
                return percent_change, rows.index[0], rows.index[-1]
            else:
                return False

        # Iterate over each unique option
        for option in unique_options:
            # Filter rows for the current option
            option_rows = file[file['selection_md.name'] == option]
            
            # Group rows by 10-minute intervals based on 'publishTime'
            grouped_rows = option_rows.groupby(pd.Grouper(key='publishTime', freq='10T'))

            # Flag to track if any rows meet the criteria
            any_rows_meet_criteria = False
            
            # Iterate over each group
            for _, group in grouped_rows:
                # Check if there is a 25% change in "percent_money_on_market" column
                percent_change_info = check_percent_change(group)
                if percent_change_info:
                    # Print the related rows and their row numbers
                    #print(f"Rows {percent_change_info[1]} to {percent_change_info[2]}:")
                    #print(group)
                    # Print the percentage change along with the row numbers
                    #print(f"Percentage change in percent_money_on_market at rows {percent_change_info[1]} to {percent_change_info[2]}: {percent_change_info[0]}%")
                    print("Anomalie alert: 5. criteria: ", {file_path})
                    criteria = "5. criteria"
                    market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                    bet = option
                    explanation = f"Anomaly detected based on criteria 5 with {percent_change_info[0]}% change"
                    c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                              (criteria, market, bet, file_path, explanation))
                    conn.commit()
                    any_rows_meet_criteria = True
            # Print a message if no rows meet the criteria for the current option
            if not any_rows_meet_criteria:
                #print("No rows meet the criteria.")
                pass

        #8.criteri : Big and sharp bets at the end of the game
        # Change factor x to 4x for the last 10 minutes for odds

        # consider only the second half of the DataFrame and check for changes

        file['publishTime'] = pd.to_datetime(file['publishTime'], format='%d.%m.%Y %H:%M:%S')

        # Split the DataFrame into two halves
        half_index = len(file) // 2
        second_half = file.iloc[half_index:]

        # Get unique options in the selection_md.name column
        unique_options = second_half['selection_md.name'].unique()

        # Define a function to check for 4x change in the "selection_totalMatched" column
        def check_total_matched_change(rows):
            # Get the first and last row for the 10-minute interval
            first_row = rows.iloc[0]
            last_row = rows.iloc[-1]
            
            # Check for zero or invalid values in the first row's selection_totalMatched
            if first_row['selection_totalMatched'] == 0 or np.isnan(first_row['selection_totalMatched']):
                return False

            # Calculate change in "selection_totalMatched" column
            try:
                change_factor = last_row['selection_totalMatched'] / first_row['selection_totalMatched']
            except ZeroDivisionError:
                # Handle division by zero error
                return False

            # Return the change factor along with the row numbers if it is 4x or more
            if change_factor >= 5:
                return change_factor, rows.index[0], rows.index[-1]
            else:
                return False

        # Iterate over each unique option
        for option in unique_options:
            # Filter rows for the current option
            option_rows = second_half[second_half['selection_md.name'] == option]
            
            # Group rows by 10-minute intervals based on 'publishTime'
            grouped_rows = option_rows.groupby(pd.Grouper(key='publishTime', freq='10T'))
            
            # Flag to track if any rows meet the criteria
            any_rows_meet_criteria = False
            
            # Iterate over each group
            for _, group in grouped_rows:
                if len(group) < 2:
                    continue
                # Check if there is a 4x change in "selection_totalMatched" column
                total_matched_change_info = check_total_matched_change(group)
                if total_matched_change_info:
                    # Print the related rows and their row numbers
                    #print(f"Rows {total_matched_change_info[1]} to {total_matched_change_info[2]}:")
                    #print(group)
                    # Print the change factor along with the row numbers
                    #print(f"Change factor in selection_totalMatched at rows {total_matched_change_info[1]} to {total_matched_change_info[2]}: {total_matched_change_info[0]}x")
                    print("Anomalie alert: 8. criteria: ", {file_path})
                    criteria = "8. criteria"
                    market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                    bet = option
                    explanation = f"Anomaly detected based on criteria 8 with {total_matched_change_info[0]}x change"
                    c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                              (criteria, market, bet, file_path, explanation))
                    conn.commit()
                    any_rows_meet_criteria = True
            
            # Print a message if no rows meet the criteria for the current option
            if not any_rows_meet_criteria:
                #print(f"No rows meet the criteria for option: {option}.")
                pass

        

        # 9. Criteria
        
        # Lays bets
        # the odds raise for instance from 1.75 to 3 in 10 minutes. And more than 20% of the money left the market.

        file['publishTime'] = pd.to_datetime(file['publishTime'], format='%d.%m.%Y %H:%M:%S')

        # Get unique options in the selection_md.name column
        unique_options = file['selection_md.name'].unique()

        # Define a function to check for the conditions
        def check_conditions(rows):
            # Check if there are one or more value changes in "selection_ex.availableToBack.price"
            price_changes = rows['selection_ex.availableToBack.price'].nunique() > 2
            
            # Check if "percent_money_on_market" decreases by more than 20%
            percent_change = rows['percent_money_on_market'].iloc[-1] - rows['percent_money_on_market'].iloc[0]
            percent_change_condition = percent_change < -30
            
            return price_changes and percent_change_condition

        # Iterate over each unique option
        for option in unique_options:
            # Filter rows for the current option
            option_rows = file[file['selection_md.name'] == option]
            
            # Group rows by 10-minute intervals based on 'publishTime'
            grouped_rows = option_rows.groupby(pd.Grouper(key='publishTime', freq='10T'))

            # Flag to track if any rows meet the criteria
            any_rows_meet_criteria = False

            # Iterate over each group
            for _, group in grouped_rows:
                if len(group) <= 2:
                    continue
                if check_conditions(group):
                    # Print the related rows
                    #print(group)
                    print("Anomalie alert: 9. criteria: ", {file_path})
                    criteria = "9. criteria"
                    market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                    bet = option
                    explanation = "Anomaly detected based on criteria 9"
                    c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                              (criteria, market, bet, file_path, explanation))
                    conn.commit()
                    any_rows_meet_criteria = True

            # Print a message if no rows meet the criteria for the current option
            if not any_rows_meet_criteria:
                #print(f"No rows meet the criteria for option: {option}.")
                pass

        
        # 10. criteria
        # Disproportion of bets
        # if in first 10 minutes , there is a disportion ???

        # Convert 'publishTime' to datetime
        file['publishTime'] = pd.to_datetime(file['publishTime'], format='%d.%m.%Y %H:%M:%S')

        # Filter rows based on the given conditions
        filtered_rows = file[
            (file['Minute'] <= 10) & 
            (file['percent_money_on_market'] > 90) & 
            (file['selection_ex.availableToBack.price'] > 4)
        ]

        # Print the filtered rows
        if not filtered_rows.empty:
            #print(filtered_rows)
            print("Anomalie alert: 10. criteria: ", {file_path})
            criteria = "10. criteria"
            market = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
            bet = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
            explanation = "Anomaly detected based on criteria 10"
            c.execute("INSERT INTO anomaly_detections (criteria, market, bet, file_path, explanation) VALUES (?, ?, ?, ?, ?)",
                      (criteria, market, bet, file_path, explanation))
            conn.commit()
        else:
            pass
            #print("No rows meet the criteria.")
conn.close()

