from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# import crawler
import pandas as pd
import time, re, os, requests
import datetime
from config import local_cities

from models import Listing, User, Owner, Parcel, Log, Chat, Lead

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

def init_app(app):
    db = SQLAlchemy(app)
    db.init_app(app)
    
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = "secret"
    app.config['SERVER_NAME'] = 'localhost:8080'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:margaglio22@127.0.0.1:3306/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    
    return db

def _list_tables():
    with app.app_context():
        for t in db.metadata.tables:
            print t

def _add_data():
    #crawler.crawler()
    data = pd.read_csv("full_data.csv")
    print "New Entries: ", len(data)
    added_count = 0
    for row in data.iterrows():
        print row[0]
        row[1][pd.isnull(row[1])]=None
        p = Listing()
        #try:
        p.addViaRow(row[1])
        if not db.session.query(Listing).filter(Listing.ml == p.ml).count():
            added_count += 1
            db.session.add(p)
            db.session.commit()
        #except:
        #    print("An error occurred: ")
        #    for j in row[1]:
        #        print(j)
        #    print
    os.remove("full_data.csv")
    print "Added " + str(added_count) + " new entries."
            
def register(email, password):
    with app.app_context():
        usr = User()
        usr.set_email(email)
        usr.set_password(password)
        db.session.add(usr)
        db.session.commit()
        
def remove_user(email):
    User.query.filter_by(email=email).delete()
    db.session.commit()
        
def _create_database():
    db.create_all()
    print("All tables created")
    
def remove_duplicates():
    print("Removing duplicates...")
    ls = db.session.query(Listing).filter(Listing.status == 'X').filter(Listing.exp_date >= datetime.datetime.now().date() - datetime.timedelta(days=2)).all()
    for n,l in enumerate(ls):
        fl = db.session.query(Listing).filter(Listing.ml == l.ml).all()
        if len(fl) > 1:
            for i in fl[1:]:
                db.session.delete(i)
            db.session.commit()
        print n/float(len(ls))
            
# YellowPages
def parser(db, listing):
    url = "http://people.yellowpages.com/whitepages?first={}&last={}&zip={}&state=ny"
    re_address = """<div class="address">\n(.*?)<"""
    re_phone = """<div class="phone">\n(.*?)<"""

    first = listing.o1fn
    last = listing.o1ln

    if listing.ozip:
        zipcode = listing.ozip
    else:
        zipcode = listing.zipc

    time.sleep(2)
    r = requests.get(url.format(first, last, zipcode))
        
    addresses = re.findall(re_address, r.text)
    phones = re.findall(re_phone, r.text)
    results = zip(addresses, phones)
    for n in results:
        print "Res: " + n[0].lstrip().rstrip().split(' ')[0]
        print "List: " + str(listing.stnum)
        if str(listing.stnum) in n[0]:
            phone = n[1].lstrip().rstrip()
            listing.phone_number = phone
            print "Phone: " + phone
            break

    db.session.add(listing)
    db.session.commit()
            
def getNumbers(db):
    working_list = db.session.query(Listing).join(Owner).filter(Listing.notes != None).filter(Listing.phone_number == None).filter(Listing.city.in_(local_cities)).order_by(Listing.exp_date.desc()).all()
    print len(working_list)
    for n, listing in enumerate(working_list):
        print float(n)/len(working_list)
        print listing.phone_number
        parser(db, listing)
        print

if __name__ == '__main__':
    app = Flask(__name__)
    db = init_app(app)
    count = 0
    with app.app_context():
        for q in Listing.query.filter(Listing.city.in_(local_cities)).filter(Listing.status == 'X').filter(Listing.notes != '').all():
            lead = Lead()
            break

            data = {}
            data['address'] = q.address
            data['city'] = q.city
            data['zipcode'] = q.zipc

            data['owner_name'] = q.o1fn + ' ' + q.o1ln
            data['owner_address'] = q.address
            data['owner_city'] = q.city
            data['owner_zipcode'] = q.zipc
            data['owner_phone'] = q.phone_number

            data['notes'] = 'ALPHA LEAD\n' + q.notes
            data['phone_status'] = 'not_checked'

            lead.date_created = datetime.datetime.now()-datetime.timedelta(days=39)
            lead.update(data)

            db.session.add(lead)
            db.session.commit()
            print(count)
            count+=1











