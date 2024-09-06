import os
import re
from typing import List, Dict, Any
import json

import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from sqlalchemy_utils import database_exists, create_database
from data_cleaning import *

import config

engine = create_engine(
    f'mysql+mysqlconnector://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB_NAME}')
print('Engine Created')


def get_column_names_for_tables(cnx: mysql.connector.MySQLConnection, table_names: List[str]) -> Dict[str, List[str]]:
    cursor = cnx.cursor()
    columns_info = {}  # Dictionary to store the result
    for table_name in table_names:
        cursor.execute(
            f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{config.MYSQL_DB_NAME}' AND TABLE_NAME='{table_name}';"
        )
        # Fetch all columns for the current table and store them in the dictionary
        columns_info[table_name] = [(col[0], col[1]) for col in cursor]
    cursor.close()
    print('Columns Name Fetched for provided tables')
    return columns_info

# def get_column_names(cnx: mysql.connector.MySQLConnection, table_name: str) -> list[str]:
#     cursor = cnx.cursor()
#     column_names = []
#     cursor.execute(
#         f"SELECT * FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='{config.MYSQL_DB_NAME}' AND `TABLE_NAME`='{table_name}';")
#     for col in cursor:
#         column_names.append([col[3], col[7]])
#     cursor.close()
#     print('Columns Name Fetched')
#     return column_names


print('Checking DB.')

if not database_exists(engine.url):
    create_database(engine.url)

print(f'DB exists - {database_exists(engine.url)}.')

cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASSWORD,
                              host=config.MYSQL_HOST, port=config.MYSQL_PORT, database=config.MYSQL_DB_NAME)


##------------------------------------------------------------##

print('Reading the columns names')

# List of table names you want to fetch column names for
table_names = ['vw_QuestionData', 'vw_MetaData_Numm']

# Fetching the column names
columns_info = get_column_names_for_tables(cnx, table_names)

# Printing the fetched column names
for table, columns in columns_info.items():
        print(f"Columns for {table}: {columns}")





print('Reading the CSV files.')

CSV_DIR = 'csv_data'
DEFINITION_DIR = 'data_definition'

csv_files = os.listdir(CSV_DIR)

for csv_file in csv_files:
    if os.path.isfile(os.path.join(CSV_DIR, csv_file)):
        file_name = csv_file.rsplit('.', 1)[0]
        file_extention = csv_file.rsplit('.', 1)[1]
        if 'csv' in file_extention:
            new_file_name = remove_special_characters(file_name)
            new_file_name = ''.join(char.lower()
                                    for char in new_file_name if not char.isdigit())
            new_file_name = new_file_name.replace(' ', '_')
            new_file_name += f'.{file_extention}'
            new_file_path = os.path.join(CSV_DIR, new_file_name)
            os.rename(os.path.join(CSV_DIR, csv_file), new_file_path)
            print(f"Renamed '{csv_file}' to '{new_file_name}'.")

for csv_file in csv_files:
    if os.path.isfile(os.path.join(CSV_DIR, csv_file)):
        file_name = csv_file.rsplit('.', 1)[0]
        file_extention = csv_file.rsplit('.', 1)[1]
        if 'csv' in file_extention:
            csv_file_path = os.path.join(CSV_DIR, csv_file)
            print(f'Working on the {csv_file_path}.')
            data = pd.read_csv(csv_file_path)
            print('Cleaning CSV data.')
            data.columns = [clean_column_names(col) for col in data.columns]
            for col in data.columns:
                data[col] = convert_to_datetime(data[col])
            print('Creating table and pushing the data.')
            table_name = csv_file.rsplit('.', 1)[0]
            data.to_sql(table_name, engine, if_exists='replace',
                        index=False, method='multi', chunksize=100)
            print('Creating empty data definitions.')
            data_definitions = {
                "tables": [
                    {
                        "name": table_name,
                        "description": "",
                        "columns": []
                    }
                ]
            }
            columns = get_column_names_for_tables(cnx, table_name)
            for column in columns:
                data_definitions['tables'][0]['columns'].append(
                    {
                        "name": str(column[0]),
                        "type": str(column[1]),
                        "description": ""
                    }
                )
            print('Writing data definitions.')
            with open(os.path.join(DEFINITION_DIR, f'{table_name}.json'), 'w') as file:
                file.write(json.dumps(data_definitions, indent=2))
            print(f'Finished working on the {csv_file_path}.')
