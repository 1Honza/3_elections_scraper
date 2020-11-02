
from bs4 import BeautifulSoup
import requests
import sys
import csv

def main():

    mesta = pridej_mesta()
    zadej_soubor(mesta)

def zadej_soubor(mesta_seznam):
# vytvori soubor

    soubor = input('Zadej nazev souboru pro ulozeni vysledku z uvedeného odkazu (napr: ''volby''): ').strip()
    adresa = 'https://www.volby.cz/pls/ps2017nss/' + mesta_seznam[0][2]

    hlavicka_info = pridej_info(adresa)
    hlavicka = vytvoreni_souboru(hlavicka_info)

    with open('{}.csv'.format(soubor), 'w', newline='') as file:
        zapis = csv.writer(file)
        zapis.writerow(hlavicka)

        for mesto in mesta_seznam:
            print('Pridane mesto {}.'.format(mesto[1]))
            adresa = 'https://www.volby.cz/pls/ps2017nss/' + mesto[2]

            info = pridej_info(adresa)
            vsechno = pridej_vysledek(info)
            zapis.writerow([mesto[0], mesto[1]] + vsechno)

def pridej_mesta():
# vycteni informaci podle zadane adresy

    print('Uvedeny link na stazeni volebnich vysledku: ','https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
    adresa =  ('https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ').strip()
    info = pridej_info(adresa)

    mesta_pocet = pridej_mesta_pocet(info)
    mesta_nazvy = pridej_jmena_mest(info)
    mesta_adresy = pridej_adresy_mest(info)

    return list(zip(mesta_pocet, mesta_nazvy, mesta_adresy))


def pridej_info(adresa):
# vyjimka na spatnou adresu

    try:
        odpoved = requests.get(adresa)
    except Exception as exc:
        print('Spatna adresa: %s' % (exc))
        sys.exit()

    return BeautifulSoup(odpoved.text, 'html.parser')


def pridej_mesta_pocet(info_para):
# generovani uzemi

    dalsi_prvky = pridej_dalsi_prvky(info_para, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1','t4sa1 t4sb1','t5sa1 t5sb1'
                                     ,'t6sa1 t6sb1','t7sa1 t7sb1','t8sa1 t8sb1','t9sa1 t9sb1','t10sa1 t10sb1','t11sa1 t11sb1'
                                     ,'t12sa1 t12sb1','t13sa1 t13sb1','t14sa1 t14sb1')
    dalsi_pocet = []

    for dalsi in dalsi_prvky:
        if dalsi.find('a'):
            dalsi_prvek = dalsi.find('a')
            dalsi_pocet.append(dalsi_prvek.text)
    return dalsi_pocet


def pridej_jmena_mest(info_para):
# nacteni mest
    dalsi_prvky = pridej_dalsi_prvky(info_para, 't1sa1 t1sb2', 't2sa1 t2sb2', 't3sa1 t3sb2','t4sa1 t4sb2','t5sa1 t5sb2'
                                     ,'t6sa1 t6sb2','t7sa1 t7sb2','t8sa1 t8sb2','t9sa1 t9sb2','t10sa1 t10sb2','t11sa1 t11sb2'
                                     ,'t12sa1 t12sb2','t13sa1 t13sb2','t14sa1 t14sb2')
    return [dalsi.text for dalsi in dalsi_prvky]


def pridej_adresy_mest(info_para):
# vytrideni mest na umistneni

    dalsi_prvky = pridej_dalsi_prvky(info_para, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1','t4sa1 t4sb1','t5sa1 t5sb1'
                                     ,'t6sa1 t6sb1','t7sa1 t7sb1','t8sa1 t8sb1','t9sa1 t9sb1','t10sa1 t10sb1','t11sa1 t11sb1'
                                     ,'t12sa1 t12sb1','t13sa1 t13sb1','t14sa1 t14sb1')
    dalsi_adresy = []

    for dalsi in dalsi_prvky:
        if dalsi.find('a'):
            dalsi_prvek = dalsi.find('a')
            dalsi_adresy.append(dalsi_prvek.get('href'))
    return dalsi_adresy


def pridej_dalsi_prvky(info_para, *hodnoty):
# nacteni informaci z hlavicky
    prvky = []

    for hodnota in hodnoty:
        prvky += info_para.select('td[headers="{}"]'.format(hodnota))
    return prvky


def vytvoreni_souboru(info_para):
# vytvoereni hlavicky

    informace = ['kod obce', 'mesto', 'volici', 'obalky', 'hlasy']
    casti = pridej_casti(info_para)
    return informace + casti


def pridej_casti(info_para):
# nazvy stran
    prvky = pridej_dalsi_prvky(info_para, 't1sa1 t1sb2', 't2sa1 t2sb2')
    return [prvek.text for prvek in prvky if prvek.text != '-']


def pridej_vysledek(info_para):
# vysledek voleb

    return pridej_hodnoty(info_para) + pridej_hlasy(info_para)


def pridej_hodnoty(info_para):
# seznam volicu, obalek, hlasu

    casti_hlavicky = ['sa2', 'sa3', 'sa6']
    seznam = []

    for cast_hlavicky in casti_hlavicky:
        seznam_info = info_para.find( 'td',{'headers' :'{}'.format(cast_hlavicky)})
        seznam_info = seznam_info.text
        seznam_info = seznam_info.replace('\xa0', '')
        seznam.append(int(seznam_info))
    return seznam


def pridej_hlasy(info_para):
# vrati seznam hlasu stran

    prvky = pridej_dalsi_prvky(info_para, 't1sa2 t1sb3', 't2sa2 t2sb3')
    seznam_hlasu = []

    for prvek in prvky:
        if prvek.text != '-':
            prvek = prvek.text.replace('\xa0', '')
            seznam_hlasu.append(int(prvek))
    return seznam_hlasu

main()