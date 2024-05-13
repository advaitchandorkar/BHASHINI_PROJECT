from flask import Flask, render_template, request, redirect, url_for,jsonify
import io
import subprocess
import sqlite3
import pyaudio
import wave
import threading
from subprocess import Popen

app = Flask(__name__)

# Set parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (mono)
RATE = 44100              # Sampling rate (samples per second)
CHUNK = 1024              # Number of frames per buffer

# Initialize PyAudio object
audio = pyaudio.PyAudio()

# Initialize variables for recording
frames = []
recording = False


# Function to start recording audio
def start_recording():
    global recording, frames
    frames = []
    recording = True
    
    # Open audio stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording started.")
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
    print("done recoding")
    # Close the audio stream
    stream.stop_stream()
    stream.close()

# Function to stop recording audio
def stop_recording():
    global recording
    recording = False

@app.route('/start_recording', methods=['POST'])
def start_rec():
    global recording_thread
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()
    # return redirect(url_for('index'))
    return jsonify({'status': ''})

@app.route('/stop_recording', methods=['POST'])
def stop_rec():
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
    output_file.close()
    # return redirect(url_for('index'))
    return jsonify({'status': ''})

# Function to create the users table
def create_users_table():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Dummy data for users
users = [{'username': 'user1', 'password': 'password1'},
         {'username': 'user2', 'password': 'password2'}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

def navigate():
    # Redirect to the second page
    return redirect(url_for('inventorytrack.html'))


@app.route('/execute-python-file', methods=['POST'])
def execute_python_file():
    # Assuming the Python file you want to execute is named 'script.py'
    subprocess.run(['python', 'test.py'])
    return 'Python file executed successfully!'

@app.route('/delete_python', methods=['POST'])
def delete_python():
    # Assuming the Python file you want to execute is named 'script.py'
    subprocess.run(['python', 'delete.py'])
    return 'Python file executed successfully!'



@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return f'Welcome, {user[1]}!'
    else:
        return 'Invalid email or password'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            return 'Passwords do not match'

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
                  (name, email, phone, password))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/aboutus')
def aboutus():
    return render_template('about.html')

@app.route('/Inventorytrack')
def Inventorytrack():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Query the database to retrieve inventory data
    c.execute("SELECT * FROM inventory")
    inventory_data = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the HTML template with inventory data
    return render_template('inventorytrack.html', inventory=inventory_data)
   


@app.route('/start_streamlit', methods=['GET'])
def start_streamlit():
    # Start the Streamlit app using a subprocess
   streamlit_process = Popen(['C:\\Users\\ASUS\\OneDrive\\Desktop\\bhashini\\steamlit.py', 'run', 'streamlit.py'])
   return redirect('/')

@app.route('/notification')
def notification():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Query the database to retrieve inventory data
    c.execute("SELECT * FROM inventory")
    inventory_data = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the HTML template with inventory data
    return render_template('notification.html', inventory=inventory_data)

# @app.route('/trigger_notifications', methods=['POST'])
# def trigger_notifications():
#     subprocess.run(['python', 'notification.py'])
#     return jsonify({'message': 'Notification script executed successfully!'})

@app.route('/run_notification_script', methods=['POST'])
def run_notification_script():
    subprocess.run(['python', 'notification.py'])
    return jsonify({'message': 'Notification script executed successfully!'})


@app.route('/addProduct')
def addProduct():
    return render_template('addProduct.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

#restock code

@app.route('/manufacturers')
def manufacturers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Query the database to retrieve inventory data
    c.execute("SELECT * FROM inventory")
    inventory_data = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the HTML template with inventory data
    return render_template('manufacturers.html', inventory=inventory_data)


#add product code

def insert_data(company_name, product_name, quantity, price, expiry_date):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (company_name, product_name, quantity, price, expiry) VALUES (?, ?, ?, ?, ?)",
                   (company_name, product_name, quantity, price, expiry_date))
    conn.commit()
    conn.close()

# Route to handle form submission
@app.route('/submit_product', methods=['POST'])
def submit_product():
    if request.method == 'POST':
        company_name = request.form['companyName']
        product_name = request.form['productName']
        quantity = request.form['Quantity']
        price = request.form['price']
        expiry_date = request.form['expiryDate']

        insert_data(company_name, product_name, quantity, price, expiry_date)

        return redirect(url_for('addProduct'))  # Redirect to the inventory page after submission

#product inventory

@app.route('/product_inventory')
def product_inventory():
   
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Query the database to retrieve inventory data
    c.execute("SELECT * FROM inventory")
    inventory_data = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the HTML template with inventory data
    return render_template('product_inventory.html', inventory=inventory_data)


def update_inventory_item(item_id, company_name, product_name, quantity, price, expiry_date):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET company_name=?, product_name=?, quantity=?, price=?, expiry_date=? WHERE id=?",
              (company_name, product_name, quantity, price, expiry_date, item_id))
    conn.commit()
    conn.close()

# Function to delete an item from the inventory database
def delete_inventory_item(item_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

@app.route('/save_item', methods=['POST'])
def save_item():
    data = request.json
    item_id = data['itemId']
    company_name = data['companyName']
    product_name = data['productName']
    quantity = data['quantity']
    price = data['price']
    expiry_date = data['expiryDate']
    
    update_inventory_item(item_id, company_name, product_name, quantity, price, expiry_date)
    return jsonify({'status': 'success'})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.json
    item_id = data['itemId']
    
    delete_inventory_item(item_id)
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    create_users_table()  # Create the users table when the application starts
    app.run(debug=True)

from flask import request, jsonify

# Route to handle saving edited data
@app.route('/save_edited_data', methods=['POST'])
def save_edited_data():
    data = request.json
    product_name = data['productName']
    quantity = data['quantity']
    price = data['price']

    # Update the database with the edited values (you'll need to implement this)
    # Example:
    # update_inventory_item(product_name, quantity, price)

    return jsonify({'status': 'success'})
