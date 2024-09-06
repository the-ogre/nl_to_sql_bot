import json

from response_generation import chat_completion_request, format_sql_response
from db_comm import get_database_schema_string, execute_function_call, get_database_definitions
from prompts import get_sql_tool, get_chat_completion_prompt

from db_comm import *
import streamlit as st


"""
SQL Tool Initialization
The sql_tool variable is initialized by calling get_sql_tool, which takes the database schema string and database definitions as arguments. 
These are obtained from get_database_schema_string and get_database_definitions functions respectively. 
"""



"""
Formatting Chat History
The format_chat_history function formats the chat history into a list of dictionaries. 
Each dictionary represents a message with a role (either 'user' or 'assistant') and the message content. 
This structured format is necessary for processing chat history in subsequent operations.
"""
def format_chat_history(chat_history: list[list]) -> list[list]:
    formated_chat_history = []
    for ch in chat_history:
        formated_chat_history.append({
            'role': 'user',
            'content': ch[0]
        })
        if ch[1] == None:
            pass
        else:
            formated_chat_history.append({
                'role': 'assistant',
                'content': ch[1]
            })
    st.sidebar.write(f'formatted  history- {formated_chat_history}')
    return formated_chat_history


"""
Handling Chat Completion
The handle_chat_completion function processes the latest user query from the chat history. 
It formats the chat history and sends it to chat_completion_request along with the sql_tool. 
Depending on the response, it either generates a SQL query to fetch data from the database or retrieves a response directly. 
If a SQL query is executed, the response is formatted and added to the chat history. Otherwise, an error message or the assistant's message is added.
"""
def handle_chat_completion(chat_history: list[list], sql_tool):
    # Extract the latest user query
    query = chat_history[-1][0]
    st.sidebar.write(f'User query -> {query}')

    # Format the chat history for processing
    formatted_chat_history = format_chat_history(chat_history)
    st.sidebar.write(formatted_chat_history)

    # Send the chat history and sql_tool to the chat_completion_request function
    chat_response = chat_completion_request(messages=formatted_chat_history, tools=sql_tool, tool_choice=None)
    st.sidebar.write(f'Chat response -> {chat_response}')

    # Assuming chat_response is the response object, we need to extract the assistant's message correctly
    assistant_message = chat_response.choices[0].message.content if chat_response.choices else None

    if assistant_message:
        response = assistant_message
    else:
        # Initialize an empty response
        response = "No response generated."

        # Check if there's a tool call for a SQL query
        tool_calls = chat_response.choices[0].message.tool_calls if chat_response.choices[0].message.tool_calls else []
        for tool_call in tool_calls:
            if tool_call.function.name == "ask_database":
                sql_query = json.loads(tool_call.function.arguments)["query"]
                st.sidebar.write(f'SQL query -> {sql_query}')

                # Execute the SQL query
                sql_response = execute_function_call(sql_query)
                st.sidebar.write(f'SQL response -> {sql_response}')

                # If there's a SQL response, format it
                if sql_response:
                    formatted_response = format_sql_response(sql_response, query)
                    response = formatted_response.choices[0].message.content
                else:
                    # Generate a response if SQL response is empty
                    chat_completion_prompt = get_chat_completion_prompt(query, formatted_chat_history)
                    response = chat_completion_request(chat_completion_prompt)
                    response = response.choices[0].message.content

    # Update the chat history with the response
    if len(chat_history[-1]) > 1:
        chat_history[-1][1] = response
    else:
        chat_history[-1].append(response)

    st.sidebar.write(f'Agent response -> {response}')

    return chat_history

"""
Handling User Query
The handle_user_query function updates the chat history with the user's latest message, setting the assistant's response to None initially. 
This prepares the chat history for processing the user's query.
"""
def handle_user_query(prompt: str, chat_history: list[tuple]) -> tuple:
    chat_history += [[prompt, None]]
    return '', chat_history

def get_response(instruction: str) -> str:
    messages = []
    messages.append({'role': 'user', 'content': instruction})
    response = chat_completion_request(messages)
    response = response['choices'][0]['message']['content']

    return response