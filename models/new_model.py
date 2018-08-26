class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broker_name = db.Column(db.String(30), nullable=False)
    contact =  db.Column(db.String(30), nullable=False)

    city = db.relationship('City' , secondary='broker_city' , backref='broker' , lazy = 'dynamic')

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), unique=True, nullable=False)
    

db.Table('broker_city',
    db.Column('broker_id' , db.Integer , db.ForeignKey('broker.id')),
    db.Column('city_id' , db.Integer , db.ForeignKey('city.id'))
    )

class Invoice(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    invoice_no = db.Column(db.Integer)
    contact_id = db.Column(db.Integer , db.ForeignKey('contact.id'))
    firm = db.Column(db.Integer , db.ForeignKey('firm.id'))

class Comm(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    comm_channel = db.Column(db.Integer , db.ForeignKey('comm_channel.id') )
    mssg_detail = db.Column(db.String(100))
    group = db.Column(db.Integer , db.ForeignKey('group.id'))
    date = db.Column(db.Date)

class Contact(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    company_name = db.Column(db.String(50))
    company_per = db.Column(db.String(50))
    contact_one = db.Column(db.String(20) , nullable = True)
    wh_contact = db.Column(db.String(20) , nullable = True)
    email = db.Column(db.String(50) , unique = True , nullable = True)
    address_one = db.Column(db.String(100))
    address_two = db.Column(db.String(100))
    address_three = db.Column(db.String(100))
    address_pin = db.Column(db.String(10))
    
    
    city = db.relationship('City' , secondary='contact_city' , backref='contact' , lazy = 'dynamic')
    buss_cat = db.relationship('BussCat' , secondary='contact_buss' , backref='contact' , lazy = 'dynamic')
    prod_cat = db.relationship('ProdCat' , secondary='contact_prod' , backref='contact' , lazy = 'dynamic')
    broker = db.relationship('Broker' , secondary='contact_broker' , backref='contact' , lazy = 'dynamic')
    comm_channel = db.relationship('CommChannel' , secondary='contact_comm_a' , backref='contact' , lazy = 'dynamic')
    health_code = db.relationship('HealthCode' , secondary='contact_health' , backref='contact' , lazy = 'dynamic')
    pref_comm_channel = db.relationship('CommChannel' , secondary='contact_comm_b' , backref='contact' , lazy = 'dynamic')
    group = db.relationship('Group' , secondary='contact_group' , backref='contact' , lazy = 'dynamic')
    invoice = db.relationship('Invoice' , backref="contact" , lazy='dynamic')

class CommChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(30), unique=True, nullable=False) 

db.Table('contact_comm_a',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('channel_id' , db.Integer , db.ForeignKey('comm_channel.id'))
)

db.Table('contact_comm_b',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('channel_id' , db.Integer , db.ForeignKey('comm_channel.id'))
)

db.Table('contact_city',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('city_id' , db.Integer , db.ForeignKey('city.id'))
    )

db.Table('contact_buss',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('buss_id' , db.Integer , db.ForeignKey('buss_cat.id'))
    )

db.Table('contact_prod',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('prod_id' , db.Integer , db.ForeignKey('prod_cat.id'))
    )

db.Table('contact_broker',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('broker_id' , db.Integer , db.ForeignKey('broker.id'))
    )

db.Table('contact_health',
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('health_id' , db.Integer , db.ForeignKey('health_code.id'))
    )

db.Table('contact_group', 
    db.Column('contact_id' , db.Integer , db.ForeignKey('contact.id')),
    db.Column('group_id' , db.Integer , db.ForeignKey('group.id'))
)