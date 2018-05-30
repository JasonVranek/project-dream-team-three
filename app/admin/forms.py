from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextField, IntegerField, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import DateField
# Import fixes issues parsing DateFields:
import wtforms.ext.dateutil
from app import gettext

from ..models import *


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField( gettext('Name'), validators=[DataRequired()])
    description = StringField(gettext('Description'), validators=[DataRequired()])
    submit = SubmitField(gettext('Submit'))


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField( gettext('Name'), validators=[DataRequired()])
    description = StringField( gettext('Description'), validators=[DataRequired()])
    submit = SubmitField( gettext('Submit'))


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField( gettext('Submit'))


class CustomerForm(FlaskForm):
    """
    Form for admin to add or edit a customer
    """
    acc_code = StringField(gettext('Account Code'), validators=[DataRequired()])
    comp_name = StringField(gettext('Company Name'), validators=[DataRequired()])
    f_name = StringField(gettext('First Name'), validators=[DataRequired()])
    l_name = StringField(gettext('Last Name'), validators=[DataRequired()])
    phone = StringField(gettext('Phone Number'), validators=[DataRequired()])
    email = StringField(gettext('Email Address'), validators=[DataRequired()])
    b_address = StringField(gettext('Billing Address'))
    city = StringField(gettext('City'))
    state_province = StringField(gettext('State or Province'))
    post_code = StringField(gettext('Postal Code'))        #implicitly fill from city?
    count_region = StringField(gettext('Country/Region'))   #query from list of regions?
    cont_title = StringField(gettext('Contact Title'))
    fax = StringField(gettext('Fax Number'))
    notes = StringField(gettext('Notes'))
    order = StringField(gettext('Order'))
    state = StringField(gettext('State'))
    status = StringField(gettext('Status'))
    rating = StringField(gettext('Rating'))

    submit = SubmitField(gettext('Submit'))


class ContactForm(FlaskForm):
    """
    Form for admin to add or edit a customer
    """
    # acc_code = QuerySelectField('Account Code', query_factory=lambda: Customer.query.all(),
    #                         get_label="acc_code") 
    acc_code = SelectField(gettext('Account Code'), coerce=int)
    f_name = StringField(gettext('First Name'), validators=[DataRequired()])
    l_name = StringField(gettext('Last Name'), validators=[DataRequired()])
    phone = StringField(gettext('Phone Number'))
    email = StringField(gettext('Email Address'))
    b_address = StringField(gettext('Billing Address'))
    city = StringField(gettext('City'))
    state_province = StringField(gettext('State or Province'))
    post_code = StringField(gettext('Postal Code'))          
    count_region = StringField(gettext('Country/Region'))
    cont_title = StringField(gettext('Contact Title'))
    fax = StringField(gettext('Fax Number'))
    notes = StringField(gettext('Notes'))

    submit = SubmitField(gettext('Submit'))


class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a product
    """
    p_number = StringField(gettext('Part Number'), validators=[DataRequired()])                    
    p_name = StringField(gettext('Product Name'), validators=[DataRequired()])
    unit_price = FloatField(gettext('Unit Price'), validators=[DataRequired()])
    p_note = StringField(gettext('Product Note to show'))
    cost_native = FloatField(gettext('Cost Native'))
    exchange_rate = FloatField(gettext('Exchange Rate used'))
    unit_cost = FloatField(gettext('Unit Cost'), validators=[DataRequired()])
    supplier = StringField(gettext('Supplier'))
    p_category = StringField(gettext('Product Category'))
    p_status = StringField(gettext('Product Status'))
    date_created = DateField(gettext('Date Created'))  #date field?
    person_created = QuerySelectField(gettext('Person Created'), query_factory=lambda: Employee.query.all(),
                            get_label="username")
    remarks = TextField(gettext('Remarks'))

    submit = SubmitField(gettext('Submit'))


class QuotationForm(FlaskForm):
    """
    Form for admin to add or edit a quotation
    """
    # acc_code = QuerySelectField('Account Code', query_factory=lambda: Customer.query.all(),
    #                         get_label="acc_code", id='acc_code')   
    acc_code = SelectField(gettext('Account Code'), id='acc_code', coerce=int)
    contact = SelectField(gettext('Contact'), id='contacts', coerce=int, validators=[Optional()])
    q_num = IntegerField(gettext('Quotation Number'), validators=[DataRequired()])
    e_id = QuerySelectField(gettext('Employee'), query_factory=lambda: Employee.query.all(),
                            get_label="username")
    date = DateField(gettext('Quotaton Date'))
    revision = StringField(gettext('Revision'))
    pay_terms = SelectField(gettext('Payment Terms'), choices=[('None', ''),
                                                    ('net15', 'Net 15'), 
                                                    ('net30', 'Net 30'), 
                                                    ('net45', 'Net 45'),
                                                    ('net60', 'Net60'),
                                                    ('prepaid', 'Prepaid T/T'),
                                                    ('lc', 'L/C')])
    title = StringField(gettext('Title'), id='title')
    f_name = StringField(gettext('First Name'), id='f_name')
    l_name = StringField(gettext('Last Name'), id='l_name')
    address = StringField(gettext('Address'), id='address')
    city = StringField(gettext('City'), id='city')
    state = StringField(gettext('State'), id='state')
    country = StringField(gettext('Country'), id='country')
    postal = StringField(gettext('Zip'), id='zip')
    tel = StringField(gettext('TEL'), id='tel')
    s_sched = StringField(gettext('Ship Schedule (Weeks)'))
    s_term = SelectField(gettext('Shipment Term'), choices=[('None', ''), ('Ex-Works', 'Ex-Works'), ('FOB: Origin', 'FOB: Origin'), ('CIF: Destination', 'CIF: Destination')])
    q_title = StringField(gettext('Quotation Title'))
    q_note = TextField(gettext('Quotation Note'))
    #q_amount = IntegerField('Quote Amount')

    submit = SubmitField(gettext('Submit'))


class OpportunityForm(FlaskForm):
    """
    Form for admin to add or edit an opportunity
    """
    q_num = QuerySelectField(gettext('Quotation Number'), query_factory=lambda: Quotation.query.all(),
                            get_label="q_num")       
    source_of_lead = StringField(gettext('Source of Lead'))
    sale_ref_fee = StringField(gettext('Sales referal Fee'))
    competitors = IntegerField(gettext('Competitors'))
    sales_stage = IntegerField(gettext('Sales Stage'))
    close_date = DateField(gettext('Close Date'), validators=[DataRequired()])
    probability = FloatField(gettext('Probability'))
    rev_category = StringField(gettext('Revenue Category'))
    proj_note = StringField(gettext('Project Note'))
    application = StringField(gettext('Application'))
    family = StringField(gettext('Family'))
    potential_money = FloatField(gettext('Potential $'))
    probable_money = FloatField(gettext('Probable $'))
    actual_money = FloatField(gettext('Actual $'))
    revenue = FloatField(gettext('Revenue $'))
    integrator = StringField(gettext('Integrator'))
    region = StringField(gettext('Region'))
    
    submit = SubmitField(gettext('Submit'))


class Quotation_DetailForm(FlaskForm):
    """
    Form for admin to add or edit a quotation_detail
    """
    #q_num = QuerySelectField('Quotation Number', query_factory=lambda: Quotation.query.all(),
    #                        get_label="q_num") 
    q_num = SelectField(gettext('Quotation Number'), coerce=int)    
    p_num = SelectField(gettext('Product Number'), coerce=int, id='product')           
    # p_num = QuerySelectField('Product Number', query_factory=lambda: Product.query.all(),
    #                         get_label="p_number", id='product')
    p_name = StringField(gettext('Product Name'), id='product_name')
    quantity = FloatField(gettext('Quantity'), validators=[DataRequired()])
    discount = FloatField(gettext('Discount'))#, validators=[DataRequired()])
    unit_price = FloatField(gettext('Unit Price'), id='unit_price')
    q_price = FloatField(gettext('Quote Price'), id='quote_price')#, validators=[DataRequired()])       
    option = BooleanField(gettext('Optional'))

    submit = SubmitField(gettext('Submit'))


class SearchForm(FlaskForm):
    search_string = StringField(gettext('Search'))

    submit = SubmitField(gettext('Submit'))


    
