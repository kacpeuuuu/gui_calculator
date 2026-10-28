import math
import tkinter as tk
from tkinter import messagebox

def oblicz(arg1, znak, arg2):
    arg1 = float(arg1)
    arg2 = float(arg2)
    if znak == "+":
        return arg1 + arg2
    elif znak == "-":
        return arg1 - arg2
    elif znak == "/":
        if arg2 == 0:
            raise Exception("Dzielenie przez zero!")
        return arg1 / arg2
    elif znak == "*":
        return arg1 * arg2
    elif znak == "^":
        return arg1 ** arg2
    elif znak == "sqrt":
        if arg1 < 0:
            raise Exception("Pierwiastek z liczby ujemnej!")
        return math.sqrt(arg1)  # arg2 to 0
    raise Exception("NIEZNANY SYMBOL")

def sprawdz_znak(znak):
    if len(znak) > 1:
        znak = znak.replace(".", "")
        if znak[0] == "-":
            znak = znak[1:]
            return str(znak).isdigit()
        return str(znak).isdigit()
    else:
        return str(znak).isdigit()

def odwrocona_notacja_polska(wejscie_tekst):
    wejscie = wejscie_tekst.strip().split(" ")
    wejscie = [x for x in wejscie if x != ""] #znaki biale

    if not wejscie:
        raise Exception("PUSTE WEJSCIE")

    stos = []
    wyjscie = []
    idx = 0
    while idx < len(wejscie):
        znak = wejscie[idx]
        if sprawdz_znak(znak):
            wyjscie.append(float(znak))
        else:
            stos.append(znak)

        # jednoargumentowe
        if "sqrt" in stos:
            if len(wyjscie) < 1:
                raise Exception("ZA MALO CYFR NA WEJSCIU")
            wynik = oblicz(wyjscie[-1], stos[0], 0)
            stos.pop(0)
            wyjscie.pop(-1)
            wyjscie.append(wynik)

        # dwuargumentowe
        elif stos != []:
            if len(wyjscie) < 2:
                pass
            else:
                print(wyjscie)
                print(stos)
                wynik = oblicz(wyjscie[-2], stos[0], wyjscie[-1])
                wyjscie.pop(-1)
                wyjscie.pop(-1)
                stos.pop(0)
                wyjscie.append(wynik)

        idx += 1

    if stos != []:
        raise Exception("NIEWYKORZYSTANE OPERATORY")

    if len(wyjscie) > 1:
        raise Exception("ZA DUZO WARTOSCI NA KONCU DZIALAN")

    if len(wyjscie) == 0:
        raise Exception("BRAK WYNIKU")

    return wyjscie[-1]


PRIORYTET = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "sqrt": 4}

def postac_infiksowa_na_onp(wyrazenie):
    wyjscie = []
    stos = []
    for t in wyrazenie.split():
        if sprawdz_znak(t):
            wyjscie.append(t)
        elif t == "(" or t == "sqrt":
            stos.append(t)
        elif t == ")":
            while stos and stos[-1] != "(":
                wyjscie.append(stos.pop())
            if not stos:
                raise Exception("BRAK NAWIASU (")
            stos.pop()  
        elif t in PRIORYTET:
            #dzialania wykonac zgodzie z kolejnoscia 
            prog = PRIORYTET[t]
            if t == "^":
                prog += 1 
            while stos and stos[-1] in PRIORYTET and PRIORYTET[stos[-1]] >= prog:
                wyjscie.append(stos.pop())
            stos.append(t)
        else:
            raise Exception("NIEZNANY SYMBOL: " + t)
    if "(" in stos:
        raise Exception("BRAK NAWIASU )")
    while stos:
        wyjscie.append(stos.pop())
    return " ".join(wyjscie)


def onp_na_infiks(tekst):
    stos = []
    for t in tekst.split():
        if sprawdz_znak(t):
            stos.append(t) #liczba -> stos
        elif t == "sqrt":
            if len(stos) < 1:
                raise Exception("ZA MALO LICZB")
            a = stos.pop()
            stos.append("sqrt ( " + a + " )")
        elif t in ["+", "-", "*", "/", "^"]:
            if len(stos) < 2:
                raise Exception("ZA MALO LICZB")
            b = stos.pop() #x1[-1]
            a = stos.pop() #x2[-2]   
            stos.append("( " + a + " " + t + " " + b + " )")
        else:
            raise Exception("NIEZNANY SYMBOL: " + t)
    if len(stos) != 1:
        raise Exception("BLAD W ONP")
    wynik = stos[0]
    if wynik.startswith("( "):
        wynik = wynik[2:-2] # zewnetrzne nawiasy sa bezuzyyteczne
    return wynik

def formatuj(liczba):
    liczba = round(liczba, 10)
    return str(int(liczba)) if liczba == int(liczba) else str(liczba)

class KalkulatorONP:
    def __init__(self, root):
        root.title("Kalkulator ONP")
        root.resizable(False, False)
        self.entry = tk.Entry(root, width=10, font=("Arial", 14), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 2), sticky="we")
        self.historia = tk.Text(root, width=10, height=5, font=("Arial", 9), state="disabled")
        self.historia.grid(row=1, column=0, columnspan=4, padx=10, pady=(2, 10), sticky="we")

        #w 2
        tk.Button(root, text="C", width=8, height=2, bg="lightcoral", command=self.czysc).grid(row=2, column=0, padx=2, pady=2)
        tk.Button(root, text="<-", width=8, height=2, bg="lightcoral", command=self.cofnij).grid(row=2, column=1, padx=2, pady=2)
        tk.Button(root, text="(", width=8, height=2, bg="lightgray", command=lambda: self.dopisz("( ")).grid(row=2, column=2, padx=2, pady=2)
        tk.Button(root, text=")", width=8, height=2, bg="lightgray", command=lambda: self.dopisz(" )")).grid(row=2, column=3, padx=2, pady=2)

        #w 3
        tk.Button(root, text="7", width=8, height=2, bg="white", command=lambda: self.dopisz("7")).grid(row=3, column=0, padx=2, pady=2)
        tk.Button(root, text="8", width=8, height=2, bg="white", command=lambda: self.dopisz("8")).grid(row=3, column=1, padx=2, pady=2)
        tk.Button(root, text="9", width=8, height=2, bg="white", command=lambda: self.dopisz("9")).grid(row=3, column=2, padx=2, pady=2)
        tk.Button(root, text="/", width=8, height=2, bg="lightgray", command=lambda: self.dopisz(" / ")).grid(row=3, column=3, padx=2, pady=2)

        #w 4
        tk.Button(root, text="4", width=8, height=2, bg="white", command=lambda: self.dopisz("4")).grid(row=4, column=0, padx=2, pady=2)
        tk.Button(root, text="5", width=8, height=2, bg="white", command=lambda: self.dopisz("5")).grid(row=4, column=1, padx=2, pady=2)
        tk.Button(root, text="6", width=8, height=2, bg="white", command=lambda: self.dopisz("6")).grid(row=4, column=2, padx=2, pady=2)
        tk.Button(root, text="*", width=8, height=2, bg="lightgray", command=lambda: self.dopisz(" * ")).grid(row=4, column=3, padx=2, pady=2)

        #w 5
        tk.Button(root, text="1", width=8, height=2, bg="white", command=lambda: self.dopisz("1")).grid(row=5, column=0, padx=2, pady=2)
        tk.Button(root, text="2", width=8, height=2, bg="white", command=lambda: self.dopisz("2")).grid(row=5, column=1, padx=2, pady=2)
        tk.Button(root, text="3", width=8, height=2, bg="white", command=lambda: self.dopisz("3")).grid(row=5, column=2, padx=2, pady=2)
        tk.Button(root, text="-", width=8, height=2, bg="lightgray", command=self.minus).grid(row=5, column=3, padx=2, pady=2)

        #w 6
        tk.Button(root, text="0", width=8, height=2, bg="white", command=lambda: self.dopisz("0")).grid(row=6, column=0, padx=2, pady=2)
        tk.Button(root, text=".", width=8, height=2, bg="white", command=lambda: self.dopisz(".")).grid(row=6, column=1, padx=2, pady=2)
        tk.Button(root, text="^", width=8, height=2, bg="lightgray", command=lambda: self.dopisz(" ^ ")).grid(row=6, column=2, padx=2, pady=2)
        tk.Button(root, text="+", width=8, height=2, bg="lightgray", command=lambda: self.dopisz(" + ")).grid(row=6, column=3, padx=2, pady=2)

        #w 7
        tk.Button(root, text="sqrt", width=8, height=2, bg="lightgray", command=lambda: self.dopisz(" sqrt ")).grid(row=7, column=0, padx=2, pady=2)
        tk.Button(root, text="->ONP", width=8, height=2, bg="lightblue", command=lambda: self.konwertuj(postac_infiksowa_na_onp)).grid(row=7, column=1, padx=2, pady=2)
        tk.Button(root, text="->Infiks", width=8, height=2, bg="lightblue", command=lambda: self.konwertuj(onp_na_infiks)).grid(row=7, column=2, padx=2, pady=2)
        tk.Button(root, text="°C->°F", width=8, height=2, bg="lightyellow", command=self.celsjusz_na_fahrenheit).grid(row=7, column=3, padx=2, pady=2)

        #w 8
        tk.Button(root, text="SPACJA", height=2, bg="lightgray", command=lambda: self.dopisz(" ")).grid(row=8, column=0, columnspan=2, padx=2, pady=(2, 10), sticky="we")
        tk.Button(root, text="=", height=2, bg="lightgreen", command=self.oblicz_wynik).grid(row=8, column=2, columnspan=2, padx=2, pady=(2, 10), sticky="we")

        #tk.Button(root, text="pi", height=2, bg="lightblue", command=lambda: self.dopisz("3.145")).grid(row=9, columnspan=4, padx=2, pady=(2,2), sticky='ew')

        root.bind("<Return>", lambda e: self.oblicz_wynik())
        self.entry.focus_set()

    def dopisz(self, tekst):
        self.entry.insert(tk.END, tekst)

    def minus(self):
        # poczatek lub spacja to znak inaczej to operator
        if self.entry.get() == "" or self.entry.get().endswith(" "):
            self.dopisz("-")
        else:
            self.dopisz(" - ")

    def czysc(self):
        self.ustaw("")

    def cofnij(self):
        #usuwa op wraz ze spacja
        self.ustaw(self.entry.get().rstrip()[:-1])

    def ustaw(self, tekst):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, tekst)

    def dodaj_do_historii(self, wpis):
        self.historia.config(state="normal")
        self.historia.insert(tk.END, wpis + "\n")
        self.historia.config(state="disabled")
        self.historia.see(tk.END)

    def konwertuj(self, funkcja):
        tekst = " ".join(self.entry.get().split())
        try:
            wynik = funkcja(tekst)
            self.dodaj_do_historii(tekst + " -> " + wynik)
            self.ustaw(wynik)
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def celsjusz_na_fahrenheit(self):
        try:
            c = float(self.entry.get())
            f = formatuj(c * 9 / 5 + 32)
            self.dodaj_do_historii(formatuj(c) + " °C = " + f + " °F")
            self.ustaw(f)
        except ValueError:
            messagebox.showerror("Błąd", "Wpisz liczbę Celsjusza")

    def oblicz_wynik(self):
        wyrazenie = self.entry.get().strip()
        try:
            # jesli wyrazenie na koncu to onp
            onp = wyrazenie
            if not wyrazenie.endswith(("+", "-", "*", "/", "^", "sqrt")):
                onp = postac_infiksowa_na_onp(wyrazenie)
            wynik = formatuj(odwrocona_notacja_polska(onp))
            self.dodaj_do_historii(wyrazenie + " = " + wynik)
            self.ustaw(wynik)
        except Exception as e:
            messagebox.showerror("Błąd", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    icon_image = tk.PhotoImage(file="images.png")
    root.iconphoto(True, icon_image)
    #root.iconbitmap("images.ico")
    app = KalkulatorONP(root)
    root.mainloop()