from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import socket
import mtranslate as mt

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage", "en-US")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            if (recognition) recognition.stop();
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                // Do not auto-restart here, let the python script decide.
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) recognition.stop();
            output.textContent = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file, ensuring the Data directory exists.
if not os.path.isdir('Data'):
    os.makedirs('Data')
with open(r"Data\\Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the current working directory.
current_dir = os.getcwd()

# Generate the absolute file path for the HTML file.
Link = os.path.abspath(os.path.join(current_dir, "Data", "Voice.html"))
# Convert Windows backslashes to forward slashes for a proper file URL.
Link = "file:///" + Link.replace("\\", "/")

# Global driver placeholder
_driver = None

def init_driver():
    """Initialize or reconnect the Selenium driver."""
    global _driver
    if _driver is not None:
        try:
            _driver.title
            return _driver
        except Exception:
            try: _driver.quit()
            except: pass
            _driver = None
    
    # Set Chrome options
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("-use-fake-ui-for-media-stream")
    chrome_options.add_argument("-use-fake-device-for-media-stream")
    chrome_options.add_argument("--headless=new") # Run in headless mode to save resources and speed up
    
    # Check if remote debugging port is listening
    def is_port_open(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return s.connect_ex(("127.0.0.1", port)) == 0
    
    try:
        if is_port_open(9222):
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        # Fallback to fresh browser without debuggerAddress
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("-use-fake-ui-for-media-stream")
        chrome_options.add_argument("-use-fake-device-for-media-stream")
        chrome_options.add_argument("--headless=new")
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return _driver

# Define the path for temporary files.
TempDirPath = os.path.join(current_dir, "Frontend", "Files")

# Function to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    if not new_query: return ""
    
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(new_query.startswith(word) for word in question_words):
        if new_query[-1] not in ['.', '?', '!']:
            new_query += "?"
    else:
        if new_query[-1] not in ['.', '?', '!']:
            new_query += "."
    return new_query.capitalize()

# Universal translator function to translate text.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition():
    driver = init_driver()
    
    # Only load the page if it's not already loaded
    try:
        if driver.current_url != Link:
            driver.get(Link)
    except:
        driver.get(Link)

    # Clear previous output and start recognition
    driver.execute_script("stopRecognition(); startRecognition();")

    while True:
        try:
            # Get the recognized text from the HTML output element.
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                # Stop recognition
                driver.execute_script("stopRecognition();")

                # Process the recognized text
                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))

        except Exception as e:
            if "InvalidSessionIdException" in str(e):
                driver = init_driver()
                driver.get(Link)
                driver.execute_script("startRecognition();")
                continue
            pass

# Function to initialize and setup the speech recognition driver.
def SetupSpeechRecognition():
    driver = init_driver()
    driver.get(Link)
    print("[SpeechToText] Ready.")

# Main execution block.
if __name__ == "__main__":
    SetupSpeechRecognition()
    while True:
        Text = SpeechRecognition()
        print(f"Recognized: {Text}")
