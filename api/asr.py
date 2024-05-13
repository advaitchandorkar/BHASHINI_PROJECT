# AUDIO RECORDING PART 
import pyaudio
import wave
import audioop
import threading

# Set parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (mono)
RATE = 44100              # Sampling rate (samples per second)
CHUNK = 1024              # Number of frames per buffer

# Threshold for detecting silence (adjust as needed)
SILENCE_THRESHOLD = 1000

# Minimum consecutive frames of silence to consider before stopping
MIN_SILENCE_FRAMES = 30

# Initialize PyAudio object
audio = pyaudio.PyAudio()

# Initialize variables for recording
frames = []
recording = False

# Function to start recording audio
def start_recording():
    global recording
    recording = True
    
    # Open audio stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording started. Press Enter to stop recording...")

    # Continue recording until recording flag is set to False
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
    
    # Close the audio stream
    stream.stop_stream()
    stream.close()

# Function to stop recording audio
def stop_recording():
    global recording
    recording = False

# Start recording in a separate thread
recording_thread = threading.Thread(target=start_recording)
recording_thread.start()

# Wait for user to press Enter to stop recording
input("Press Enter to stop recording...\n")

# Stop recording
stop_recording()
recording_thread.join()

# Create a WAV file to write the audio data
output_file = wave.open("recorded_audio.wav", "wb")
output_file.setnchannels(CHANNELS)
output_file.setsampwidth(audio.get_sample_size(FORMAT))
output_file.setframerate(RATE)

# Write recorded audio data to file
for frame in frames:
    output_file.writeframes(frame)

print("Recording finished.")

# Close the WAV file
output_file.close()

# Terminate PyAudio object
audio.terminate()





# ASR WORKING

import requests
import base64

with open("recorded_audio.wav", "rb") as audio_file:
    audio_data = audio_file.read()
    base64_encoded_audio_data = base64.b64encode(audio_data).decode("utf-8")

# Define your actual values
source_language = "en"
asr_service_id = "ai4bharat/whisper-medium-en--gpu--t4"
base64_audio_content = base64_encoded_audio_data
# API endpoint for ASR
asr_url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

# Request payload for ASR
asr_payload = {
    "pipelineTasks": [
        {
            "taskType": "asr",
            "config": {
                "language": {
                    "sourceLanguage": source_language
                },
                "serviceId": asr_service_id,
                "audioFormat": "wav",  # Corrected audio format
                "samplingRate": 16000
            }
        }
    ],
    "inputData": {
        "audio": [
            {
                "audioContent": base64_audio_content
            }
        ]
    }
}

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "ULCA_API_KEY": "37c6c46ede-42d0-4323-986b-bcfc7d4d7a8d",
    "USER_ID": "8ef603f5ad0d4a61860a68baf15a4178",
    "Authorization": "vYOsFgEoUt7WA7CenVqcN0S6iVjUhsU_LnkXZm98Z0TwwdoOdT_Q2c7L5xEFIpzy"
}

# Send POST request to ASR API with headers
response = requests.post(asr_url, json=asr_payload, headers=headers)

# Print the response
if response.ok:
    # Parse the JSON response
    response_data = response.json()
    # print(response_data['pipelineResponse'][0]['output'][0]['source'])
    data = response_data['pipelineResponse'][0]['output'][0]['source']
else:
    print("Error:", response.status_code, response.reason)
import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyAusIrjsAZ2CKqxHGLYDCKxkFd3xhBIZTI')

model = genai.GenerativeModel('gemini-pro')
question = ' This system will streamline categorization and retrieval processes by accurately extracting essential terms such as product company , product name, quantity, and price(only these are to be extracted). Follow this format for example : Parle biscuit: 5 packets, 10rs each.  Ensure high-level accuracy in recognizing crucial details to optimize inventory management workflows and facilitate seamless integration with inventory systems.'
response = model.generate_content(f'{question } {data}')

print(response.text)


# MAKE THE LIST OF THE PRODUCTS 

items = response.text.strip().split('\n')

# # Split data by lines
# data = """
# Amul milk: 1 packet, 60rs
# Cheese cube: 2 pieces, 30rs each
# Vim bar: 12 pieces, 5rs each
# """

# Split data by lines

# Initialize a 2D list to store product information
product_info = []

# Extract information from each item
for item in items:
    # Split item into product name, quantity, and price
    name_quantity_price = item.split(': ')
    
    # Extract product name
    product_name = name_quantity_price[0].split()[-1]  # Extract the last word as product name
    
    # Extract quantity and price
    quantity_price = name_quantity_price[1].split(', ')
    quantity = quantity_price[0].split()[0]
    price = quantity_price[1].split()[0]
    
    # Remove 'rs' or 'rupees' from price if present
    if price.endswith('rs') or price.endswith('rupees'):
        price = price[:-2]

    # Append product information to the 2D list
    product_info.append([product_name, quantity, price])

# Print the 2D list
for item in product_info:
    print(item)
