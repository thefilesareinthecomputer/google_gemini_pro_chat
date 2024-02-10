# Command Line Chat Interface for Google Gemini-Pro

This is a simple command-line chat interface for the Google Gemini-Pro model. 
The script is designed to be straightforward and easy to extend upon.
There's no user interface intended for this application, but it can be easily adapted to work with a GUI or web interface. The intention for this is an easy copy / paste code template that can be added to any repo for a command line pair programmer or assistant. 
There are 2 alternate variations of the chat assistant - 1 has access to howdoi and 1 has access to wikipedia.

## Requirements

- Python 3.11+
- Internet connection
- Google Gemini API key

## Setup

Before running the application, ensure you have a `.env` file in the project directory with your Google Gemini API key:

GOOGLE_GEMINI_API_KEY=your_api_key_here


## Installation

1. Clone this repository or copy the source code.
2. Install the required dependencies by running `pip install -r requirements.txt` in your terminal.

## Usage

To start the chat interface, run the provided Python script from your terminal:

python chat_interface.py

Upon launching, the interface will prompt you for input. The prompt template can be customized and tools can be added. 
To end the chat session, type any of the exit commands (`exit`, `quit`, `stop`, `end`, `bye`, `goodbye`, `done`, `break`).

## Note

This application is designed for educational purposes only. Please ensure you comply with Google's API usage policies and guidelines.

## Support

For issues and inquiries, please refer to the [Google Gemini-Pro documentation](https://developers.google.com/generative-ai/gemini/pro) or open an issue in this repository.
