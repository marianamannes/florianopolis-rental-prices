# Importing libraries
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re


# Creating the data scrapper class
class DataScrapper:
    def __init__(self, size):
        self.size = size
        self.df = pd.DataFrame(columns=['text',
                                        'region',
                                        'district',
                                        'square_meters',
                                        'condominium_fee',
                                        'bedrooms',
                                        'bathrooms',
                                        'garages',
                                        'price'])
        self.regions = {'centro': 'downtown',
                        'continente': 'continent',
                        'leste': 'east',
                        'norte': 'north',
                        'sul': 'south'}
        self.rental_information()

    # Getting all rental information needed by ad
    def rental_information(self):
        for key, value in self.regions.items():
            regioncounter = 0
            pagecounter = 1
            while regioncounter != self.size / 5:
                cards = self.html_reader(key, pagecounter)
                for card in cards:
                    text = self.find_text(card)
                    attributes, valid = self.find_attributes(card)
                    if self.text_check(text) and self.card_check(card) and valid:
                        self.add_new_row(self.df, text, value, card, attributes)
                        if self.df.shape[0] > self.df.drop_duplicates().reset_index(drop=True).shape[0]:
                            self.df = self.df.drop_duplicates().reset_index(drop=True)
                        else:
                            regioncounter += 1
                            if regioncounter >= self.size / 5:
                                break
                pagecounter += 1

    # Adding a new row to the dataframe
    def add_new_row(self, dataframe, text, region, card, attributes):
        df_new_row = pd.DataFrame({'text': [text],
                                   'region': [region],
                                   'district': [self.find_district(card)],
                                   'square_meters': [self.find_square_meters(attributes)],
                                   'condominium_fee': [self.find_condominium_fee(card)],
                                   'bedrooms': [self.find_bedrooms(attributes)],
                                   'bathrooms': [self.find_bathrooms(attributes)],
                                   'garages': [self.find_garages(attributes)],
                                   'price': [self.find_price(card)]})
        self.df = pd.concat([dataframe, df_new_row])
        self.df.reset_index(drop=True, inplace=True)

    # Creating the html reader
    def html_reader(self, region, page):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        url = f'https://www.olx.com.br/imoveis/aluguel/estado-sc/florianopolis-e-regiao/{region}?o={page}'
        req = Request(url, headers=headers)
        response = urlopen(req)
        html = response.read()
        html = html.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.findAll('a', {'data-ds-component': 'DS-AdCardHorizontal'})
        return cards

    # Returning the rental price
    def find_price(self, card):
        price = card.find('span', {'data-ds-component': 'DS-Text'}).getText()
        if price != "":
            price = price.split()[1]
            price = price.replace(".", "")
            if price == '0':
                price = None
        else:
            price = None
        return price

    # Returning the ad text
    def find_text(self, card):
        return card.find('h2').getText()

    # Returning the district name
    def find_district(self, card):
        div = card.find('div', {'class': 'sc-iNhVCk geaanK'})
        if div is not None:
            district = div.span.get_text().split(', ')[1]
        else:
            district = None
        return district

    # Returning the condominium fee
    def find_condominium_fee(self, card):
        div = card.find('div', {'class': 'sc-cHSUfg fmLZyg'})
        condominium_fee = None
        if div is not None:
            for span in div:
                text = span.get_text()
                if "Condomínio" in text.split():
                    condominium_fee = text.split()[-1]
                    condominium_fee = condominium_fee.replace(".", "")
        return condominium_fee

    # Returning all attributes
    def find_attributes(self, card):
        ul = card.find('ul', {'class': 'sc-cmjSyW hXtObT'})
        if ul is not None:
            attributes = ul.findAll('span')
            for i in range(len(attributes)):
                attributes[i] = attributes[i]['aria-label']
            r = re.compile('^(.*quartos?|.*metros? quadrados?|.*banheiros?)$')
            f_attributes = list(filter(r.match, attributes))
            if (len(f_attributes) == 3) and (self.find_price(card) is not None):
                valid = True
                r = re.compile('.*garagem')
                garages = list(filter(r.match, attributes))
                if len(garages) > 0:
                    f_attributes.append(garages[0])
            else:
                valid = False
        else:
            f_attributes = []
            valid = False
        return f_attributes, valid

    # Returning the number of bedrooms
    def find_bedrooms(self, attributes):
        bedrooms = attributes[0].split()[0]
        return bedrooms

    # Returning the property size in square meters
    def find_square_meters(self, attributes):
        square_meters = attributes[1].split()[0]
        return square_meters

    # Returning the number of bathrooms
    def find_bathrooms(self, attributes):
        bathrooms = attributes[2].split()[0]
        return bathrooms

    # Returning the number of garages
    def find_garages(self, attributes):
        garages = 0
        if len(attributes) == 4:
            garages = attributes[3].split()[0]
        return garages

    # Text Check
    def text_check(self, text):
        seasonal = re.compile(r'temporada', flags=re.IGNORECASE).search(text)
        commercial = re.compile(r'comercial', flags=re.IGNORECASE).search(text)
        sale = re.compile(r'vend.', flags=re.IGNORECASE).search(text)
        return all(a is None for a in [seasonal, commercial, sale])

    # Card check
    def card_check(self, card):
        h3 = card.find('h3')
        if h3 is not None:
            text = h3.getText()
            text = text.split()[0]
        else:
            text = None
        return text == 'Apartamento'
