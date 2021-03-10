import subprocess, re, os
from tkinter import*
from tkinter import font
import pyttsx3

cwd = os.path.dirname(os.path.realpath(__file__))

class AlFileUnlatcher():
    
    def __init__(self):
        root = Tk(className = " ALFILEUNLATCHER ")
        root.geometry("400x125+1500+890")
        root.config(bg="#ffe69b")
        color = '#ffe69b'

        def speak(audio):
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(audio)
            engine.runAndWait()

        def find():
            inputFile = fileText.get()
            fileName = os.path.join(cwd+'\AlFileUnlatcher','files_database.lst')
            if os.path.exists(fileName):
                pass
            else:
                dFile = open(fileName, "x")
                dFile.close()
            filesList = []   
            notFoundList = [] 
            dFile = open(fileName,"r")
            for file in dFile:
                file = file.replace('\n','')
                if os.path.basename(file) == inputFile:
                    if os.path.isfile(file):
                        filesList.append(file)
                    else:
                        notFoundList.append(file)
                        del(file)
            dFile.close()
            if (len(filesList) == 0) or (len(notFoundList) != 0 and len(filesList) == 0) or (len(notFoundList) != 0):
                check = subprocess.check_output(f'python {cwd}\AlFileUnlatcher\AlFileSearcher.py "'+inputFile+'"').decode("utf-8").replace('\r\n',',:;')
                output = check.split(',:;')[:-1]
                allFiles = [i + '\n' for i in output]
                dFile = open(fileName,'a')
                dFile.writelines(allFiles)
                dFile.close()
                for file in output:
                    if os.path.basename(file) == inputFile:
                        filesList.append(file)
            if len(filesList) == 0:
                text.delete(1.0, END)
                text.insert(1.0, 'Invalid input file')
                speak('Invalid input file')
            else:
                for file in filesList:
                    directory = os.path.dirname(file)
                    filename = os.path.basename(file)
                    try:
                        text.delete(1.0, END)
                        speak('Opening '+inputFile)
                        text.insert(1.0, 'Opening '+inputFile)
                        os.startfile(os.path.join(directory,filename))
                    except:
                        text.insert(1.0, 'Set a default application to open the input file')
                        speak('Set a default application to open the input file')

        appHighlightFont = font.Font(family='sans-serif', size=12, weight='bold')
        textHighlightFont = font.Font(family='Segoe UI', size=12, weight='bold')

        #file widget
        fileText = Label(root, text="FILE TO BE SEARCHED AND OPENED")
        fileText.pack()
        fileText.config(bg=color,fg="#0078d7",font=textHighlightFont)
        fileText= Entry(root, bg="#0078d7", fg='white', highlightbackground=color, highlightcolor=color, highlightthickness=3, bd=0,font=appHighlightFont)
        fileText.pack(fill=X)

        #submit button
        find = Button(root, borderwidth=0, highlightthickness=3, text="OPEN FILE", command=find)
        find.config(bg=color,fg="#0078d7",font=textHighlightFont)
        find.pack(fill=X)

        text = Text(root, font="sans-serif",  relief=SUNKEN , highlightbackground=color, highlightcolor=color, highlightthickness=5, bd=0)
        text.config(bg="#0078d7", fg='white', height=2, font=appHighlightFont)
        text.pack(fill=BOTH, expand=True)

        root.mainloop()

if __name__ == "__main__":
    AlFileUnlatcher() 