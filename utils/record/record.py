import errno
import os
import subprocess
import tkinter as tk
import time

from datetime import datetime
from picamera import PiCamera
from tkinter import ttk
from tkinter import Button
from tkinter import StringVar
from tkinter import Label
from configparser import ConfigParser

# https://automaticaddison.com/how-to-set-up-real-time-video-using-opencv-on-raspberry-pi-4/
# https://roboticsbackend.com/raspberry-pi-camera-picamera-python-library/

# read configuration.ini for sampling configuration
config_object = ConfigParser()

# Example "/home/pi/Desktop/CONFIGURATION.ini"
config_object.read("CONFIGURATION.ini")

# parse file
camera_conf = config_object["CAMERA_CONFIGURATION"]
resolution = camera_conf["resolution"]
fps = int(camera_conf["fps"])

FPS = 30
RESOLUTION = (1280, 720)

if (fps != 0 or fps != ""):
    FPS = fps

if (resolution != ""):
    W, H = resolution.split("x")
    RESOLUTION = (int(W), int(H))

print("*** Video configuration ***")
print("Resolution: " + str(RESOLUTION))
print("Frames per second: " + str(fps))


class recorder():
    def __init__(self):
        # root window
        self.root = tk.Tk()
        self.root.geometry('190x140+300+300')
        self.root.resizable(False, False)
        self.root.title('Video recorder')
        self.camera = PiCamera()
        self.camera.framerate = FPS
        self.camera.resolution = RESOLUTION
        self.camera.preview_fullscreen = False
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        self.camera.preview_window = (round(ws/2), 160, 640, 360)
        self.camera.start_preview()
        self.video_out_file = ""
        self.mp4out = ""
        self.aviout = ""
        self.output_path = "/home/pi/Desktop/VIDEOS/"

        # Video output generation
        if not os.path.exists(self.output_path):
            print("Create output path")
            os.makedirs(self.output_path)

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


        # Convert to mp4  button
        #self.mp4_button = Button(self.root, text='Convert to mp4', command=self.convert2mp4)
        self.mp4_button = Button(self.root, text='Generate mp4, avi videos', command=self.process_videos)
        self.mp4_button.config(width=20, height=1)
        self.mp4_button.grid(row=3, column=0)
        self.mp4_button.config(state=tk.DISABLED)


        # Exit button
        self.exit_button = Button(self.root, text='Exit', command=self.quit)
        self.exit_button.config(width=20, height=1)
        self.exit_button.grid(row=4, column=0)


    def stop(self):
        self.state.set("Ready to record")
        self.lbl.config(bg="white")
        self.exit_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.mp4_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.camera.stop_recording()
        print("saved on " + self.video_out_file)


    def start(self):
        now = datetime.now()
        self.video_basename = self.output_path + now.strftime("%d_%m_%Y-%H_%M_%S")
        self.video_out_file = self.video_basename + ".h264"
        self.state.set("Recording...")
        self.start_button.config(state=tk.DISABLED)
        self.mp4_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.lbl.config(bg="yellow")
        self.camera.start_recording(self.video_out_file)
        print("start recording...")


    def convert2mp4(self):
        print("convert to mp4")
        if (self.is_MP4Box_tool()):
            video_format = '{0}:fps={1}'.format(self.video_out_file, FPS)
            print(video_format)
            self.mp4out = self.video_basename + ".mp4"
            process = subprocess.Popen(['MP4Box', '-add', video_format, "-new", self.mp4out],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout.decode("UTF-8"))
            print(stderr.decode("UTF-8"))
        else:
            print("error: MP4Box no found")
            self.mp4_button.config(state=tk.DISABLED)

    def convert_mp4_2_avi(self):
        self.aviout = self.video_basename + ".avi"
        print("convert to AVI, this may take some time...")
        #process = subprocess.Popen(['ffmpeg', '-i', self.mp4out, "-vcodec", "copy", "-acodec", "copy", tmp],
        #        stdout=subprocess.PIPE,
        #        stderr=subprocess.PIPE)
        #stdout, stderr = process.communicate()
        process = subprocess.Popen(['ffmpeg', '-i', self.mp4out, "-f", "avi", "-vcodec", "mjpeg", self.aviout],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode("UTF-8"))
        print(stderr.decode("UTF-8"))
        print("===========================================================")
        print("Finish video generation!!!")


        #ffmpeg -i file.mp4 -vcodec copy -acodec copy file.avi
        #ffmpeg -i input.avi -f avi -vcodec mjpeg output.avi

        #ffmpeg -i file.mp4 -f avi -vcodec mjpeg out.avi


    def process_videos(self):
        self.convert2mp4()
        self.convert_mp4_2_avi()

    def is_MP4Box_tool(self):
        try:
            devnull = open(os.devnull)
            subprocess.Popen(["MP4Box"], stdout=devnull, stderr=devnull).communicate()
        except OSError as e:
            if e.errno == errno.ENOENT:
                return False
        return True


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
