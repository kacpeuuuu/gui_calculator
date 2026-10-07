#ONP
import math

def oblicz(arg1, znak, arg2):
    arg1 = float(arg1)
    arg2 = float(arg2)
    if znak == "+":
        return arg1 + arg2
    elif znak == "-":
        return arg1 - arg2
    elif znak == "/":
        if arg2 == 0:
            raise Exception(ZeroDivisionError)
        return arg1 / arg2
    elif znak == "*":
        return arg1 * arg2
    elif znak == "^":
        return arg1 ** arg2
    elif znak == "sqrt":
        return math.sqrt(arg1) #arg2 to 0
    raise Exception("NIEZNANY SYMBOL")

def sprawdz_znak(znak):
    if len(znak) > 1:
        znak = znak.replace(".","")
        if znak[0] == "-":
            znak = znak[1:]
            return str(znak).isdigit()
        return str(znak).isdigit()
    else:
        return str(znak).isdigit()

def odwrocona_notacja_polska(wejscie_tekst):
    wejscie = wejscie_tekst.split(" ")
    stos = []
    wyjscie = []
    idx = 0
    while idx < len(wejscie):
        znak = wejscie[idx]
        if sprawdz_znak(znak):
            wyjscie.append(float(znak))
        else:
            stos.append(znak)

        #jednoargumentowe 
        if "sqrt" in stos:    
            wynik = oblicz(wyjscie[-1], stos[0], 0)
            stos.pop(0)
            wyjscie.pop(-1)
            wyjscie.append(wynik)

        #dwuargumentowe
        if stos != []:
            if len(wyjscie)<2:
                raise Exception("ZA MALO CYFR NA WEJSCIU")
            print(wyjscie)
            print(stos)
            wynik = oblicz(wyjscie[-2], stos[0], wyjscie[-1])
            wyjscie.pop(-1)
            wyjscie.pop(-1)
            stos.pop(0)
            wyjscie.append(wynik)
            

        idx += 1

    if len(wyjscie)>1:
        raise Exception("ZA DUZO WARTOSCI NA KONCU DZIALAN")
    return wyjscie[-1]
e