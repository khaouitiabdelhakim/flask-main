import pandas as pd
import sqlite3

# Specify the path to the Excel file
excel_file_path = './pharmacies.xlsx'

# Read the Excel file into a DataFrame
data_frame = pd.read_excel(excel_file_path)

# Specify the path and name of the SQLite database file
database_file_path = './database.db'

# Create a connection to the SQLite database
connection = sqlite3.connect(database_file_path)
cursor = connection.cursor()

# Define the table structure
table_name = 'pharmacies'
columns = ['ID', 'Nom', 'Latitude', 'Longitude']
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"

# Create the table
cursor.execute(create_table_query)

# Insert the data into the table
for index, row in data_frame.iterrows():
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?)"
    values = (row['ID'], row['Nom'], row['Latitude'], row['Longitude'])
    cursor.execute(insert_query, values)

# Commit the changes and close the connection
connection.commit()
connection.close()