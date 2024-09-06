import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME')
MYSQL_TABLES = os.getenv('TABLE_NAMES')

cwd = os.getcwd()
DEFINITION_DIR = 'data_definition'

ERROR_MESSAGE = 'We are facing an issue at this moment, please try after sometime.'
