from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Department, Role, Customer


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
    comp_name = StringField('CompanyName', validators=[DataRequired()])
    f_name = StringField('ContactFirstName', validators=[DataRequired()])
    l_name = StringField('ContactLastName', validators=[DataRequired()])
    phone = StringField('PhoneNumber', validators=[DataRequired()])
    email = StringField('EmailAddress', validators=[DataRequired()])
    b_address = StringField('BillingAddress')
    city = StringField('City')
    state_province = StringField('StateOrProvince')
    post_code = StringField('PostalCode')          #implicitly fill from city?
    count_region = StringField('Country/Region')   #query from list of regions?
    cont_title = StringField('ContactTitle')
    fax = StringField('FaxNumber')
    notes = StringField('Notes')
    order = StringField('Order')
    state = StringField('State')
    status = StringField('Status')
    rating = StringField('Rating')

    submit = SubmitField('Submit')

    
