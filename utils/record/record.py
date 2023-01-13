import tkinter as tk
import time

from datetime import datetime
from picamera import PiCamera
from tkinter import ttk
from tkinter import Button
from tkinter import StringVar
from tkinter import Label

RESOLUTION = (1280, 720)

# https://automaticaddison.com/how-to-set-up-real-time-video-using-opencv-on-raspberry-pi-4/
# https://roboticsbackend.com/raspberry-pi-camera-picamera-python-library/

class recorder():
    def __init__(self):
        # root window
        self.root = tk.Tk()
        self.root.geometry('190x140+300+300')
        self.root.resizable(False, False)
        self.root.title('Video recorder')
        self.camera = PiCamera()
        self.camera.framerate = 30
        self.camera.resolution = RESOLUTION
        self.camera.preview_fullscreen = False
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        self.camera.preview_window = (round(ws/2), 160, 640, 360)
        self.camera.start_preview()

        #Label
        self.state = StringVar()
        self.state.set("Ready to record")
        self.lbl = Label(self.root, textvariable=self.state, bg="white")
        self.lbl.config(width=23, height=1)
        self.lbl.grid(row=0, column=0)

        # Start recording button
        self.start_button = Button(self.root, text='Start recording', command=self.start)
        self.start_button.config(width=20, height=1)
        self.start_button.grid(row=1, column=0)


        # Stop recording button
        self.stop_button = Button(self.root, text='Stop recording', command=self.stop)
        self.stop_button.config(width=20, height=1)
        self.stop_button.grid(row=2, column=0)
        self.stop_button.config(state=tk.DISABLED)

        # Exit button
        self.exit_button = Button(self.root, text='Exit', command=self.quit)
        self.exit_button.config(width=20, height=1)
        self.exit_button.grid(row=3, column=0)


    def stop(self):
        self.state.set("Ready to record")
        self.lbl.config(bg="white")
        self.exit_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.camera.stop_recording()
        print("saved on " + self.video_out_file)

    def start(self):
        now = datetime.now()
        self.video_out_file = now.strftime("%d_%m_%Y-%H_%M_%S") + ".h264"
        self.state.set("Recording...")
        self.start_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.lbl.config(bg="yellow")
        self.camera.start_recording(self.video_out_file)
        print("start recording...")

    def display(self):
        self.root.mainloop()


    def quit(self):
        self.camera.stop_preview()
        print("Exit...")
        self.root.quit()


def main():
    r = recorder()
    r.display()

if __name__ == "__main__":
    main()
