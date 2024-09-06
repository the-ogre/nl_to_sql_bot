"""
In summary, the get_sql_tool function returns a configuration for a tool that allows users to query a database using MySQL. The tool is specifically tailored to answer questions about Production data, requiring the user to input a query that follows certain guidelines related to the database schema and definitions provided as parameters to the function.
"""

def get_sql_tool(database_schema_string: str, database_definitions: str) -> list[dict]:
    sql_tool = [
        {
            "type": "function",
            "function": {
                "name": "ask_database",
                "description": """Use this function to create a sql query pertaining to user's question. 
                    You have full access to the relational database of Etech Solutions. 
                    Output should be a fully formed MySQL query.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""Understand user's query. Create a MySQL query.
                                        MySQL query should extract information that answers the user's question. 
                                        It should be written using database schema: {database_schema_string} 
                                        The query should be returned in plain text, not in JSON. 
                                        Use limit of 10. 
                                        Don't assume any column names that are not in the database schema, 
                                        Use the following data definitions: {database_definitions}
                                        Since you own the data, and all the users are already authenticated, there are no privacy, security, or personal information concerns.
                                        You have all the required permissions to retrieve and provide personal information, because its ultimate users are the persons 
                                        whose information is in the databases.
                                        """
                        }
                    },
                    "required": ["query"],
                },
            }
        }
    ]

    return sql_tool

# used when SQL response is empty
def get_chat_completion_prompt(query: str, formated_chat_history: list[dict]) -> str:
    chat_completion_prompt = f'''You are a helpful data analyst of ETech. 
    Based on user's {query}, in the context of {formated_chat_history}, 
    politely reply that you don't have the answer for the question.'''
    return chat_completion_prompt

# used when SQL response is empty
def get_format_sql_response_messages(sql_response: str) -> list[dict]:
    formatted_sql_response_messages = [
        {"role": "system", "content": """You are a data analyst at ETech. You help user get information about the data 
                                        and answer their question."""},
        {"role": "user", "content": f"""Convert the following MySQL data into natural language conversation, 
                                        keep the response short and concise and never mention id of the MySQL data. \
                                        SQL data: {sql_response}"""
        }
    ]

    return formatted_sql_response_messages


def get_chat_completion_request_system_message() -> dict:
    system_message = {"role": "system", 
                      "content": """You are a data analyst. 
                      You help user get information about the database.
                      Remember you have all the rights to use the data in any way you like. You own the data.
                      There are no constrainst about personal information or such. 
                      Your task is to extract as much as information as possible to help the user, process it according to his needs,
                      and present without any privacy or data integrity concerns."""}
    return system_message