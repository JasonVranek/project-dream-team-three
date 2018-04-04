from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, DateField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Department, Role, Customer, Employee, Product


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
    person_created = QuerySelectField(query_factory=lambda: Employee.query.all(),
                            get_label="username")
    remarks = TextField('Remarks')
    
    submit = SubmitField('Submit')


    
