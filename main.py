#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import pylab as lab
MAX_GRAFU = 2

class AppError(Exception):
    def __init__(self, message):
        super().__init__(message)

class App(tk.Tk):
    name = "Graf"
    def __init__(self):
        super().__init__(className=self.name)
        self.title = self.name
        self.config(borderwidth=5)
        self.gui()

        self.pocetgrafu = 0

    def gui(self):
        # Vyber funkce
        self.oknofunkce = tk.LabelFrame(self, text="Matematicke funkce")
        self.oknofunkce.grid(column=1, row=1, padx=10, pady=10)

        self.oknofunkcejmeno = tk.Label(self.oknofunkce)
        self.oknofunkcejmeno.grid(column=1, row=1)

        # Samotny vyber z funkci
        self.vyberfunkce = tk.IntVar()
        self.vyberfunkce.set(1)
        self.funkcesin = tk.Radiobutton(self.oknofunkce, text="Sinus",
                                    variable=self.vyberfunkce, value=1).grid(
                                        column=1, row=1)
        self.funkcecos = tk.Radiobutton(self.oknofunkce, text="Cosin",
                                    variable=self.vyberfunkce, value=2).grid(
                                        column=1, row=2)
        self.funkceexp = tk.Radiobutton(self.oknofunkce, text="Expon",
                                    variable=self.vyberfunkce, value=3).grid(
                                        column=1, row=3)

        # Okna pro od / do
        self.odjmeno = tk.Message(self.oknofunkce, text="Od: ").grid(column=2, row=1)
        #self.odmessage = tk.Message(self.odjmeno, text="Od:").grid(column=1, row=1)
        self.odpromena = tk.StringVar()
        self.odpromena.set("0")
        self.odentry = tk.Entry(self.oknofunkce, textvariable=self.odpromena,
                                    width=10).grid(column=3, row=1, padx=10)

        self.dojmeno = tk.Message(self.oknofunkce, text="Do: ").grid(column=2, row=2)
        #self.odmessage = tk.Message(self.odjmeno, text="Od:").grid(column=1, row=1)
        self.dopromena = tk.StringVar()
        self.dopromena.set("100")
        self.doentry = tk.Entry(self.oknofunkce, textvariable=self.dopromena,
                                    width=10).grid(column=3, row=2, padx=10)

        # Tlacitko pro generovani grafu
        self.udelejgrafbutton = tk.Button(self, text="Vytvor graf",
                                                command=self.udelejgraf("vygenerovat")).grid(
                                                column=2, row=1)

        # Okno pro generovani ze souboru
        self.oknosouboru = tk.LabelFrame(self, text="Nacteni ze souboru")
        self.oknosouboru.grid(column=1, row=2, padx=10, pady=10)

        self.oknosouborujmeno = tk.Label(self.oknosouboru)
        self.oknosouborujmeno.grid(column=1, row=1)

        self.cestapromena = tk.StringVar()
        self.cestaentry = tk.Entry(self.oknosouboru,
                                    textvariable=self.cestapromena).grid(
                                    column=1, row=2, padx=10, pady=10)

        self.vybersouborubutton = tk.Button(self.oknosouboru, text="Vyber soubor",
                                    command=self._vybersoubor).grid(
                                    column=2, row=2, padx=10, pady=10)

        self.grafyesoubbutton = tk.Button(self, text="Vytvor graf",
                                                command=self.udelejgraf("soubor")).grid(
                                                column=2, row=2)

        # Okno pro popisky os
        self.oknoos = tk.LabelFrame(self, text="Popisky os")
        self.oknoos.grid(column=1, row=3, padx=10, pady=10)

        self.oknofunkcejmeno = tk.Label(self.oknoos)
        self.oknofunkcejmeno.grid(column=1, row=1)

        self.popisekx = tk.Label(self.oknoos, text="osa X:").grid(column=1, row=2)
        self.popiseky = tk.Label(self.oknoos, text="osa Y:").grid(column=1, row=3)

        self.osaxvar = tk.StringVar()
        self.osaxvar.set("x")
        self.osayvar = tk.StringVar()
        self.osayvar.set("y")

        self.osaxentry = tk.Entry(self.oknoos, textvariable=self.osaxvar).grid(
                                    column=2, row=2)
        self.osayentry = tk.Entry(self.oknoos, textvariable=self.osayvar).grid(
                                    column=2, row=3)

    def _makeFloat(self, text):
        try:
            return float(text)
        except ValueError:
            raise AppError("Musite napsat cislo")

    def _vybersoubor(self):
        cesta = filedialog.askopenfilename(title="Vyber soubor")
        if cesta:
            self.cestapromena.set(cesta)

    def _kontrolapopisku(self):
        if not(self.osaxvar.get()):
            self.osaxvar.set("x")
        if not(self.osayvar.get()):
            self.osayvar.set("y")

    def nactidata(self, cesta):
        try:
            with open(cesta, "r") as f:
                line = f.readline()
                x, y = [], []
                while line:
                    data = line.split()
                    if len(data) != 2:
                        raise AppError("Data jsou ve spatnem formatu")
                    x.append(float(data[0]))
                    y.append(float(data[1]))
                    line = f.readline()
            return x, y
        except Exception as e:
            raise AppError(str(e))

    def udelejdata(self):
        od = self._makeFloat(self.odpromena.get())
        do = self._makeFloat(self.dopromena.get())
        if od == do:
            raise AppError("Od a do jsou stejna cisla")
        x = lab.linspace(od, do, 500)
        vyber = self.vyberfunkce.get()
        if vyber == 1:
            y = lab.sin(x)
        if vyber == 2:
            y = lab.cos(x)
        if vyber == 3:
            if max(x) > 10000:
                raise AppError("Moc velka cisla")
            y = lab.exp(x)
        return x, y

    def vytvorgraf(self, x, y):
        fig = lab.figure()
        fig.canvas.mpl_connect("close_event", self._zavrenigrafu)
        lab.plot(x, y)
        lab.xlabel(self.osaxvar.get())
        lab.ylabel(self.osayvar.get())
        lab.grid(True)
        self.pocetgrafu += 1
        lab.show()

    def udelejgraf(self, odkud):
        def grafak():
            try:
                if self.pocetgrafu >= MAX_GRAFU:
                    raise AppError("Prekrocen maximalni pocet grafu")
                if odkud == "soubor":
                    x, y = self.nactidata(self.cestapromena.get())
                elif odkud == "vygenerovat":
                    x, y = self.udelejdata()
                self._kontrolapopisku()
                self.vytvorgraf(x, y)
            except AppError as e:
                tk.messagebox.showerror(title="Chyba", message=e)
            else:
                self.destroy()
        return grafak

    def _zavrenigrafu(self, args):
        self.pocetgrafu -= 1

def main():
     app = App()
     app.mainloop()

if __name__ == '__main__':
    main()
