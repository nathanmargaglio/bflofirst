from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import string

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:margaglio22@127.0.0.1:3307/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
else:
    db = SQLAlchemy()

class Parcel(db.Model):
    # Parcel information obtainable via Erie County Parcel Search
    # http://www2.erie.gov/ecrpts/index.php?q=real-property-parcel-search
    # Presumably, every parcel in Erie County is available on here,
    # so using this as a 'base' class is appropriate
    
    __tablename__ = 'parcels'
    
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    
    parcel_status = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    sbl = db.Column(db.String(128), nullable=True)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    
    owner_street = db.Column(db.String(128), nullable=True)
    owner_city = db.Column(db.String(128), nullable=True)
    owner_zip = db.Column(db.String(128), nullable=True)
    
    prop_location = db.Column(db.String(128), nullable=True)
    mailing_address = db.Column(db.String(128), nullable=True)
    prop_class = db.Column(db.String(128), nullable=True)
    
    assessment = db.Column(db.Integer, nullable=True)
    taxable = db.Column(db.Integer, nullable=True)
    
    desc = db.Column(db.String(128), nullable=True)
    deed_book = db.Column(db.Integer, nullable=True)
    deed_page = db.Column(db.Integer, nullable=True)
    
    frontage = db.Column(db.Integer, nullable=True)
    depth = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    sqft = db.Column(db.Integer, nullable=True)
    beds = db.Column(db.Integer, nullable=True)
    baths = db.Column(db.Integer, nullable=True)
    fireplace = db.Column(db.Integer, nullable=True)
    school = db.Column(db.String(128), nullable=True)
    
    village = db.Column(db.String(128), nullable=True)
    swis = db.Column(db.Integer, nullable=True)
    acres = db.Column(db.Integer, nullable=True)
    
    owner_notes = db.Column(db.String(128), nullable=True)
    
    def __repr__(self):
        return str(self.prop_location)
    
class Owner(db.Model):
    # This is Owner information related to any parcel in our database.
    # This information is aggregated across the board, so the information
    # may not be consistent.  In any case, info related to a specific
    # individual is stored here.
    
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    first = db.Column(db.String(128), nullable = True)
    middle = db.Column(db.String(128), nullable = True)
    last = db.Column(db.String(128), nullable = True)
    
    phone = db.Column(db.String(128), nullable = True)
    email = db.Column(db.String(128), nullable = True)
    
    checked_yp = db.Column(db.Boolean, default=False)
    checked_number = db.Column(db.Boolean, default=False)
    # assume number is bad until checked
    phone_status = db.Column(db.String(128), nullable=True)
    
    #parcel_id = db.Column(db.Integer, db.ForeignKey('parcels.id'))
    listings = db.relationship('Listing', backref='owner', cascade="all, delete-orphan", lazy='dynamic')
    parcels = db.relationship('Parcel', backref='owner', cascade="all, delete-orphan", lazy='dynamic')
    

# [START model]

class Listing(db.Model):
    # This is for Listing information.  This is to organize parcel/owner
    # information temporally (i.e., an owner may have lived in more than
    # one house over some span of time).  This is raw, so that this
    # information is collected via the MLS, then organized later.
    
    __tablename__ = 'listings'

    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    #parcel = db.relationship('Parcel', cascade="all, delete-orphan", backref='listing')
    
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
    
    #owner = db.relationship('Owner', backref='listing', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    o1fn = db.Column(db.String(128), nullable=True)
    o1ln = db.Column(db.String(128), nullable=True)
    o1mi = db.Column(db.String(128), nullable=True)
    #checked_yp = db.Column(db.Boolean, default=False)
    #o1phone = db.relationship('PhoneNumber', backref='owner', lazy='dynamic')
    
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
    
    strings = {'ML #':'ml', 'Address':'address', 'St':'status','School District Name':'scl_dis',
                   'Street Name':' stname', 'Town/City':'city', 
                   'Owner 1 First Name':'o1fn', 'Owner 1 Last Name':'o1ln',
                   'Owner 2 First Name':'o2fn', 'Owner 2 Last Name':'o2ln',
                   'Owner 1 Middle Initial':'o1mi', 'Owner 2 Middle Initial':'o2mi',
                   'Owner City State':'ocit_state', 'Owner Street Num Street Name':'osnumsname',
                   'Parcel Number':'parcel_num', 'List Agent Direct Work Phone':'ladwp',
                   'List Agent Email':'laemail', 'List Agent Full Name':'lafulln',
                   'List Agent MLSID':'lamlsid', 'List Office MLSID':'lomsid',
                   'List Office Name':'loname', 'List Office Phone':'lophone'}
    
    numbers = {'Current Price':'cur_pri', 'List Price':'lis_pri', 'Sq Ft Total':'sqft', 
               'Num Fireplaces Total ':'fire', 'Baths Total':'bths', 'Beds Total':'beds',
               'Year Built':'year', 'Lot Dimensions Depth':'dpth', 'Lot Dimensions Frontage':'frnt',
               'City Village Tax':'ctax', 'School Tax':'stax', 'Total Taxes':'ttax',
               'Town County Tax':'tctax', 'Street Number':'stnum', 'Zip Code':'zipc', 'DOM':'dom'}
    
    dates = {'Expiration Date':'exp_date', 'List Date':'listdate'}
    
    fields = dict(strings.items()+numbers.items()+dates.items())
    
    def __getitem__(self, arg):
        return str(getattr(self, self.fields[arg]))
    
    def __setitem__(self,key,value):
        setattr(self,self.fields[key],value)


    def str_to_num(self, field):
        rem = ['$',',']
        rem += list(string.ascii_lowercase)
        rem += list(string.ascii_uppercase)
        try:
            return int(str(field).translate(None, ''.join(rem)))
        except:
            return None
    
    def addViaRow(self,row):
        import pandas as pd
        for k in self.strings:
            self[k] = row[k]
        
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
    
class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(1024))
    store = db.Column(db.String(64))
    admin = db.Column(db.Boolean, default=False)
    
    def set_email(self,email):
        self.email = email
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def set_store(self, store):
        self.store = store
    
    def check_password(self,password):
        return check_password_hash(self.password,password)
        
    def __repr__(self):
        return "<"+self.email+">"
        
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
    
class FacebookLead(db.Model):
    __tablename__="facebook_lead"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    notes = db.Column(db.String(512), nullable=True)
    date_added = db.Column(db.Date)
    
    #From CSV v
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
    
class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
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
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    key = db.Column(db.String(128), nullable=True)
    owner = db.Column(db.String(128), nullable=True)
    book_date = db.Column(db.String(128), nullable=True)
    date = db.Column(db.Date, nullable=True)
    

class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    time = db.Column(db.DateTime)
    user = db.Column(db.String(128), db.ForeignKey('users.email'))
    info = db.Column(db.String(512))
    
class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    time = db.Column(db.DateTime)
    user = db.Column(db.String(128), db.ForeignKey('users.email'))
    message = db.Column(db.String(512))
    
if __name__=="__main__":
    db.create_all()
    """
    migrate = Migrate(app, db)
    manager = Manager(app)
    
    manager.add_command('db', MigrateCommand)
    manager.run()
    """