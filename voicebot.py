import speech_recognition as sr
import requests
import pyttsx3

bot_message = ""

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio,language='en')
        print("You said:", recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print("Error fetching results:", e)

def send_text_to_rasa(user_text):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Replace with your Rasa server URL
    data = {
        "sender": "user",
        "message": user_text
    }
    response = requests.post(url, json=data)
    print(response.json())
    return response.json()

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        user_input = recognize_speech()
        if user_input:
            # Check if the user's message contains "bye" or "take care"
            if "bye" in user_input.lower() or "take care" in user_input.lower():
                print("Goodbye! Have a nice day!")
                break  # Exit the loop and stop the conversation

            rasa_response = send_text_to_rasa(user_input)
            if rasa_response and len(rasa_response) > 0:
                print("Bot says:")
                for i in rasa_response:
                    bot_message = i['text']
                    print(bot_message)
                    text_to_speech(bot_message)