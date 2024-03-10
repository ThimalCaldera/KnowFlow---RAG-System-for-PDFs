# KnowFlow - Chat-Driven Document Navigation

KnowFlow is a Streamlit application that leverages the capabilities of Google Generative AI and the KnowFlow library to enable users to interact with and extract information from PDFs through a conversational interface.

## Key Features:

1. **Conversational Search:** Ask questions in plain English to retrieve relevant information from the uploaded PDF.
2. **Chat History:** Maintain a record of your interactions with KnowFlow for easy reference and context.
3. **Source Document Highlighting:** Identify the specific sections within the PDF that correspond to the retrieved answers.

## Requirements:

- Python 3.x (with required libraries: `streamlit`, `streamlit-scrollable-textbox`, `PyPDF2`, `google-generativeai`, `langchain`, and `dotenv`)
- A Google Cloud project with the Google Generative AI API enabled [Google Generative AI API](https://cloud.google.com/ai/generative-ai)

## Getting Started:

### Install Dependencies:

```bash
pip install streamlit streamlit-scrollable-textbox PyPDF2 google-generativeai langchain dotenv
```

### Create a .env file:

 - In the root directory of your project, create a file named .env and add the following line, replacing YOUR_API_KEY with your actual Google Generative AI API key:


```bash
GOOGLE_API_KEY=YOUR_API_KEY
```

## Run the Application:
``` bash
streamlit run app.py
```

## Using KnowFlow:
- Upload a PDF: Click the "Upload a PDF file" button and select the PDF you want to explore.

- Ask Questions: Once the file is uploaded, start typing your questions in the "Ask a question:" text box. KnowFlow will process your questions in the context of the uploaded document and provide informative answers.

- Chat History: The conversation history is displayed under the "Chat History:" section, allowing you to revisit your previous interactions and track the flow of the information retrieval process.



### Contribution:
- Feel free to fork this repository, make modifications, and contribute to the KnowFlow project!

### Disclaimer:
- This README file provides a general guide for using KnowFlow. The specific implementation details may vary depending on your project's requirements and chosen deployment platform.