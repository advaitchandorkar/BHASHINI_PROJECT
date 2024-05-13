# import requests
# import base64

# # Read the audio file as binary data
# with open("marathi.mp3", "rb") as audio_file:
#     audio_data = audio_file.read()

# # Encode the binary audio data to base64
# base64_encoded_audio_data = base64.b64encode(audio_data).decode("utf-8")

# # Now you can include base64_encoded_audio_data in your API request payload

# # Construct the request payload
# request_payload = {
#     "pipelineTasks": [
#         {
#             "taskType": "asr",
#             "config": {
#                 "serviceId": "ai4bharat/conformer-hi-gpu--t4",
#                 "language": {
#                     "sourceLanguage": "en",  # Source language of the audio
#                     "sourceScriptCode": ""   # Script code if applicable
#                 },
#                 "audioFormat": "mp3",        # Format of the audio file
#                 "encoding": "base64",        # Encoding of the audio data
#                 "samplingRate": 16000,       # Sampling rate of the audio
#                 "postProcessors": None       # Post-processing options if any
#             }
#         }
#     ],
#     "inputData": {
#         "audio": [
#             {
#                 "audioContent": base64_encoded_audio_data
#             }
#         ]
#     }
# }

# # Send the API request
# api_endpoint = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
# response = requests.post(api_endpoint, json=request_payload)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the response to extract ASR output
#     asr_output = response.json()

#     # Handle the ASR output as needed
#     print(asr_output)
# else:
#     print("Error:", response.text)


import requests
import base64

# Read the audio file as binary data and encode it to base64
with open("marathi.mp3", "rb") as audio_file:
    audio_data = audio_file.read()
    base64_encoded_audio_data = base64.b64encode(audio_data).decode("utf-8")

# Define your API endpoint
url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

# Replace these placeholders with actual values
ULCA_API_KEY = "{{37c6c46ede-42d0-4323-986b-bcfc7d4d7a8d}}"
USER_ID = "{{8ef603f5ad0d4a61860a68baf15a4178}}"
AUDIO_BASE64_DATA = base64_encoded_audio_data
SOURCE_LANGUAGE = "{{mr}}"
PIPELINE_ID = "{{ai4bharat/conformer-hi-gpu--t4}}"  # Replace with the specific pipeline ID for ASR

# API endpoint for ASR
API_ENDPOINT = url

# Construct the request headers
headers = {
    "userID": USER_ID,
    "ulcaApiKey": ULCA_API_KEY,
    "Content-Type": "application/json"
}

# Construct the request payload
payload = {
    "userId": USER_ID,
    "ulcaApiKey": ULCA_API_KEY,
    "pipelineId": PIPELINE_ID,
    "pipelineTasks": [
        {
            "taskType": "asr",
            "config": {
                "language": {
                    "sourceLanguage": SOURCE_LANGUAGE
                }
            }
        }
    ],
    "inputData": {
        "audio": [
            {
                "audioContent": AUDIO_BASE64_DATA
            }
        ]
    }
}

# Make the API call
try:
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        # Request successful, parse the response
        result = response.json()
        print("ASR Response:", result)
    else:
        print("Error:", response.status_code, response.text)
except Exception as e:
    print("Exception occurred:", str(e))