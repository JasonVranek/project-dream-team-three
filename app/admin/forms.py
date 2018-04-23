from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextField, IntegerField, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
# Import fixes issues parsing DateFields:
import wtforms.ext.dateutil

from ..models import *


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


class CustomerForm(FlaskForm):
    """
    Form for admin to add or edit a customer
    """
    acc_code = StringField('Account Code', validators=[DataRequired()])
    comp_name = StringField('Company Name', validators=[DataRequired()])
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    b_address = StringField('Billing Address')
    city = StringField('City')
    state_province = StringField('State or Province')
    post_code = StringField('Postal Code')          #implicitly fill from city?
    count_region = StringField('Country/Region')   #query from list of regions?
    cont_title = StringField('Contact Title')
    fax = StringField('Fax Number')
    notes = StringField('Notes')
    order = StringField('Order')
    state = StringField('State')
    status = StringField('Status')
    rating = StringField('Rating')

    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a product
    """
    p_number = StringField('Part Number', validators=[DataRequired()])                    
    p_name = StringField('Product Name', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    p_note = StringField('Product Note to show')
    cost_native = FloatField('Cost Native')
    exchange_rate = FloatField('Exchange Rate used')
    unit_cost = FloatField('Unit Cost', validators=[DataRequired()])
    supplier = StringField('Supplier')
    p_category = StringField('Product Category')
    p_status = StringField('Product Status')
    date_created = DateField('Date Created')  #date field?
    person_created = QuerySelectField('Person Created', query_factory=lambda: Employee.query.all(),
                            get_label="username")
    remarks = TextField('Remarks')

    submit = SubmitField('Submit')


class QuotationForm(FlaskForm):
    """
    Form for admin to add or edit a quotation
    """
    c_id = QuerySelectField('Customer Id', query_factory=lambda: Customer.query.all(),
                            get_label="c_id")
    q_num = IntegerField('Quotation Number', validators=[DataRequired()])
    e_id = QuerySelectField('Employee', query_factory=lambda: Employee.query.all(),
                            get_label="username")
    date = DateField('Quotaton Date')
    revision = StringField('Revision')
    pay_terms = StringField('Payment Terms')
    title = StringField('Title')
    f_name = StringField('First Name')
    l_name = StringField('Last Name')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    country = StringField('Country')
    postal = StringField('Zip')
    tel = StringField('TEL')
    s_sched = StringField('Ship Schedule')
    s_term = StringField('Shipment Term')
    q_title = StringField('Quotation title')
    q_note = TextField('Quotation Note')
    q_amount = IntegerField('Quote Amount')

    submit = SubmitField('Submit')


class OpportunityForm(FlaskForm):
    """
    Form for admin to add or edit an opportunity
    """
    q_id = QuerySelectField('Quotation Id', query_factory=lambda: Quotation.query.all(),
                            get_label="q_id")
    source_of_lead = StringField('Source of Lead')
    sale_ref_fee = StringField('Sales referal Fee')
    competitors = IntegerField('Competitors')
    sales_stage = IntegerField('Sales Stage')
    close_date = DateField('Close Date', validators=[DataRequired()])
    probability = FloatField('Probability')
    rev_category = StringField('Revenue Category')
    proj_note = StringField('Project Note')
    application = StringField('Application')
    family = StringField('Family')
    potential_money = FloatField('Potential $')
    probable_money = FloatField('Probable $')
    actual_money = FloatField('Actual $')
    revenue = FloatField('Revenue $')
    integrator = StringField('Integrator')
    region = StringField('Region')
    
    submit = SubmitField('Submit')


class Quotation_DetailForm(FlaskForm):
    """
    Form for admin to add or edit a quotation_detail
    """
    q_id = QuerySelectField('Quotation Id', query_factory=lambda: Quotation.query.all(),
                            get_label="q_id")
    q_num = QuerySelectField('Quotation Number', query_factory=lambda: Quotation.query.all(),
                            get_label="q_num")             
    p_id = QuerySelectField('Product Id', query_factory=lambda: Product.query.all(),
                            get_label="p_id")
    p_name = QuerySelectField('Product Name', query_factory=lambda: Product.query.all(),
                            get_label="p_name")
    p_name = QuerySelectField('Product Number', query_factory=lambda: Product.query.all(),
                            get_label="p_number")
    # p_name = StringField('Product Name')
    quantity = FloatField('Quantity', validators=[DataRequired()])
    discount = FloatField('Discount', validators=[DataRequired()])
    q_price = FloatField('Quote Price')#, validators=[DataRequired()])       
    option = BooleanField('Option')

    submit = SubmitField('Submit')


    
