from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os, re
from email_logger import send_log
from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests

from models import Property
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def init_app(app):
    db = SQLAlchemy(app)
    db.init_app(app)
    
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = "secret"
    app.config['SERVER_NAME'] = 'localhost:8080'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:margaglio22@127.0.0.1:3307/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    
    return db

def crawl_parcels(start=0, end=-1):
    app = Flask(__name__)
    db = init_app(app)
    
    #.format(sbl,key)
    parcel_info_url = "https://paytax.erie.gov/webprop/property_info_details.asp?sbl={}&KEY={}"
    #.format(key)
    parcel_hist_url = "https://paytax.erie.gov/webprop/property_info_history.asp?sblkey={}"
    
    csvfile = open("parcel_links.csv")
    parcels = list(csv.reader(csvfile))
    t0 = time.time()
    total_length = float(len(parcels[start:end]))
    
    for n,r in enumerate(parcels[start:end]):
        p = Property()
        p.key = r[1]
        html_data = requests.get(parcel_info_url.format(r[0],r[1])).text
        soup = BeautifulSoup(html_data,'lxml')
        
        p.parcel_status = str(soup.findAll("tr")[0].findAll("td")[0].find(text=True))
        p.city = str(soup.findAll("tr")[0].findAll("td")[1].find(text=True))
        p.village = str(soup.findAll("tr")[0].findAll("td")[2].find(text=True))
        
        p.sbl = str(soup.findAll("tr")[1].findAll("td")[0].find(text=True))
        p.owner = str(soup.findAll("tr")[1].findAll("td")[1].find(text=True))
        p.swis = str(soup.findAll("tr")[1].findAll("td")[2].find(text=True))
        
        p.property_location = str(soup.findAll("tr")[2].findAll("td")[0].find(text=True))
        p.mailing = str(soup.findAll("tr")[2].findAll("td")[1].find(text=True))
        
        p.property_class = str(soup.findAll("tr")[3].findAll("td")[0].find(text=True))
        p.line2 = str(soup.findAll("tr")[3].findAll("td")[1].find(text=True))
        
        p.assessment = str(soup.findAll("tr")[4].findAll("td")[0].find(text=True))
        p.line3 = str(soup.findAll("tr")[4].findAll("td")[1].find(text=True))
        
        p.taxable = str(soup.findAll("tr")[5].findAll("td")[0].find(text=True))
        p.street = str(soup.findAll("tr")[5].findAll("td")[1].find(text=True))
        
        p.desc = str(soup.findAll("tr")[6].findAll("td")[0].find(text=True))
        p.owner_city = str(soup.findAll("tr")[6].findAll("td")[1].find(text=True))
        
        p.desc_alt = str(soup.findAll("tr")[7].findAll("td")[0].find(text=True))
        p.zip = str(soup.findAll("tr")[7].findAll("td")[1].find(text=True))
        
        p.dead_book = str(soup.findAll("tr")[8].findAll("td")[0].find(text=True))
        p.deed_page = str(soup.findAll("tr")[8].findAll("td")[1].find(text=True))
        
        p.frontage = str(soup.findAll("tr")[9].findAll("td")[0].find(text=True))
        p.depth = str(soup.findAll("tr")[9].findAll("td")[1].find(text=True))
        p.acres = str(soup.findAll("tr")[9].findAll("td")[2].find(text=True))
        
        p.year_built = str(soup.findAll("tr")[10].findAll("td")[0].find(text=True))
        p.square_ft = str(soup.findAll("tr")[10].findAll("td")[1].find(text=True))
        
        p.beds = str(soup.findAll("tr")[11].findAll("td")[0].find(text=True))
        p.baths = str(soup.findAll("tr")[11].findAll("td")[1].find(text=True))
        
        p.fireplace = str(soup.findAll("tr")[12].findAll("td")[0].find(text=True))
        p.school = str(soup.findAll("tr")[12].findAll("td")[1].find(text=True))
        
        if not db.session.query(Property).filter(Property.key == p.key).count():
            db.session.add(p)
            db.session.commit()
            print "Added:  " + str(n+start) + ", " + str(n/total_length)
        else:
            print "Failed: " + str(n+start) + ", " + str(n/total_length)
        
    print "Time: " + str(time.time() - t0)
    
if __name__ == "__main__":
    user = raw_input("> ")
    for i in [0]:
        try:
            arg = int(user)
        except:
            arg = '-'
        slct = {        '-':[64599,-1],
                        0:[64527, 129054],
                        1:[129054, 193581],
                        2:[193581, 258108],
                        3:[258108, -1]
                        }
        crawl_parcels(slct[arg][0], slct[arg][1])
    print "Done!"
