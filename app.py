#!usr/bin/python

from flask import Flask , render_template , request , redirect , session , abort , url_for , g , flash , jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , login_user  , login_required , logout_user , current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload
import datetime
import re

import copy
# Models
# Flask app intitialization 

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

# SQLAlchemy initialization 
import MySQLdb
db = SQLAlchemy(app)
engine = db.engine
conn = engine.connect()
Base = declarative_base()

from models import login_model

# Hepler functions
from functions import GroupTableCreator , human_format
# # Flask Login Initiialization 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Base route 
@app.route('/' , methods = ['GET' , 'POST'])
@login_required
def index():
    user = current_user.username 
    session['check'] = "a"
    session['check_t'] = "a"
    session['mssg_a'] = None
    session['mssg_b'] = None
    session['mssg_c'] = None
    session['mssg_d'] = None
    session['mssg_e'] = ""
    session['mssg_f'] = ""
    session['mssg_g'] = ""
    session['mssg_h'] = ""
    session['mssg_i'] = ""
    session['mssg_j'] = ""
    session['mssg_t_a'] = ""
    session['mssg_t_b'] = ""
    session['mssg_c_a'] = None
    session['query'] = ""


    contacts = len(db.session.query(login_model.AddContact).all())
    invoices = len(db.session.query(login_model.Invoice).all())
    comms = len(db.session.query(login_model.Comm).all())
    print(contacts)
    

    return render_template('home.html' , user = user , c_len = human_format(contacts) , i_len = human_format(invoices) , com_len = human_format(comms)) , 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    """
    form = login_model.LoginForm()
    mssg = ""

    if form.validate_on_submit():
        user = login_model.User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)

                return redirect(url_for('index'))
            else:
                return render_template('login.html', subtitle="Login", form=form, error_mssg="Invalid Username or Password")
        else:
            return render_template('login.html', subtitle="Login", form=form, error_mssg="Invalid Username or Password")
    return render_template('login.html', subtitle="Login", form=form, error_mssg=mssg), 200


@app.route('/signup' , methods=['GET', 'POST'])
def signup():
    form = login_model.SignupForm()
    mssg = ""
    if form.validate_on_submit():
        user = login_model.User.query.filter_by(email = form.email.data).first()
        if user is None:
            hashed_pass = generate_password_hash(form.password.data , method='sha256')
            new_user = login_model.User(username = form.username.data , email = form.email.data , password = hashed_pass)
            # user_table = UserTableCreator(form.email.data)
            # Base.metadata.create_all(engine)        
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return redirect(url_for('login'))
        else:
            return render_template('signup.html' , form = form ,subtitle = "Signup" ,error_mssg = "Email already exists.")

    return render_template('signup.html' , subtitle = "Signup" , form = form , error_mssg = mssg),200

@app.route('/forgot' , methods=['GET', 'POST'])
def forgot():
    return render_template('login.html' , subtitle = "Forgot"),200


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return login_model.User.query.get(int(user_id))

# Function Routes
@app.route('/user' , methods=['GET' , 'POST'])
@login_required
def user():
    '''
        User setup done here
        - Username
        - Email for sending
        - Delete Account
        - Reset data
        - Export data 
    '''
    user = current_user.username 

    return render_template('settings.html' ,user=user),200


@app.route('/contacts' , methods=['GET' , 'POST'])
@login_required
def contacts():
    '''
        Add contacts to database with option to export 
        and import data onto Peep.

        FIX: add to Groups
    '''
    user = current_user.username 
    form = login_model.AddContactForm()
    form_add_group = login_model.AddGroupForm()
    form_add_group.group.choices = [ (r.id , r.group ) for r in login_model.Group.query.order_by('group') ]
    form_add_group.contact.choices = [ (r.id , r.company_name ) for r in login_model.AddContact.query.order_by('company_name') ]

    if form_add_group.validate_on_submit():
        group = login_model.Group.query.filter_by(id=int(form_add_group.group.data)).first().group
        for x in form_add_group.contact.data:
            sql = 'insert into {}(contact)  values ({})'.format(group , int(x))
            conn.execute(sql )
            conn.close()

    contact_list = db.session.query(login_model.AddContact).all()
    print(contact_list)
    return render_template('contacts.html' , user = user ,form = form , error_mssg_c_a = session['mssg_c_a'] ,
    contact_list = contact_list , form_add_group=form_add_group) , 200

@app.route('/contacts/add' , methods=['POST'])
@login_required
def contacts_add():

    if request.method == 'POST':
        prod_list = list()
        buss_list = list()
        comm_a_list = list()
        comm_b_list = list()
        data = request.get_json()    
        data = data['data']
        for key , value in data.items():
            if (key.find('prod_cat') != -1) :
                prod_list.append(value)
            if (key.find('buss_cat') != -1) :
                buss_list.append(value)
            if (key.find('comm_channel') != -1) :
                comm_a_list.append(value)
            if (key.find('comm_a_cat') != -1) :
                comm_a_list.append(value)
            if (key.find('pref_comm_channel') != -1) :
                comm_b_list.append(value)
            if (key.find('comm_b_channel') != -1) :
                comm_b_list.append(value)  
        
        prod_list = list(set(prod_list))
        buss_list = list(set(buss_list))
        comm_a_list = list(set(comm_a_list))
        comm_b_list = list(set(comm_b_list))
        
        if (False) :
            mssg = "Duplicate data"
            return jsonify({'mssg' : mssg})
        
        else:
            city = login_model.City.query.filter_by(id=int(data['city'])).first()
            new_data = login_model.AddContact(company_name = data['company_name'].upper(),
            company_per = data['company_per'].upper(), contact_one = data['contact_one'], wh_contact = data['wh_contact'],
            email = data['email'],address_one = data['address_one'], address_two = data['address_two'],
            address_three = data['address_three'],address_pin = data['address_pin'] ) 
            
            try:
                db.session.add(new_data)
                new_data.city.append(city)

                for id in buss_list:
                    busscat = login_model.BussCat.query.filter_by(id=int(id)).first()
                    print(busscat.buss_cat)
                    busscat.contact_buss.append(new_data)

                for id in prod_list:
                    prodcat = login_model.ProdCat.query.filter_by(id=int(id)).first()
                    prodcat.contact_prod.append(new_data)      

                for id in comm_a_list:
                    commcat = login_model.CommChannel.query.filter_by(id=int(id)).first()
                    commcat.contact_comm_a.append(new_data) 

                for id in comm_b_list:
                    commcat = login_model.CommChannel.query.filter_by(id=int(id)).first()
                    commcat.contact_comm_b.append(new_data) 

                health_code = login_model.HealthCode.query.filter_by(id=int(data['health_code'])).first()
                health_code.contact_health.append(new_data)

                broker = login_model.Broker.query.filter_by(id=int(data['broker'])).first()
                broker.contact_broker.append(new_data)

                group = login_model.Group.query.filter_by(id=int(data['group'])).first()
                group.contact_group.append(new_data)

                db.session.commit()
                db.session.close()
                mssg = "Data Successfully added 👍"

                # try:
                #     group = login_model.Group.query.filter_by(id=int(data['group'])).first().group
                #     sql = 'insert into {}(contact)  values ({})'.format(group , int(new_data.id))
                #     conn.execute(sql)

                # except Exception as e:
                #     mssg = "Error occured while adding data to Group 😵. Here's the error : "+str(e)
                #     return jsonify({'mssg' : mssg})

                return jsonify({'mssg' : mssg})


            except Exception as e:
                print("Here")
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                return jsonify({'mssg' : mssg})

@app.route('/insights' , methods=['GET' , 'POST'])
@login_required
def insights():
    '''
        Get insights based of various filters 
            - Period
            - Business Category
            - Product dealing IN
            - City
            - State
            - Country
            - Customer Credit Health
            - broker
            - preffered Comm channel
            - no of times comm done
            - No fo Invoice
            - Sales for that user
    '''
    user = current_user.username 
    form = login_model.FilterForm()
    form.buss_cat.choices = [(r.id , r.buss_cat) for r in login_model.BussCat.query.all()]
    form.prod_cat.choices = [(r.id , r.prod_cat) for r in login_model.ProdCat.query.all()]
    form.city.choices = [(r.id , r.city) for r in login_model.City.query.all()]
    form.state.choices = [(r.id , r.state) for r in login_model.State.query.all()]
    form.country.choices = [(r.id , r.country) for r in login_model.Country.query.all()]
    form.broker.choices = [(r.id , r.broker_name) for r in login_model.Broker.query.all()]
    form.health_code.choices = [(r.id , r.health) for r in login_model.HealthCode.query.all()]
    form.comm_channel.choices = [(r.id , r.channel) for r in login_model.CommChannel.query.all()]
    form_save = login_model.FilterSaveForm()
    savedfilters = db.session.query(login_model.FilterSave).all()
    if form.validate_on_submit():
        buss_cat = form.buss_cat.data
        prod_cat = form.prod_cat.data
        broker = form.broker.data
        city = form.city.data
        health_code = form.health_code.data
        comm_channel = form.comm_channel.data
        date_start = form.date_start.data
        date_end = form.date_end.data
        state = form.state.data
        country = form.country.data
        no_invoice = form.no_invoice.data
        amount = form.amount.data
        no_comm = form.no_comm.data
        
        # Building filter lists

        # Bussiness category
        buss_list = list()
        for id in buss_cat:
            buss_list.append(db.session.query(login_model.BussCat).filter_by(id = int(id)).first().buss_cat)
        
        # Product category
        prod_list = list()
        for id in prod_cat:
            prod_list.append(db.session.query(login_model.ProdCat).filter_by(id = int(id)).first().prod_cat)

        # Broker list        
        broker_list = list()
        for id in broker:
            x = db.session.query(login_model.Broker).filter_by(id = int(id)).first().broker_name
            broker_list.append(x)

        city_list = list()
        for id in city:
            city_list.append(db.session.query(login_model.City).filter_by(id = int(id)).first().city)
        
        state_list = list()
        for id in state:
            state_list.append(db.session.query(login_model.State).filter_by(id = int(id)).first().state)
        
        country_list = list()
        for id in country:
            country_list.append(db.session.query(login_model.Country).filter_by(id = int(id)).first().country)
        
        comm_list = list()
        for id in comm_channel:
            comm_list.append(db.session.query(login_model.CommChannel).filter_by(id = int(id)).first().channel)

        hcode_list = list()
        for id in health_code:
            hcode_list.append(db.session.query(login_model.HealthCode).filter_by(id = int(id)).first().health)

        # End filter lists

        # Conditional Queries 

        query =  db.session.query(login_model.AddContact, login_model.Invoice).join(login_model.Invoice)

        if date_start:
            query = query.filter(login_model.Invoice.date >= date_start)
        
        if date_end:
            query = query.filter(login_model.Invoice.date <= date_end)
        
        if broker_list:
            query = query.filter(login_model.AddContact.broker.any(login_model.Broker.broker_name.in_(broker_list)))

        if city_list:
            query = query.filter(login_model.AddContact.city.any(login_model.City.city.in_(city_list)))

        if state_list:
            query = query.filter(login_model.AddContact.city.any(login_model.City.state.in_(state_list)))

        if country_list:
            query = query.filter(login_model.AddContact.city.any(login_model.City.country.in_(country_list)))

        if comm_list:
            query = query.filter(login_model.AddContact.comm_channel.any(login_model.CommChannel.channel.in_(comm_list)))

        if hcode_list:
            query = query.filter(login_model.AddContact.health_code.any(login_model.HealthCode.health.in_(hcode_list)))

        if buss_list:
            query = query.filter(login_model.AddContact.buss_cat.any(login_model.BussCat.buss_cat.in_(buss_list)))

        if prod_list:
            query = query.filter(login_model.AddContact.prod_cat.any(login_model.ProdCat.prod_cat.in_(prod_list)))

        if amount:
            query = query.filter(login_model.Invoice.amount >= amount)

        
        results = query.all()
        
        if no_comm:
            pass

        if no_invoice:
            ref_list = {}
            for x in query:
                if x[0] in ref_list:
                    ref_list[x[0]] = ref_list[x[0]]+1
                else:
                    ref_list[x[0]] = 1

            for key in ref_list:
                if int(ref_list[key]) >= int(no_invoice):
                    pass
                else:
                    for item in results:
                        print(item[0])
                        if str(key) == str(item[0]):
                            results.remove(item)

        chart_insights = []
        session['query'] = str(query)
        filter_con = len(set([x[0] for x in results ]))
        total_con = db.session.query(login_model.AddContact).count()
        total_rev_t =[x.amount for x in db.session.query(login_model.Invoice).all()]
        total_rev = 0
        for t in total_rev_t:
            total_rev = int(t)+total_rev
        
        filter_rev= sum( [ x[1].amount for x in results])
    
        chart_insights.append(filter_con)
        chart_insights.append(total_con)
        chart_insights.append(filter_rev)
        chart_insights.append(total_rev)

        db.session.close()

        return render_template('insights.html' , user = user , form_save = form_save  , filter_list = results , form = form , chart_insights = chart_insights , savedfilters = savedfilters) , 200
    
    else:  # You only want to print the errors since fail on validate
        print(form.errors) 

    return render_template('insights.html' , user = user , form = form , form_save = form_save , savedfilters = savedfilters) , 200

@app.route('/insights/save' , methods = ['POST'])
@login_required
def filter_save():
    if request.method == 'POST':
        data = request.get_json()    
        data = data['data']['name']
        print(data)
        temp = login_model.FilterSave(report_name = data , query = session['query'])
        db.session.add(temp)
        db.session.commit()
        return jsonify({"mssg" :"Report saved"})

@app.route('/insights/view/<r_id>' , methods= ['GET' , 'POST'])
@login_required
def view_report(r_id):
    print(r_id)
    user = current_user.username

    data_query = db.session.query(login_model.FilterSave).filter( login_model.FilterSave.id == int(r_id)).first().query
    results = engine.execute(text(data_query))
    print(results)    
    return render_template('view_insights.html' , user = user , filter_list = results ,chart_insights = chart_insights ) , 200

@app.route('/transaction' , methods=['GET' , 'POST'])
@login_required
def transaction():
    user = current_user.username 
    mssg = ""
    form_invoice = login_model.InvoiceForm()    
    invoice_list = db.session.query(login_model.Invoice).all()

    form_comm = login_model.CommForm()
    comm_list = db.session.query(login_model.Comm).all()

    form_comm.comm_channel.choices = [ (r.id , r.channel ) for r in login_model.CommChannel.query.order_by('channel') ]
    form_comm.group.choices = [ (r.id , r.group ) for r in login_model.Group.query.order_by('group') ]

   
    if form_comm.validate_on_submit():
        mssg = ""
        session['check_t'] = 'b'
        session['mssg_t_b'] = mssg

        comm_channel = login_model.CommChannel.query.filter_by(id=int(form_comm.comm_channel.data)).first().channel
        group = login_model.Group.query.filter_by(id=int(form_comm.group.data)).first().group
        print(comm_channel)
        date_new = datetime.date(int(form_comm.date.data.split('-')[0]),int(form_comm.date.data.split('-')[1]),int(form_comm.date.data.split('-')[2]))
        new_data = login_model.Comm(comm_channel=comm_channel , mssg_detail = form_comm.mssg_detail.data, 
            date = date_new  , group = group)  
        print(new_data)
        try:
            print('Going In')
            db.session.add(new_data)
            print('Going 2')
            db.session.commit()
            print('Going 3')
            db.session.close()  

            mssg = "Data Successfully added 👍"
            session['mssg_t_b'] = mssg
            
            return redirect(url_for('transaction'))
   
        except Exception as e:
            mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
            session['mssg_t_b'] = mssg
            return redirect(url_for('transaction'))
    
        
        if session['check_t']:
            pass
        else:
            session['check_t'] = 'a'

    else:
        print(form_comm.errors)

    return render_template('transaction.html' , user = user ,form_invoice = form_invoice, form_comm = form_comm,
    commlist = comm_list ,invoicelist = invoice_list , check =session['check_t'] , error_mssg_t_a = session['mssg_t_a'] ,error_mssg_t_b = session['mssg_t_b'] ) , 200

@app.route('/transaction/invoice' , methods=['GET' , 'POST'])
@login_required
def transaction_invoice():
    # FIX : Convert to Validate_on_submit
    session['check_t'] = 'a'
    prod = login_model.Invoice.query.filter_by(invoice_no=request.form['invoice_no'].upper()).first()
    if prod :
        mssg = "Duplicate Data "
        session['mssg_t_a'] = mssg
        return redirect(url_for('basic_master'))

    else:
        firm = login_model.Firm.query.filter_by(id=int(request.form['firm'])).first()
        print(firm)
        date_new = datetime.date(int(request.form['date'].split('-')[0]),int(request.form['date'].split('-')[1]),int(request.form['date'].split('-')[2]))
        try:
            contact = login_model.AddContact.query.filter_by(id=int(request.form['company_name'])).first()
            new_data = login_model.Invoice(invoice_no=request.form['invoice_no'].upper() , amount = request.form['amount'] , date = date_new )
            contact.invoice.append(new_data)  
            firm.invoice.append(new_data)
            db.session.add(new_data)
            db.session.commit()
            mssg = "Data Successfully added 👍"
            session['mssg_t_a'] = mssg
            db.session.close()

            return redirect(url_for('transaction'))

        
        except Exception as e:
            mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
            session['mssg_t_a'] = mssg
            print(mssg)
            return redirect(url_for('transaction'))



@app.route('/basic_master' , methods=['GET' , 'POST'])
@login_required
def basic_master():
    '''
        Basic master setup done here
    '''
    mssg = ""
    user = current_user.username 
    form_broker = login_model.BrokerForm()
    form_comm = login_model.CommChannelForm()
    form_health = login_model.HealthCodeForm()
    form_prod = login_model.ProdCatForm()
    form_buss = login_model.BussCatForm()
    form_state = login_model.StateForm()
    form_country = login_model.CountryForm()
    form_city = login_model.CityForm()
    form_firm = login_model.FirmForm()
    form_group = login_model.GroupForm()


    prod_list = db.session.query(login_model.ProdCat).all()
    health_list = db.session.query(login_model.HealthCode).all()
    commlist = db.session.query(login_model.CommChannel).all()
    busslist = db.session.query(login_model.BussCat).all()
    broklist = db.session.query(login_model.Broker).all()
    statelist = db.session.query(login_model.State).all()
    countrylist = db.session.query(login_model.Country).all()
    citylist = db.session.query(login_model.City).all()
    firmlist = db.session.query(login_model.Firm).all()
    grouplist = db.session.query(login_model.Group).all()

    # Form choices for select fields

    if form_comm.validate_on_submit():
        # Checks for Comm submit 
        mssg = ""
        session['check'] = 'd'
        session['mssg_d'] = mssg
        prod = login_model.CommChannel.query.filter_by(channel=form_comm.channel.data).first()
        if prod :
            mssg = "Duplicate Data "
            session['mssg_d'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.CommChannel(channel=form_comm.channel.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_d'] = mssg
                db.session.close()
                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_d'] = mssg
                return redirect(url_for('basic_master'))


    if form_health.validate_on_submit():
        # Checks for health code submit 
        mssg = ""
        session['check'] = 'b'
        session['mssg_b'] = mssg

        prod = login_model.HealthCode.query.filter_by(health=form_health.health.data).first()
        if prod :
            mssg = "Duplicate Data "
            session['mssg_b'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.HealthCode(health=form_health.health.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_b'] = mssg        
                db.session.close()
                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_b'] = mssg
                return redirect(url_for('basic_master'))

    if form_prod.validate_on_submit():
        mssg = ""
        session['check'] = 'a'
        session['mssg_a'] = mssg
        prod = login_model.ProdCat.query.filter_by(prod_cat=form_prod.prod_cat.data).first()

        if prod :
            mssg = "Duplicate Data "
            session['mssg_a'] = mssg

            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.ProdCat(prod_cat = form_prod.prod_cat.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_a'] = mssg
                db.session.close()
                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_a'] = mssg       
                return redirect(url_for('basic_master'))

    if form_buss.validate_on_submit():
        # Checks for Bussiness Category submit
        mssg = ""
        session['check'] = 'e'
        session['mssg_e'] = mssg

        prod = login_model.BussCat.query.filter_by(buss_cat=form_buss.buss_cat.data).first()

        if prod :
            mssg = "Duplicate Data "
            session['mssg_e'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.BussCat(buss_cat = form_buss.buss_cat.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_e'] = mssg
                db.session.close()
                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_e'] = mssg
                return redirect(url_for('basic_master'))

    if form_state.validate_on_submit():
        # Checks for Location submit
        mssg = ""
        session['check'] = 'f'
        session['mssg_f'] = mssg

        prod = login_model.State.query.filter_by(state=form_state.state.data).first()

        if prod :
            mssg = "Duplicate Data "
            session['mssg_f'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.State(state=form_state.state.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_f'] = mssg
                db.session.close()

                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_f'] = mssg
                return redirect(url_for('basic_master'))

    if form_country.validate_on_submit():
        # Checks for Location submit
        session['check'] = 'g'
        mssg = ""
        session['mssg_g'] = mssg
        prod = login_model.Country.query.filter_by(country=form_country.country.data).first()

        if prod :
            mssg = "Duplicate Data "
            session['mssg_g'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.Country(country=form_country.country.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_g'] = mssg
                db.session.close()

                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_g'] = mssg
                return redirect(url_for('basic_master'))
    
    if form_firm.validate_on_submit():
        # Checks for Location submit
        mssg = ""
        session['check'] = 'i'
        session['mssg_i'] = mssg

        prod = login_model.Firm.query.filter_by(firm=form_firm.firm.data).first()

        if prod :
            mssg = "Duplicate Data "
            session['mssg_i'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.Firm(firm=form_firm.firm.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                session['mssg_i'] = mssg
                db.session.close()

                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_i'] = mssg
                return redirect(url_for('basic_master'))
    
    if form_group.validate_on_submit():
        # Checks for Location submit
        session['check'] = 'j'

        prod = login_model.Group.query.filter_by(group=form_group.group.data).first()

        if prod :
            mssg = "Duplicate Data "
            session['mssg_j'] = mssg
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.Group(group=form_group.group.data.upper())  
            GroupTableCreator(form_group.group.data.upper())
            try:
                db.session.add(new_data)
                db.session.commit()
                Base.metadata.create_all(engine)
                mssg = "Data Successfully added 👍"
                session['mssg_j'] = mssg
                db.session.close()

                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                session['mssg_j'] = mssg
                return redirect(url_for('basic_master'))
    
    if session['check']:
        pass
    else:
        session['check'] = 'a'

    return render_template('basic_master.html' , user = user , 
        form_broker = form_broker , form_buss = form_buss , form_comm = form_comm ,
        form_health = form_health , form_state = form_state , form_prod = form_prod ,
        form_country = form_country , form_city = form_city , error_mssg = mssg ,
        form_firm = form_firm , form_group = form_group , firmlist = firmlist , grouplist = grouplist,
        subtitle = "Basic Master" , plist = prod_list , hlist = health_list ,
        commlist = commlist , busslist = busslist , broklist = broklist ,
        statelist = statelist , countrylist = countrylist , citylist = citylist ,
        check = session['check'] , error_mssg_d = session['mssg_d'] ,
        error_mssg_a = session['mssg_a'] ,error_mssg_b = session['mssg_b'] ,
        error_mssg_c = session['mssg_c'] ,error_mssg_e = session['mssg_e'] ,
        error_mssg_f = session['mssg_f'] ,error_mssg_g = session['mssg_g'] ,
        error_mssg_h = session['mssg_h'] , error_mssg_i = session['mssg_i'] ,
        error_mssg_j = session['mssg_j']) , 200


@app.route('/city_form' , methods= ['GET' , 'POST'])
@login_required
def city_form():
    # UP : Work on securing this route
    session['check'] = 'h'
    mssg = ""
    session['mssg_h'] = mssg

    prod = login_model.City.query.filter_by(city=request.form['city']).first()
    if prod :
            mssg = "Duplicate Data "
            session['mssg_h'] = mssg
            db.session.close()
                
            return redirect(url_for('basic_master'))
    else:
        state = login_model.State.query.filter_by(id=int(request.form['state'])).first().state
        country = login_model.Country.query.filter_by(id=int(request.form['country'])).first().country
        new_data = login_model.City(city=request.form['city'].upper() , state = state ,
        country = country ) 

        try:
            db.session.add(new_data)
            db.session.commit()
            mssg = "Data Successfully added 👍"
            session['mssg_h'] = mssg
            db.session.close()
                
            return redirect(url_for('basic_master'))


        except Exception as e:
            mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
            session['mssg_h'] = mssg
            return redirect(url_for('basic_master'))

@app.route('/broker_form' , methods= ['GET' , 'POST'])
@login_required
def broker_form():
    # UP : Work on securing this route
    session['check'] = 'c'
    mssg = ""
    session['mssg_c'] = mssg
    prod = login_model.Broker.query.filter_by(broker_name=request.form['broker_name'].upper()).first()
    prod_a = login_model.Broker.query.filter_by(contact=request.form['contact']).first()

    if prod and prod_b:
            mssg = "Duplicate Data "
            session['mssg_c'] = mssg
            print(mssg)
            return redirect(url_for('basic_master'))
    else:
        query = login_model.City.query.filter_by(id=int(request.form['city'])).first()
        new_data = login_model.Broker(broker_name=request.form['broker_name'].upper() ,
                   contact = request.form['contact'] ) 
        try:
            db.session.add(new_data)
            query.broker.append(new_data)
            db.session.commit()
            mssg = "Data Successfully added 👍"
            session['mssg_c'] = mssg
            print(mssg)
            db.session.close()
                
            return redirect(url_for('basic_master'))


        except Exception as e:
            print(e)
            mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
            session['mssg_c'] = mssg
            return redirect(url_for('basic_master'))

@app.route('/delete_session_mssg/<mssg>' , methods=['POST'])
@login_required
def delete_session_mssg(mssg):
    session[mssg] = ''
    return jsonify({'mssg' :'Emptying session mssg t_a' })

################## Delete & Edit Production category Routes ################
#############################################################################


@app.route('/delete/product/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_prod(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'a'
    login_model.ProdCat.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_a'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/product/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_prod(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'a'
    temp = login_model.ProdCat.query.filter_by(id=int(item_id)).first()
    temp.prod_cat = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    db.session.close()
                
    session['mssg_a'] = mssg

    return redirect(url_for('basic_master'))


################## Delete & Edit Comm Channels Routes ################
#############################################################################


@app.route('/delete/comm/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_comm(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'd'
    login_model.CommChannel.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    db.session.close()
                
    session['mssg_d'] = mssg

    return redirect(url_for('basic_master'))

@app.route('/edit/comm/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_comm(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'd'
    
    temp = login_model.CommChannel.query.filter_by(id=int(item_id)).first()
    temp.channel = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_d'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit Credit Health Routes ################
#############################################################################


@app.route('/delete/health/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_health(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'b'
    login_model.HealthCode.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_b'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/health/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_health(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'b'
    temp = login_model.HealthCode.query.filter_by(id=int(item_id)).first()
    temp.health = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_b'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit Bussniess Category Routes ################
#############################################################################


@app.route('/delete/buss/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_buss(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'e'
    login_model.BussCat.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_e'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/buss/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_buss(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'e'
    temp = login_model.BussCat.query.filter_by(id=int(item_id)).first()
    temp.buss_cat = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_e'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit State Routes ################
#############################################################################


@app.route('/delete/state/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_state(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'f'
    login_model.State.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_f'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/state/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_state(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'f'

    temp = login_model.State.query.filter_by(id=int(item_id)).first()
    temp.state = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_f'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))


################## Delete & Edit Country Routes ################
#############################################################################


@app.route('/delete/country/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_country(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'g'
    login_model.Country.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_g'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/country/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_country(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'g'
    temp = login_model.Country.query.filter_by(id=int(item_id)).first()
    temp.country = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_g'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit City Routes ################
#############################################################################


@app.route('/delete/city/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_city(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'h'
    login_model.City.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_h'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/city/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_city(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'h'    
    temp = login_model.City.query.filter_by(id=int(item_id)).first()
    temp.city = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_h'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit Broker Routes ################
#############################################################################


@app.route('/delete/broker/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_broker(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'c'
    login_model.Broker.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_c'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/broker/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_broker(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'c'
    temp = login_model.Broker.query.filter_by(id=int(item_id)).first()
    temp.broker_name = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_c'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit Firm Routes ################
#############################################################################


@app.route('/delete/firm/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_firm(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'i'
    login_model.Firm.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_i'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/firm/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_firm(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'i'

    temp = login_model.Firm.query.filter_by(id=int(item_id)).first()
    temp.firm = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_i'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit Group Routes ################
#############################################################################


@app.route('/delete/group/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_group(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    session['check'] = 'j'
    login_model.Group.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_j'] = mssg
    db.session.close()
                
    return redirect(url_for('basic_master'))

@app.route('/edit/group/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_group(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    session['check'] = 'j'

    temp = login_model.Group.query.filter_by(id=int(item_id)).first()
    temp.group = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited"
    session['mssg_j'] = mssg 
    db.session.close()
                
    return redirect(url_for('basic_master'))

################## Delete & Edit Invoice Routes ################
################################################################


@app.route('/delete/invoice/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_invoice(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    login_model.Invoice.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_t_a'] = mssg
    session['check'] = 'a'
    db.session.close()
                
    return redirect(url_for('transaction'))

@app.route('/edit/invoice/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_invoice(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    # session['check'] = 'j'

    temp = login_model.Invoice.query.filter_by(id=int(item_id)).first()
    temp.invoice_no = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_t_a'] = mssg
    session['check'] = 'a'
    db.session.close()
                
    return redirect(url_for('transaction'))

################## Delete & Edit Contact Routes ################
################################################################


@app.route('/delete/contact/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_contact(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    login_model.AddContact.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_c_a'] = mssg
    session['check'] = 'a'
    db.session.close()
                
    return redirect(url_for('contacts'))

@app.route('/edit/contact/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_contact(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    temp = login_model.AddContact.query.filter_by(id=int(item_id)).first()
    temp.company_name = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_c_a'] = mssg
    session['check'] = 'a'
    db.session.close()
                
    return redirect(url_for('contacts'))

################## Delete & Edit Transaction Communication Routes ################
################################################################


@app.route('/delete/comm_adv/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_comm_adv(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    login_model.Comm.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    session['mssg_t_b'] = mssg
    session['check'] = 'b'
    db.session.close()
                
    return redirect(url_for('transaction'))

@app.route('/edit/comm_adv/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_comm_adv(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    temp = login_model.Comm.query.filter_by(id=int(item_id)).first()
    temp.company_name = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    session['mssg_t_b'] = mssg
    session['check'] = 'b'
    db.session.close()
                
    return redirect(url_for('transaction'))
