from gtts import gTTS
import pyttsx3          
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import sys
from contextlib import redirect_stdout
from deep_translator import GoogleTranslator

# Function to play audio using pygame
def play_audio(file_path):
    try:
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull) :
                pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue  # Wait for the audio to finish
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.mixer.quit()

# Function to speak using gTTS
def speak_gtts(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        play_audio(audio_file)
        os.remove(audio_file)  # Clean up after playing
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not speak in language '{lang}'.")

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Function to configure pyttsx3 settings
def configure_pyttsx3():
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name}")
    
     # Let the user manually select a voice
    selected_voice = None
    for voice in voices:
        if "male" in voice.name.lower() or "man" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            selected_voice = voice
            print(f"Defaulting to male voice: {voice.name}")
            break

    if not selected_voice:
        print("Male voice not found. Retaining the default voice.")

    change_voice = input("Do you want to select a specific voice? (yes/no): ").strip().lower()
    if change_voice == "yes":
        print("Select a voice from the following options:")
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name}")
        try:
            voice_choice = int(input("Enter the voice number: ").strip())
            if 0 <= voice_choice < len(voices):
                engine.setProperty('voice', voices[voice_choice].id)
                print(f"Voice switched to: {voices[voice_choice].name}")
            else:
                print("Invalid choice. Retaining the current voice.")
        except ValueError:
            print("Invalid input! Retaining the current voice.")
       

    change_rate = input("Do you want to adjust the speaking rate? (yes/no): ").lower()
    if change_rate == "yes":
        try:
            rate = int(input("Enter the speaking rate (100-200): "))
            if 100 <= rate <= 200:
                engine.setProperty('rate', rate)
                print(f"Speaking rate set to: {rate}")
            else:
                print("Invalid rate! Keeping the default rate of 150.")
        except ValueError:
            print("Invalid input! Keeping the default rate of 150.")

    change_volume = input("Do you want to adjust the volume? (yes/no): ").lower()
    if change_volume == "yes":
        try:
            volume = float(input("Enter the volume level (0.0 to 1.0): "))
            if 0.0 <= volume <= 1.0:
                engine.setProperty('volume', volume)
                print(f"Volume set to {volume}")
            else:
                print("Invalid volume level! Keeping the default volume of 0.9.")
        except ValueError:
            print("Invalid input! Keeping the default volume of 0.9.")

# Main program
if __name__ == "__main__":
    text = ("Welcome to Multilingual RoboSpeaker 1.1 by Sandesh Thapa")
    print("(Type 'q' to quit, 'repeat' to repeat the last message, or 'history' to view command history.)")
    language = "en"  # English
    speak_gtts(text, lang=language)

    command_history = []
    last_message = ""

    configure_pyttsx3()

    languages = {
        
    "1": ("English", "en"),
    "2": ("Hindi", "hi"),
    "3": ("French", "fr"),
    "4": ("Nepali", "ne"),
 
}

   

    print("Available languages:")
    for key, (lang_name, _) in languages.items():
        print(f"{key}: {lang_name}")

    selected_lang = "en"  # Default language is English

    while True:
        x = input("\nEnter what you want to speak in English (or you can change the language press 1. for English, 2. for Hindi, 3. for French, 4. for Nepali): ").strip()

        if x.lower() == "q":
            engine.say("Thank you! Goodbye!")
            engine.runAndWait()
            break

        elif x.lower() == "repeat":
            if last_message:
                print(f"Repeating: {last_message}")
                speak_gtts(last_message, lang=selected_lang)
            else:
                print("No previous message to repeat.")
            continue

        elif x.lower() == "history":
            if command_history:
                print("Command History:")
                for i, cmd in enumerate(command_history, 1):
                    print(f"{i}: {cmd}")
            else:
                print("No history available.")
            continue

        # Detect language change command by just entering a number
        if x in languages:
            selected_lang = languages[x][1]
            print(f"Language switched to {languages[x][0]}")
            continue  # Skip the translation part and prompt again for text input

        try:
            translated_text = GoogleTranslator(source='en', target=selected_lang).translate(x)
            print(f"Translated text: {translated_text}")
            speak_gtts(translated_text, lang=selected_lang)
        except Exception as e:
            print(f"Error during translation or speech synthesis: {e}")

        command_history.append(x)
        last_message = translated_text
