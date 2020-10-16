from tkinter import *
#import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
import threading
import time
import imutils
import cv2
from imutils.video import VideoStream

#Tk = tkinter.Tk

class GUIapp():

    def save_info(self):
        m = self.entry1.get()
        print(m)
        with open('email-list.txt', 'a') as the_file:
            the_file.write(m + '\n')
        self.clear_text()

    def clear_text(self):
        self.entry1.delete(0, 'end')

    def __init__(self):
        self.i = 0
        root = Tk()
        root.geometry("750x450")
        root.attributes('-fullscreen', False)
        root.title("R2 GUI")
        self.note = ttk.Notebook(root)

        self.tab1 = ttk.Frame(self.note)
        self.tab2 = ttk.Frame(self.note)
        self.tab3 = ttk.Frame(self.note)
        self.tab4 = ttk.Frame(self.note)
        self.quitButton = ttk.Button(self.note, text="Quit the program", command=quit)
        self.panel = None

        # tab 1 information : General Info
        Cup_Label_path = "cup.jpg"
        img = Image.open(Cup_Label_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        Label_Img = ImageTk.PhotoImage(img)
        label_pic = Label(self.tab1, image=Label_Img)
        label_pic.place(x=0, y=0)

        text_intro = Label(self.tab1, text="Hi, this is Cornell Cup Robotics!", width=30, font=("Arial", 17, "bold"))
        text_intro.place(x=130, y=30)

        info = "        The original R2D2 Project focused upon creating a semi-autonomous " \
               "lab assistant that could navigate and map out its surrounding " \
               "environment. Since last year, the team has expanded upon R2's ability " \
               "to interact with its surroundings, enabling the droid to complete tasks " \
               "such as lifting baskets, recognizing and greeting people " \
               "and interacting with users via voice" \
               "To generate excitement and interest in robotics and engineering, " \
               "the team aims to advertise the R2 project and " \
               "generate interest in its design process through a Kickstarter campaign.\n" \
               "        This hopefully will work toward the long-term goal of " \
               "having our R2 robot appear in a Star Wars movie."
        text = Label(self.tab1, text=info, width= 60 , wraplength = 450, font=("Arial, 12"), justify = 'left')
        text.place(x= -10 , y=120)

        # tab 2 information : Visual Img
        # initialize video stream
        self.vs = VideoStream().start()
        video_thread = threading.Thread(target=self.videoLoop)
        video_thread.start()

        # tab 3 information : Data Streaming
        Facial_Recognition_Photo_path = "cropped.png"
        img = Image.open(Facial_Recognition_Photo_path)
        img = img.resize((180, 180), Image.ANTIALIAS)
        Facial_Recognition_Photo_img = ImageTk.PhotoImage(img)
        
        Object_Detection_Photo_path = "backimage.png"
        img2 = Image.open(Object_Detection_Photo_path)
        img2 = img2.resize((320, 180), Image.ANTIALIAS)
        Object_Detection_Photo_img = ImageTk.PhotoImage(img2)

        c1 = Label(self.tab3, text="Voice Recognition Text", font=("Helvetica", 14,"bold"))
        c2 = Label(self.tab3, text="Sentiment Analysis Output", font=("Helvetica", 14,"bold"))
        c3 = Label(self.tab3, text="Facial Recognition Photo", font=("Helvetica", 14,"bold"))
        c4 = Label(self.tab3, text="Object Detection Result", font=("Helvetica", 14,"bold"))
        c5 = Label(self.tab3, text="Facial Recognition Result", font=("Helvetica", 14,"bold"))
        self.data1 = Label(self.tab3, text="", font=("Courier", 13))
        self.data2 = Label(self.tab3, text="", font=("Courier", 13))
        self.data3 = Label(self.tab3, image=Facial_Recognition_Photo_img)
        self.data4 = Label(self.tab3, image=Object_Detection_Photo_img)
        self.data5 = Label(self.tab3, text="", font=("Courier", 13))

        c1.grid(row=0, column=0, padx=2, pady=0)
        c2.grid(row=0, column=1, padx=2, pady=0)
        c3.grid(row=2, column=0, padx=2, pady=0)
        c4.grid(row=2, column=1, padx=2, pady=0)
        c5.grid(row=4, column=0, padx=2, pady=0, rowspan=1)
        self.data1.grid(row=1, column=0, padx=2, pady=0)
        self.data2.grid(row=1, column=1, padx=2, pady=0)
        self.data3.grid(row=3, column=0, padx=2, pady=0)
        self.data4.grid(row=3, column=1, padx=2, pady=0)
        self.data5.grid(row=5, column=0, padx=2, pady=0, rowspan=1)

        # tab 4 information : Sign up
        self.text = Label(self.tab4, text="Enter your Email here: ", font=("Helvetica", 18 ,"bold"))
        self.text.pack(side=LEFT)
        self.entry1 = Entry(self.tab4)
        self.text.grid(row=3, sticky=W)
        self.entry1.grid(row=3, column=1)
        b = Button(self.tab4, text="OK", command=self.save_info, height = 5, width = 10, font="Helvetica")
        b.grid(row=3, column = 3, sticky=E)

        self.note.add(self.tab1, text="General Info")
        self.note.add(self.tab2, text="Visual Img")
        self.note.add(self.tab3, text="Data Streaming")
        self.note.add(self.tab4, text="Sign up")
        self.note.add(self.quitButton, text="For Staff Only")
        self.note.pack()

        # create a thread to constantly update the text in the streaming tab
        thread1 = threading.Thread(target=self.update_stream_text)
        thread1.start()

        root.mainloop()

    # update the text in the streaming tab once a second
    def update_stream_text(self):
        while 1:
            # update the text
            VoiceRecognitionText = open('VoiceRecognitionText.txt', 'r').read()
            SentimentAnalysisOutput = open('SentimentAnalysisOutput.txt', 'r').read()
            FacialRecognitionResult = open('FacialRecognitionResult.txt', 'r').read()
            #ObjectDetectionResult = open('ObjectDetectionResult.txt', 'r').read()
            self.data1['text'] = VoiceRecognitionText
            self.data2['text'] = SentimentAnalysisOutput
            self.data5['text'] = FacialRecognitionResult

            img = Image.open("cropped.png")
            img = img.resize((180, 180), Image.ANTIALIAS)
            Facial_Recognition_Photo_img = ImageTk.PhotoImage(img)
                    
            img2 = Image.open("backimage.png")
            img2 = img2.resize((320, 180), Image.ANTIALIAS)
            Object_Detection_Photo_img = ImageTk.PhotoImage(img2)

            # update the photos
            self.data3['image'] = Facial_Recognition_Photo_img            
            self.data4['image'] = Object_Detection_Photo_img
            self.tab3.update()
            
            # make the system sleep for 1 second
            time.sleep(1)

    def videoLoop(self):
        # keep looping over frames until we are instructed to stop
        while 1:
            # grab the frame from the video stream and resize it to
            # have a maximum width of 300 pixels
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=500)
            # OpenCV represents images in BGR order; however PIL
            # represents images in RGB order, so we need to swap
            # the channels, then convert to PIL and ImageTk format
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            # if the panel is not None, we need to initialize it
            if self.panel is None:
                self.panel = Label(self.tab2, image=image, width=500)
                self.panel.image = image
                self.panel.pack(side="left", padx=10, pady=10)

            # otherwise, simply update the panel
            else:
                self.panel.configure(image=image)
                self.panel.image = image

GUIapp()
