import sys

opcodes = ["PUSH","POP","READ","ADD","SUB","PRINT","HALT","JUMP.EQ.0","JUMP.GT.0"]
debug = True
Dateipfadabfrage = False

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
        LoopFinished = True
        for Variable in Variablen:
            [Variablenname, Variablenwert] = Variable
            if Variablenname == raw_number:
                LoopFinished = False
                try:
                    self.stack[self.sp] = int(Variablenwert)
                except ValueError:
                    print("\033[31m" + f"ValueError: Zeile:{jetzige_Zeile + 1} Argument nimmt nur int nicht str" + "\033[0m")
                    sys.exit()
                else:
                    self.sp += 1
                break
        if LoopFinished:
            try:
                self.number = int(raw_number)
            except ValueError:
                print("\033[31m" + f"ValueError: Zeile:{jetzige_Zeile + 1} Argument nimmt nur int nicht str" + "\033[0m")
                sys.exit()
            else:
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
        
    def JUMPEQO(self, zielLabelname):
        LabelHere = False
        Wert1 = self.stack[self.sp - 1]
        if Wert1 == 0:
            for Label in Labels:
                [Zeilenangabe, Labelname, LabelCode] = Label
                if Labelname == zielLabelname:
                    LabelHere = True
                    break
            if not LabelHere:
                print("\033[31m" + f"LabelNotFoundError: Zeile:{jetzige_Zeile} Label \"{zielLabelname}\" gibt es nicht" + "\033[0m")
            Operationen_ausführen(LabelCode)
            
    def JUMPGTO(self, zielLabelname):
        LabelHere = False
        Wert1 = self.stack[self.sp - 1]
        if Wert1 >= 0:
            for Label in Labels:
                [Zeilenangabe, Labelname, LabelCode] = Label
                if Labelname == zielLabelname:
                    LabelHere = True
                    break
            if not LabelHere:
                print("\033[31m" + f"LabelNotFoundError: Zeile:{jetzige_Zeile} Label \"{zielLabelname}\" gibt es nicht" + "\033[0m")
            Operationen_ausführen(LabelCode)
        
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
Variablen = []
Zeilennummer = 1
inLabel = False
inLabelCode = []
for Zeile in Zeilen:
    Variable = []
    Zeilennummer += 1
    operation = []
    operations_teil = ""
    skipAppend = False
    isString = False
    isLabel = False
    isEndLabel = False
    isVariable = False
    for letter in Zeile:
        if letter != " " and letter != "\n" and letter != "\"" and letter != ":" and letter != ";" and letter != "=":
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
        elif letter == "=":
            if isVariable:
                print("\033[31m" + f"VariablenDeklarierError: Zeile:{Zeilennummer} \"{letter}\" ist an der falschen Stelle" + "\033[0m")
            else:
                isVariable = True
                Variable.append(operations_teil)
                operations_teil = ""
        elif letter == "\n":
            if Zeile != "\n" and not inLabel and not isVariable:
                operation.append(operations_teil)          
            elif Zeile == "\n":
                skipAppend = True
            elif inLabel:
                if not isLabel:
                    operation.append(operations_teil)
                else:
                    pass
                skipAppend = True
            elif isVariable:
                Variable.append(operations_teil)
            break
    if not skipAppend and not isLabel and not isVariable:
        operationen.append(operation)
    elif inLabel and not isLabel:
        inLabelCode.append(operation)
        if debug:
            print(f"Operations teil:{operations_teil}")
            print(f"Operation:{operation}")
            print(f"Label Code:{inLabelCode}")
    elif isVariable:
        Variablen.append(Variable)
        if debug:
            print(f"Variablen:{Variablen}")

if debug:
    print(f"Operationen:{operationen}")
    print(f"Labels:{Labels}")
    
# Hier werden die Operationen ausgefürt
def Operationen_ausführen(operationen):
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
        elif operations_teil == "JUMP.EQ.0":
            stack.JUMPEQO(operation[1])
        elif operations_teil == "JUMP.GT.0":
            stack.JUMPGTO(operation[1])
        jetzige_Zeile += 1
        
Operationen_ausführen(operationen)

stack.debug()
