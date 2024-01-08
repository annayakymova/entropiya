from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from Crypto.Cipher import AES
import hashlib
import lab9util

inputFilePath = None
keyFilePath = None
bufferSize = 16

def encrypt():
    global inputFilePath, keyFilePath
    if inputFilePath == None:
        messagebox.showerror("Помилка","Оберіть файл для шифрування")
        return
    if keyFilePath == None:
        messagebox.showerror("Помилка","Оберіть ключовий файл")
        return
    try:
        outputPath = fd.asksaveasfilename(defaultextension=".enc")
        if outputPath != "":
            with open(inputFilePath, "rb") as source, open(outputPath, "wb") as output, open(keyFilePath, "rb") as keyFile:
                encryptionKey = hashlib.shake_256(keyFile.read()).digest(24)
                cipher = AES.new(encryptionKey, AES.MODE_CFB)
                output.write(cipher.iv)
                while True:
                    data = source.read(bufferSize)
                    if not data:
                        break
                    output.write(cipher.encrypt(data))
                messagebox.showinfo("Повідомлення", "Файл зашифровано")
                
    except Exception as e:
        print(e)

def decrypt():
    global inputFilePath, keyFilePath
    if inputFilePath == None:
        messagebox.showerror("Помилка","Оберіть файл для розшифрування")
        return
    if keyFilePath == None:
        messagebox.showerror("Помилка","Оберіть ключовий файл")
        return
    try:
        outputPath = fd.asksaveasfilename()
        if outputPath != "":
            with open(inputFilePath, "rb") as source, open(outputPath, "wb") as output, open(keyFilePath, "rb") as keyFile:
                encryptionKey = hashlib.shake_256(keyFile.read()).digest(24)
                iv = source.read(16)
                cipher = AES.new(encryptionKey, AES.MODE_CFB, iv)
                while True:
                    data = source.read(bufferSize)
                    if not data:
                        break
                    output.write(cipher.decrypt(data))
                messagebox.showinfo("Повідомлення", "Файл розшиврофано")
                
    except Exception as e:
        print(e)

def analyzeFile(path):
    if path == None:
        messagebox.showerror("Помилка", "Оберіть файл!")
        return
    with open(path,"rb") as file:
        data = file.read()
        sequence = lab9util.toBinarySequence(data)
        entropyL2["text"] = "H(A) = " + str(lab9util.testEntropy(sequence))
        
        lab9util.graph1(data, test1OutputGraph)
        lab9util.graph2(sequence, test2OutputGraph, test2OutputL2, test2OutputL3, test2OutputL4)
        lab9util.graph3(sequence, test3OutputGraph, test3OutputL2, test3OutputL3)
def selectFile():
    global inputFilePath
    try:
        path = fd.askopenfilename()
        if path != "":
            inputFilePath = path
            fileSelectB["text"] = inputFilePath
    except Exception as e:
        print(e)
def selectKey():
    global keyFilePath
    try:
        path = fd.askopenfilename()
        if path != "":
            keyFilePath = path
            keySelectB["text"] = keyFilePath
    except Exception as e:
        print(e)

root = Tk()
root.geometry("800x750")

author = Label(root, text="Якимова РЗ-212, варіант 18")
fileSelectFrame = Frame(root)
fileSelectL = Label(fileSelectFrame, text="Файл:", font=("",16))
fileSelectB = Button(fileSelectFrame, text="Обрати файл...", font=("",16))
keySelectFrame = Frame(root)
keySelectL = Label(keySelectFrame, text="Ключ:", font=("",16))
keySelectB = Button(keySelectFrame, text="Обрати файл...", font=("",16))
buttonsFrame = Frame(root)
encryptB = Button(buttonsFrame, text="Зашифрувати", font=("",16))
decryptB = Button(buttonsFrame, text="Розшифрувати", font=("",16))
analyze1B = Button(root, text="Аналіз файлу", font=("",16))
analyze2B = Button(root, text="Аналіз ключа", font=("",16))
entropyL1 = Label(root, font=("",16),text="Інформаційна Ентропія")
entropyL2 = Label(root, font=("",13),text="")
testsFrame = Frame(root,height=400)
test1Frame = Frame(testsFrame)
test1OutputL1 = Label(test1Frame, font=("",16),text="Критерій\nгістограми")
test1OutputGraph = Canvas(test1Frame, width=225, height=225)
test2Frame = Frame(testsFrame)
test2OutputL1 = Label(test2Frame, font=("",16),text="Критерій\nмонотоності")
test2OutputL2 = Label(test2Frame, font=("",13),text="")
test2OutputL3 = Label(test2Frame, font=("",13),text="")
test2OutputGraph = Canvas(test2Frame, width=225, height=225)
test2OutputL4 = Label(test2Frame, font=("",13),text="")
test3Frame = Frame(testsFrame)
test3OutputL1 = Label(test3Frame, font=("",16),text="Критерій\nсерій")
test3OutputL2 = Label(test3Frame, font=("",13),text="")
test3OutputL3 = Label(test3Frame, font=("",13),text="")
test3OutputGraph = Canvas(test3Frame, width=225, height=225)

author.pack(pady=(5,0))
fileSelectFrame.pack(pady=(15,0))
fileSelectL.pack(side=LEFT)
fileSelectB.pack(side=LEFT)
keySelectFrame.pack(pady=(15,0))
keySelectL.pack(side=LEFT)
keySelectB.pack(side=LEFT)
buttonsFrame.pack(pady=(30,0))
encryptB.pack(side=LEFT)
decryptB.pack(side=LEFT, padx=(10,0))
analyze1B.place(anchor=NW,y=230)
analyze2B.place(anchor=NW,y=230,x=150)
entropyL1.pack(pady=(65,0))
entropyL2.pack(pady=(0,0))
testsFrame.pack(pady=(10,0),fill=X)
test1Frame.place(anchor=N,relx=0.5,x=-800/3)
test1OutputL1.pack()
test1OutputGraph.pack()
test2Frame.place(anchor=N,relx=0.5)
test2OutputL1.pack()
test2OutputL2.pack()
test2OutputL3.pack()
test2OutputGraph.pack()
test2OutputL4.pack(pady=(10,0))
test3Frame.place(anchor=N,relx=0.5,x=800/3)
test3OutputL1.pack()
test3OutputL2.pack()
test3OutputL3.pack()
test3OutputGraph.pack()

fileSelectB["command"] = selectFile
keySelectB["command"] = selectKey
encryptB["command"] = encrypt
decryptB["command"] = decrypt
analyze1B["command"] = lambda: analyzeFile(inputFilePath)
analyze2B["command"] = lambda: analyzeFile(keyFilePath)

root.mainloop()