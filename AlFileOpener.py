import subprocess, re, os
from tkinter import*
from tkinter import font
import pyttsx3

class AlFileOpener():
    
    def __init__(self):
        root = Tk(className = " AlFileOpener ")
        root.geometry("400x125+1500+890")
        root.config(bg="#f0ce69")
        color = '#f0ce69'

        def speak(audio):
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(audio)
            engine.runAndWait()

        def find():
            inputFile = fileText.get()
            fileName = './AlFileOpener/files_database.lst'
            if os.path.exists(fileName):
                pass
            else:
                dFile = open(fileName, "x")
                dFile.close()
            filesList=[]    
            dFile = open(fileName,"r")
            for file in dFile:
                file = file.replace('\n','')
                if os.path.basename(file) == inputFile:
                    filesList.append(file)
            dFile.close()
            if not filesList:
                check = subprocess.check_output('python ./AlFileOpener/AlFileSearcher.py "'+inputFile+'"').decode("utf-8").replace('\r\n',',:;')
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
        textHighlightFont = font.Font(family='LEMON MILK', size=10, weight='bold')

        #file widget
        fileText = Label(root, text="File to be searched and opened")
        fileText.pack()
        fileText.config(bg=color,fg="#0474d4",font=textHighlightFont)
        fileText= Entry(root, bg="white", fg='black', highlightbackground=color, highlightcolor=color, highlightthickness=3, bd=0,font=appHighlightFont)
        fileText.pack(fill=X)

        #submit button
        find = Button(root, borderwidth=0, highlightthickness=3, text="Open file", command=find)
        find.config(bg=color,fg="#0474d4",font=textHighlightFont)
        find.pack(fill=X)

        text = Text(root, font="sans-serif",  relief=SUNKEN , highlightbackground=color, highlightcolor=color, highlightthickness=5, bd=0)
        text.config(bg="white", fg='black', height=2, font=appHighlightFont)
        text.pack(fill=BOTH, expand=True)

        root.mainloop()

if __name__ == "__main__":
    AlFileOpener() 