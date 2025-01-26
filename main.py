class Stack():
    def __init__(self):
        self.sp = 0
        self.Stack = []
        for _ in range(0,64):
            self.Stack.append(None)
        self.sp_value = self.Stack[self.sp]
    def debug(self):
        print(f"pointer:{self.sp}")
        print(f"Wert des Pointers:{self.sp_value}")
        
Stapel = Stack()
Stack.debug(Stapel)