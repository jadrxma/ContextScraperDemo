import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests
import re

# Function to scrape and clean website content
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get all text from the website
        text = soup.get_text()
        # Use a regular expression to replace multiple spaces, newlines, and tabs with a single space
        cleaned_text = re.sub(r'\s+', ' ', text)
        return cleaned_text
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return ""

# Initialize session state for storing messages if not already done
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Sidebar for API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View Source Code](https://github.com/your-repo/your-project)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/your-repo/your-project)")

# Main app
st.title("💬 You Personal AI Scraper")

# Input for website URL
website_url = st.text_input("Enter a website URL to scrape for context")

# Scrape Website Button
if st.button('Scrape Website'):
    if website_url:
        with st.spinner('Scraping website...'):
            scraped_content = scrape_website(website_url)
            if scraped_content:
                st.session_state['website_content'] = scraped_content  # Store scraped content in session state
                st.text_area("Scraped content (preview)", value=scraped_content[:50000], height=250)
            else:
                st.error("Failed to scrape content. Please check the URL and try again.")
    else:
        st.error("Please enter a website URL.")

# Chat input
user_input = st.text_input("Ask me something...")

# Chat Button
if st.button('Send'):
    if user_input:
        if not openai_api_key:
            st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        else:
            openai.api_key = openai_api_key
            st.session_state['messages'].append({"role": "user", "content": user_input})
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-0125-preview",
                    messages=st.session_state['messages']
                )
                chat_response = response.choices[0].message['content']
                st.session_state['messages'].append({"role": "assistant", "content": scraped_content})
                st.write(chat_response)
            except Exception as e:
                st.error(f"Failed to call OpenAI API: {e}")

# Optionally display the chat history
st.write("Chat History:")
for msg in st.session_state.get('messages', []):
    st.text(f"{msg['role'].capitalize()}: {msg['content']}")
