import streamlit as st
import openai
from pathlib import Path
import json
from datetime import datetime
import os

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for message history and results
if "messages" not in st.session_state:
    st.session_state.messages = []
if "results" not in st.session_state:
    st.session_state.results = {}  # Dictionary to store results with timestamps as keys

# Set up the page
st.set_page_config(page_title="CustomGPT Creator", page_icon="🤖", layout="wide")

# Create two columns - one for the sidebar content and one for the main chat
sidebar_col, main_col = st.columns([1, 3])

with main_col:
    st.title("CustomGPT Creator Assistant")

# Sidebar
with sidebar_col:
    # Load and display local image
    st.sidebar.image("everythingengineer.png", use_container_width=True)
    
    # Corporate information
    st.sidebar.markdown("""
    ### Created by
    **Dirk Wonhoefer**  
    AI Engineering  
    [dirk.wonhoefer@ai-engineering.ai](mailto:dirk.wonhoefer@ai-engineering.ai)  
    [ai-engineering.ai](https://ai-engineering.ai)
    """)
    
    st.sidebar.markdown("""
    ### About
    EXAMPLE PROMPT: A customGPT that helps me to create a business plan for my business ideas.
            """)
    
    # Results section
    st.sidebar.markdown("### Your CustomGPT Results")
    
    # Display saved results with download buttons
    for timestamp, result in st.session_state.results.items():
        with st.sidebar.expander(f"Result from {timestamp}"):
            st.markdown(result[:200] + "..." if len(result) > 200 else result)
            
            # Markdown download
            md_filename = f"CustomGPT_Instructions_{timestamp}.md"
            st.download_button(
                "Download as Markdown",
                result,
                file_name=md_filename,
                mime="text/markdown"
            )
    
    # Clear buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("Clear Results"):
            st.session_state.results = {}
            st.rerun()
    
    if st.sidebar.button("Start New Chat"):
        st.session_state.messages = []
        st.rerun()

# Function to load system prompt
def load_system_prompt():
    try:
        with open("systemprompt.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("System prompt file (systemprompt.md) not found!")
        return None

# Function to generate response
def generate_response(messages):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            temperature=0.7,
            max_tokens=4000,
            stream=True
        )
        
        # Initialize empty string for the response
        full_response = ""
        message_placeholder = st.empty()
        
        # Stream the response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        return full_response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# Main chat interface
if openai.api_key:
    # Load system prompt
    system_prompt = load_system_prompt()
    
    if system_prompt:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("What kind of CustomGPT would you like to create?"):
            # Add user message to chat
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.chat_message("assistant"):
                messages = [
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ]
                response = generate_response(messages)
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Save first response of each chat as a result
                    if len(st.session_state.messages) == 2:  # First response (after user's first message)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.results[timestamp] = response
else:
    st.warning("Please enter your OpenAI API key in the sidebar to start.") 