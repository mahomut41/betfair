import sqlite3
import os
import csv
import pandas as pd
import numpy as np  # Import numpy for NaN values
from pandas.errors import EmptyDataError

# Create a new SQLite database file
conn = sqlite3.connect('Anomaly_detection_results.db')
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS anomaly_detections
(ID INTEGER PRIMARY KEY AUTOINCREMENT, Criteria TEXT, Event TEXT, Market TEXT, Market_option TEXT, Status TEXT, Explanation TEXT, Details TEXT)''')

# Define the folder path containing event folders
event_folders = "/Users/noahroni/Documents/Betfair/Market_Folder_Final !!!/"
#print(event_folders)

# Get a list of all subdirectories in the event_folders directory
subdirectories = [os.path.join(event_folders, d) for d in os.listdir(event_folders) if os.path.isdir(os.path.join(event_folders, d))]
#print(subdirectories[0])   
#               

def get_selection_status(file, selection_name):
    selection_rows = file[file['selection_md.name'] == selection_name]
    
    if 'WINNER' in selection_rows['selection_status'].str.upper().values:
        return 'WINNER'
    if 'LOSER' in selection_rows['selection_status'].str.upper().values:
        return 'LOSER'


# Iterate over all subdirectories
for subdirectory in subdirectories:
    # Get a list of all files in the subdirectory
    files = [os.path.join(subdirectory, f) for f in os.listdir(subdirectory) if os.path.isfile(os.path.join(subdirectory, f)) and f.endswith('.csv')]
    
    half_time = None
    for file_path in files:
        if "halftimescore" in file_path.lower():
            try:
                file_rows = pd.read_csv(file_path, dtype=str, low_memory=False)
                file_rows['Minute'] = pd.to_numeric(file_rows['Minute'], errors='coerce')
                minute_value = file_rows.iloc[-1]['Minute']
                if 0 < minute_value < 51 and (minute_value is not None):
                    half_time = minute_value # No need to assign half_time to itself
                else:
                    half_time = 45
            except (pd.errors.EmptyDataError, KeyError, IndexError):
                half_time = 45

    # Iterate over all files in the subdirectory
    for file_path in files:        
        try:
            file = pd.read_csv(file_path, dtype=str, low_memory=False)
            
            # Add this condition to skip GoalLines markets
            if "Goal Lines" in file['md.name'].iloc[0]:
                continue # Skip this file and move to the next one
        
            # Convert necessary columns to appropriate data types
            file['percent_money_on_market'] = pd.to_numeric(file['percent_money_on_market'], errors='coerce')
            file['selection_ex.availableToBack.price'] = pd.to_numeric(file['selection_ex.availableToBack.price'], errors='coerce')
            file['selection_totalMatched'] = pd.to_numeric(file['selection_totalMatched'], errors='coerce')
            file['Minute'] = pd.to_numeric(file['Minute'], errors='coerce')
        except EmptyDataError:
            continue
        except pd.errors.ParserError:
            continue
        except TimeoutError:
            continue
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            continue
        
        # Assuming 'publishTime' is in datetime format, if not convert it first
        file['publishTime'] = pd.to_datetime(file['publishTime'], format='%d.%m.%Y %H:%M:%S')

        # 1. criteria: 
        # Percent of money on market is above 95%, total matched exceeds 10,000, and selection price is above 4.

        # Filter the DataFrame based on the given conditions
        filtered_file = file[
            (file['percent_money_on_market'] > 95) & 
            (file['selection_ex.availableToBack.price'] > 4) & 
            (file['selection_totalMatched'] > 10000)
        ]

        # Print the filtered DataFrame with related columns
        if not filtered_file.empty:
            for _, row in filtered_file.iterrows():
                Status = get_selection_status(file, row['selection_md.name'])
                Criteria = "1. criteria"
                Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                Market_option = row['selection_md.name'].replace(' ', '').replace('/', '')
                Explanation = "Anomaly detected based on criteria 1"
                Details = "Percent of money on market is above 95%, total matched exceeds 10,000, and selection price is above 4."
                c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                conn.commit()

            # check if there is a this criteria, as last time goal ??

        # 2. criteria  (only for small leagues!!)
        # For different leagues - different summ of bets. 
        #For example, for Indonesia 1 league 7,000 dollars in goal in a half, this is a small bets. 
        #For Brazil U-20 are already significant bets

        # Filter the DataFrame based on the given conditions
        if half_time is not None:
            filtered_file = file[
                (file['Minute'] < (half_time - 5)) &
                ((file['Minute'] > half_time) & (file['Minute'] < (file['Minute'].max() - 4))) &
                (file['selection_ex.availableToBack.price'] > 1.3) &
                (file['selection_totalMatched'] > 11000)
            ]
        else:
            filtered_file = file[
            (file['Minute'] < 40) &
            ((file['Minute'] > 50) & (file['Minute'] < (file['Minute'].max() - 4))) &
            (file['selection_ex.availableToBack.price'] > 1.3) &
            (file['selection_totalMatched'] > 11000) 
        ]

        # Print the filtered DataFrame with related columns
        if not filtered_file.empty:
            for _, row in filtered_file.iterrows():
                Status = get_selection_status(file, row['selection_md.name'])
                Criteria = "2. criteria"
                Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                Market_option = row['selection_md.name'].replace(' ', '').replace('/', '')
                Explanation = "Anomaly detected based on criteria 2"
                Details = "Throughout the match, excluding the last 5 minutes, the total matched exceeds 13,000, and the selection price is above 1.3."
                c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                conn.commit()
        
        # 3. criteria: 

        # Filter the DataFrame based on the given conditions

        if half_time is not None:
            filtered_file = file[
                (file['percent_money_on_market'] > 80) &
                (file['Minute'] < (half_time - 5)) &
                ((file['Minute'] > half_time) & (file['Minute'] < (file['Minute'].max() - 4)))
            ]
        else:
            filtered_file = file[
                (file['percent_money_on_market'] > 80) &
                (file['Minute'] < 40) &
                ((file['Minute'] > 50) & (file['Minute'] < 85)) 
            ]

        # Print the filtered DataFrame with related columns
        if not filtered_file.empty:
            for _, row in filtered_file.iterrows():
                Status = get_selection_status(file, row['selection_md.name'])
                Criteria = "3. criteria"
                Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                Market_option = row['selection_md.name'].replace(' ', '').replace('/', '')
                Explanation = "Anomaly detected based on criteria 3"
                Details = "During both halftimes, excluding the last 5 minutes, the percentage of money in the market is higher than 85%."
                c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                conn.commit()
        
        # 4. criteria: 

        # There is at least a 25% sharp increase during the last 10 minutes of both halftimes, excluding the last 5 minutes.

        # Get unique options in the selection_md.name column
        unique_options = file['selection_md.name'].unique()

        # Define a function to check for 25% change in the "percent_money_on_market" column
        def check_percent_change(rows):
            # Check if the group has at least two rows
            if len(rows) < 2:
                return False
            
            if half_time is not None:
                if (rows['Minute'] > (half_time - 5)).any() and ((rows['Minute'] > (rows['Minute'].max() - 4)).any()):
                    return False
            else:
                if (rows['Minute'] > 40).any() and ((rows['Minute'] > (rows['Minute'].max() - 4)).any()):
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
                
                # Check if percent_change is positive
                if percent_change >= 0:
                    # Return the percent change along with the row numbers
                    if percent_change >= 25:   # Change threshold could be more than 20%
                        return percent_change, rows.index[0], rows.index[-1]
                else:
                    # Ignore negative percent change values
                    return False
                    
            except ZeroDivisionError:
                # Handle division by zero error
                return False
            
            # Return the percent change along with the row numbers
            if abs(percent_change) >= 25:   # Change threshold could be more than 20%
                return percent_change, rows.index[0], rows.index[-1]
            else:
                return False

        # Iterate over each unique option
        for option in unique_options:
            
            # Filter rows for the current option and WINNER status
            option_rows = file[(file['selection_md.name'] == option)]
       
            # Group rows by 10-minute intervals based on 'publishTime'
            grouped_rows = option_rows.groupby(pd.Grouper(key='publishTime', freq='10T'))

            # Flag to track if any rows meet the criteria
            any_rows_meet_criteria = False
            
            # Iterate over each group
            for _, group in grouped_rows:
                # Check if there is a 25% change in "percent_money_on_market" column
                percent_change_info = check_percent_change(group)
                if percent_change_info: 
                    Status = get_selection_status(file, option)
                    Criteria = "4. criteria"
                    Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                    Market_option = option
                    Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                    if percent_change_info:
                        Explanation = f"Anomaly detected based on criteria {Criteria} with {percent_change_info[0]:.2f}% change in 10 minutes except the last 5 minutes for both half times"
                        
                        start_row_index = percent_change_info[1]
                        end_row_index = percent_change_info[2]
                        
                        if start_row_index >= 0 and start_row_index < len(file_rows) and end_row_index >= 0 and end_row_index < len(file_rows):
                            start_minute = file_rows.iloc[start_row_index]['Minute']
                            end_minute = file_rows.iloc[end_row_index]['Minute']
                            Details = f"Percentage change in percent_money_on_market from row {start_row_index} (minute {start_minute}) to row {end_row_index} (minute {end_minute}): {percent_change_info[0]:.2f}%"
                        else:
                            Details = f"Percentage change in percent_money_on_market from row {start_row_index} to row {end_row_index}: {percent_change_info[0]:.2f}%"
                        
                        c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                        conn.commit()
                    any_rows_meet_criteria = True
            # Print a message if no rows meet the criteria for the current option
            if not any_rows_meet_criteria:
                #print("No rows meet the criteria.")
                pass

        #5.criteria: 
        
        #There are big and sharp bets at the end of the game, with a change factor of more than 3x in the last 10 minutes, excluding the last 3 minutes.

        # Get unique options in the selection_md.name column
        unique_options = file['selection_md.name'].unique()

        # Define a function to check for 4x change in the "selection_totalMatched" column
        def check_total_matched_change(rows):

            if half_time is not None:
                if (rows['Minute'] > (half_time - 3)).any() and ((rows['Minute'] > (rows['Minute'].max() - 3)).any()):
                    return False
            else:
                if (rows['Minute'] > 42).any() and ((rows['Minute'] > (rows['Minute'].max() - 3)).any()):
                    return False
                
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

            # Return the change factor along with the row numbers if it is 3x or more
            if change_factor >= 3:
                return change_factor, rows.index[0], rows.index[-1]
            else:
                return False

        # Iterate over each unique option
        for option in unique_options:
            # Filter rows for the current option and WINNER status
            option_rows = file[(file['selection_md.name'] == option)]
            
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
                    #print("Anomalie alert: 8. criteria: ", {file_path})
                    Status = get_selection_status(file, option)
                    Criteria = "5. criteria"
                    Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                    Market_option = option
                    Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                    if percent_change_info:
                        Explanation = f"Anomaly detected based on criteria {Criteria} with {total_matched_change_info[0]:.2f}% change in 10 minutes except the last 5 minutes for both half times"
                        
                        start_row_index = total_matched_change_info[1]
                        end_row_index = total_matched_change_info[2]
                        
                        if start_row_index >= 0 and start_row_index < len(file_rows) and end_row_index >= 0 and end_row_index < len(file_rows):
                            start_minute = file_rows.iloc[start_row_index]['Minute']
                            end_minute = file_rows.iloc[end_row_index]['Minute']
                            Details = f"Percentage change in percent_money_on_market from row {start_row_index} (minute {start_minute}) to row {end_row_index} (minute {end_minute}): {total_matched_change_info[0]:.2f}%"
                        else:
                            Details = f"Percentage change in percent_money_on_market from row {start_row_index} to row {end_row_index}: {total_matched_change_info[0]:.2f}%"
                        
                        c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                        conn.commit()
                    any_rows_meet_criteria = True
            
            # Print a message if no rows meet the criteria for the current option
            if not any_rows_meet_criteria:
                #print(f"No rows meet the criteria for option: {option}.")
                pass

        # 6. Criteria
        
        # The odds (price) sharply increase, for instance, from 1.75 to 3 in 10 minutes, and more than 25% of the money leaves the market.

        file['percent_money_on_market'] != 0

        # Get unique options in the selection_md.name column
        unique_options = file['selection_md.name'].unique()

        # Define a function to check for the conditions
        def check_conditions(rows):
            # Check if there are one or more value changes in "selection_ex.availableToBack.price"
            price_changes = rows['selection_ex.availableToBack.price'].nunique() > 2
            
            # Check if "percent_money_on_market" decreases by more than 20%
            percent_change = rows['percent_money_on_market'].iloc[-1] - rows['percent_money_on_market'].iloc[0]
            percent_change_condition = (percent_change < -25).any()
            
            return price_changes and percent_change_condition
        
        # Iterate over each unique option
        for option in unique_options:
            # Filter rows for the current option and WINNER status
            option_rows = file[(file['selection_md.name'] == option)]

### Add this to all criteria --> match ended

            # Exclude rows where 'status' is "Match Ended"
            option_rows = option_rows[option_rows['status'] != "Match Ended"]
            option_rows = option_rows[option_rows['totalMatched'] != "0"]
            
            # Group rows by 10-minute intervals based on 'publishTime'
            grouped_rows = option_rows.groupby(pd.Grouper(key='publishTime', freq='7T'))

            # Flag to track if any rows meet the criteria
            any_rows_meet_criteria = False

            # Iterate over each group
            for _, group in grouped_rows:
                if len(group) <= 2:
                    continue
                if check_conditions(group):
                    # Print the related rows
                    #print(group)
                    #print("Anomalie alert: 6. criteria: ", {file_path})
                    Status = get_selection_status(file, option)
                    Criteria = "6. criteria"
                    Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                    Market_option = option
                    Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                    start_row_index = group.index[0]
                    end_row_index = group.index[-1]
                    start_minute = group['Minute'].iloc[0]
                    end_minute = group['Minute'].iloc[-1]
                    percent_change = (group['percent_money_on_market'].iloc[-1] - group['percent_money_on_market'].iloc[0]) / group['percent_money_on_market'].iloc[0] * 100
                    Explanation = f"Anomaly detected based on criteria 6 with {percent_change:.2f}% change in 10 minutes "
                    Details = f"The odds raise (for instance from 1.75 to 3 in 10 minutes) and more than 20% of the money left the market from row {start_row_index} (minute {start_minute}) to row {end_row_index} (minute {end_minute}): {percent_change:.2f}%"
                    c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                    conn.commit()
                    any_rows_meet_criteria = True

            # Print a message if no rows meet the criteria for the current option
            if not any_rows_meet_criteria:
                #print(f"No rows meet the criteria for option: {option}.")
                pass

        # 7. criteria
        # Disproportion of bets
        # If in the first 10 minutes, there is a disproportion with the percentage of money between 60% and 70%, the price is above 3, and the total matched money is above 15,000.

        # Filter rows based on the given conditions
        filtered_rows = file[
            (file['Minute'] <= 10) &
            ((file['percent_money_on_market'] > 60) & (file['percent_money_on_market'] < 70)) & 
            (file['selection_ex.availableToBack.price'] > 3) &
            (file['selection_totalMatched'] > 10000) 
        ]

        # Print the filtered rows
        if not filtered_rows.empty:
            for _, row in filtered_rows.iterrows():
                Status = get_selection_status(file, row['selection_md.name'])
                Criteria = "7. criteria"
                Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                Market_option = file['selection_md.name'].iloc[0].replace(' ', '').replace('/', '')
                Explanation = "Anomaly detected based on criteria 7"
                Details = f"In first 10 minutes, there is a disproportion of bets (percent_money_on_market = {row['percent_money_on_market']:.2f}) and the odds raise (selection_ex.availableToBack.price = {row['selection_ex.availableToBack.price']:.2f}) at row {row.name}"
                c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                conn.commit()

        # winrate criteria

        # 8. criteria: Selection price > 1.5, percentage of money > 98%, total matched > 10,000

        filtered_file_8 = file[
            (file['selection_ex.availableToBack.price'] > 1.5) &
            (file['percent_money_on_market'] > 98) &
            (file['selection_totalMatched'] > 10000) 
        ]
        
        if not filtered_file_8.empty:
            for _, row in filtered_file_8.iterrows():
                    # Additional analysis can be added here for score conditions if needed
                Status = get_selection_status(file, row['selection_md.name'])
                Criteria = "8. criteria"
                Event = file['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                Market = file['md.name'].iloc[0].replace(' ', '').replace('/', '')
                Market_option = file['selection_md.name'].iloc[0].replace(' ', '').replace('/', '')
                Explanation = "Anomaly detected based on criteria 8"
                Details = "Win rate is greater than 1.5, percentage of money on market is greater than 98%, and total matched is more than 10,000."
                c.execute("INSERT INTO anomaly_detections (Criteria, Event, Market, Market_option, Status, Explanation, Details) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (Criteria, Event, Market, Market_option, Status, Explanation, Details))
                conn.commit()


conn.close()

