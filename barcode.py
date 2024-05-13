import tkinter as tk
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import requests
import numpy as np

class LiveVideoApp:
    def __init__(self, window, window_title, ip_address, port):
        self.window = window
        self.window.title(window_title)
        self.url = f"http://{ip_address}:{port}/video"

        # Open the video stream from IP Webcam
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            print("Error: Couldn't open the video stream.")
            return

        # Get video frame dimensions
        self.frame_width, self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(window, width=self.frame_width, height=self.frame_height)
        self.canvas.pack()

        # Create an empty ImageTk object (updated on each frame)
        self.photo = None

        # Flag to indicate if a barcode is detected in the current frame
        self.barcode_detected = False

        # Call the update function to start capturing and displaying
        self.update()

        # Bind 'q' key to quit
        self.window.bind('<KeyPress-q>', self.quit_app)

    def update(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        if ret:
            # Convert frame to RGB for Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Decode barcodes (optional: adjust frequency based on needs)
            decoded_objects = decode(frame)

            self.barcode_detected = False  # Reset flag before processing frame

            # Process detected barcodes
            if decoded_objects:
                for obj in decoded_objects:
                    cv2.rectangle(frame_rgb, obj.rect, (0, 255, 0), 2)
                    barcode_data = obj.data.decode("utf-8")
                    barcode_type = obj.type
                    # Process barcode data here (e.g., print, display on canvas)
                    print("Barcode Type:", barcode_type)
                    print("Barcode Data:", barcode_data)
                    self.barcode_detected = True  # Set flag if barcode found

            # Convert frame to ImageTk format and update canvas
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the next update (adjust delay for smooth display)
        self.window.after(10, self.update)

    def quit_app(self, event):
        self.cap.release()
        self.window.destroy()


def main():
    # IP address and port number provided by IP Webcam app
    ip_address = "192.168.51.117"  # Enclosed in quotes
    port = 8080

    root = tk.Tk()
    app = LiveVideoApp(root, "Live Video Feed", ip_address, port)
    root.mainloop()


if __name__ == "__main__":
    main()
