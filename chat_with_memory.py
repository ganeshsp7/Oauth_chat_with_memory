import os
import psycopg
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_postgres import PostgresChatMessageHistory
from auth import authenticate_user  # Import the authenticate function

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get credentials from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Establish synchronous connection to PostgreSQL
sync_connection = psycopg.connect(DATABASE_URL)

# Create table if not exists (should ideally be done once)
PostgresChatMessageHistory.create_tables(sync_connection, "message_store")

# Authenticate the user
authenticate_user()  # Calls the authentication function from auth.py

# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Check if email exists in session state and start chat
if "email" in st.session_state:
    st.write(f"Welcome, {st.session_state.user_name} ({st.session_state.email})!")

    # Initialize chat history
    chat_history = PostgresChatMessageHistory(
        "message_store",
        st.session_state.session_id,
        sync_connection=sync_connection
    )

    # Load existing messages from the database
    if not st.session_state.chat_history:
        st.session_state.chat_history = chat_history.messages
        # Add welcome message if new session
        if not st.session_state.chat_history:
            welcome_msg = AIMessage(content="Hello! How can I assist you today?")
            chat_history.add_message(welcome_msg)
            st.session_state.chat_history.append(welcome_msg)

    # Display chat messages
    for msg in st.session_state.chat_history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # Chat input and processing
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to history
        user_msg = HumanMessage(content=prompt)
        st.session_state.chat_history.append(user_msg)
        chat_history.add_message(user_msg)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display spinner while generating AI response
        with st.spinner("Generating AI response..."):
            # Generate AI response
            def get_response(query, history):
                template = """You are a helpful assistant. Answer considering chat history.
                
                Chat History: {chat_history}
                User Question: {user_question}
                
                Provide a clear, concise response."""
                
                prompt_template = ChatPromptTemplate.from_template(template)
                llm = ChatOpenAI(model="gpt-4o")
                chain = prompt_template | llm | StrOutputParser()
                
                return chain.stream({
                    "chat_history": history,
                    "user_question": query
                })

            # Display AI response
            with st.chat_message("assistant"):
                response = st.write_stream(get_response(prompt, st.session_state.chat_history))
            
            # Add AI response to history
            ai_msg = AIMessage(content=response)
            st.session_state.chat_history.append(ai_msg)
            chat_history.add_message(ai_msg)

