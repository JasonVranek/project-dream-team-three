from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Customer(UserMixin, db.Model):
    """
    Create a Employee table
    """
    __tablename__ = 'customers'

    c_id = db.Column('CustomerID', db.Integer, primary_key=True)
    acc_code = db.Column('Account Code', db.String(20), unique=True, nullable=False)
    comp_name = db.Column('CompanyName', db.String(20))
    f_name = db.Column('ContactFirstName', db.String(20))
    l_name = db.Column('ContactLastName', db.String(20))
    b_address = db.Column('BillingAddress', db.String(40))
    city = db.Column('City', db.String(20))
    state_province = db.Column('StateOrProvince', db.String(20))
    post_code = db.Column('PostalCode', db.String(10))
    count_region = db.Column('Country/Region', db.String(20))
    cont_title = db.Column('ContactTitle', db.String(30))
    phone = db.Column('PhoneNumber', db.String(20))
    fax = db.Column('FaxNumber', db.String(20))
    email = db.Column('EmailAddress', db.String(20), unique=True)
    notes = db.Column('Notes', db.String(100))
    order = db.Column('Order', db.String(50))
    state = db.Column('State', db.String(50))
    status = db.Column('Status', db.String(50))
    rating = db.Column('Rating', db.String(50))

    quotations = db.relationship('Quotation', backref='customer',
                                lazy='dynamic')

    def __repr__(self):
        return '<Customer: {}>'.format(self.c_id)


class Quotation(UserMixin, db.Model):
    """
    Create a Quotation table
    """
    __tablename__ = 'quotations'

    q_id = db.Column('QuotationID', db.Integer, primary_key=True)  # FOREIGN KEY PARENT OF QUOTATION DETAILS AND OPPORTUNITIES
    c_id = db.Column('CustomerID', db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)                           # FOREIGN KEY CHILD OF CUSTOMERS: CustomerID
    e_id = db.Column('EmployeeID', db.Integer)
    date = db.Column('Quotaton Date', db.String(50))
    q_num = db.Column('Quotation Number', db.Integer)
    revision = db.Column('Revision', db.String(50))
    pay_terms = db.Column('Payment Terms', db.String(50))
    title = db.Column('Title', db.String(50))
    f_name = db.Column('FirstName', db.String(50))
    l_name = db.Column('LastName', db.String(50))
    address = db.Column('Address', db.String(50))
    city = db.Column('City', db.String(50))
    state = db.Column('State', db.String(50))
    country = db.Column('Country', db.String(50))
    postal = db.Column('Zip', db.String(50))
    tel = db.Column('TEL', db.String(50))
    s_sched = db.Column('Ship Schedule', db.String(50))
    s_term = db.Column('Shipment Term', db.String(50))
    q_title = db.Column('Quotation title', db.String(50))
    q_note = db.Column('Quotation Note', db.String(50))
    q_amount = db.Column('Quote Amount', db.Integer)

    opportunities = db.relationship('Opportunity', backref='quotation',
                                lazy='dynamic')

    quote_details = db.relationship('Quotation_Detail', backref='quotation',
                                lazy='dynamic')

    def __repr__(self):
        return '<Quotation: {}>'.format(self.q_id)


class Opportunity(UserMixin, db.Model):
    """
    Create an Opportunity table
    """
    __tablename__ = 'opportunities'

    o_id = db.Column('OpportunityID', db.Integer, primary_key=True)  
    q_id = db.Column('QuotationID', db.Integer, db.ForeignKey('quotations.QuotationID'), nullable=False)                 
    source_of_lead = db.Column('Source of Lead', db.String(50))
    sale_ref_fee = db.Column('Sales referal Fee', db.Float)
    competitors = db.Column('Competitors', db.Integer)
    sales_stage = db.Column('Sales Stage', db.Integer)
    close_date = db.Column('Close Date', db.Date)       
    probability = db.Column('Probability', db.Float)
    rev_category = db.Column('Revenue Category', db.String(50))
    proj_note = db.Column('Project Note', db.String(100))
    application = db.Column('Application', db.String(50))
    family = db.Column('Family', db.String(50))
    potential_money = db.Column('Potential $', db.Float)
    probable_money = db.Column('Probable $', db.Float)
    actual_money = db.Column('Actual $', db.Float)
    revenue = db.Column('Revenue $', db.Float)
    integrator = db.Column('Integrator', db.String(50))
    region = db.Column('Region', db.String(50))


    def __repr__(self):
        return '<Opportunity: {}>'.format(self.o_id)


class Quotation_Detail(UserMixin, db.Model):
    """
    Create an Opportunity table
    """
    __tablename__ = 'quotation_details'

    quote_detail_id = db.Column('QuotationDetailID', db.Integer, primary_key=True)  
    q_id = db.Column('QuotationID', db.Integer, db.ForeignKey('quotations.QuotationID'), nullable=False)                 
    p_id = db.Column('ProductID', db.String(50))    # Foreign key of Products
    p_name = db.Column('Product Name', db.String(50))
    quantity = db.Column('Quantity', db.Float)
    discount = db.Column('Discount', db.Float)
    q_price = db.Column('Quote Price', db.Float)       
    option = db.Column('Option', db.Float)
    
    def __repr__(self):
        return '<Quotation Detail: {}>'.format(self.quote_detail_id)



class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
