import pygame     # Import pygame library for handling audio playback
import random     # Import random for generating random choices
import asyncio    # Import asyncio for asynchronous operations
import edge_tts     # Import edge_tts for text-to-speech functionality
import os   # Import os for file path handling
import time # Import time for sleep
from dotenv import dotenv_values  # Import dotenv for reading environment variables from a .env file

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice") or "en-IN-PrabhatNeural"  # Get the AssistantVoice from the environment variables

# Initialize pygame mixer once at the module level
pygame.mixer.init()

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    try:
        if os.path.exists(file_path):
            # Ensure the mixer releases the file
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            os.remove(file_path)
    except Exception as e:
        print(f"Internal TTS Clean-up Error: {e}")

    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

# Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    count = 0
    while count < 3:
        try:
            asyncio.run(TextToAudioFile(Text))

            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(15)
            
            # CRITICAL: Unload the file immediately after use to prevent permission errors next time
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            return True

        except Exception as e:
            print(f"Error in TTS: {e}")
            count += 1
            if count < 3:
                time.sleep(0.5)

        finally:
            # Call the provided function with False to signal the end of TTS
            try:
                func(False)
            except: pass
    
    return False

# Function to manage Text-to-Speech with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".") 

    responses = [
        "The rest of the result has been printed to the chat screen.",
        "The rest of the text is on the chat screen.",
        "You can see the rest of the text on the chat screen.",
        "The remaining part of the text is on the chat screen.",
        "More details are on the chat screen.",
        "The rest of the answer is on the chat screen.",
        "Please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen."
    ]

    # If the text is very long (more than 4 sentences and 250 characters), abbreviate it
    if len(Data) > 4 and len(Text) >= 250:
        short_text = " ".join(Text.split(".")[0:2]) + ". " + random.choice(responses)
        TTS(short_text, func)
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))
