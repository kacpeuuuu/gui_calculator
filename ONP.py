#ONP
wejscie = input()

stos = wejscie.split(" ")

def oblicz(arg1, arg2, znak):
    arg1 = int(arg1)
    arg2 = int(arg2)
    if znak == "+":
        return arg1 + arg2
    elif znak == "-":
        return arg1 - arg2
    elif znak == "/":
        return arg1 / arg2
    elif znak == "*":
        return arg1 * arg2

temp_stos = []
print(temp_stos)
ilosc_znakow = 0
for i in range(len(stos)):
    if (stos[i].isnumeric()):
        temp_stos.append(stos[i])
    else:
        if len(temp_stos) < 1:
            print("za malo liczb")
        else:
            liczba_1 = temp_stos[i-2-ilosc_znakow]
            liczba_2 = temp_stos [i-1-ilosc_znakow]
            print(oblicz(liczba_1, liczba_2, stos[i]))
            ilosc_znakow += 1
print(temp_stos)



# idx = 0
# while len(stos) != 1:
#     if 