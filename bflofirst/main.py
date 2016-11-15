from flask import (Flask,  g,  render_template,  request,  Response,
                   redirect,  url_for,  jsonify,  flash,  session)
from flask_login import (LoginManager,  current_user,  login_required, 
                            login_user,  logout_user,  UserMixin, 
                            confirm_login,  fresh_login_required, 
                            AnonymousUserMixin)
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from models import Owner, Listing, Parcel, User, Log, db
import time
import random
import zipfile
from io import BytesIO
import os
from config import local_cities, admins, example_streets
import datetime

def dev_mode():
    return os.environ['SERVER_SOFTWARE'].startswith('Development')

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SERVER_NAME'] = 'buffalodataserver.com'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:margaglio22@/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'
if dev_mode():
    app.config['SERVER_NAME'] = 'localhost:8080'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:margaglio22@127.0.0.1:3307/bflofirstdb?unix_socket=/cloudsql/bravofoxtrot-141119:us-central1:bflofirstdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user = db.session.query(User).filter(User.email==user_id).first()
    except:
        user = AnonymousUserMixin
    return user

@app.after_request
def after_request(r):
    try:
        email = current_user.email
        l = Log()
        l.user = email
        l.info = request.url
        l.time = datetime.datetime.now()
        db.session.add(l)
        db.session.commit()
    except:
        pass
    return r

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    flash("You are logged in as {}".format(current_user.email))
    return render_template("index_b.html")

@app.route('/labels', methods=['GET', 'POST'])
def labels():
    if request.args.get('start_index'):
        ind0 = int(request.args.get('start_index'))
    else:
        ind0 = 0
    
    query = Listing.query.filter(Listing.status == 'X').filter(Listing.city.in_(local_cities))
    
    if request.args.get('fresh'):
        if request.args.get('fresh') == 'true':
            query = query.filter(Listing.mailed == False or Listing.mailed == None)
    
    try:
        if request.args.get('from'):
            from_day = request.args.get('from')
            query = query.filter(Listing.exp_date >= datetime.datetime.strptime(from_day, '%m-%d-%y'))
        
        if request.args.get('to'):
            to_day = request.args.get('to')
            query = query.filter(Listing.exp_date <= datetime.datetime.strptime(to_day, '%m-%d-%y'))
    except:
        flash("Incorrect Date Format.  Use 'm-d-y' (i.e., 10-03-94)")
        return redirect(url_for('index'))
    
    exp = query.order_by(Listing.exp_date.desc()).all()
    data = []
    ind = 0
    for y in range(20):
        data.append([])
        for x in range(4):
            data[y].append([])
            if ind < ind0:
                data[y][x] = False
                ind += 1
                continue
            try:
                lis = exp[ind-ind0]
                data[y][x].append("CURRENT RESIDENT")
                data[y][x].append(lis.address)
                data[y][x].append(lis.city+", NY " + str(lis.zipc))
            except:
                data[y][x] = False
            ind += 1
            
    return render_template("labels.html", data=data)


@app.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
    if current_user.email not in admins:
        flash("You cannot access this page without permission")
        return render_template("index.html")
    
    ret = []
    
    count = 0
    for l in Log.query.order_by(Log.time.desc()).all():
        if l.user != "nathanmargaglio@gmail.com":
            ret.append(l)
            count += 1
            if count > 50:
                break
    return render_template('logs.html', entries=ret)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.query.filter(User.email==email).first()
            if user.check_password(password):
                login_user(user, remember=True)
                db.session.commit()
                return redirect(url_for('index'))
            flash("Incorrect Credentials.  Try Again.")
        except:
            flash("This user doesn't seem to exist.")
        
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('login_b.html')
    
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if User.query.filter(User.email==email).first():
            flash("This email is already registered.  Try again.")
            return render_template('register.html')
        
        if password != confirm:
            flash("Your password didn't match your confirmation.  Try again.")
        
        user = User()
        user.set_email(email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Successfully Registered!  Please Login.")
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    return redirect(url_for('index'))

@app.route('/form', methods=['GET','POST'])
def form_page():
    return render_template("form.html")

@app.route('/test', methods=['GET','POST'])
def test_page():
    return render_template("test.html")

@app.route('/_update')
def _update():
    t = request.args.get('t')
    r = request.args.get('r')
    i = request.args.get('i')

    if t == "result":
        owner = Owner.query.filter(Owner.id == i).first()
        if r == 'true': 
            r = True
        else: 
            r = False
        owner.checked_number = r
        db.session.add(owner)
        db.session.commit()
        
    if t == "notes":
        listing = Listing.query.filter(Listing.id == i).first()
        listing.notes = r
        db.session.add(listing)
        db.session.commit()
    
    return jsonify(res = "success")

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/expires', methods=["GET", "POST"])
@login_required
def expires():
    page = request.args.get('page')
    if not page:
        page = 0
    
    working_list = Listing.query.join(Owner)
    
    cont_params = ""
    
    if request.args.get('expired'):
        working_list = working_list.filter(Listing.status == 'X')
        cont_params += "&expired="+request.args.get('expired')
        
    if request.args.get('phone'):
        working_list = working_list.filter(Owner.phone != None)
        cont_params += "&phone="+request.args.get('phone')

    if request.args.get('locality'):
        working_list = working_list.filter(Listing.city.in_(local_cities))
        cont_params += "&locality="+request.args.get('locality')

    entry_list = working_list.order_by(Listing.exp_date.desc()).all()
    return render_template("results.html", page=int(page), params = cont_params, max_page=int(len(entry_list)/25.), entries=entry_list[25*int(page):25*(int(page)+1)])

