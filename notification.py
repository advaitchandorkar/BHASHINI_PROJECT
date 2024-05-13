# import sqlite3
# from twilio.rest import Client
# import pyttsx3
# import time

# # Initialize Twilio client
# account_sid = 'ACb8fa6601b413af33fd481b4fd7b47de0'  # Your Twilio Account SID
# auth_token = 'd1c0677d42e5111af262becebf39760f'   # Your Twilio Auth Token
# client = Client(account_sid, auth_token)

# # Function to fetch data from the database
# def fetch_data():
#     conn = sqlite3.connect('inventory.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT product_name, quantity FROM inventory WHERE quantity < 10")  # Updated query
#     data = cursor.fetchall()
#     conn.close()
#     return data

# # Function to send SMS notification using Twilio
# def send_sms(receiver_number, product_name, quantity):
#     twilio_phone_number = '++12563635910'  # Your Twilio phone number
#     message = client.messages.create(
#         body=f"Product Name: {product_name}, Quantity: {quantity} , Restock NOW !!!",
#         from_=twilio_phone_number,
#         to=receiver_number
#     )
#     print("Message SID:", message.sid)  # Print the SID for debugging purposes

# # Function to convert text to speech
# def convert_to_speech(product_name, quantity):
#     engine = pyttsx3.init()
#     engine.say(f"Product Name: {product_name}, Quantity: {quantity}")
#     engine.runAndWait()

# # Main function to send notifications every 5 hours
# def send_notifications():
#     while True:
#         # Fetch data from the database
#         data = fetch_data()

#         for product in data:
#             product_name, quantity = product
#             receiver_number = "+918369196926"  # Corrected phone number format

#             # Send SMS notification using Twilio
#             send_sms(receiver_number, product_name, quantity)

#         # Convert text to speech
#         for product in data:
#             product_name, quantity = product
#             convert_to_speech(product_name, quantity)

#         # Sleep for 5 hours before sending the next notification
#         time.sleep(5 * 60 * 60)

# # Function to trigger notifications manually
# def trigger_notifications_manually():
#     # Fetch data from the database
#     data = fetch_data()

#     for product in data:
#         product_name, quantity = product
#         receiver_number = "+918369196926"  # Corrected phone number format


#         # Send SMS notification using Twilio
#         send_sms(receiver_number, product_name, quantity)

#     # Convert text to speech
#     for product in data:
#         product_name, quantity = product
#         convert_to_speech(product_name, quantity)

# # Example usage of manual trigger
# trigger_notifications_manually()



import sqlite3
from twilio.rest import Client
import pyttsx3
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize Twilio client
account_sid = 'ACb8fa6601b413af33fd481b4fd7b47de0'  # Your Twilio Account SID
auth_token = 'd1c0677d42e5111af262becebf39760f'   # Your Twilio Auth Token
client = Client(account_sid, auth_token)

# Function to fetch data from the database
def fetch_data():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, quantity FROM inventory WHERE quantity < 10")  # Updated query
    data = cursor.fetchall()
    conn.close()
    return data

def send_combined_sms(receiver_number, items):
    twilio_phone_number = '++12563635910'  # Your Twilio phone number
    message_body = "\n".join([f"Product Name: {item[0]}, Quantity: {item[1]}" for item in items])
    message = client.messages.create(
        body=f"Items needing restocking:\n{message_body}\nRestock NOW !!!",
        from_=twilio_phone_number,
        to=receiver_number
    )
    print("Message SID:", message.sid)

# Function to send combined email notification
def send_combined_email(receiver_email, items):
    sender_email = "advaitchandorkar612@gmail.com"
    password = "fcme lbop jrqt drqq"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Inventory Notification"

    message_body = "\n".join([f"Product Name: {item[0]}, Quantity: {item[1]}" for item in items])
    body = f"Items needing restocking:\n{message_body}\nRestock NOW !!! JYADA GULU GULU MAT KAR"
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Function to convert text to speech
def convert_to_speech(product_name, quantity):
    engine = pyttsx3.init()
    engine.say(f"Product Name: {product_name}, Quantity: {quantity}")
    engine.runAndWait()

# Main function to send notifications every 5 hours
def send_notifications():
    while True:
        # Fetch data from the database
        data = fetch_data()

        # Accumulate items needing restocking
        items_needing_restocking = []

        for product in data:
            product_name, quantity = product
            items_needing_restocking.append((product_name, quantity))

        # Check if any items need restocking
        if items_needing_restocking:
            # Send combined SMS notification using Twilio
            receiver_number = "+918454049903"  # Corrected phone number format
            send_combined_sms(receiver_number, items_needing_restocking)

            # Send combined email notification
            receiver_email = "advaitc612@gmail.com"
            send_combined_email(receiver_email, items_needing_restocking)

            # Convert text to speech for each item separately
            for item in items_needing_restocking:
                product_name, quantity = item
                convert_to_speech(product_name, quantity)

        # Sleep for 5 hours before sending the next notification
        time.sleep(5 * 60 * 60)

# Function to trigger notifications manually
def trigger_notifications_manually():

    data = fetch_data()

    # Accumulate items needing restocking
    items_needing_restocking = []

    for product in data:
        product_name, quantity = product
        items_needing_restocking.append((product_name, quantity))

    # Check if any items need restocking
    if items_needing_restocking:
        # Send combined SMS notification using Twilio
        receiver_number = "+918454049903"  # Corrected phone number format
        send_combined_sms(receiver_number, items_needing_restocking)

        # Send combined email notification
        receiver_email = "advaitc612@gmail.com"
        send_combined_email(receiver_email, items_needing_restocking)

        # Convert text to speech for each item separately
        for item in items_needing_restocking:
            product_name, quantity = item
            convert_to_speech(product_name, quantity)

# Example usage of manual trigger
trigger_notifications_manually()