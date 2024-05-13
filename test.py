import pyaudio
import wave
import audioop
import threading
import sqlite3
import requests
import base64
import google.generativeai as genai


# ASR WORKING

# Read the recorded audio file and encode it
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
    data = response_data['pipelineResponse'][0]['output'][0]['source']
else:
    print("Error:", response.status_code, response.reason)

genai.configure(api_key='AIzaSyAusIrjsAZ2CKqxHGLYDCKxkFd3xhBIZTI')

model = genai.GenerativeModel('gemini-pro')
question = ' This system will streamline categorization and retrieval processes by accurately extracting essential terms such as product company , product name, quantity, and price(only these are to be extracted) and expiry date if given. Follow this format for example : Parle biscuit: 5 packets, 10rs each , expiry 10th june 2024.  Ensure high-level accuracy in recognizing crucial details to optimize inventory management workflows and facilitate seamless integration with inventory systems.'
response = model.generate_content(f'{question } {data}')

print(response.text)

# Extract information from the response
items = response.text.strip().split('\n')

# Initialize a connection to the database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create the inventory table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS inventory
             (id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, product_name TEXT, quantity INTEGER, price INTEGER, expiry_date date)''')
conn.commit()

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

    # Check if the product already exists in the database
    c.execute("SELECT * FROM inventory WHERE product_name = ?", (product_name,))
    existing_product = c.fetchone()

    if existing_product:
        # Update the quantity of the existing product
        current_quantity = existing_product[3]  # Extract current quantity
        new_quantity = current_quantity + int(quantity)  # Calculate new quantity
        # Update the database with the new quantity
        c.execute("UPDATE inventory SET quantity = ? WHERE product_name = ?", (new_quantity, product_name))
    else:
        # Insert the new product into the database
        c.execute("INSERT INTO inventory (product_name, quantity, price) VALUES (?, ?, ?)", (product_name, int(quantity), float(price)))

# Commit changes and close the connection
conn.commit()
conn.close()

