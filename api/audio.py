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

