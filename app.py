import streamlit as st

st.set_page_config(
    page_title="SQL AI Assistant",        
    layout="wide",                        
    initial_sidebar_state="expanded",    
    page_icon=":books:",               
)

from main import *
import time


def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Put your question"}]

st.subheader("""Welcome to SQL AI Assistant. Whether you are an Agent or a Supervisor, I am here to help you with your questions""")
st.write("For example, you can questions like 'Check my total evaluations for today', 'Are there any areas where I could have performed better?' etc.")
st.markdown("<hr>", unsafe_allow_html=True)

with st.sidebar:
    st.title("ETech AI Assistant")
    st.button('Clear Chat', on_click=clear_chat())

global sql_tool
sql_tool = get_sql_tool(get_database_schema_string(),
                        get_database_definitions())
st.sidebar.write('sql_tool fetched')
st.sidebar.write(sql_tool)



# Streamlit App Setup and Main Function
def main():
    global chat_history 
    chat_history = []
    hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
    st.markdown(hide_default_format, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            /* Add your custom CSS rules here */
            body {
                background-color: white;
            }
            /* Example: Change the color of buttons */
            .stButton > button {
                background-color: teal;
                color: white;
            }
            /* Example: Change the color of chat messages */
            .stChatMessage {
                background-color: babyblue;
                color: black;
            }
            /* Example: Change the color of chat input */
            .stTextInput > div > div > input {
                background-color: deepskyblue;
                color: white;
            }
            /* Example: Adjust logo size and position */
            .sidebar .sidebar-content {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .logo-container {
                margin-top: 5px;
            }
            .logo-container img {
                width: 50px;  /* Adjust the width as needed */
            }
            /* Change link color on hover */
            a:hover {
                color: deepblue !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.image("logo.jpeg",use_column_width=True)
    # create the message history state
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # # render older messages
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # st.session_state.chat_history = []
    prompt = st.chat_input("Please put your query.")
    
    if prompt:
        # st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            retrieval_container = st.container()
            message_placeholder = st.empty()
            time_start =time.time()
            retrieval_status = retrieval_container.status("**Looking for an answer...**")

            # handle_user_query(prompt, st.session_state.history)
            # response = handle_chat_completion(st.session_state.history)[-1][-1]
            st.sidebar.write(chat_history)
            handle_user_query(prompt, chat_history)
            st.sidebar.write(chat_history)
            chat_history = handle_chat_completion(chat_history, sql_tool)
            response = chat_history[-1][-1]
            st.sidebar.write(chat_history)
            message_placeholder.markdown(response)
            time_end = time.time()
            st.write("Time Taken to create response: ", (time_end-time_start))
            retrieval_status.update(state="complete")
        # st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()