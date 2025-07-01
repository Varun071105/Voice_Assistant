from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import sys
import smtplib
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

command_history = []

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("hey I am Tung Tung Tung Tung Tung Tung Sahur how may i help you varun Sir")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:    
        print(f"Error: {str(e)}")
        speak("Sorry, I wasn't able to send the email.")
    return query

def sendEmail(to, subject, content):
    try:
        # Sender's email credentials (Use an app password if 2-factor authentication is enabled)
        sender_email = 'varun071105@gmail.com'
        sender_password = 'Password'  # Use an app password instead of the actual email password

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = to
        message['Subject'] = subject

        # Add body to email
        message.attach(MIMEText(content, 'plain'))

        # Establish the SMTP server connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        text = message.as_string()

        # Send the email
        server.sendmail(sender_email, to, text)
        server.close()

        speak("Email has been sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        speak("Sorry, I wasn't able to send the email.")
        
def search_files(keyword, search_dir='C:/'):
    matches = []
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if keyword.lower() in file.lower():
                matches.append(os.path.join(root, file))
    return matches

def read_text_file(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if not file_path.endswith(('.txt', '.md')):
            raise ValueError("Unsupported file format")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            speak("Reading the file now")
            speak(content)
    except FileNotFoundError:
        speak("File not found")
    except UnicodeDecodeError:
        speak("Could not read the file due to encoding issues")
    except Exception as e:
        speak(f"Error reading file: {str(e)}")

def exitTung():
    speak("Okay, shutting down. Have a nice day Varun Sir!")
    print("Tung Tung Tung Tung Tung Tung Sahur is shutting down...")
    sys.exit()  # Exit the program



if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()  # Strip extra spaces

            try:
                results = wikipedia.summary(query, sentences=5, auto_suggest=False)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            except wikipedia.DisambiguationError as e:
                speak(f"The term {query} is ambiguous. Please be more specific.")
                print(f"Suggested options: {e.options[:3]}")  # Show only 3 suggestions
                speak(f"Did you mean {', '.join(e.options[:3])}?")

            except wikipedia.PageError:
                print(f"PageError: The page for '{query}' does not exist.")
                speak(f"Sorry, I couldn't find a Wikipedia page for {query}.")

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                speak("Sorry, an error occurred while fetching information.")


        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Okk Sir Youtube is Opened")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Okk Sir Google is Opened")

        elif 'open stack overflow' in query:
            webbrowser.open("https://www.stackoverflow.com")
            speak("Okk Sir Stack overflow is Opened")

        elif 'play music' in query:
            music_dir = r'C:\Users\Music'  # Use raw string literal to handle backslashes
            songs = os.listdir(music_dir)
            if songs:
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Okk Sir music is now playing")
            else:
                speak("No music files found in the directory.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\Project\Tung_yourassistant-main\ai.py"
            if os.path.exists(codePath):
                os.startfile(codePath)
                speak("Code is opened now")
            else:
                speak("The code file was not found.")

        elif 'email to' in query:
             try:
                 speak("What should I say?")
                 content = takeCommand()
                 to = "email_of_reciever"  # Replace with actual recipient
                 subject = "Email from Tung Tung sahur "
                 sendEmail(to, subject, content)
             except Exception as e:
                 speak(f"Error: {e}")
                 
        elif 'search file' in query:
            speak("What keyword should I search for?")
            keyword = takeCommand()
            results = search_files(keyword)
            if results:
                speak(f"Found {len(results)} files")
                for r in results[:5]:
                    print(r)
            else:
                speak("No matching files found")

         # Read file block
        elif 'read file' in query:
            speak("Please say the full file path")
            path = takeCommand()
            read_text_file(path)

         # Command history block
        elif 'show history' in query:
            speak("Here is your recent command history")
            for cmd in command_history[-5:]:
                print(cmd)     
                 
        elif 'exit' in query or 'quit' in query or 'stop' in query:
            exitTung()
