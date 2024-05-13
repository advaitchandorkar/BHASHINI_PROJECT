import requests

# API endpoint for translation
url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

headers = {
    "ULCA_API_KEY": "37c6c46ede-42d0-4323-986b-bcfc7d4d7a8d",
    "USER_ID": "8ef603f5ad0d4a61860a68baf15a4178",
    "Authorization": "vYOsFgEoUt7WA7CenVqcN0S6iVjUhsU_LnkXZm98Z0TwwdoOdT_Q2c7L5xEFIpzy"
}

# Payload for translation and TTS request
payload = {
    "pipelineTasks": [
        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": "hi",
                    "targetLanguage": "en"
                },
               "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4",
                    "modelId": "641d1cd18ecee6735a1b372a",
            }
        },
        {
            "taskType": "tts",
            "config": {
                "language": {
                    "sourceLanguage": "en"
                },
                "serviceId": "ai4bharat/indic-tts-coqui-misc-gpu--t4",
                    "modelId": "63f7384c2ff3ab138f88c64e",
                "gender": "female"
            }
        }
    ],
    "inputData": {
        "input": [
            {
                "source": "मेरा नाम विहिर है और मैं भाषाावर्ष यूज कर रहा हूँ"
                # "source": "My name is Vihir and I am using the language Varsh."
            }
        ],
    }
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    response_data = response.json()
    
    translated_text = response_data['pipelineResponse'][0]['output'][0]['target']
    print("Translated text:", translated_text)
    
    tts_audio_url = response_data['pipelineResponse'][1]['audio'][0]['audioContent']
    print("TTS audio URL:", tts_audio_url)
else:
    print("Error:", response.status_code, response.text)

# STORING VOICE COMMAND
    
import base64
import wave

# Audio content encoded in base64
audio_content_base64 = tts_audio_url

# Decode base64 audio content
audio_content_bytes = base64.b64decode(audio_content_base64)

# Specify the output file path
output_file_path = "output_audio.wav"

# Write the audio content to a WAV file
with wave.open(output_file_path, "wb") as audio_file:
    # Set parameters for the WAV file
    audio_file.setnchannels(1)  # Mono
    audio_file.setsampwidth(2)  # 2 bytes per sample
    audio_file.setframerate(22050)  # Sample rate: 22050 Hz
    audio_file.writeframes(audio_content_bytes)

print("Audio file saved successfully:", output_file_path)
