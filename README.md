# Command Line Chat Interface for Google Gemini-Pro

This is a simple command-line chat interface that leverages the Google Gemini-Pro generative AI model to facilitate conversational interactions. The tool is designed to be straightforward and user-friendly, without any superfluous features.

## Requirements

- Python 3.x
- An active internet connection
- A valid Google Gemini API key

## Setup

Before running the application, ensure you have a `.env` file in the project directory with your Google Gemini API key:

GOOGLE_GEMINI_API_KEY=your_api_key_here


## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies by running `pip install -r requirements.txt` in your terminal. This command installs the necessary Python packages, including the Google Generative AI library and dotenv for environment variable management.

## Usage

To start the chat interface, run the provided Python script from your terminal:

python chat_interface.py


Upon launching, the interface will prompt you to enter your queries. The system will respond based on the capabilities of the Google Gemini-Pro model. To end the chat session, type any of the exit commands (`exit`, `quit`, `stop`, `end`, `bye`, `goodbye`, `done`, `break`).

## Note

This application is designed for educational and experimental purposes. Please ensure you comply with Google's API usage policies and guidelines.

## Support

For issues and inquiries, please refer to the [Google Gemini-Pro documentation](https://developers.google.com/generative-ai/gemini/pro) or open an issue in this repository.
