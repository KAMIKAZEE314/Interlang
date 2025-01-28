import sys

opcodes = ["PUSH","POP","READ","ADD","SUB","PRINT","HALT","JUMP.EQ.0"]
debug = False
Dateipfadabfrage = True

class Stack():
    def __init__(self):
        self.sp = 0
        self.stack = []
        for _ in range(0,64):
            self.stack.append(None)
        self.sp_target = self.stack[self.sp]
    
    def debug(self):
        if debug:
            print(f"pointer:{self.sp}")
            print(f"Wert des Pointers:{self.sp_target}")
            print(f"Stack{self.stack}")
        
    def PUSH(self, raw_number):
        try:
            self.number = int(raw_number)
        except ValueError:
            print("\033[31m" + f"ValueError: Zeile:{jetzige_Zeile + 1} Argument nimmt nur int nicht str" + "\033[0m")
            sys.exit()
        
        self.stack[self.sp] = self.number
        self.sp += 1
    
    def POP(self):
        self.sp -= 1
        self.vorher = self.stack[self.sp]
        self.stack[self.sp] = None
        return self.vorher
    
    def READ(self):
        self.IO = input(":")
        self.PUSH(self.IO)
        
    def ADD(self):
        self.Summand1 = self.POP()
        self.Summand2 = self.POP()
        self.PUSH(self.Summand1 + self.Summand2)
    
    def SUB(self):
        self.Minuend = self.POP()
        self.Subtrahend = self.POP()
        self.PUSH(self.Subtrahend - self.Minuend)
        
def PRINT(string):
    print(string)
    
def HALT():
    sys.exit()
                
stack = Stack()

# Hier werden die Zeilen aus der .txt gespeichert
DateipfadError = True
while DateipfadError:
    try:
        if Dateipfadabfrage:
            dateipfad = input("Dateipfad:")
        else:
            dateipfad = "/home/linux-lover1/Programmiersprache/Test.txt"

        with open(dateipfad, "r") as datei:
            Zeilen = datei.readlines()
    except FileNotFoundError:
        print("\033[31m" + f"FileNotFoundError: Dateipfad gibt es nicht: {dateipfad}" + "\033[0m")
    else:
        DateipfadError = False
        
if debug:
    print(f"Pure Zeilen:{Zeilen}")

# Hier werden die Zeilen zu operationen verarbeitet
Labels = []
operationen = []
Zeilennummer = 1
<<<<<<< HEAD
inLabel = False
inLabelCode = []
=======
>>>>>>> ac0f5c0efbe7c57cfb6f201373b4a41ce9674afa
for Zeile in Zeilen:
    Zeilennummer += 1
    operation = []
    operations_teil = ""
    skipAppend = False
    isString = False
<<<<<<< HEAD
    isLabel = False
    isEndLabel = False
    for letter in Zeile:
        if letter != " " and letter != "\n" and letter != "\"" and letter != ":" and letter != ";":
=======
    for letter in Zeile:
        if letter != " " and letter != "\n" and letter != "\"" and letter != ":":
>>>>>>> ac0f5c0efbe7c57cfb6f201373b4a41ce9674afa
            operations_teil += letter
        elif letter == " ":
            if not isString:
                operation.append(operations_teil)
                operations_teil = ""
            else:
                operations_teil += " "
        elif letter == "\"":
            if isString:
                isString = False
            else:
                isString = True
        elif letter == ":":
<<<<<<< HEAD
            if not inLabel:
                Labels.append([Zeilennummer,operations_teil])
                inLabel = True
                isLabel = True
        elif letter == ";":
            if not inLabel:
                print("\033[31m" + f"LabelEndError: Zeile:{Zeilennummer} Label wurde beendet, aber nicht gestartet" + "\033[0m")
            else:
                isEndLabel = True
                isLabel = True
                for Label in Labels:
                    [Zeilenangabe, Labelname] = Label
                    if Labelname == operations_teil:
                        Label.append(inLabelCode)
        elif letter == "\n":
            if Zeile != "\n" and not inLabel:
                operation.append(operations_teil)          
            elif Zeile == "\n":
                skipAppend = True
            elif inLabel:
                if not isLabel:
                    operation.append(operations_teil)
                else:
                    pass
                skipAppend = True
            break
    if not skipAppend and not isLabel:
        operationen.append(operation)
    elif inLabel and not isLabel:
        inLabelCode.append(operation)
        print(f"Operations teil:{operations_teil}")
        print(f"Operation:{operation}")
        print(f"Lablel Code:{inLabelCode}")
=======
            Labels.append([Zeilennummer,operations_teil])
            skipAppend = True
        elif letter == "\n":
            if not Zeile == "\n":
                operation.append(operations_teil)          
            else:
                skipAppend = True
            break
    if not skipAppend:
        operationen.append(operation)
>>>>>>> ac0f5c0efbe7c57cfb6f201373b4a41ce9674afa

if debug:
    print(f"Operationen:{operationen}")
    print(f"Labels:{Labels}")
    
# Hier werden die Operationen ausgefürt
jetzige_Zeile = 0
while jetzige_Zeile <= len(operationen) - 1:
    operation = operationen[jetzige_Zeile]
    operations_teil = operation[0]
    if not operations_teil in opcodes:
        print("\033[31m" + f"OperationError: Zeile:{jetzige_Zeile + 1} Operation {operations_teil} gibt es nicht" + "\033[0m")
    elif operations_teil == "PUSH":
        stack.PUSH(operation[1])
    elif operations_teil == "POP":
        stack.POP()
    elif operations_teil == "READ":
        stack.READ()
    elif operations_teil == "ADD":
        stack.ADD()
    elif operations_teil == "SUB":
        stack.SUB()
    elif operations_teil == "PRINT":
        PRINT(operation[1])
    elif operations_teil == "HALT":
        HALT()
    jetzige_Zeile += 1

stack.debug()
