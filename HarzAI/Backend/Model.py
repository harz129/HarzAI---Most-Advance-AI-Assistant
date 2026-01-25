try:
    import cohere  # Import the Cohere library for AI services.
except ImportError:
    cohere = None

from rich import print  # Import the Rich library to enhance terminal outputs.
from dotenv import dotenv_values  # Import dotenv to load environment variables.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key.
CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a Cohere client using the provided API key safely.
co = None
if cohere and CohereAPIKey:
    try:
        co = cohere.Client(api_key=CohereAPIKey)
    except Exception as e:
        print(f"Error initializing Cohere: {e}")

# Define a list of recognized function keywords for task categorization.
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder" , "generate video", "generate slides",
    "timer", "notification", "tasks"
]

# Define the preamble that guides the AI model on how to categorize queries.
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc. Respond with 'realtime (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'realtime what's the time?'.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'generate video (video prompt)' if a query is requesting to generate a video with given prompt like 'generate video of a sunset', 'generate video of a car', etc. but if the query is asking to generate multiple videos, respond with 'generate video 1st video prompt, generate video 2nd video prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' ONLY if a query is explicitly asking to write a long-form document, letter, code, email, or a detailed essay about a topic. If the user says "write this" or "write that" without a clear long-form context, or is just chatting, respond with 'general (query)'.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google.
-> Respond with 'youtube search (topic)' if a query is asking to search something on YouTube.
-> Respond with 'generate slides (slide topic)' if a query is requesting to generate a presentation or slides with given topic like 'generate slides of global warming', 'make a presentation on python', etc.
-> Respond with 'timer (time) (optional message)' if a query is asking to set a timer OR give a notification after some time like 'set a timer for 10 minutes' respond with 'timer 10 minutes'.
-> Respond with 'tasks (action) (task content)' if a query is asking to show, add, or remove tasks. 
    - For showing tasks: 'tasks show'
    - For adding tasks: 'tasks add task_description'
    - For removing tasks: 'tasks remove task_number'
    Example: 'what are my tasks' -> 'tasks show', 'add buy milk to my tasks' -> 'tasks add buy milk', 'remove task 2' -> 'tasks remove 2'.
*** If the query is asking to perform multiple tasks like 'open facebook and search funny cats on youtube' respond with 'open facebook, youtube search funny cats' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query, if the query is a short phrase, or if it's a task not mentioned above. ***
"""

# Define a chat history with predefined user-chatbot interactions for context.
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today’s date and by the way remind me that I have a dancing performance on August 5."},
    {"role": "Chatbot", "message": "general what is today’s date, reminder 11:00pm 5th Aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."},
    {"role": "User", "message": "what are my tasks and also add study for exam to my tasks."},
    {"role": "Chatbot", "message": "tasks show, tasks add study for exam"}
]

# Define the main function for decision-making on queries.
def FirstLayerDMM(prompt: str = "test"):
    # If Cohere client is not initialized, return a default 'general' decision.
    if co is None:
        print("Cohere not initialized. Defaulting to 'general'.")
        return [f"general {prompt}"]

    try:
        # Using co.chat instead of co.chat_stream for faster non-streaming response
        # Using a balanced model for accuracy and speed
        response = co.chat(
            model='command-a-03-2025', 
            message=prompt,
            temperature=0.1,
            chat_history=ChatHistory,
            preamble=preamble,
            prompt_truncation='OFF'
        )
        content = response.text
    except Exception as e:
        print(f"Error in FirstLayerDMM (Cohere): {e}")
        return [f"general {prompt}"]

    # Remove newline characters and split responses into individual tasks.
    content = content.replace("\n", "")
    tasks = content.split(",")

    # Strip leading and trailing whitespaces from each task.
    tasks = [i.strip() for i in tasks]

    # Filter the tasks based on recognized function keywords.
    filtered_tasks = []
    for task in tasks:
        for func in funcs:
            if task.startswith(func):
                filtered_tasks.append(task)
                break

    # If nothing matched, default to general
    if not filtered_tasks:
        return [f"general {prompt}"]

    return filtered_tasks

# Entry point for the script.
if __name__ == "__main__":
    while True:
        user_input = input(">>>")
        if user_input.lower() in ['exit', 'quit']:
            break
        print(FirstLayerDMM(user_input))