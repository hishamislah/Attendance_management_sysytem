import tkinter as tk
from tkinter import messagebox
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

window = tk.Tk()
window.title("Attendance System")
window.configure(background='pink')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

x_cord = 75
y_cord = 20

# Labels and UI elements
message = tk.Label(window, text="RSET", bg="white", fg="black", width=20, height=2, font=('Times New Roman', 25, 'bold'))
message.place(x=1150, y=760)

title = tk.Label(window, text="ATTENDANCE MANAGEMENT PORTAL", bg="pink", fg="black", width=40, height=1,
                 font=('Times New Roman', 35, 'bold underline'))
title.place(x=200, y=20)

lbl = tk.Label(window, text="Enter Your College ID", width=20, height=2, fg="black", bg="Pink",
               font=('Times New Roman', 25, ' bold '))
lbl.place(x=200 - x_cord, y=200 - y_cord)

txt = tk.Entry(window, width=30, bg="white", fg="blue", font=('Times New Roman', 15, ' bold '))
txt.place(x=250 - x_cord, y=300 - y_cord)

lbl2 = tk.Label(window, text="Enter Your Name", width=20, fg="black", bg="pink", height=2,
                font=('Times New Roman', 25, ' bold '))
lbl2.place(x=600 - x_cord, y=200 - y_cord)

txt2 = tk.Entry(window, width=30, bg="white", fg="blue", font=('Times New Roman', 15, ' bold '))
txt2.place(x=650 - x_cord, y=300 - y_cord)

lbl3 = tk.Label(window, text="NOTIFICATION", width=20, fg="black", bg="pink", height=2,
                font=('Times New Roman', 25, ' bold '))
lbl3.place(x=1060 - x_cord, y=200 - y_cord)

message = tk.Label(window, text="", bg="white", fg="blue", width=30, height=1, activebackground="white",
                   font=('Times New Roman', 15, ' bold '))
message.place(x=1075 - x_cord, y=300 - y_cord)

lbl3 = tk.Label(window, text="ATTENDANCE", width=20, fg="white", bg="lightgreen", height=2,
                font=('Times New Roman', 30, ' bold '))
lbl3.place(x=120, y=570 - y_cord)

message2 = tk.Label(window, text="", fg="red", bg="yellow", activeforeground="green", width=60, height=4,
                    font=('times', 15, ' bold '))
message2.place(x=700, y=570 - y_cord)

lbl4 = tk.Label(window, text="STEP 1", width=20, fg="green", bg="pink", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl4.place(x=240 - x_cord, y=375 - y_cord)

lbl5 = tk.Label(window, text="STEP 2", width=20, fg="green", bg="pink", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl5.place(x=645 - x_cord, y=375 - y_cord)

lbl6 = tk.Label(window, text="STEP 3", width=20, fg="green", bg="pink", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl6.place(x=1100 - x_cord, y=362 - y_cord)


def clear1():
    txt.delete(0, 'end')
    message.config(text="")


def clear2():
    txt2.delete(0, 'end')
    message.config(text="")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = txt.get()
    name = txt2.get()
    if not Id:
        res = "Please enter Id"
        message.config(text=res)
        MsgBox = messagebox.askquestion("Warning",
                                        "Please enter roll number properly , press yes if you understood",
                                        icon='warning')
        if MsgBox == 'no':
            messagebox.showinfo('Your need', 'Please go through the readme file properly')
    elif not name:
        res = "Please enter Name"
        message.config(text=res)
        MsgBox = messagebox.askquestion("Warning",
                                        "Please enter your name properly , press yes if you understood",
                                        icon='warning')
        if MsgBox == 'no':
            messagebox.showinfo('Your need', 'Please go through the readme file properly')

    elif is_number(Id) and name.isalpha():
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        # Make sure TrainingImage directory exists
        if not os.path.exists("TrainingImage"):
            os.makedirs("TrainingImage")

        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(f"TrainingImage/{name}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                cv2.imshow('frame', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name

        # Make sure StudentDetails directory exists
        if not os.path.exists("StudentDetails"):
            os.makedirs("StudentDetails")

        with open('StudentDetails/StudentDetails.csv', 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Id, name])
        message.config(text=res)
    else:
        if is_number(Id):
            res = "Enter Alphabetical Name"
            message.config(text=res)
        if name.isalpha():
            res = "Enter Numeric Id"
            message.config(text=res)


def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Ids = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Ids))

    # Make sure TrainingImageLabel directory exists
    if not os.path.exists("TrainingImageLabel"):
        os.makedirs("TrainingImageLabel")

    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Image Trained"
    clear1()
    clear2()
    message.config(text=res)
    messagebox.showinfo('Completed', 'Your model has been trained successfully!!')


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    
    faces = []
    Ids = []
    
    for imagePath in imagePaths:
        # Skip non-image files like .DS_Store
        if imagePath.endswith(".jpg") or imagePath.endswith(".png") or imagePath.endswith(".jpeg"):
            try:
                pilImage = Image.open(imagePath).convert('L')
                imageNp = np.array(pilImage, 'uint8')
                Id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces.append(imageNp)
                Ids.append(Id)
            except Exception as e:
                print(f"Skipping file {imagePath}, error: {e}")
        else:
            print(f"Skipping non-image file: {imagePath}")
    return faces, Ids



def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    
    # Make sure ImagesUnknown directory exists
    if not os.path.exists("ImagesUnknown"):
        os.makedirs("ImagesUnknown")

    while True:
        ret, im = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                if len(aa) > 0:
                    name = aa[0]
                else:
                    name = "Unknown"
                tt = str(Id) + "-" + name
                attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
            else:
                Id = 'Unknown'
                tt = str(Id)
                if conf > 75:
                    noOfFile = len(os.listdir("ImagesUnknown")) + 1
                    cv2.imwrite(f"ImagesUnknown/Image{noOfFile}.jpg", im[y:y + h, x:x + w])

            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if cv2.waitKey(1) == ord('q'):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    
    # Make sure Attendance directory exists
    if not os.path.exists("Attendance"):
        os.makedirs("Attendance")

    fileName = f"Attendance/Attendance_{date}_{Hour}-{Minute}-{Second}.csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()
    message2.config(text=str(attendance))
    res = "Attendance Taken"
    message.config(text=res)
    messagebox.showinfo('Completed', 'Congratulations! Your attendance has been marked successfully for the day!!')


def quit_window():
    MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if MsgBox == 'yes':
        messagebox.showinfo("Greetings", "Thank You very much for using our software. Have a nice day ahead!!")
        window.destroy()


takeImg = tk.Button(window, text="IMAGE CAPTURE BUTTON", command=TakeImages, fg="white", bg="blue", width=25, height=2,
                    activebackground="pink", font=('Times New Roman', 15, ' bold '))
takeImg.place(x=245 - x_cord, y=425 - y_cord)

trainImg = tk.Button(window, text="MODEL TRAINING BUTTON", command=TrainImages, fg="white", bg="blue", width=25,
                     height=2, activebackground="pink", font=('Times New Roman', 15, ' bold '))
trainImg.place(x=645 - x_cord, y=425 - y_cord)

trackImg = tk.Button(window, text="ATTENDANCE MARKING BUTTON", command=TrackImages, fg="white", bg="red", width=30,
                     height=3, activebackground="pink", font=('Times New Roman', 15, ' bold '))
trackImg.place(x=1075 - x_cord, y=412 - y_cord)

quitWindow = tk.Button(window, text="QUIT", command=quit_window, fg="white", bg="red", width=10, height=2,
                       activebackground="pink", font=('Times New Roman', 15, ' bold '))
quitWindow.place(x=700, y=735 - y_cord)

window.mainloop()
