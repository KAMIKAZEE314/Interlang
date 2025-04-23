import sys
from colorist import Color

OpCodes = ["PUSH", "POP", "ADD", "SUB", "HALT", "READ", "PRINT", "JUMP.EQ.0", "JUMP.GT.0", "JUMP.LT.0", "JUMP.NE.0", "VAR"]
debug = True
Dateipfadabfrage = False

class Stack():
    def __init__(self):
        self.stack = []
        for _ in range(0,64):
            self.stack.append(None)
        self.sp = 0
    def PUSH(self, num):
        try:
            num = int(Variablen.get(num))
        except KeyError:
            num = int(num)
        except ValueError:
            print(f"{Color.RED} ArgumentFehler: die PUSH Anweisung nimmt nur integers!!{Color.OFF}")
            sys.exit()
        self.stack[self.sp] = num
        self.sp += 1
    def POP(self):
        self.sp -= 1
        value = self.stack[self.sp]
        self.stack[self.sp] = None
        return value
    def ADD(self):
        self.PUSH(self.POP() + self.POP())
    def SUB(self):
        self.PUSH(self.POP() - self.POP())
    def READ(self):
        try:
            self.PUSH(int(input(":")))
        except ValueError:
            print(f"{Color.RED}ValueError: READ Anweisung nimmt nur Integers!!{Color.OFF}")
            sys.exit()
    def JUMPEQO(self, input_label):
        try:
            InLabelCode = Labels[input_label]
        except KeyError:
            print(f"{Color.RED}LabelNotFoundError: Label {input_label} gibt es nicht!!{Color.OFF}")
            sys.exit()
        if self.stack[self.sp - 1] == 0:
            for Operation in InLabelCode:
                Operation_ausfueren(*Operation)
    def JUMPGTO(self, input_label):
        try:
            InLabelCode = Labels[input_label]
        except KeyError:
            print(f"{Color.RED}LabelNotFoundError: Label {input_label} gibt es nicht!!{Color.OFF}")
            sys.exit()
        if self.stack[self.sp - 1] > 0:
            for Operation in InLabelCode:
                Operation_ausfueren(*Operation)
    def JUMPLTO(self, input_label):
        try:
            InLabelCode = Labels[input_label]
        except KeyError:
            print(f"{Color.RED}LabelNotFoundError: Label {input_label} gibt es nicht!!{Color.OFF}")
            sys.exit()
        if self.stack[self.sp - 1] < 0:
            for Operation in InLabelCode:
                Operation_ausfueren(*Operation)
    def JUMPNEO(self, input_label):
        try:
            InLabelCode = Labels[input_label]
        except KeyError:
            print(f"{Color.RED}LabelNotFoundError: Label {input_label} gibt es nicht!!{Color.OFF}")
            sys.exit()
        if self.stack[self.sp - 1] != 0:
            for Operation in InLabelCode:
                Operation_ausfueren(*Operation)
        
stack = Stack()

def HALT():
    sys.exit()
def VAR(name, wert):
    Variablen[name] = wert
def PRINT(text):
    try:
        text = Variablen.get(text)
    except KeyError:
        pass
    finally:
        print(text)

DateipfadError = True
while DateipfadError:
    try:
        if Dateipfadabfrage:
            dateipfad = input("Dateipfad:")
        else:
            dateipfad = "/home/linux-lover1/Dokumente/Python/Interlang/programm.txt"

        with open(dateipfad, "r") as datei:
            Zeilen = datei.readlines()
    except FileNotFoundError:
        print("\033[31m" + f"FileNotFoundError: Dateipfad gibt es nicht: {dateipfad}" + "\033[0m")
    else:
        DateipfadError = False
        
if debug:
    print(f"Pure Zeilen:{Zeilen}")

Variablen = {}
Labels = {}
isInLabel = False
Label_kopf = ""
inLabelCode = []
for Zeile in Zeilen:
    Operations_kopf = ""
    Parameter = []
    Operations_teil = ""
    isParameter = False
    isString = False
    isLabelDeclaration = False
    skipLine = False
    for letter in Zeile:
        if letter != " " and letter != "\n" and letter != "\"" and letter != "<" and letter != ">" and letter != "=":
            Operations_teil += letter
        elif letter == " ":
            if not isParameter:
                isParameter = True
                Operations_kopf = Operations_teil
                Operations_teil = ""
            else:
                if Operations_teil != "" and not isString:
                    Parameter.append(Operations_teil)
                    Operations_teil = ""
                elif isString:
                    Operations_teil += " "
        elif letter == "\"":
            if not isString:
                isString = True
            else:
                isString = False
        elif letter == "<":
            if isInLabel:
                print(f"{Color.RED}InvalidTokenError: Invalid Token \"<\"{Color.OFF}")
                sys.exit()
            isInLabel = True
            isLabelDeclaration = True
            Label_kopf = Operations_kopf
            skipLine = True
        elif letter == ">":
            isInLabel = False
            Labels[Label_kopf] = inLabelCode
            skipLine = True
        elif letter == "=":
            Parameter.append(Operations_teil)
            Operations_teil = ""
        elif letter == "\n":
            if isParameter:
                Parameter.append(Operations_teil)
            else:
                Operations_kopf = Operations_teil
            if isInLabel and not isLabelDeclaration:
                inLabelCode.append((Operations_kopf, Parameter))
                skipLine = True
            elif isLabelDeclaration:
                skipLine = True
    
    if skipLine:
        continue
    
    def Operation_ausfueren(kopf, pars):
        if kopf in OpCodes:
            if kopf == "PUSH":
                stack.PUSH(pars[0])
            elif kopf == "POP":
                stack.POP()
            elif kopf == "ADD":
                stack.ADD()
            elif kopf == "SUB":
                stack.SUB()
            elif kopf == "HALT":
                HALT()
            elif kopf == "READ":
                stack.READ()
            elif kopf == "PRINT":
                PRINT(pars[0])
            elif kopf == "JUMP.EQ.0":
                stack.JUMPEQO(pars[0])
            elif kopf == "JUMP.GT.0":
                stack.JUMPGTO(pars[0])
            elif kopf == "JUMP.LT.0":
                stack.JUMPLTO(pars[0])
            elif kopf == "JUMP.NE.0":
                stack.JUMPNEO(pars[0])
            elif kopf == "VAR":
                VAR(pars[0], pars[1])
        else:
            print(f"{Color.RED}OperationsError: Operation {kopf} gibt es nicht{Color.OFF}")
            sys.exit()
    
    Operation_ausfueren(Operations_kopf, Parameter)

if debug:
    print(stack.stack)
