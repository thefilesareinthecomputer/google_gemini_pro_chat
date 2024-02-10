'''straightforward command line chat interface for google gemini-pro augmented with results from wikipedia injected into prompts'''
'''requires a .env file with a GOOGLE_GEMINI_API_KEY variable'''

from dotenv import load_dotenv
import google.generativeai as genai
import wikipedia
import os

# bring in the environment variables from the .env file
load_dotenv()
google_gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY')

genai.configure(api_key=google_gemini_api_key)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

prompt = """### <SYSTEM MESSAGE> <START> ### 
    You are a research assistant chatbot that *helps the user learn and get answers*. 
    You will interpret the user's input alongside the results from wikipedia and then you will *provide a fully accurate response*. 
    Please *carefully plan and think through all of your responses step by step* before you finish generating them. 
    Please make sure to *avoid any critical errors or bias*. 
    You will interpret the user's input alongside the results from wikipedia and then you will *provide a fully accurate response*. 
    ### <SYSTEM MESSAGE> <END> ###"""
primer = chat.send_message(f'{prompt}')
# primer.resolve()
primer_response = primer.text
print(primer_response)

exit_words = ['exit', 'quit', 'stop', 'end', 'bye', 'goodbye', 'done', 'break']

while True:
    user_input = input('\n\nUser: ')
        
    if not user_input or user_input.lower().split()[0] in exit_words:
        print('Ending chat.')
        break

    # try:
    #     page = wikipedia.page(user_input)
    #     page_content = page.content[:1500]  # Get the first 1500 characters of the page content
    # except wikipedia.exceptions.DisambiguationError as e:
    #     print("Your query may refer to multiple topics:")
    #     for option in e.options[:5]:  # Show top 5 options for simplicity
    #         print(f"- {option}")
    #     specific_input = input("\nPlease be more specific or choose from the above options: ")
    #     try:
    #         page = wikipedia.page(specific_input)
    #         page_content = page.content[:1500]
    #     except Exception as e:
    #         page_content = f"An error occurred: {str(e)}"
    # except wikipedia.exceptions.PageError:
    #     page_content = "The page you requested does not exist. Please try a different query."

    try:
        page = wikipedia.page(user_input)
        page_content = page.content[:15000]  # Get the first 15000 characters of the page content
    except wikipedia.exceptions.DisambiguationError as e:
        print("Your query may refer to multiple topics:")
        for index, option in enumerate(e.options[:5], start=1):  # Show top 5 options for simplicity
            print(f"{index}. {option}")
        
        # Prompt the user to select an option
        selection = input("\nPlease select the appropriate number or type 'exit' to cancel: ")
        if selection.lower() == 'exit':
            print('Exiting...')
            break  # or use 'continue' if you want to return to the start of the loop

        try:
            # Convert the user input into an integer and get the corresponding topic
            selected_option = e.options[int(selection) - 1]
            page = wikipedia.page(selected_option)
            page_content = page.content[:15000]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
            continue  # Return to the start of the loop to let the user try again or ask a new question
        except wikipedia.exceptions.PageError:
            print("The selected topic does not have a detailed page. Please try a different selection.")
            continue
    except wikipedia.exceptions.PageError:
        page_content = "The page you requested does not exist. Please try a different query."

    print('\n\n#----------------------------------------Wikipedia----------------------------------------#\n\n')
    print(page_content)
    print('\n\n#----------------------------------------Wikipedia----------------------------------------#\n\n')

    llm_prompt = f"I need information on the following topic: {user_input}. Here's what I found on Wikipedia: {page_content}. Can you provide more details or a better more accurate and thorough explanation? Thanks!"

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
                        
                        
                        