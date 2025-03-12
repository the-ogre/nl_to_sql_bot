# Project Overview
This is a SQL AI Assistant built with Streamlit that allows users to query databases using natural language. 
The system:
1. Takes natural language questions from users
2. Converts these questions into SQL queries
3. Executes the queries against a database
4. Returns formatted, human-readable responses

The project currently uses a MySQL database but can be adapted for any SQL database with minimal changes. In another
file in the project I have described the implementation of postgres with chinook database. 

# System Components
The system consists of these key components:
1. Web Interface (Streamlit app in app.py) - Provides the chat interface where users interact with the AI
2. Query Processor (main.py) - Handles user queries and manages conversation flow
3. Response Generator (response_generation.py) - Uses an LLM to convert SQL results to natural language
4. Database Communication (db_comm.py) - Manages database connections and query execution
5. Data Cleaning (data_cleaning.py) - Contains utilities for data preprocessing
6. Database Update (update_database.py) - Tool for importing and updating database tables
7. Configuration (config.py) - Centralized configuration management
8. Prompts (prompts.py) - Templates for LLM interactions

The current implementation uses an LLM (specifically Llama2) running locally via Ollama for processing queries and generating responses.