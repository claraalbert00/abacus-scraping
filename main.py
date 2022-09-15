import sys
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

def processaURL(link,categoria,pagina):
    htmlfile = urllib.request.urlopen(link).read().decode()
    soup = BeautifulSoup(htmlfile, 'html.parser')
    productes =[]

    prods = soup.find_all('div', attrs={'class':'product'})

    for prod in prods:
        pid = prod['data-pid']
        nom = prod.find('h3').text.replace('\xa0',' ')
        descripcio = prod.find('div', attrs={'class':'product-desc'}).text.strip('\n ')
        prices = prod.find('div',attrs={'class':'prices abaPrices'})
        preusoci = prices.find('div', attrs={'class':'priceblock memberPrice'}).find('div',attrs={'class':'price'}).find('span',attrs={'class':'value'}).text.strip('\n ').replace(',','.')
        preusoci=preusoci[0:len(preusoci)-1]
        preunosoci = prices.find('div', attrs={'class':'priceblock standardPrice'}).find('div', attrs={'class': 'price'}).find('span', attrs={'class': 'value'}).text.strip('\n ').replace(',','.')
        preunosoci = preunosoci[0:len(preunosoci) - 1]

        producte = {'pid':pid,'nom': nom,'descripcio':descripcio,'preusoci':preusoci,'preunosoci':preunosoci,'categoria':categoria, 'pagina':pagina, 'link':link}
        productes.append(producte)

    return productes

print('Categories: ')
print('1. Videojocs')
print('2. Audio')
print('3. Cinema i música')
print('4. Informàtica')

correcte = False
while correcte == False:
    categoria = input('Quina categoria esculls? (Escriu el número de la categoria)')
    if categoria == '1':
        link = 'https://www.abacus.coop/es/tecnologia/videojuegos-y-consolas'
        correcte = True
    elif categoria == '2':
        link = 'https://www.abacus.coop/es/tecnologia/audio'
        correcte = True
    elif categoria == '3':
        link = 'https://www.abacus.coop/es/tecnologia/cine-y-musica'
        correcte = True
    elif categoria == '4':
        link = 'https://www.abacus.coop/es/tecnologia/informatica'
        correcte = True
    else:
        print('Error')

correcte = False
totes = False
while correcte == False:
    pagina = input('Quina pàgina vols (1-3)? T=totes')
    if pagina == '1':
        link = link
        correcte = True
    elif pagina == '2':
        link = link + '?pageNo=2'
        correcte = True
    elif pagina == '3':
        link = link + '?pageNo=3'
        correcte = True
    elif pagina == 'T' or pagina == 't':
        totes = True
        correcte = True
    else:
        print('Error')

print('Categoria:',categoria)
productes = []
if totes == True:
    links = {link, link + '?pageNo=2', link + '?pageNo=3'}
    pagina = 0
    for link in links:
        pagina = pagina + 1
        ppag = processaURL(link,categoria,pagina)
        productes += ppag
        #print('Pagina:',pagina)
        #for p in ppag:
            #print('Nom:', p['nom'],'\tPreu Soci:',p['preusoci'],'\tPreu No Soci:',p['preunosoci'], '\tDescripcio:',p['descripcio'][0:20])
else:
    productes = processaURL(link,categoria,pagina)
    #print('Pagina:', pagina)
    #for p in productes:
        #print('Nom:', p['nom'],'\tPreu Soci:',p['preusoci'],'\tPreu No Soci:',p['preunosoci'], '\tDescripcio:',p['descripcio'][0:20])

# Creem base de dades
conn = sqlite3.connect('abacus.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS Productes;')
c.execute("""CREATE TABLE Productes (
            "Id" INTEGER PRIMARY KEY NOT NULL,
            "Nom" TEXT NOT NULL,
            "Descripcio" TEXT,
            "Preu Soci" REAL NOT NULL,
            "Preu No Soci" REAL NOT NULL,
            "Link" TEXT NOT NULL,
            "Categoria" INTEGER NOT NULL,
            "Pagina" INTEGER NOT NULL);""")

i=1
for p in productes:
    c.execute('INSERT INTO Productes VALUES ({},"{}","{}",{},{},"{}",{},{});'.format(i,p['nom'],p['descripcio'],p['preusoci'],p['preunosoci'],p['link'],p['categoria'],p['pagina']))
    conn.commit()
    i=i+1


result = c.execute("SELECT * FROM Productes;")
for r in result:
    print(r)

conn.close()


