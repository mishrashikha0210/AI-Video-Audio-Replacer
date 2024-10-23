AI-Video-Audio-Replacer

## Description

This project takes a video with improper audio—containing grammatical mistakes, unnecessary fillers and replaces it with corrected, AI-generated speech.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/streamlit-v0.88.0-orange.svg)](https://streamlit.io/)

## Features

- Corrects grammatical mistakes in audio.
- Replaces fillers with AI-generated speech.
- Easy to set up and run using Streamlit.


## Installation

1. Clone the repository or download the project files.

2. Navigate to the project directory in your terminal.

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

Before running the app, you need to set up the Azure API credentials as environment variables. Use the following format:

```bash
AZURE_API_KEY=your_key
AZURE_ENDPOINT=your_end_point
```

You can set these environment variables in your system, or create a `.env` file in the project root directory with the above content.

## Running the App

Once you've completed the installation and environment setup, you can run the Streamlit app using the following command:

```bash
streamlit run curious.py
```

The app should now be running and accessible through your web browser at `http://localhost:8501`.

## Troubleshooting

If you encounter any issues:

1. Make sure all required packages are installed correctly.
2. Verify that the environment variables are set properly.
3. Check the console output for any error messages.

For further assistance, please create an issue in the project repository.



"# AI-Video-Audio-Replacer" 
