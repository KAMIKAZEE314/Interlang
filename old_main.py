import sys
stack = [0] #erstellt den stack
opcodes = ["PUSH","POP","ADD","SUB","PRINT","READ","JUMP.EQ.0","JUMP.GT.0","HALT"]
dateipfad = "Test.txt" #speichert den Dateipfad in einer Variable
Debug = True

stack.pop() #löscht die erste 0 im stack

def PUSH(number): #PUSH anweisung wird erstellt
    stack.append(number)
    
def POP():
    Wert = stack[len(stack) - 1]
    stack.pop()
    return Wert

def ADD():
    Wert1 = POP()
    Wert2 = POP()
    PUSH(int(Wert1) + int(Wert2))
    
def SUB():
    Wert1 = POP()
    Wert2 = POP()
    PUSH(int(Wert2) - int(Wert1))
    
def PRINT(string):
    print(string)
    
def READ():
    IO = input(":")
    PUSH(IO)
    
def JUMPEQO(label_unprocessed):
    if stack[len(stack) - 1] == 0:
        labelHere = False
        for Label in Labels:
            (zeilenangabe,Labelname,code) = Label
            label = f"/{label_unprocessed}/"
            if Labelname == label:
                labelHere = True
                break
        if labelHere:
            for operation in code:
                operations_teil = operation[0]
                if not operations_teil in opcodes:
                    print("Falsche Operation!")
                    break
                elif operations_teil == "PUSH":
                    PUSH(operation[1])
                elif operations_teil == "POP":
                    POP()
                elif operations_teil == "ADD":
                    ADD()
                elif operations_teil == "SUB":
                    SUB()
                elif operations_teil == "PRINT":
                    PRINT(operation[1])
                elif operations_teil == "READ":
                    READ()
                elif operations_teil == "JUMP.EQ.0":
                    JUMPEQO(operation[1])
                elif operations_teil == "JUMP.GT.0":
                    JUMPGTO(operation[1])
                elif operations_teil == "HALT":
                    HALT()

def JUMPGTO(label_unprocessed):
    if stack[len(stack) - 1] > 0:
        labelHere = False
        for Label in Labels:
            (zeilenangabe,Labelname,code) = Label
            label = f"/{label_unprocessed}/"
            if Labelname == label:
                labelHere = True
                break
        if labelHere:
            for operation in code:
                operations_teil = operation[0]
                if not operations_teil in opcodes:
                    print("Falsche Operation!")
                    break
                elif operations_teil == "PUSH":
                    PUSH(operation[1])
                elif operations_teil == "POP":
                    POP()
                elif operations_teil == "ADD":
                    ADD()
                elif operations_teil == "SUB":
                    SUB()
                elif operations_teil == "PRINT":
                    PRINT(operation[1])
                elif operations_teil == "READ":
                    READ()
                elif operations_teil == "JUMP.EQ.0":
                    JUMPEQO(operation[1])
                elif operations_teil == "JUMP.GT.0":
                    JUMPGTO(operation[1])
                elif operations_teil == "HALT":
                    HALT()
                    
def HALT():
    sys.exit()
                    
with open(dateipfad, "r") as datei: #öffnet diesen Dateipfad mit Lese-berechtigung
    Zeilen_raw = datei.readlines() #speichert die Zeilen in einer Liste

if Debug:
    print(Zeilen_raw) #DEBUGGING: gibt die Liste aus

Zeilen = []
Labels = []
Zeilenangabe = 0
inLabel = False
inLabelCode = []
inLabelCodeOperation = []
for Zeile in Zeilen_raw:
    operation = []
    operations_teil = ""
    Zeilenangabe += 1
    inString = False
    label = False
    for letter in Zeile:
        if letter != " " and letter != ";" and letter != "/" and letter != "\\" and letter != "\"":
            operations_teil += letter
        elif letter == " ":
            if not inLabel and not inString:
                operation.append(operations_teil)
                operations_teil = ""
            elif inLabel:
                inLabelCodeOperation.append(operations_teil)
                operations_teil = ""
            elif inString:
                operations_teil += " "
        elif letter == "/":
            label = True
            inLabel = True
            if "/" in operations_teil:
                operations_teil += letter
                Labels.append([Zeilenangabe,operations_teil])
                break
            else:
                operations_teil += letter
        elif letter == "\\": #TO-DO: End LAbel fertig machen sowie der JUMP.EQ.0 command
            inLabel = False
            if "\\" in operations_teil:
                label = Labels[len(Labels) - 1]
                label.append(inLabelCode)
                inLabelCode = []
            else:
                operations_teil += "\\"
        elif letter == "\"":
            if inString:
                inString = False
            else:
                inString = True
        elif letter == ";":
            if not inLabel:
                operation.append(operations_teil)
            else:
                inLabelCodeOperation.append(operations_teil)
                inLabelCode.append(inLabelCodeOperation)
            break
    if not label: 
        Zeilen.append(operation)
    if not Zeilen[len(Zeilen) - 1]:
        
if Debug:
    print(Zeilen)

jetzigeZeile = 0
while jetzigeZeile <= len(Zeilen) - 1:
    operation = Zeilen[jetzigeZeile]
    operations_teil = operation[0]
    if not operations_teil in opcodes:
        print("Falsche Operation!")
        break
    elif operations_teil == "PUSH":PUSH(operation[1])
    elif operations_teil == "POP":POP()
    elif operations_teil == "ADD":ADD()
    elif operations_teil == "SUB":SUB()
    elif operations_teil == "PRINT":PRINT(operation)
    elif operations_teil == "READ":READ()
    elif operations_teil == "JUMP.EQ.0":JUMPEQO(operation[1])
    elif operations_teil == "JUMP.GT.0":JUMPGTO(operation[1])
    elif operations_teil == "HALT":HAlT()
    jetzigeZeile += 1

if Debug:
    print(stack)
    print(Labels)