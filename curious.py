import streamlit as st
import moviepy.editor as mp
from openai import AzureOpenAI
import tempfile
import os
import speech_recognition as sr
from pydub import AudioSegment
import requests
import io
import time
from openai import APIConnectionError  # Add this import
import openai
from dotenv import load_dotenv

load_dotenv()

# Set up Azure OpenAI credentials
azure_api_key = os.getenv("AZURE_API_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
print(azure_api_key)

# Initialize OpenAI client with increased timeout
openai_client = AzureOpenAI(
    api_key=azure_api_key,
    api_version="2024-08-01-preview",
    azure_endpoint=azure_endpoint,
    timeout=30.0 
)

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio"
    except sr.RequestError:
        return "Could not request results from the speech recognition service"

def correct_text(text):
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that corrects grammar and removes filler words."},
                    {"role": "user", "content": f"Please correct the following text, removing grammatical errors and filler words: {text}"}
                ]
            )
            return response.choices[0].message.content
        except APIConnectionError as e:
            if attempt < max_retries - 1:
                st.warning(f"Connection error. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                st.error(f"Failed to connect to Azure OpenAI API after {max_retries} attempts. Please check your internet connection and API configuration.")
                raise
        except Exception as e:
            st.error(f"An error occurred while correcting the text: {str(e)}")
            raise

import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[0].id)  # Voice type
    
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        audio_path = temp_audio_file.name

    # Save the speech to a file
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    
    return audio_path

def replace_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    audio = mp.AudioFileClip(audio_path)
    
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)
    else:
        video = video.subclip(0, audio.duration)
    
    final_video = video.set_audio(audio)
    output_path = "output_video.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

def main():
    st.title("Video Audio Replacement PoC")
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            temp_video_file.write(uploaded_file.read())
            video_path = temp_video_file.name
        
        st.video(video_path)
        
        if st.button("Process Video"):
            with st.spinner("Processing..."):
                try:
                    # Extract audio from video
                    video = mp.VideoFileClip(video_path)
                    audio_path = "temp_audio.wav"
                    video.audio.write_audiofile(audio_path)
                    
                    # Transcribe audio
                    transcription = transcribe_audio(audio_path)
                    st.text("Original Transcription:")
                    st.write(transcription)
                    
                    # Correct transcription
                    corrected_text = correct_text(transcription)
                    st.text("Corrected Transcription:")
                    st.write(corrected_text)
                    
                    # Generate new audio
                    new_audio_path = text_to_speech(corrected_text)
                    
                    if new_audio_path:
                        # Replace audio in video
                        output_video_path = replace_audio(video_path, new_audio_path)
                        
                        st.success("Video processing complete!")
                        st.video(output_video_path)
                        
                        # Clean up temporary files
                        os.unlink(video_path)
                        os.unlink(audio_path)
                        os.unlink(new_audio_path)
                except Exception as e:
                    print()


if __name__ == "__main__":
    main()