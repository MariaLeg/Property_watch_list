from __future__ import annotations
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
from typing import List
import datetime
from property import Property
import csv
import re
import json

class PropertyScraper:
    def __init__(self):
        # Ignore SSL certificate errors
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def scrape_right_move(self, url: str) -> Property:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        home = Property()
        home.link = url

        #Get the price and status if sold (Sold STC, Under Offer)
        price_tag = soup.find_all('p', class_='property-header-price')[0]
        home.price = price_tag.find_all('strong')[0].text.strip()
        price_comments = price_tag.find_all('small', class_='property-header-qualifier')
        if len(price_comments) > 0:
            tmp = price_comments[0].text.strip()
            if tmp == 'Offers in Excess of':
                home.price = tmp + ' ' + home.price
            elif tmp == 'Sold STC' or tmp == 'Under Offer':
                home.status = tmp

        #Get the address
        home.address = soup.find_all('address')[0].text
        home.address = home.address.replace("\r\n", "")

        #Get Added On date
        home.date_added = soup.find_all('div', id='firstListedDateValue')[0].text

        #Get the agency name
        home.agency = soup.find_all('a', id='aboutBranchLink')[0].text

        #Get school information
        property_id = re.findall('sale/property-([0-9]*).',url)
        url_school = 'https://www.rightmove.co.uk/ajax/schools/property/' + property_id[0] + '?ageGroupType=primary'
        contents = urllib.request.urlopen(url_school).read()
        parsed_json = json.loads(contents.decode('UTF-8'))
        for i in range(3):
            school = parsed_json["schools"][i]["schoolRating"]["label"] + ', ' + parsed_json["schools"][i]["name"] + ', ' + parsed_json["schools"][i]["distance"]
            home.schools = home.schools + school + '\n'
        home.schools = home.schools.rstrip()
        return home

    def load_new_properties(self, new_properties: List[str]) -> None:
        loaded_properties = list()
        for i in range(len(new_properties)):
            home = self.scrape_right_move(new_properties[i])
            loaded_properties.append(home)

        csvfile = open('Properties.csv', 'a', encoding = 'utf-8-sig', newline='')
        for i in range(len(loaded_properties)):
            Property.write_property_to_file(loaded_properties[i], csvfile)
        csvfile.close()