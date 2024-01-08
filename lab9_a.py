from tkinter import *
from tkinter import filedialog as fd
import lab9util

inputFilePath = None

def selectFile():
    global inputFilePath
    try:
        path = fd.askopenfilename()
        if path != "":
            inputFilePath = path
            fileSelectB["text"] = inputFilePath
            with open(inputFilePath, "rb") as file:
                data = file.read()
                sequence = lab9util.toBinarySequence(data)
                entropyL2["text"] = "H(A) = " + str(lab9util.testEntropy(sequence))
                lab9util.graph1(data, test1OutputGraph)
                lab9util.graph2(sequence, test2OutputGraph, test2OutputL2, test2OutputL3, test2OutputL4)
                lab9util.graph3(sequence, test3OutputGraph, test3OutputL2, test3OutputL3)
    except Exception as e:
        print(e)

root = Tk()
root.geometry("800x600")

author = Label(root, text="Якимова РЗ-212, варіант 18")
fileSelectFrame = Frame(root)
fileSelectL = Label(fileSelectFrame, text="Файл:", font=("",16))
fileSelectB = Button(fileSelectFrame, text="Обрати файл...", font=("",16))
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
entropyL1.pack(pady=(40,0))
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

root.mainloop()