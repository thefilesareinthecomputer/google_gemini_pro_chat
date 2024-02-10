'''straightforward command line chat interface for google gemini-pro augmented with results from howdoi injected into prompts'''
'''requires a .env file with a GOOGLE_GEMINI_API_KEY variable'''

from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
import subprocess

# bring in the environment variables from the .env file
load_dotenv()
google_gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY')

genai.configure(api_key=google_gemini_api_key)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

prompt = """### <SYSTEM MESSAGE> <START> ### 
    You are a pair programmer chatbot that *helps the user solve coding problems and write Python code*. 
    You will interpret the user's input alongside the results from howdoi and then you will *provide a fully accurate response in Python code*. 
    Please *carefully plan and think through all of your responses step by step* before you finish generating them. 
    Please make sure to *avoid any critical errors or bias*. 
    The user is a Python developer working on software and they are asking for your help as a pair programmer. 
    You will interpret the user's input alongside the results from howdoi and then you will *provide a fully accurate response in Python code*. 
    Here are some question / andwer pairs to help calibrate your responses:
    User: "How do I do ___ in Python?" 
    Gemini: "You can do ___ in Python by using this code: ___. Many of the resources recommend ___, but that is outdated. I recommend this Python implementation of the solution instead: ___ "
    User: "What is the best way to ___ in Python?" 
    Gemini: "There is a reliable ready-made solution for this issue with the ___ Python library. Here is the complete Python code to implement it: ___." 
    User: "I'm trying to ___ but I don't know the best way to do it." 
    Gemini: "Interesting problem. I'm not aware of any libraries to abstract this, but here's the code to implement it in vanilla Python yourself: ___."
    You will interpret the user's input alongside the results from howdoi and then you will *provide a fully accurate response in Python code*. 
    ### <SYSTEM MESSAGE> <END> ###"""
primer = chat.send_message(f'{prompt}', stream=True)
primer.resolve()
primer_response = primer.text
print(primer_response)

exit_words = ['exit', 'quit', 'stop', 'end', 'bye', 'goodbye', 'done', 'break']

while True:
        user_input = input('\n\nUser: ')
        
        command = f"howdoi {user_input} in Python -j"
        result = subprocess.run(command.split(), stdout=subprocess.PIPE)

        answers = json.loads(result.stdout)  # This is now expected to be a list
        
        print('\n\n#----------------------------------------howdoi----------------------------------------#\n\n')
        for item in answers:
            print(item.get('answer'))  # Use .get() to avoid KeyError if 'answer' key is missing
        print('\n\n#----------------------------------------howdoi----------------------------------------#\n\n')

        llm_prompt = f"I need information on the following topic: {user_input}. Here's what I found: {'; '.join(item.get('answer', '') for item in answers)}. Can you provide more details or examples? If you are able to responde only with Python code, please do so. Please ensure your responses are factually correct, and ensure the code is accurate. Thanks!"
        
        if not user_input:
            continue

        query = user_input.lower().split()
        if not query:
            continue

        if query[0] in exit_words or query[1] in exit_words:
            print('Ending chat.')
            break

        else:
            response = chat.send_message(f'{llm_prompt}')
            if response:
                print(response.text)
            if not response:
                attempt_count = 1  # Initialize re-try attempt count
                while attempt_count < 5:
                    response = chat.send_message(f'{llm_prompt}')
                    attempt_count += 1  # Increment attempt count
                    if response:
                        print(response.text)
                    else:
                        print('Chat failed.')
                        
                        
                        