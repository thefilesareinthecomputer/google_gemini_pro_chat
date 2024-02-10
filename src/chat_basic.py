'''straightforward command line chat interface for google gemini-pro'''
'''requires a .env file with a GOOGLE_GEMINI_API_KEY variable'''

from dotenv import load_dotenv
import google.generativeai as genai
import os

# bring in the environment variables from the .env file
load_dotenv()

google_gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY')

genai.configure(api_key=google_gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

exit_words = ['exit', 'quit', 'stop', 'end', 'bye', 'goodbye', 'done', 'break']

prompt = """### <SYSTEM MESSAGE> <START> ### 
    You are a helpful and insightful chatbot that helps the user solve problems, generate ideas, and get answers. 
    You will respond to the user in a direct, sincere, and accurate way. 
    You must think all of your responses through step by step. 
    You must check your responses for errors and bias before you send them. 
    You must check your responses for accuracy before you send them. 
    You will make sure to avoid any errors or bias. 
    ### <SYSTEM MESSAGE> <END> ###"""

chat = model.start_chat(history=[])
primer = chat.send_message(f'{prompt}', stream=True)
primer.resolve()
primer_response = primer.text
print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>BOT----------------------------------------------------------------\n")
print(primer_response)
print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>YOU----------------------------------------------------------------\n")
    
while True:
    user_input = input('You: ')
    if not user_input:
        continue

    query = user_input.lower().split()
    if not query:
        continue

    if query[0] in exit_words:
        print('Ending chat.')
        break

    else:
        response = chat.send_message(f'{user_input}', stream=True)
        if response:
            print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>BOT----------------------------------------------------------------\n")
            for chunk in response:
                if hasattr(chunk, 'parts'):
                    # Concatenate the text from each part
                    full_text = ''.join(part.text for part in chunk.parts)
                    print(full_text)
                else:
                    # If it's a simple response, just print the text
                    print(chunk.text)
            print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>YOU----------------------------------------------------------------\n")
        if not response:
            attempt_count = 1  # Initialize re-try attempt count
            while attempt_count < 5:
                response = chat.send_message(f'{user_input}', stream=True)
                attempt_count += 1  # Increment attempt count
                if response:
                    print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>BOT----------------------------------------------------------------\n")
                    for chunk in response:
                        if hasattr(chunk, 'parts'):
                            # Concatenate the text from each part
                            full_text = ''.join(part.text for part in chunk.parts)
                            print(full_text)
                        else:
                            # If it's a simple response, just print the text
                            print(chunk.text)
                    print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>YOU----------------------------------------------------------------\n")
                else:
                    print('Chat failed.')