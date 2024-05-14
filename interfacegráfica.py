import customtkinter as ct
from CTkMenuBar import *

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("SADJud")
        w = 1024
        h = 760
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.menu = self.menus()

    def menus(self):
        menu = CTkMenuBar(self)
        btnResFavGov = menu.add_cascade("Resgates a Favor do Estado")
        dropdown1 = CustomDropdownMenu(widget=btnResFavGov)
        dropdown1.add_option(option="Por Data", command=self.rfvPorData)
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Conta Judicial")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Processo Judicial")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por CPF/CNPJ do Reclamante")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por CPF/CNPJ do Reclamado")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por CPF/CNPJ do Reclamante")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Nome do Reclamante")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Nome do Reclamado")
        dropdown1.add_separator()
        btnSair = menu.add_cascade("Sair")
        dropdownsair = CustomDropdownMenu(widget=btnSair)
        dropdownsair.add_option(option="Sobre")
        dropdownsair.add_separator()
        dropdownsair.add_option(option="Sair", command=quit)


    def rfvPorData(self):
        rfvDataWindow  = ct.CTkToplevel(self)
        rfvDataWindow.title("Resgates a Favor do Governo por Data")
        w = 400
        h = 200
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        rfvDataWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
        rfvDataWindow.resizable(False, False)
        label = ct.CTkLabel(rfvDataWindow, text='Data')
        label.place(x = 110, y = 70)
        dataInfo = ct.CTkEntry(rfvDataWindow, placeholder_text='dd/mm/yyyy')
        dataInfo.place(x = 150, y = 70)
        btnExecutar = ct.CTkButton(rfvDataWindow, text='Pesquisar', command=self.pesquisarPorData)
        btnExecutar.place(x = 130, y = 110)

    def pesquisarPorData(self):
        print("Data pressionada")





app = App()
app.mainloop()