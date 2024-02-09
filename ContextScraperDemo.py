import openai
import streamlit as st
from bs4 import BeautifulSoup
import requests

# Initialize session state for storing messages if not already done
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Sidebar for API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")
    # Assuming you have links or instructions for your code or additional resources
    st.markdown("[View Source Code](https://github.com/your-repo/your-project)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/your-repo/your-project)")

# Main app
st.title("💬 Chatbot with Context")

# Input for website URL
website_url = st.text_input("Enter a website URL to scrape for context")

# Function to scrape website and return content
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Simple example: get all text; customize this as needed
        text = soup.get_text()
        return text
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return ""

# When a URL is entered, scrape the website
if website_url:
    with st.spinner('Scraping website...'):
        website_content = scrape_website(website_url)
        # For demonstration, showing a part of the scraped content
        st.text_area("Scraped content (preview)", value=website_content[:5000], height=250)
    # Add the scraped content as a system message for context
    st.session_state['messages'].append({"role": "system", "content": website_content})

# Chat input
user_input = st.text_input("Ask me something...")

if user_input:
    # Check for OpenAI API key
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
    else:
        # Set OpenAI API key
        openai.api_key = openai_api_key

        # Append user message to session state
        st.session_state['messages'].append({"role": "user", "content": user_input})

        # Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0125-preview",
                messages=st.session_state['messages']
            )
        
            # Extract the response and display it
            chat_response = response.choices[0].message['content']
            st.session_state['messages'].append({"role": "assistant", "content": chat_response})
            st.write(chat_response)
        except Exception as e:
            st.error(f"Failed to call OpenAI API: {e}")

# Display the chat history
st.write("Chat History:")
for msg in st.session_state['messages']:
    st.text(f"{msg['role'].capitalize()}: {msg['content']}")
