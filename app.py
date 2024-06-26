import streamlit as st 
import openai

st.title("Echo Bot")  

openai.api_key =  st.secrets["OPENAI_API_KEY"]
print(f"OpenAI Key: {openai.api_key}")
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


# Checking if 'messages' key is in the session state dictionary
# If not, initialize it with an empty list
if "messages" not in st.session_state:
    st.session_state.messages = []

# Iterating over each message in the session state messages list
for message in st.session_state.messages:
    # Creating a chat message container with the role specified in the message
    with st.chat_message(message["role"]):
        # Displaying the content of the message using markdown
        st.markdown(message["content"])

# Creating a chat input widget with the placeholder text "What is up?"
prompt = st.chat_input("What is up?")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Call OpenAI API to get a response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Create the chat completion request
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        # Extract the response content
        full_response = response.choices[0].message["content"]
        message_placeholder.markdown(full_response)
    
    # Append assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})