from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# Function to get tasks from the Tasks.data file.
def GetTasks():
    try:
        current_dir = os.getcwd()
        tasks_path = os.path.join(current_dir, "Frontend", "Files", "Tasks.data")
        if os.path.exists(tasks_path):
            with open(tasks_path, "r", encoding='utf-8') as f:
                tasks = f.read().strip()
                if tasks:
                    return f"\n\nUser's Tasks from memory:\n{tasks}"
        return ""
    except:
        return ""

def GetSystemMessage():
    System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
{GetTasks()}
"""
    return [{"role": "system", "content": System}]

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return f"Real-time Info: {current_date_time.strftime('%A, %d %B %Y %H:%M:%S')}"

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Main chatbot function to handle user queries.
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """

    try:
        # Load the existing chat log
        try:
            with open(r"Data\\ChatLog.json", "r", encoding='utf-8') as f:
                messages = load(f)
        except:
            messages = []

        # Prepare the full context for the AI
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API - disable streaming for faster internal processing
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=GetSystemMessage() + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=False # Faster for Python to handle non-streamed results
        )

        Answer = completion.choices[0].message.content
        Answer = Answer.replace("</s>", "").strip()

        # Update and save the chat log
        messages.append({"role": "assistant", "content": Answer})
        
        with open(r"Data\\ChatLog.json", "w", encoding='utf-8') as f:
            dump(messages, f, indent=4)
        
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error in ChatBot: {e}")
        return f"I'm sorry, I'm having trouble connecting to my brain right now. (Error: {e})"

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
