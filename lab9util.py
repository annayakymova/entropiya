from tkinter import *
import math

sequenceBase = 2

def toBinarySequence(byteSequence):
    return bin(int(byteSequence.hex(),16))[2:].zfill(8)

def igamc(a,x):
    upperBoundIntegrated = 0
    for i in range(a):
        power = (a-i-1)
        factorial = math.factorial(a-i-1)
        coff = math.factorial(a-1)/(max(1,power)*math.factorial(max(power-1,0)))
        upperBoundIntegrated += x**(a-i-1)*math.factorial(a-i-1)
    upperBound = -math.e**(-x)*upperBoundIntegrated
    lowerBound = -1*(math.factorial(a-1))
    P = 1/math.gamma(a) * (upperBound-lowerBound)
    return 1-P

def erfc(z):
    integral = (math.pi**0.5)/2 - (math.pi**0.5)*math.erf(z)/2
    return 2*integral/(math.pi**0.5)

def testEntropy(sequence):
    zeros = 0
    ones = 0
    length = 0
    for byte in sequence:
        zeros += byte.count("0")
        ones+=byte.count("1")
        length+=len(byte)
    return -zeros/length*math.log2(zeros/length)-ones/length*math.log2(ones/length)

def testRuns(sequence):
    #NIST SP 800-22 2.3
    n = len(sequence)
    pi = sequence.count("1")/n
    totalRuns = 1
    runLength = 1
    runStatistics = {}
    for i in range(n-1):
        if sequence[i:i+1] == sequence[i+1:i+2]:
            runLength += 1
        else:
            totalRuns += 1
            if not runLength in runStatistics:
                runStatistics[runLength] = 0
            runStatistics[runLength] += 1
            runLength = 1
    if not runLength in runStatistics:
        runStatistics[runLength] = 0
    runStatistics[runLength] += 1
    numerator = abs(totalRuns-2*n*pi*(1-pi))
    denominator = 2*math.sqrt(2*n)*pi*(1-pi)
    p = erfc(numerator/denominator)
    return p>=0.01, p, runStatistics

def testSerial(sequence, m=3):
    #NIST SP 800-22 2.11
    augmented = sequence + sequence[:m-1]
    n = len(sequence)
    psis = [0,0,0]
    allPatterns = {}
    for i in range(3,0,-1):
        patterns = {}
        for j in range(0, sequenceBase**(i)):
            patternId = [str(int(j/(sequenceBase**(i-bit-1)))%sequenceBase) for bit in range(i)]
            patternId = ''.join(patternId)
            patterns[patternId] = 0
            for char in range(len(sequence)):
                if augmented[char:char+i] == patternId:
                    patterns[patternId] += 1
            allPatterns[patternId] = patterns[patternId]
        
        psi = (sequenceBase**(i))/n * sum([x**2 for x in patterns.values()]) - n
        psis[3-i] = psi
    
    deltaPsi1 = psis[0] - psis[1]
    deltaPsi2 = psis[0] - 2*psis[1] + psis[2]
    
    p1 = igamc(sequenceBase**(m-2), deltaPsi1/2)
    p2 = igamc(sequenceBase**(m-3), deltaPsi2/2)
    return (p1 >= 0.01 and p2 >= 0.01), (p1,p2), allPatterns

def graph1(data, graph):
    graph.delete("all")
    height = int(graph["height"])
    occurances = [0 for i in range(256)]
    for i in data:
        occurances[i] += 1
    normalized = [i for i in occurances if i > 0]
    sizeRatio = (int(graph["width"])-2)/len(normalized)
    highest = max(normalized)
    for i in range(0,len(normalized)):
        graph.create_rectangle(2+i*sizeRatio,height,1+i*sizeRatio+max(1, sizeRatio),height*(1 - normalized[i]/highest), fill="#3090C0",outline="")

def graph2(sequence, graph, outputL2, outputL3, outputL4):
    success2, p2, stat2 = testRuns(sequence)
    outputL2["text"] = "Успіх" if success2 else "Провал"
    outputL3["text"] = "p=" + str(p2)
    graph.delete("all")
    stat2 = dict(sorted(stat2.items()))
    xSpread = len(stat2)
    ySpread = stat2[1]
    for x,y in stat2.items():
        xSpread = x
        ySpread = max(ySpread, y)
    barGap = max(0, 10 - max(0, xSpread/4-20))
    barWidth = math.ceil(175/xSpread) - barGap
    width = int(graph["width"])
    height = int(graph["height"])
    for i in range(0,5):
        graph.create_text(35,(height-25)*i/5+5,anchor=NE,text=str(int(ySpread*(1-i/5))))
    graph.create_text(35,height-20,text="0")
    if xSpread <= 20:
        for x in range(0,xSpread):
            graph.create_text(45 + (x*(barGap + barWidth) + barWidth/2), height-15, anchor=N,text=str(x+1))
    else:
        for x in range(0, 6):
            graph.create_text(45 + (165*x/5), height-15, anchor=N,text=1 if x == 0 else str(int(x*xSpread/5)))
    for x,y in stat2.items():
        graph.create_rectangle(
            45+(x-1)*(barGap+barWidth),height-15,45+(x-1)*(barGap+barWidth)+barWidth,10+(height-25)*(1 - y/ySpread),
            fill="#3090C0", outline=""
        )
    outputL4["text"] = "Найбільша\nпослідовність: " + str(xSpread)

def graph3(sequence, graph, outputL2, outputL3):
    success3, p3, stat3 = testSerial(sequence)
    outputL2["text"] = "Успіх" if success3 else "Провал"
    outputL3["text"] = "p1=%s\np2=%s" % (p3)
    graph.delete("all")
    xSpread = []
    ySpread = 0
    for x,y in stat3.items():
        xSpread.append(x)
        ySpread = max(ySpread, y)
        if len(xSpread) >= 8:
            break
    barGap = 0
    barWidth = math.ceil(175/len(xSpread)) - barGap
    width = int(graph["width"])
    height = int(graph["height"])
    for i in range(0,5):
        graph.create_text(35,(height-25)*i/5+5,anchor=NE,text=str(int(ySpread*(1-i/5))))
    graph.create_text(35,height-20,text="0")
    for x in range(0,len(xSpread)):
        graph.create_text(45 + (x*(barGap + barWidth) + barWidth/2), height-15, anchor=N,text=xSpread[x])
    for i in range(len(xSpread)):
        x = xSpread[i]
        y = stat3[x]
        graph.create_rectangle(
            45+(i)*(barGap+barWidth),height-15,45+(i)*(barGap+barWidth)+barWidth,10+(height-25)*(1 - y/ySpread),
            fill="#3090C0", outline=""
        )