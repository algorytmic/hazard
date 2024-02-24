import socket
import os
import requests
import idna
import domain2idna
import time
from termcolor import colored


from bs4 import BeautifulSoup

print("Weryfikator domen hazardowych - Łukasz Prus v 1.0 beta")
print("Rozpoczynam skrypt..")
api_url = "https://hazard.mf.gov.pl/api/Register/"
ip_mf = '145.237.235.240'
print("Ustanawiam połączenie ze stroną MF i pobieram xml")

## Pobranie danych z API Ministerstwa Finansow
## Ustawienie crona na pobieranie danych co 2 godziny

response = requests.get(api_url)
with open('hazard.xml', 'wb') as file:
    file.write(response.content)


##Odczytanie danych z pliku XML
with open('hazard.xml', 'r', encoding="utf-8") as f:
    dane = f.read()

print("XML pobrany - rozpoczynam parsowanie")

dane_domen = BeautifulSoup(dane, features="xml")

adresy_domen = dane_domen.find_all('AdresDomeny')


gotowe_dane = list()
gotowe_dane_bind = list()

count_wadliwe = 0
count_poprawne = 0
count_wszystkie = 0
count_nierozwiazane = 0
wadliwe_list = []
nie_mozna_rozwiazac = []

print("Rozpoczynam weryfikacje domen")

for dane in adresy_domen:
    dane = dane.get_text()
    if any(ord(c) > 127 for c in dane):
        if idna:
            print("Tak jest IDNA:  " + dane)
            dane = dane.encode('idna')
            dane = str(dane).replace("b'", "").replace("'","")

    try:
        addr = socket.gethostbyname(dane)
        if(addr == '145.237.235.240'):
            # print(colored("Domena "+dane+" jest poprawnie rozwiazana i ma IP: "+addr , 'green'))
            count_poprawne = count_poprawne + 1
            print("Zablokowane domeny: " +str(count_poprawne) + " blokowana domena ------> " + dane)
            # print("Poprawnie rozwiązane domeny: " + count_poprawne)
        else:
            print(" Domena  " +dane+ " nie jest BLOKOWANA!!")
            count_wadliwe = count_wadliwe + 1
            waliwe_list.append(dane)

    except:
        print("Nie można rozwiązać hosta: " + dane)
        count_nierozwiazane = count_nierozwiazane + 1
        nie_mozna_rozwiazac.append(dane)

    count_wszystkie = count_wszystkie +1

print("############### PODSUMOWANIE ###############")
print("Wszystkich domen w pliku: " +str(count_wszystkie))
print("Poprawne: " + str(count_poprawne))

if len(wadliwe_list) == 0:
    print("Wszystkie domeny z listy są zablokowane")
else:
    print("Domeny ktore nie sa blokowane: " + str(count_wadliwe))
    print(wadliwe_list)


if len(nie_mozna_rozwiazac) != 0:
    print("Domeny ktorych nie mozna rozwiazac: " + str(count_nierozwiazane))
    print(nie_mozna_rozwiazac)
input("Najciśnij Enter żeby wyjść;")