import requests


headers = {
    "ULCA_API_KEY": "37c6c46ede-42d0-4323-986b-bcfc7d4d7a8d",
    "USER_ID": "8ef603f5ad0d4a61860a68baf15a4178",
    "Authorization":"vYOsFgEoUt7WA7CenVqcN0S6iVjUhsU_LnkXZm98Z0TwwdoOdT_Q2c7L5xEFIpzy"
}


api_url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

payload = {
    "pipelineTasks": [
        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": "en",
                    "targetLanguage": "hi"
                },
                "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
            }
        }
    ],
    "inputData": {
        "input": [
            {
                # "source": "मेरा नाम विहिर है और मैं भाषाावर्ष यूज कर रहा हूँ"
                "source": "My name is Vihir and I am using the language Varsh."
            }
        ],
        "audio": [
            {
                "audioContent": "null"
            }
        ]
    }
}

response = requests.post(api_url, json=payload, headers=headers)

if response.status_code == 200:
    translation_result = response.json()
    print(translation_result['pipelineResponse'][0]['output'][0]['target'])
else:
    print("Error:", response.status_code, response.text)

