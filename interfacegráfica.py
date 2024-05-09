import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()


class Janela:
    def __init__(self,toplevel):
        self.fr1 = Frame(toplevel)
        self.fr1.pack()




if __name__ == '__main__':
    myapp = App()

    #
    # here are method calls to the window manager class
    #
    myapp.master.title("My Do-Nothing Application")
    myapp.master.maxsize(1000, 400)

    # start the program
    myapp.mainloop()