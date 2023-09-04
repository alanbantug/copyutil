import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import os
import shutil

from time import time
import subprocess as sp

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()
        self.copied = IntVar()
        self.copying = 0
        self.source = ""
        self.target = ""
        self.script = ""
        self.allSet = True
        self.newFiles = IntVar()
        self.initFolders = IntVar()
        self.build = IntVar()

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", background="white", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width='46')
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TCheckButton", font="Verdana 8")

        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        # Create widgets
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="COPY FILE UTILITY", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="Copies python files from a source folder to a target folder. The source files ", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="that are new (not in the target folder) or updated will be listed, and user   ", style="S.TLabel" )
        self.subLabelC = Label(self.main_container, text="can select which of them to copy. This will simplify the folder backup,", style="S.TLabel" )
        self.subLabelD = Label(self.main_container, text="resulting in quicker turn around times.", style="S.TLabel" )

        self.sourceTarget = LabelFrame(self.main_container, text=' Source - Target Options ', style="O.TLabelframe")
        self.selectSource = Button(self.sourceTarget, text="SOURCE FOLDER", style="B.TButton", command=self.setSource)
        self.sourceLabel = Label(self.sourceTarget, text="None", style="B.TLabel" )
        self.sourceFiles = LabelFrame(self.sourceTarget, text=' Select files to copy', style="O.TLabelframe")
        self.fscroller = Scrollbar(self.sourceFiles, orient=VERTICAL)
        self.fileList = Listbox(self.sourceFiles, yscrollcommand=self.fscroller.set, selectmode='multiple', width=67, height=6)
        self.selectTarget = Button(self.sourceTarget, text="TARGET FOLDER", style="B.TButton", command=self.setTarget)
        self.targetLabel = Label(self.sourceTarget, text="None", style="B.TLabel" )
        self.newFilesOnly = Checkbutton(self.sourceTarget, text="New files only", style="B.TCheckbutton", variable=self.newFiles)
        self.getFiles = Button(self.sourceTarget, text="SHOW SOURCE FILES TO COPY", style="B.TButton", command=self.getSourceFiles)

        self.clearFolders = Checkbutton(self.main_container, text="Clear Folders", style="B.TCheckbutton", variable=self.initFolders)
        self.createScript = Checkbutton(self.main_container, text="Build Script", style="B.TCheckbutton", variable=self.build)
        self.sep_s = Separator(self.sourceTarget, orient=HORIZONTAL)
        self.sep_t = Separator(self.sourceTarget, orient=HORIZONTAL)

        self.submit = Button(self.main_container, text="COPY", style="B.TButton", command=self.startProcess)
        self.reset = Button(self.main_container, text="RESET", style="B.TButton", command=self.resetProcess)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)

        # Position widgets
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelD.grid(row=4, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_a.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.selectSource.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.sourceLabel.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.sep_s.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.selectTarget.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')
        self.targetLabel.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.newFilesOnly.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.sep_t.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.fileList.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.fscroller.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.sourceFiles.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.getFiles.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sourceTarget.grid(row=8, column=0, columnspan=3, rowspan=5, padx=5, pady=5, sticky='NSEW')

        self.submit.grid(row=14, column=0, columnspan=1, padx=5, pady=0, sticky='NSEW')
        self.reset.grid(row=14, column=1, padx=5, pady=0, sticky='NSEW')
        self.exit.grid(row=14, column=2, padx=5, pady=0, sticky='NSEW')
        self.sep_d.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.progress_bar.grid(row=18, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.newFiles.set(0)
        self.initFolders.set(0)
        self.build.set(0)

    def setSource(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.sourceLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
            self.source = pathname


    def setTarget(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.targetLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
            self.target = pathname

    def getSourceFiles(self):

        if not self.checkFolders():
            return

        for folder, subs, files in os.walk(self.target):
            targetFiles = files
            print(targetFiles)

        self.fileList.delete(0, END)

        to_copy = 0

        for folder, subs, files in os.walk(self.source):

            for file in files:
                if file in targetFiles:
                    pass 
                else:
                    self.fileList.insert(END, file)
                    to_copy += 1
        
        if to_copy == 0:
            messagebox.showwarning('No Files', 'All source files in target folder. No files to copy.')

        self.fscroller.config(command=self.fileList.yview)


    # def setScript(self):

    #     pathname = askdirectory()

    #     if os.path.isdir(pathname):
    #         self.scriptLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
    #         self.script = pathname


    def startProcess(self):

        if not self.checkFolders():
            return

        files_to_copy = [self.fileList.get(i) for i in self.fileList.curselection()]

        if files_to_copy:
            pass 
        else:
            messagebox.showerror("No files selected", "No source files selected.")
            return False

        self.processControl(1)
        copied = 0 

        for folder, subs, fileNames in os.walk(self.source):

            for file in fileNames:
                if file in files_to_copy:
                    shutil.copy(os.path.join(folder, file), self.target)                        
                    copied += 1

        self.processControl(0)
        self.getSourceFiles()
        messagebox.showinfo("Files copied", f"{copied} files copied to target folder.")
        
        
        

        # if self.submit["text"] == "START":
        #     self.checkFolders()

        #     if self.allSet:
        #         self.submit["text"] = "PROCESS"
        #         self.reset["state"] = "DISABLED"
        #         # self.statusLabel["text"] = "Click PROCESS to start or RESTART to change settings"

        # else:
        #     self.checkFolders()

        #     if self.allSet:
        #         self.processRequest()


    def checkFolders(self):

        if self.source == "":
            messagebox.showerror("Source not selected", "Source folder not yet selected.")
            return False

        if self.target == "":
            messagebox.showerror("Target not selected", "Target folder not yet selected.")
            return False

        if len(os.listdir(self.source)) == 0:
            messagebox.showerror("Source empty", "Source folder is empty.")
            return False

        return True

    def processControl(self, mode):

        if mode:
            self.progress_bar.start()

            # disable all buttons

            self.selectSource["state"] = DISABLED
            self.selectTarget["state"] = DISABLED
            self.getFiles["state"] = DISABLED
            self.reset["state"] = DISABLED
            self.submit["state"] = DISABLED
            self.exit["state"] = DISABLED

        else:
            self.progress_bar.stop()
            
            # enable all buttons

            self.selectSource["state"] = NORMAL
            self.selectTarget["state"] = NORMAL
            self.getFiles["state"] = NORMAL
            self.reset["state"] = NORMAL
            self.submit["state"] = NORMAL
            self.exit["state"] = NORMAL


    def copyFiles(self):

        self.progress_bar.start()
        self.copying = 0

        # get start time

        t0 = time()

        # disable all buttons

        self.selectSource["state"] = DISABLED
        self.selectTarget["state"] = DISABLED
        self.getFiles["state"] = DISABLED
        self.reset["state"] = DISABLED
        self.submit["state"] = DISABLED
        self.exit["state"] = DISABLED

        # if self.initFiles.get() == 1:

        #     # Target folder will be initialized to ensure that it has same structure as source
        #     for folderName, subFolders, fileNames in os.walk(self.target):

        #         # Delete all files first
        #         for file in fileNames:
        #             os.remove(os.path.join(folderName, file))

        # if self.initFolders.get() == 1:

        #     for folderName, subFolders, fileNames in os.walk(self.target, topdown=False):

        #         # Delete all folders in target folder next
        #         for folder in subFolders:
        #             os.rmdir(os.path.join(folderName, folder))


        # if self.build.get() == 1:

        #     self.buildScript()


        # # Walk thru the source folder, creating subfolders and copying files into the target folder

        # for folderName, subFolders, fileNames in os.walk(self.source):

        #     for files in fileNames:

        #         if files[-3:] == '.py':

        #             sub = os.path.relpath(folderName, self.source)

        #             # Check if the subfolder already exists in the target folder and create it if it is not

        #             if sub != ".":
        #                 if os.path.exists(os.path.join(self.target, sub)):
        #                     pass
        #                 else:
        #                     os.chdir(self.target)
        #                     os.makedirs(sub)

        #             shutil.copy(os.path.join(folderName, files), os.path.join(self.target, sub))
        #             self.copying += 1

        self.selectSource["state"] = NORMAL
        self.selectTarget["state"] = NORMAL
        self.getFiles["state"] = NORMAL
        self.reset["state"] = NORMAL
        self.submit["state"] = NORMAL
        self.exit["state"] = NORMAL

        self.progress_bar.stop()
        # self.statusLabel["text"] = str(self.copying) + " file(s) copied successfully in %0.1fs." % (time() - t0)


    # def buildScript(self):

    #     scriptFile = open("script.bat", "w")

    #     script_line = 'Attention! Delete this line and others that are not needed for the script to run'
    #     scriptFile.write(script_line)
    #     scriptFile.write("\n")

    #     for folderName, subFolders, fileNames in os.walk(self.source):

    #         for files in fileNames:

    #             if files[-3:] == '.py':

    #                 script_line = '@pyw ' + self.target.lower() + '/' + files + ' %*'
    #                 scriptFile.write(script_line)
    #                 scriptFile.write("\n")

    #     scriptFile.close()

    #     sp.Popen(["notepad.exe", "script.bat"])


    def resetProcess(self):
        # Launch notepad to show status of last copy request

        os.chdir(self.origin)
        self.sourceLabel["text"] = "None"
        self.targetLabel["text"] = "None"
        
        self.fileList.delete(0, END)
        
        # self.initFiles.set(0)
        # self.initFolders.set(0)
        # self.build.set(0)
        self.source = ""
        self.target = ""


root = Tk()
root.title("COPY FILE UTILITY")

# Set size

wh = 510
ww = 480

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
