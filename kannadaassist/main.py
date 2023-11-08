import os
import random
from difflib import SequenceMatcher

from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr
import shutil
import wave
import pyaudio
import wave

def record_audio(output_filename, duration, sample_rate=44100, channels=2, format_=pyaudio.paInt16):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=format_,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=1024)

    print("Recording...")

    frames = []

    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording done.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format_))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


def translate_to_kannada_and_back_to_english(english_phrase):
    translator = Translator()

    # Translate English phrase to Kannada
    kannada_text = translator.translate(english_phrase, src='en', dest='kn').text

    # Translate Kannada text back to English
    translated_text = translator.translate(kannada_text, src='kn', dest='en').text

    return kannada_text, translated_text

def kannada_to_english_pronunciation(kannada_phrase):
    tts = gTTS(kannada_phrase, lang='kn')
    tts.save("temp.mp3")
    os.system("start temp.mp3")  # This will play the audio, you can comment it out if you don't want to play it.

def speech_recognition(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language='kn')
        return recognized_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""


def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

if __name__ == "__main__":
    english_phrase = input("Enter the English phrase to be translated to Kannada and back to English with pronunciation: ")
    kannada_translation, english_translation = translate_to_kannada_and_back_to_english(english_phrase)

    print("Kannada Translation:", kannada_translation)
    print("Back to English:", english_translation)

    kannada_to_english_pronunciation(kannada_translation)

    # audio_file_path = "recorded/goku.mp3"
    output_filename = input("Enter the output filename (e.g., recording.wav): ")
    duration = float(input("Enter the duration of the recording (in seconds): "))
    output_folder = "recorded"
    record_audio(output_filename, duration)
    destination = output_folder + '/' + output_filename
    shutil.move(output_filename, destination)
    print(f"File moved to {destination}")
    print(f"Recording saved as {output_filename}")

    folder_path = "recorded"


    def list_audio_files(folder_path):
        audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.wav', '.mp3', '.flac'))]
        return audio_files


    audio_files = list_audio_files(folder_path)
    print("Available audio files:")
    for idx, file_name in enumerate(audio_files, start=1):
        print(f"{idx}. {file_name}")

    selection = int(input("Select an audio file by entering its index: ")) - 1
    selected_audio_file = os.path.join(folder_path, audio_files[selection])

    recognizer = sr.Recognizer()
    with sr.AudioFile(selected_audio_file) as audio_source:
        try:
            audio_data = recognizer.record(audio_source)
            recognized_text = recognizer.recognize_google(audio_data, language="kn-IN")  # You can use other recognition methods too

            print("Recognized Text from Audio:", recognized_text)

            accuracy = calculate_similarity(recognized_text, kannada_translation)
            print(f"Accuracy: {accuracy * 100:.2f}%")

        except sr.UnknownValueError:
            print("Failed to recognize speech in the audio. Please check the audio content and try again.")
        except sr.RequestError as e:
            print(f"Error connecting to the Google API: {e}")




    if recognized_text:
        print("Recognized Text from Audio:", recognized_text)

        # Calculate accuracy
        accuracy = sr.SequenceMatcher(None, recognized_text, kannada_translation).ratio()
        print(f"Accuracy: {accuracy * 100:.2f}%")
    else:
        print("Failed to recognize the audio. Please check the audio file and try again.")

