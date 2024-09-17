# Syllabus Creator Assistant

## Overview

The Syllabus Creator Assistant is an AI-powered tool designed to help professors at Auburn University create comprehensive and well-structured course syllabi. This Streamlit-based application uses advanced language models to assist in generating syllabus content creating new ones from scratch through interactive conversation.

## Features

- **Interactive Chat Interface**: Engage with the AI assistant to create or refine your syllabus content.
- **Intelligent Syllabus Generation**: Receive suggestions and content for all essential components of a syllabus.
- **Markdown Output**: Generate the final syllabus in a clean, markdown format.
- **Flexible Creation**: Start from scratch or build upon existing content.

## Requirements

- Python 3.7+
- Streamlit
- Haystack
- PyPDF2
- python-dotenv
- An API key from Groq (for accessing the LLM)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/syllabus-creator-assistant.git
   cd syllabus-creator-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install streamlit haystack PyPDF2 python-dotenv
   ```

4. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. You will be greeted by the AI assistant and asked whether you want re-edit existing syllabus or create a new one from scratch.



4. Interact with the AI assistant through the chat interface to create or refine your syllabus. The assistant will guide you through including all essential components such as:
   - Course name and number
   - Instructor information
   - Course description
   - Course objectives
   - Required materials
   - Grading policy

5. The AI will generate syllabus content based on your interactions. You can continue to refine and adjust the content through the chat interface.

6. You can reset the conversation at any time using the "Reset Conversation" button in the sidebar.

## Project Structure

- `app.py`: Main Streamlit application file. Handles the user interface and conversation flow.
- `syllabi.py`: Contains functions for setting up the LLM pipeline, processing PDFs, and handling chat interactions with the AI.

## How It Works

1. The application uses the Groq API to access a large language model (specifically, the "llama-3.1-8b-instant" model).
2. PDFs are processed using PyPDF2 to extract text content from existing syllabi.
3. The Haystack framework is used to create a pipeline for natural language processing tasks.
4. Streamlit manages the web interface and user interactions.
5. The AI assistant is guided by a system message that defines its role and capabilities in creating comprehensive syllabi.


## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses the Groq API for language model interactions.
- Built with Streamlit and Haystack.
