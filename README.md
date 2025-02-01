# CustomGPT Creator

A Streamlit web application that helps you create CustomGPTs through a guided process with specialized AI assistants.

## Features

- Interactive chat interface
- Step-by-step guidance through the CustomGPT creation process
- Integration with OpenAI's GPT-4 Turbo model
- Export results as Markdown files
- Save and manage multiple CustomGPT results
- Corporate branding and professional interface

## Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy your app by connecting to your GitHub repository
4. In your app's settings on Streamlit Cloud, add your OpenAI API key in the Secrets section:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

## Local Development

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.streamlit/secrets.toml` file in your project directory:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. The app will guide you through the process of creating a CustomGPT
2. Your results will be saved in the sidebar
3. You can download results as Markdown (.md) files
4. Use "Clear Chat" to start a new conversation
5. Use "Clear Results" to remove saved results

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection

## Note

Make sure to keep your OpenAI API key secure and never commit it to version control. 