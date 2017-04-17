from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import string
import sys

if __name__ == "__main__":
    from flask_script import Manager
    from flask_migrate import Migrate, MigrateCommand

    # Run these commands in order
    # sudo python models.py db migrate
    # sudo python models.py db upgrade
    app = Flask(__name__)
    db = SQLAlchemy(app)
    db.init_app(app)

    app.config['SECRET_KEY'] = "secret"
    app.config['SERVER_NAME'] = 'localhost:8080'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:margaglio22@127.0.0.1:3306/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
else:
    db = SQLAlchemy()

app = Flask(__name__)
db = SQLAlchemy(app)
db.init_app(app)

app.config['SECRET_KEY'] = "secret"
app.config['SERVER_NAME'] = 'localhost:8080'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:margaglio22@127.0.0.1:3306/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

class Parcel(db.Model):
    # Parcel information obtainable via Erie County Parcel Search
    # http://www2.erie.gov/ecrpts/index.php?q=real-property-parcel-search
    # Presumably, every parcel in Erie County is available on here,
    # so using this as a 'base' class is appropriate

    __tablename__ = 'parcels'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    parcel_status = db.Column(db.String(128), default="")
    city_town = db.Column(db.String(128), default="")
    village = db.Column(db.String(128), default="")
    sbl = db.Column(db.String(128), default="")
    owner = db.Column(db.String(128), default="")
    swis = db.Column(db.String(128), default="")
    property_location = db.Column(db.String(128), default="")
    mailing_address = db.Column(db.String(128), default="")
    property_class = db.Column(db.String(128), default="")
    line_2 = db.Column(db.String(128), default="")
    assessment = db.Column(db.Integer, default="")
    line_3 = db.Column(db.String(128), default="")
    taxable = db.Column(db.Integer, default="")
    street = db.Column(db.String(128), default="")
    desc = db.Column(db.String(128), default="")
    city_state = db.Column(db.String(128), default="")
    desc_2 = db.Column(db.String(128), default="")
    zip = db.Column(db.String(128), default="")
    deed_book = db.Column(db.String(128), default="")
    deed_page = db.Column(db.String(128), default="")

    frontage = db.Column(db.Integer, default="")
    depth = db.Column(db.Integer, default="")
    acres = db.Column(db.Integer, default="")
    year_built = db.Column(db.Integer, default="")
    square_ft = db.Column(db.Integer, default="")
    beds = db.Column(db.Float, default="")
    baths = db.Column(db.Float, default="")
    fireplace = db.Column(db.Float, default="")
    school = db.Column(db.String(128), default="")

    parcel_url = db.Column(db.String(128), default="")
    parcel_history_url = db.Column(db.String(128), default="")
    # parcel_history = db.relationship('Parcel_History', backref=db.backref('parcel', lazy='dynamic'))

    def __repr__(self):
        return str(self.property_location)

    def setdic(self, data):
        for k, v in data.items():
            setattr(self, k, data[k])
        return self

    def getdic(self):
        keys = ['id', 'parcel_status', 'city_town', 'village',
        'sbl', 'owner',        'swis',        'property_location',        'mailing_address',
        'property_class',        'line_2',        'assessment',        'line_3',
        'taxable',        'street',        'desc',        'city_state',        'desc_2',
        'zip',        'deed_book',        'deed_page',        'frontage',        'depth',
        'acres',        'year_built',        'square_ft',        'beds',        'baths',
        'fireplace',        'school',        'parcel_url', 'parcel_history_url']

        dic = {}
        for k in keys:
            dic[k] = getattr(self, k)

        return dic


class Parcel_History(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    owner = db.Column(db.String(128), default="")
    bookpage_date = db.Column(db.String(128), default="")


class Owner(db.Model):
    # This is Owner information related to any parcel in our database.
    # This information is aggregated across the board, so the information
    # may not be consistent.  In any case, info related to a specific
    # individual is stored here.

    __tablename__ = 'owners'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    first = db.Column(db.String(128), nullable=True)
    middle = db.Column(db.String(128), nullable=True)
    last = db.Column(db.String(128), nullable=True)

    phone = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=True)

    checked_yp = db.Column(db.Boolean, default=False)
    checked_number = db.Column(db.Boolean, default=False)
    # assume number is bad until checked
    phone_status = db.Column(db.String(128), nullable=True)

    # parcel_id = db.Column(db.Integer, db.ForeignKey('parcels.id'))
    # listings = db.relationship('Listing', backref='owner', cascade="all, delete-orphan", lazy='dynamic')


# [START model]

class Listing(db.Model):
    # This is for Listing information.  This is to organize parcel/owner
    # information temporally (i.e., an owner may have lived in more than
    # one house over some span of time).  This is raw, so that this
    # information is collected via the MLS, then organized later.

    __tablename__ = 'listings'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # parcel = db.relationship('Parcel', cascade="all, delete-orphan", backref='listing')

    ml = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(128), nullable=True)
    exp_date = db.Column(db.Date, nullable=True)
    cur_pri = db.Column(db.Integer, nullable=True)
    lis_pri = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(128), nullable=True)
    scl_dis = db.Column(db.String(128), nullable=True)
    sqft = db.Column(db.Integer, nullable=True)
    fire = db.Column(db.Integer, nullable=True)
    bths = db.Column(db.Integer, nullable=True)
    beds = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    dpth = db.Column(db.Integer, nullable=True)
    frnt = db.Column(db.Integer, nullable=True)
    ctax = db.Column(db.Integer, nullable=True)
    stax = db.Column(db.Integer, nullable=True)

    ttax = db.Column(db.Integer, nullable=True)
    tctax = db.Column(db.Integer, nullable=True)
    assess = db.Column(db.Integer, nullable=True)

    stname = db.Column(db.String(128), nullable=True)
    stnum = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(128), nullable=True)
    zipc = db.Column(db.Integer, nullable=True)
    dom = db.Column(db.Integer, nullable=True)

    # owner = db.relationship('Owner', backref='listing', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    o1fn = db.Column(db.String(128), nullable=True)
    o1ln = db.Column(db.String(128), nullable=True)
    o1mi = db.Column(db.String(128), nullable=True)
    phone_number = db.Column(db.String(128), nullable=True)
    # checked_yp = db.Column(db.Boolean, default=False)
    # o1phone = db.relationship('PhoneNumber', backref='owner', lazy='dynamic')

    o2fn = db.Column(db.String(128), nullable=True)
    o2ln = db.Column(db.String(128), nullable=True)
    o2mi = db.Column(db.String(128), nullable=True)

    ocit_state = db.Column(db.String(128), nullable=True)
    osnumsname = db.Column(db.String(128), nullable=True)
    ozip = db.Column(db.Integer, nullable=True)

    parcel_num = db.Column(db.String(128), nullable=True)
    ladwp = db.Column(db.String(128), nullable=True)
    laemail = db.Column(db.String(128), nullable=True)
    lafulln = db.Column(db.String(128), nullable=True)
    lamlsid = db.Column(db.String(128), nullable=True)
    listdate = db.Column(db.String(128), nullable=True)
    lomsid = db.Column(db.String(128), nullable=True)
    loname = db.Column(db.String(128), nullable=True)
    lophone = db.Column(db.String(128), nullable=True)

    mailed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(512), nullable=True)
    date_added = db.Column(db.Date)

    strings = {'ML #': 'ml', 'Address': 'address', 'St': 'status', 'School District Name': 'scl_dis',
               'Street Name': ' stname', 'Town/City': 'city',
               'Owner 1 First Name': 'o1fn', 'Owner 1 Last Name': 'o1ln',
               'Owner 2 First Name': 'o2fn', 'Owner 2 Last Name': 'o2ln',
               'Owner 1 Middle Initial': 'o1mi', 'Owner 2 Middle Initial': 'o2mi',
               'Owner City State': 'ocit_state', 'Owner Street Num Street Name': 'osnumsname',
               'Parcel Number': 'parcel_num', 'List Agent Direct Work Phone': 'ladwp',
               'List Agent Email': 'laemail', 'List Agent Full Name': 'lafulln',
               'List Agent MLSID': 'lamlsid', 'List Office MLSID': 'lomsid',
               'List Office Name': 'loname', 'List Office Phone': 'lophone'}

    numbers = {'Current Price': 'cur_pri', 'List Price': 'lis_pri', 'Sq Ft Total': 'sqft',
               'Num Fireplaces Total ': 'fire', 'Baths Total': 'bths', 'Beds Total': 'beds',
               'Year Built': 'year', 'Lot Dimensions Depth': 'dpth', 'Lot Dimensions Frontage': 'frnt',
               'City Village Tax': 'ctax', 'School Tax': 'stax', 'Total Taxes': 'ttax',
               'Town County Tax': 'tctax', 'Street Number': 'stnum', 'Zip Code': 'zipc', 'DOM': 'dom'}

    dates = {'Expiration Date': 'exp_date', 'List Date': 'listdate'}

    fields = dict(strings.items() + numbers.items() + dates.items())

    def __getitem__(self, arg):
        return str(getattr(self, self.fields[arg]))

    def __setitem__(self, key, value):
        setattr(self, self.fields[key], value)

    def str_to_num(self, field):
        rem = ['$', ',']
        rem += list(string.ascii_lowercase)
        rem += list(string.ascii_uppercase)
        try:
            return int(str(field).translate(None, ''.join(rem)))
        except:
            return None

    def addViaRow(self, row):
        import pandas as pd
        for k in self.strings:
            try:
                self[k] = row[k]
            except:
                pass

        for k in self.numbers:
            self[k] = self.str_to_num(row[k])

        for k in self.dates:
            self[k] = pd.to_datetime(row[k])

        self.date_added = datetime.datetime.now()

        _owner = Owner()
        _owner.first = self.o1fn
        _owner.middle = self.o1mi
        _owner.last = self.o1ln
        db.session.add(_owner)
        db.session.commit()
        self.owner_id = _owner.id

        _parcel = Parcel()
        _parcel.owner_zip = self.zipc
        _parcel.prop_location = self.address
        _parcel.owner_id = _owner.id
        db.session.add(_parcel)
        db.session.commit()

    def __repr__(self):
        return str(self.ml)

fb_ads = db.Table('fb_ads',
                  db.Column('email', db.String(64), db.ForeignKey('users.email')),
                  db.Column('id', db.Integer, db.ForeignKey('facebook_ad.id'))
                  )

class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(1024))
    admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    unfinished_lead = db.Column(db.Boolean, default=False)
    fb_ad = db.relationship('FacebookAd', secondary=fb_ads, backref=db.backref('users', lazy='dynamic'))

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<" + self.email + ">"

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class FacebookAd(db.Model):
    __tablename__ = "facebook_ad"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fb_id = db.Column(db.String(128), nullable=True)
    #leads = db.relationship('Lead', secondary=fb_leads, backref=db.backref(''))

class FacebookLead(db.Model):
    __tablename__ = "facebook_lead"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    notes = db.Column(db.String(512), nullable=True)
    date_added = db.Column(db.Date)

    # From CSV v
    fb_id = db.Column(db.String(128), nullable=True)
    created_time = db.Column(db.String(128), nullable=True)
    ad_id = db.Column(db.String(128), nullable=True)
    ad_name = db.Column(db.String(128), nullable=True)
    adset_id = db.Column(db.String(128), nullable=True)
    adset_name = db.Column(db.String(128), nullable=True)
    campaign_id = db.Column(db.String(128), nullable=True)
    campaign_name = db.Column(db.String(128), nullable=True)
    form_id = db.Column(db.String(128), nullable=True)
    is_organic = db.Column(db.String(128), nullable=True)

    full_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    street_address = db.Column(db.String(128), nullable=True)
    zip_code = db.Column(db.String(128), nullable=True)
    phone_number = db.Column(db.String(128), nullable=True)

    def fromRow(self, row):
        # inputs data from structured CSV row (i.e., a list)
        self.fb_id = row[0]
        self.created_time = row[1]
        self.ad_id = row[2]
        self.ad_name = row[3]
        self.adset_id = row[4]
        self.adset_name = row[5]
        self.campaign_id = row[6]
        self.campaign_name = row[7]
        self.form_id = row[8]
        self.is_organic = row[9]

        self.full_name = row[10]
        self.email = row[11]
        self.street_address = row[12]
        self.zip_code = row[13]
        self.phone_number = row[14]

        self.date_added = datetime.datetime.now()


class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    key = db.Column(db.String(128), nullable=True)

    # Parcel Page
    parcel_status = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    village = db.Column(db.String(128), nullable=True)

    sbl = db.Column(db.String(128), nullable=True)
    owner = db.Column(db.String(128), nullable=True)
    swis = db.Column(db.String(128), nullable=True)

    property_location = db.Column(db.String(128), nullable=True)
    mailing = db.Column(db.String(128), nullable=True)
    property_class = db.Column(db.String(128), nullable=True)
    line2 = db.Column(db.String(128), nullable=True)
    assessment = db.Column(db.String(128), nullable=True)
    line3 = db.Column(db.String(128), nullable=True)
    taxable = db.Column(db.String(128), nullable=True)
    street = db.Column(db.String(128), nullable=True)
    desc = db.Column(db.String(128), nullable=True)
    owner_city = db.Column(db.String(128), nullable=True)
    desc_alt = db.Column(db.String(128), nullable=True)
    zip = db.Column(db.String(128), nullable=True)
    dead_book = db.Column(db.String(128), nullable=True)
    deed_page = db.Column(db.String(128), nullable=True)
    frontage = db.Column(db.String(128), nullable=True)
    depth = db.Column(db.String(128), nullable=True)
    acres = db.Column(db.String(128), nullable=True)
    year_built = db.Column(db.String(128), nullable=True)
    square_ft = db.Column(db.String(128), nullable=True)
    beds = db.Column(db.String(128), nullable=True)
    baths = db.Column(db.String(128), nullable=True)
    fireplace = db.Column(db.String(128), nullable=True)
    school = db.Column(db.String(128), nullable=True)


class OwnerHistory(db.Model):
    __tablename__ = "owner_histories"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    key = db.Column(db.String(128), nullable=True)
    owner = db.Column(db.String(128), nullable=True)
    book_date = db.Column(db.String(128), nullable=True)
    date = db.Column(db.Date, nullable=True)


class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time = db.Column(db.DateTime)
    user = db.Column(db.String(128), db.ForeignKey('users.email'))
    info = db.Column(db.String(512))


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    room = db.Column(db.String(128))
    time = db.Column(db.DateTime)
    user = db.Column(db.String(128), db.ForeignKey('users.email'))
    message = db.Column(db.String(512))


class Lead(db.Model):
    __tablename__ = "leads"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created = db.Column(db.DateTime)

    # Property Info
    address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    zipcode = db.Column(db.String(128), nullable=True)

    # Contact Info
    owner_name = db.Column(db.String(128), nullable=True)
    owner_address = db.Column(db.String(128), nullable=True)
    owner_city = db.Column(db.String(128), nullable=True)
    owner_zipcode = db.Column(db.String(128), nullable=True)
    owner_phone = db.Column(db.String(128), nullable=True)
    owner_email = db.Column(db.String(128), nullable=True)

    # Lead Info
    notes = db.Column(db.String(512), nullable=True)
    priority = db.Column(db.Float, default=0)
    status = db.Column(db.String(128), default='live')
    mail_status = db.Column(db.Boolean, default=False)
    phone_status = db.Column(db.String(128), nullable=True)
    claimed = db.Column(db.Boolean, default=False)
    claim_user = db.Column(db.String(128), nullable=True)
    claim_datetime = db.Column(db.DateTime, nullable=True)
    next_contact_date = db.Column(db.DateTime, nullable=True)
    expire_date = db.Column(db.DateTime, nullable=True)

    def __init__(self):
        self.date_created = datetime.datetime.now()
        self.phone_status = 'pre_lookup'

    def push_expire_date(self, days=1, date=None):
        if date:
            self.expire_date = date
        elif self.expire_date:
            self.expire_date += datetime.timedelta(days=days)
        else:
            self.expire_date = datetime.datetime.now() + datetime.timedelta(days=days)

        self.expire_date = self.expire_date.replace(hour=11)
        print("Exp:",self.expire_date)

    def update(self, fields):
        data = {}

        try:
            data['id'] = self.id
        except:
            pass

        try:
            data['date_created'] = self.date_created
        except:
            pass

        data['address'] = self.address
        data['city'] = self.city
        data['zipcode'] = self.zipcode

        data['owner_name'] = self.owner_name
        data['owner_address'] = self.owner_address
        data['owner_city'] = self.owner_city
        data['owner_zipcode'] = self.owner_zipcode
        data['owner_phone'] = self.owner_phone
        data['owner_email'] = self.owner_email

        data['notes'] = self.notes
        data['priority'] = self.priority
        data['status'] = self.status
        data['phone_status'] = self.phone_status
        data['mail_status'] = self.mail_status

        data['claimed'] = self.claimed

        data['claim_user'] = self.claim_user
        data['claim_datetime'] = self.claim_datetime
        data['next_contact_date'] = self.next_contact_date
        data['expire_date'] = self.expire_date

        if fields:
            for k in fields:
                data[k] = fields[k]

        self.set(data)

    def set(self, data):
        self.address = data['address']
        self.city = data['city']
        self.zipcode = data['zipcode']

        self.owner_name = data['owner_name']
        self.owner_address = data['owner_address']
        self.owner_city = data['owner_city']
        self.owner_zipcode = data['owner_zipcode']
        self.owner_phone = data['owner_phone']
        self.owner_email = data['owner_email']

        self.notes = data['notes']
        self.claim_user = data['claim_user']

        try:
            self.priority = float(data['priority'])
        except:
            pass
        self.status = data['status']
        self.phone_status = data['phone_status']
        try:
            _mail_status = bool(data['mail_status'])
            self.mail_status = _mail_status
        except:
            pass

        if data['claimed'] == 'true' or data['claimed'] == True:
            _claimed = True
        else:
            _claimed = False
        self.claimed = _claimed

        try:
            string_datetime = data['claim_datetime']
            self.claim_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d")
        except:
            pass

        try:
            string_datetime = data['date_created']
            if string_datetime != self.date_created:
                self.date_created = datetime.datetime.strptime(string_datetime, "%Y-%m-%d")
        except:
            pass

        try:
            string_datetime = data['next_contact_date']
            self.next_contact_date = datetime.datetime.strptime(string_datetime, "%Y-%m-%d").replace(hour=11)
            self.push_expire_date(date=self.next_contact_date + datetime.timedelta(days=1))
        except:
            pass

        try:
            string_datetime = data['expire_date']
            self.expire_date = datetime.datetime.strptime(string_datetime, "%Y-%m-%d").replace(hour=11)
        except:
            pass

    def claim(self, attempting_user):
        user_model = db.session.query(User).filter(User.email == attempting_user).first()

        # if user_model.unfinished_lead != True:
        #    print "\nCLAIMING\n"
        self.claim_user = attempting_user
        self.claim_datetime = datetime.datetime.now()
        self.claimed = True
        self.push_expire_date()

        user_model.unfinished_lead = True
        db.session.add(user_model)
        db.session.commit()

    def read(self):
        data = {}

        data['id'] = self.id
        data['date_created'] = self.date_created

        data['address'] = self.address
        data['city'] = self.city
        data['zipcode'] = self.zipcode

        data['owner_name'] = self.owner_name
        data['owner_address'] = self.owner_address
        data['owner_city'] = self.owner_city
        data['owner_zipcode'] = self.owner_zipcode
        data['owner_phone'] = self.owner_phone
        data['owner_email'] = self.owner_email

        data['notes'] = self.notes
        data['priority'] = self.priority
        data['status'] = self.status
        data['phone_status'] = self.phone_status
        data['mail_status'] = self.mail_status
        data['claimed'] = self.claimed
        data['claim_user'] = self.claim_user
        data['claim_datetime'] = self.claim_datetime
        data['next_contact_date'] = self.next_contact_date
        data['expire_date'] = self.expire_date

        return data


if __name__ == "__main__":
    db.create_all()

    """
    com = ""
    while com != "!exit":
        com = raw_input("> ")
        try:
            for i in db.engine.execute(com):
                print i
        except Exception as e:
            print e

    migrate = Migrate(app, db)
    manager = Manager(app)

    manager.add_command('db', MigrateCommand)
    manager.run()
    """