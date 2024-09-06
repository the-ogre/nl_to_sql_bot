from tenacity import retry, wait_random_exponential, stop_after_attempt
from prompts import get_format_sql_response_messages, get_chat_completion_request_system_message
import streamlit as st

from openai import OpenAI
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

llama_model = 'llama2'

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools, tool_choice, model=llama_model):
    new_messages = []
    system_message = get_chat_completion_request_system_message()
    new_messages.append(system_message)
    for message in messages:
        new_messages.append(message)

    payload = {"model": model, "messages": new_messages}
    #st.sidebar.write(payload)
    if tools is not None:
        payload.update({"tools": tools})
        st.sidebar.write('payload updated')
        #st.sidebar.write(payload)
    if tool_choice is not None:
        payload.update({"tool_choice": tool_choice})

    try:
        response = client.chat.completions.create(**payload)
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def format_sql_response(sql_response: str, query: str, model: str = llama_model) -> str:
    messages = get_format_sql_response_messages(sql_response, query)
    payload = {"model": model, "messages": messages}
    try:
        response = client.chat.completions.create(
            model=model,
            json=payload
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e



# from db_comm import get_database_schema_string, get_database_definitions
# from prompts import get_sql_tool
# if __name__ == "__main__":
#     sql_response = "SELECT * FROM users WHERE id = 1;"
#     query = "Format this SQL response."
#     formatted_response = format_sql_response(sql_response, query)
#     print(formatted_response)

#     sql_tool = get_sql_tool(get_database_schema_string(),
#                         get_database_definitions())
    
#     test_messages = [
#     {"role": "user", "content": "Tell me about Jonathan"},
#     {"role": "user", "content": "How many records do you have"},
#     {"role": "user", "content": "How can you help me?"}
# ]
#     answer = chat_completion_request(test_messages, tools=sql_tool)
#     print(answer)