import streamlit as st
from agent_dispatcher import *

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role":"assistant", "content": "How may I assist you today?"}]

st.markdown(
    """
<style>
    .st-emotion-cache-40y321 {
        flex-direction: row-reverse;
    }
    .st-emotion-cache-1c7y2kd {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True
)

# chat_container = st.container()

# with chat_container:
#     for message in st.session_state.messages:
#         st.write(message["content"])

# prompt = st.chat_input()

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("....."):
            response = agent_dispatcher(prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history