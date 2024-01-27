'''
KEEP IT SIMPLE TO TEST THE PIPELINE.
1. Record
2. Transcribe
3. Parse to GPT AI
4. PRINT COMMAND GIVEN BY AI

UNAME =hey_admin
PWD = hey_uiop58
'''
import os
import sys
import speech_recognition as sr 
from colorama import Fore, Style
from datetime import datetime
from elasticsearch import Elasticsearch
from openai  import OpenAI

#getting the command line options and arguments from the bash 
mode_q_v = sys.argv[1] if len(sys.argv) > 1 else None
mode_t    = sys.argv[2] if len(sys.argv) > 2 else None
text_arg = sys.argv[3] if len(sys.argv) > 3 else None


#set the api key
#client = OpenAI(    api_key = os.environ.get("OPENAI_API_KEY")  )

client = Elasticsearch(
  "https://10.8.185.120:9200/",
  #api_key="uV95z8ouTJWYgW4N-jzdAQ",
  verify_certs=False,
  ssl_show_warn=False,
  http_auth=("elastic", "0X=+wWfc5F1gHZ3++K8c"),

)

print(client.info())

'''
#Record and transcribe Audio
def rec_transcribe():
    recognizer = sr.Recognizer()

    #Adjust for ambient c
    #with sr.Microphone() as mic:
    with sr.AudioFile('nmap_query.wav') as source:
        print("Adjusting for ambient noise. Please wait...")
        #recognizer.adjust_for_ambient_noise(mic, duration=3)
        print("Listening...")

        # Record audio until a silent period of more than 2 seconds is detected
        audio = recognizer.listen(source)

    try:
        print("Transcribing...")
        # Perform the transcription
        transcribed_text = recognizer.recognize_google(audio)
        return transcribed_text
 
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Error: {e}")
        return ""

#Parse to GPT AI
def parse2ai():
    try:
        
        if not transcribed_text:
            # Handle the case where transcription is empty
            print("Transcription is empty.")
            return ""

        if mode_q_v == "quiet":
            prompt_suffix = " .I DON'T NEED THE PRE EXPLANATION OF THE COMMAND. JUST GIVE ME THE COMMAND ONLY."
            max_tokens = 40
            
        elif mode_q_v == "verbose":
            prompt_suffix = "."
            max_tokens = 80 
        
        

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{transcribed_text}{prompt_suffix}",
            }
        ],
        max_tokens=max_tokens,
        temperature=0.5,
        model="gpt-3.5-turbo",
    )
        command = chat_completion.choices[0].message.content
        return (f"{Fore.GREEN}{command}{Style.RESET_ALL}")
    
    except OpenAI.Error as e:
        # Handle OpenAI API errors
        print(f"OpenAI API Error: {e}")
        return ""
    
    except Exception as e:
        # Handle other unexpected exceptions
        print(f"Unexpected error: {e}")
        return ""


#calling the functions

#HANDLING VOICE OR TEXT INPUT
if mode_t:
    #WHEN THE TEXT MODE IS ON
    transcribed_text = text_arg

else:
    #WHEN THE TEXT MODE IS OFF
    transcribed_text = rec_transcribe()


#print command
print("\n",parse2ai())
'''