from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
# from Backend.RealtimeSearchEngine import RealtimeSearchEngine  # Removed for lazy loading
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition, SetupSpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.ImageGeneration import gemini
from Backend.VideoGeneration import ignite_automation
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import threading
import json
import os
import requests
import re

env_vars = dotenv_values(".env")
Username = env_vars.get("Username") or "User"
Assistantname = env_vars.get("Assistantname") or "Assistant"
DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}, I am doing well. How may I help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search", "generate slides", "timer", "notification"]

def ShowDefaultChatIfNoChats():
    try:
        if not os.path.exists('Data'): os.makedirs('Data')
        chat_log_path = r'Data\\ChatLog.json'
        if not os.path.exists(chat_log_path):
            with open(chat_log_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

        with open(chat_log_path, "r", encoding='utf-8') as File:
            content = File.read()
            if len(content) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                    file.write("")
                with open(TempDirectoryPath("Responses.data"), 'w', encoding='utf-8') as file:
                    file.write(DefaultMessage)
    except Exception as e:
        print(f"Error in ShowDefaultChatIfNoChats: {e}")

def ReadChatLogJson():
    chat_log_path = r'Data\\ChatLog.json'
    if not os.path.exists(chat_log_path):
        with open(chat_log_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(chat_log_path, 'r', encoding="utf-8") as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""

    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"

    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(TempDirectoryPath('Database.data'), "r", encoding='utf-8')
    Data = File.read()
    if len(str(Data)) > 0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8')
        File.write(result)
        File.close()

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()
    SetupSpeechRecognition()

InitialExecution()

def HandleTasks(Decision, Query):
    TasksPath = TempDirectoryPath("Tasks.data")
    Results = []
    
    for task_cmd in Decision:
        if task_cmd.startswith("tasks add"):
            new_task = task_cmd.replace("tasks add", "").strip()
            if not new_task: continue
            
            tasks = []
            if os.path.exists(TasksPath):
                with open(TasksPath, "r", encoding="utf-8") as f:
                    content = f.read().split('\n')
                    for line in content:
                        if line.strip():
                            t = re.sub(r'^\d+\.\s*', '', line.strip())
                            if t: tasks.append(t)
            
            tasks.append(new_task)
            with open(TasksPath, "w", encoding="utf-8") as f:
                for i, t in enumerate(tasks):
                    f.write(f"{i+1}. {t}\n\n")
            Results.append(f"Added task: {new_task}")

        elif task_cmd.startswith("tasks remove"):
            task_to_remove = task_cmd.replace("tasks remove", "").strip()
            if not task_to_remove: continue
            
            if os.path.exists(TasksPath):
                with open(TasksPath, "r", encoding="utf-8") as f:
                    content = f.read().split('\n')
                    tasks = []
                    for line in content:
                        if line.strip():
                            t = re.sub(r'^\d+\.\s*', '', line.strip())
                            if t: tasks.append(t)
                
                removed_task = None
                try:
                    idx = int(task_to_remove) - 1
                    if 0 <= idx < len(tasks):
                        removed_task = tasks.pop(idx)
                except ValueError:
                    if task_to_remove in tasks:
                        tasks.remove(task_to_remove)
                        removed_task = task_to_remove
                
                if removed_task:
                    with open(TasksPath, "w", encoding="utf-8") as f:
                        for i, t in enumerate(tasks):
                            f.write(f"{i+1}. {t}\n\n")
                    Results.append(f"Removed task: {removed_task}")
                else:
                    Results.append(f"Could not find task: {task_to_remove}")

    if Results:
        # If we modified tasks, we can either return the results or let ChatBot explain
        return ". ".join(Results)
    
    # For 'tasks show', we return None to let it fall through to ChatBot
    return None

def MainExecution(Query=None):
    TaskExecution = False

    ImageExecution = False
    VideoExecution = False

    ImageGenerationQuery = ""
    VideoGenerationQuery = ""

    if Query is None:
        SetAssistantStatus("Listening...")
        Query = SpeechRecognition()
    
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")

    try:
        Decision = FirstLayerDMM(Query)

        print(f"\nDecision: {Decision}\n")

        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])
        T = any([i for i in Decision if i.startswith("tasks")])

        TaskAns = None
        if T:
            TaskAns = HandleTasks(Decision, Query)
            if TaskAns:
                ShowTextToScreen(f"{Assistantname}: {TaskAns}")
                SetAssistantStatus("Answering...")
                TextToSpeech(TaskAns)
                return True
            else:
                # If HandleTasks returns None, it means 'tasks show' or similar, 
                # so we treat it as a general query to let ChatBot handle it conversationally.
                Decision = [d.replace("tasks show", "general what are my tasks") if d.startswith("tasks show") else d for d in Decision]
                G = True

        for queries in Decision:
            if queries.startswith("generate image"):
                ImageGenerationQuery = queries.replace("generate image", "").strip()
                ImageExecution = True
            elif queries.startswith("generate video"):
                VideoGenerationQuery = queries.replace("generate video", "").strip()
                VideoExecution = True

        # Task Execution (Automation)
        if not TaskExecution:
            for queries in Decision:
                if any(queries.startswith(func) for func in Functions):
                    run(Automation(list(Decision)))
                    TaskExecution = True
                    break

        if VideoExecution:
            SetAssistantStatus("Generating Video...")
            ShowTextToScreen(f"{Assistantname}: Generating video for '{VideoGenerationQuery}'...")
            ignite_automation(VideoGenerationQuery) 
            SetAssistantStatus("Available...")
            return True

        if ImageExecution:
            SetAssistantStatus("Generating Image...")
            ShowTextToScreen(f"{Assistantname}: Generating image for '{ImageGenerationQuery}'...")
            gemini(ImageGenerationQuery)
            SetAssistantStatus("Available...")
            return True
        
        if R:
            SetAssistantStatus("Searching...")
            try:
                from Backend.RealtimeSearchEngine import RealtimeSearchEngine
                Merged_query = " and ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")])
                Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            except Exception as e:
                Answer = f"I couldn't perform the search. (Error: {e})"
            
            ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True
        
        else:
            for Queries in Decision:
                if "general" in Queries:
                    QueryFinal = Queries.replace("general", "")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                
                elif "exit" in Queries:
                    Answer = "Okay, Goodbye! Have a nice day."
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    os._exit(1)

    except Exception as e:
        print(f"Error in MainExecution: {e}")
        SetAssistantStatus("Error!")
        ShowTextToScreen(f"{Assistantname}: I encountered an error: {e}")
        SetAssistantStatus("Available...")

def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        elif CurrentStatus == "Typed":
            try:
                with open(TempDirectoryPath("Input.data"), "r", encoding="utf-8") as f:
                    Query = f.read().strip()
                
                if Query:
                    SetMicrophoneStatus("False")
                    MainExecution(Query)
                else:
                    SetMicrophoneStatus("False")
            except Exception as e:
                print(f"Error in FirstThread (Typed): {e}")
                SetMicrophoneStatus("False")
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()