from flask import abort, flash, redirect, render_template, url_for, make_response, request, jsonify, session
from flask_login import current_user, login_required

from . import admin
from forms import *
from .. import db
from ..models import *

import random

from sqlalchemy import or_


@admin.route('/background_process/change_language/')
def change_language():
    if session.get('language') == 'en':
        session['language'] = 'ja'
        current_user.language = 'ja'
    else:
        session['language'] = 'en'
        current_user.language = 'en'

    db.session.commit()
    return redirect(url_for('home.homepage'))


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments/<int:page_num>/', methods=['GET', 'POST'])
@login_required
def list_departments(page_num):
    """
    List all departments
    """
    check_admin()

    # departments = Department.query.all()
    departments = Department.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments', page_num=1))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments', page_num=1))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>/', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments', page_num=1))

    return render_template(title="Delete Department")


# Customer Views


@admin.route('/customers/view/<int:id>', methods=['GET'])
@login_required
def view_customer(id):
    """
    View a customer
    """
    check_admin()

    customer = Customer.query.filter_by(c_id=id).first()
    # acc_code = customer.acc_code
    # contacts = Contact.query.filter_by(acc_code=acc_code).all()
    contacts = Contact.query.filter_by(c_id=id).all()

    return render_template('admin/customers/view_customer.html', action="View",
                           customer=customer, contacts=contacts, title="View Customer")


@admin.route('/customers/<int:page_num>/', methods=['GET', 'POST'])
@login_required
def list_customers(page_num):
    """
    List all customers
    """
    check_admin()

    # customers = Customer.query.all()
    # customers = Customer.query.paginate(per_page=5, page=page_num, error_out=True)

    customers = Customer.query.order_by(Customer.acc_code).all()
    form = SearchForm()
    if form.validate_on_submit():
        customers = Customer.query.filter(or_(Customer.acc_code.like("%" + form.search_string.data + "%"), 
                                        Customer.email.like("%" + form.search_string.data + "%"),
                                        Customer.f_name.like("%" + form.search_string.data + "%"),
                                        Customer.l_name.like("%" + form.search_string.data + "%"))).all()

    return render_template('admin/customers/customers.html', form=form,
                           customers=customers, title="Customers")


@admin.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    """
    Add a customer to the database
    """
    check_admin()

    add_customer = True

    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(acc_code=form.acc_code.data,
                                comp_name = form.comp_name.data,
                                f_name = form.f_name.data,
                                l_name = form.l_name.data,
                                phone = form.phone.data,
                                email = form.email.data,
                                b_address = form.b_address.data,
                                city = form.city.data,
                                state_province = form.state_province.data,
                                post_code = form.post_code.data,
                                count_region = form.count_region.data,
                                cont_title = form.cont_title.data,
                                fax = form.fax.data,
                                notes = form.notes.data,
                                order = form.order.data,
                                state = form.state.data,
                                status = form.status.data,
                                rating = form.rating.data)
        try:
            # add customer to the database
            db.session.add(customer)
            db.session.commit()
            flash('You have successfully added a new customer.')
        except:
            # in case Customer Account Code already exists
            flash('Error: Customer Account Code already exists.')

        # redirect to customers page
        return redirect(url_for('admin.list_customers', page_num=1))

    # load customer template
    return render_template('admin/customers/customer.html', action="Add",
                           add_customer=add_customer, form=form,
                           title="Add Customer")


@admin.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    """
    Edit a customer
    """
    check_admin()

    add_customer = False

    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.acc_code = form.acc_code.data
        customer.comp_name = form.comp_name.data
        customer.f_name = form.f_name.data
        customer.l_name = form.l_name.data
        customer.phone = form.phone.data
        customer.email = form.email.data
        customer.b_address = form.b_address.data
        customer.city = form.city.data
        customer.state_province = form.state_province.data
        customer.post_code = form.post_code.data
        customer.count_region = form.count_region.data
        customer.cont_title = form.cont_title.data
        customer.fax = form.fax.data
        customer.notes = form.notes.data
        customer.order = form.order.data
        customer.state = form.state.data
        customer.status = form.status.data
        customer.rating = form.rating.data

        db.session.commit()
        flash('You have successfully edited the customer.')

        # redirect to the customers page
        return redirect(url_for('admin.list_customers', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.acc_code.data = customer.acc_code 
    form.comp_name.data = customer.comp_name 
    form.f_name.data = customer.f_name 
    form.l_name.data = customer.l_name
    form.phone.data = customer.phone
    form.email.data = customer.email
    form.b_address.data = customer.b_address 
    form.city.data = customer.city
    form.state_province.data = customer.state_province
    form.post_code.data = customer.post_code
    form.count_region.data = customer.count_region
    form.cont_title.data = customer.cont_title
    form.fax.data = customer.fax 
    form.notes.data = customer.notes 
    form.order.data = customer.order 
    form.state.data = customer.state
    form.status.data = customer.status
    form.rating.data = customer.rating

    return render_template('admin/customers/customer.html', action="Edit",
                           add_customer=add_customer, form=form,
                           customer=customer, title="Edit Customer")


@admin.route('/customers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    """
    Delete a customer from the database
    """
    check_admin()

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('You have successfully deleted the customer.')

    # redirect to the customers page
    return redirect(url_for('admin.list_customers', page_num=1))


# Contact Views


@admin.route('/contacts/background_process/customer')
@login_required
def _get_customer_info():
    """
    Retrieve a list of contacts from a specified account code
    """
    check_admin()

    acc_code = request.args.get('acc_code', '1')
    customer = Customer.query.filter_by(acc_code=acc_code).first()
    # Can't serialize an sqlalchmy object using jsonify, so just make a dictionary with relevant data
    data = {}
    data['title'] = customer.cont_title
    data['f_name'] = customer.f_name
    data['l_name'] = customer.l_name
    data['address'] = customer.b_address
    data['city'] = customer.city
    data['state'] = customer.state_province
    data['country'] = customer.count_region
    data['zip'] = customer.post_code
    data['tel'] = customer.phone
    
    return jsonify(data)


@admin.route('/contacts/background_process/contact_info')
@login_required
def _get_contact_info():
    """
    Retrieve a list of contacts from a specified account code
    """
    check_admin()

    contact_id = request.args.get('contact_id', '1', type=int)
    print(contact_id)
    contact = Contact.query.filter_by(contact_id=contact_id).first()
    customer = Customer.query.filter_by(c_id=contact.c_id).first()
    # Can't serialize an sqlalchmy object using jsonify, so just make a dictionary with relevant data
    data = {}

    # Only use contact data if it's available otherwise default to the customer's data
    if contact.cont_title:
        data['title'] = contact.cont_title
    else:
        data['title'] = customer.cont_title

    if contact.f_name:
        data['f_name'] = contact.f_name
    else:
        data['f_name'] = customer.f_name

    if contact.l_name:
        data['l_name'] = contact.l_name
    else:
        data['l_name'] = customer.l_name

    if contact.city:
        data['city'] = contact.city
    else:
        data['city'] = customer.city

    if contact.state_province:
        data['state'] = contact.state_province
    else:
        data['state'] = customer.state_province

    if contact.count_region:
        data['country'] = contact.count_region
    else:
        data['country'] = customer.count_region

    if contact.phone:
        data['tel'] = contact.phone
    else:
        data['tel'] = customer.phone

    if contact.post_code:
        data['zip'] = contact.post_code
    else:
        data['zip'] = customer.post_code

    if contact.b_address:
        data['address'] = contact.b_address
    else:
        data['address'] = customer.b_address

    return jsonify(data)


@admin.route('/contacts/background_process')
@login_required
def _get_contacts_list():
    """
    Retrieve a list of contacts from a specified account code
    """
    check_admin()

    acc_code = request.args.get('acc_code', '1', type=str)
    # Query for all the contacts that share this account code and index theyre names by their contact id
    contacts = [(contact.contact_id, str(contact.f_name + ' ' + contact.l_name)) for contact in Contact.query.filter_by(acc_code=acc_code).all()]
    return jsonify(contacts)


@admin.route('/contacts/view/<int:id>', methods=['GET'])
@login_required
def view_contact(id):
    """
    View a contact
    """
    check_admin()

    contact = Contact.query.filter_by(contact_id=id).first()

    return render_template('admin/contacts/view_contact.html', action="View",
                           contact=contact, title="View Contact")


@admin.route('/contacts/<int:page_num>/', methods=['GET', 'POST'])
@login_required
def list_contacts(page_num):
    """
    List all contacts
    """
    check_admin()

    # contacts = Contact.query.paginate(per_page=5, page=page_num, error_out=True)
    contacts = Contact.query.order_by(Contact.acc_code).all()
    form = SearchForm()
    if form.validate_on_submit():
        contacts = Contact.query.filter(or_(Contact.acc_code.like("%" + form.search_string.data + "%"), 
                                        Contact.email.like("%" + form.search_string.data + "%"),
                                        Contact.f_name.like("%" + form.search_string.data + "%"),
                                        Contact.l_name.like("%" + form.search_string.data + "%"))).all()

    return render_template('admin/contacts/contacts.html', form=form,
                           contacts=contacts, title="Contacts")


@admin.route('/contacts/add/<int:c_id>', methods=['GET', 'POST'])
@login_required
def add_contact(c_id):
    """
    Add a contact to the database
    """
    check_admin()

    add_contact = True

    form = ContactForm()
    form.acc_code.choices = [(customer.c_id, str(customer.acc_code)) for customer in Customer.query.all()]
    if c_id is not None:
        form.acc_code.data = c_id
    if form.validate_on_submit():
        c_id = form.acc_code.data
        customer = Customer.query.filter_by(c_id=c_id).first()
        acc_code = customer.acc_code
        contact = Contact(c_id = c_id,
                                acc_code=acc_code,
                                f_name = form.f_name.data,
                                l_name = form.l_name.data,
                                phone = form.phone.data,
                                email = form.email.data,
                                b_address = form.b_address.data,
                                city = form.city.data,
                                state_province = form.state_province.data,
                                post_code = form.post_code.data,
                                count_region = form.count_region.data,
                                cont_title = form.cont_title.data,
                                fax = form.fax.data,
                                notes = form.notes.data)
        try:
            # add contact to the database
            db.session.add(contact)
            db.session.commit()
            flash('You have successfully added a new contact.')
        except Exception as e:
            # in case Contact Account Code already exists
            flash('Error: Customer Account Code already exists.')

        # redirect to contacts page
        return redirect(url_for('admin.list_contacts', page_num=1))

    # load customer template
    return render_template('admin/contacts/contact.html', action="Add",
                           add_contact=add_contact, form=form,
                           title="Add Contact")


@admin.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    """
    Edit a contact
    """
    check_admin()

    add_contact = False

    contact = Contact.query.get_or_404(id)
    form = ContactForm(obj=contact)
    form.acc_code.choices = [(customer.c_id, str(customer.acc_code)) for customer in Customer.query.all()]
    if form.validate_on_submit():
        c_id = form.acc_code.data
        contact.c_id = c_id
        customer = Customer.query.filter_by(c_id=c_id).first()
        contact.acc_code = customer.acc_code
        contact.f_name = form.f_name.data
        contact.l_name = form.l_name.data
        contact.phone = form.phone.data
        contact.email = form.email.data
        contact.b_address = form.b_address.data
        contact.city = form.city.data
        contact.state_province = form.state_province.data
        contact.post_code = form.post_code.data
        contact.count_region = form.count_region.data
        contact.cont_title = form.cont_title.data
        contact.fax = form.fax.data
        contact.notes = form.notes.data

        db.session.commit()
        flash('You have successfully edited the contact.')

        # redirect to the contacts page
        return redirect(url_for('admin.list_contacts', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.acc_code.data = contact.c_id 
    form.f_name.data = contact.f_name 
    form.l_name.data = contact.l_name
    form.phone.data = contact.phone
    form.email.data = contact.email
    form.b_address.data = contact.b_address 
    form.city.data = contact.city
    form.state_province.data = contact.state_province
    form.post_code.data = contact.post_code
    form.count_region.data = contact.count_region
    form.cont_title.data = contact.cont_title
    form.fax.data = contact.fax 
    form.notes.data = contact.notes 

    return render_template('admin/contacts/contact.html', action="Edit",
                           add_contact=add_contact, form=form,
                           contact=contact, title="Edit Contact")


@admin.route('/contacts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_contact(id):
    """
    Delete a contact from the database
    """
    check_admin()

    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('You have successfully deleted the contact.')

    # redirect to the contacts page
    return redirect(url_for('admin.list_contacts', page_num=1))


# Role Views


@admin.route('/roles/<int:page_num>/')
@login_required
def list_roles(page_num):
    check_admin()
    """
    List all roles
    """
    # roles = Role.query.all()
    roles = Role.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles', page_num=1))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles', page_num=1))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles', page_num=1))

    return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees/<int:page_num>')
@login_required
def list_employees(page_num):
    """
    List all employees
    """
    check_admin()

    # employees = Employee.query.all()
    employees = Employee.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees', page_num=1))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


# Product Views


@admin.route('/products/view/<int:id>', methods=['GET'])
@login_required
def view_product(id):
    """
    View a product
    """
    check_admin()

    product = Product.query.filter_by(p_id=id).first()

    return render_template('admin/products/view_product.html', action="View",
                           product=product, title="View Product")


@admin.route('/products/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_products(page_num):
    """
    List all products
    """
    check_admin()

    products = Product.query.order_by(Product.p_id).all()
    form = SearchForm()
    if form.validate_on_submit():
        products = Product.query.filter(or_(Product.p_number.like("%" + form.search_string.data + "%"), 
                                        Product.japanese_p_name.like("%" + form.search_string.data + "%"),
                                        Product.p_name.like("%" + form.search_string.data + "%"),
                                        Product.supplier.like("%" + form.search_string.data + "%"))).all()

    return render_template('admin/products/products.html',
                           products=products, title="Products", form=form)


@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    Add a product to the database
    """
    check_admin()

    add_product = True

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(p_number=form.p_number.data,
                                p_name = form.p_name.data,
                                unit_price = form.unit_price.data,
                                p_note = form.p_note.data,
                                cost_native = form.cost_native.data,
                                exchange_rate = form.exchange_rate.data,
                                unit_cost = form.unit_cost.data,
                                supplier = form.supplier.data,
                                p_category = form.p_category.data,
                                p_status = form.p_status.data,
                                date_created = form.date_created.data,
                                person_created = form.person_created.data,
                                remarks = form.remarks.data)
                                
        try:
            # add product to the database
            db.session.add(product)
            db.session.commit()
            flash('You have successfully added a new product.')
        except:
            # in case Product already exists
            flash('Error: Product already exists.')

        # redirect to products page
        return redirect(url_for('admin.list_products', page_num=1))

    # load product template
    return render_template('admin/products/product.html', action="Add",
                           add_product=add_product, form=form,
                           title="Add Product")


@admin.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Edit a product
    """
    check_admin()

    add_product = False

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.p_number = form.p_number.data
        product.p_name = form.p_name.data
        product.unit_price = form.unit_price.data
        product.p_note = form.p_note.data
        product.cost_native = form.cost_native.data
        product.exchange_rate = form.exchange_rate.data
        product.unit_cost = form.unit_cost.data
        product.unit_cost = form.unit_cost.data
        product.supplier = form.supplier.data
        product.p_category = form.p_category.data
        product.p_status = form.p_status.data
        product.date_created = form.date_created.data
        product.person_created = form.person_created.data
        product.remarks = form.remarks.data

        db.session.commit()
        flash('You have successfully edited the product.')

        # redirect to the products page
        return redirect(url_for('admin.list_products', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.p_number.data = product.p_number 
    form.p_name.data = product.p_name 
    form.unit_price.data = product.unit_price 
    form.p_note.data = product.p_note
    form.cost_native.data = product.cost_native
    form.exchange_rate.data = product.exchange_rate
    form.unit_cost.data = product.unit_cost
    form.unit_cost.data = product.unit_cost
    form.supplier.data = product.supplier 
    form.p_category.data = product.p_category
    form.p_status.data = product.p_status
    form.date_created.data = product.date_created
    form.person_created.data = product.person_created
    form.remarks.data = product.remarks

    return render_template('admin/products/product.html', action="Edit",
                           add_product=add_product, form=form,
                           product=product, title="Edit Product")


@admin.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """
    Delete a product from the database
    """
    check_admin()

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('You have successfully deleted the product.')

    # redirect to the products page
    return redirect(url_for('admin.list_products', page_num=1))

    return render_template(title="Delete Product")


# Quotation Views


@admin.route('/quotations/toggle/<int:id>/<int:locked>', methods=['GET', 'POST'])
@login_required
def lock_quotation(id, locked):
    # Modify the locked parameter of the quotation to boolean value: locked
    quotation = Quotation.query.get_or_404(id)
    quotation.locked = bool(locked)
    db.session.commit()

    # redirect to quotation_details page
    return redirect(url_for('admin.list_quotations', page_num=1))


@admin.route('/quotations/revise/<int:id>', methods=['GET'])
@login_required
def _revise_quotation(id):
    # Get the relevant db objects to make a copy of the Quotation
    quotation = Quotation.query.get_or_404(id)
    customer = Customer.query.get_or_404(quotation.c_id)
    contact = Contact.query.get_or_404(quotation.contact_id)  
    # get the current revision number to update

    # practicing lambda function, essentially (r_num = quote.r_num + 1)
    revision_num = (lambda r_num: 1 + int(r_num) if r_num else 1)(quotation.revision)

    #practicing lambda func, replace last char in string with new r_num: new_q_num = q_num[:-1] + str(revision_num)
    new_q_num = (lambda q_num, r_num: q_num[:-1] + str(r_num)) (quotation.q_num, revision_num)
    # Recreate the new Quotation
    new_quotation = Quotation(c_id = quotation.c_id,           
                                acc_code = quotation.acc_code,
                                contact_id = quotation.contact_id,
                                q_num = new_q_num,
                                e_id = quotation.e_id,           
                                date = quotation.date,
                                revision = revision_num,
                                pay_terms = quotation.pay_terms,
                                title = quotation.title,
                                f_name = quotation.f_name,
                                l_name = quotation.l_name,
                                address = quotation.address,
                                city = quotation.city,
                                state = quotation.state,
                                country = quotation.country,
                                postal = quotation.postal,
                                tel = quotation.tel,
                                s_sched = quotation.s_sched,
                                s_term = quotation.s_term,
                                q_title = quotation.q_title,
                                q_note = quotation.q_note,
                                q_amount = quotation.q_amount)
                                
    try:
        # add new quotation to the database
        db.session.add(new_quotation)
        db.session.commit()
        flash('You have successfully added a new quotation.')
    except:
        # in case Quotation already exists
        flash('Error: Quotation Revision number: ' + new_q_num +' already exists.')
        return redirect(url_for('admin.list_quotations', page_num=1))


    # Get the new quotation id
    new_q_id = Quotation.query.filter_by(q_num=new_q_num).first().q_id
    # Get all the quote details attached to this quotation
    quote_details = Quotation_Detail.query.filter_by(q_id=id).all()

    # Recreate each quote detail to be used in the new quotation
    for quote_detail in quote_details:
        product_associated = Product.query.get_or_404(quote_detail.p_id)
        new_quote_detail = Quotation_Detail(q_id = new_q_id,     
                                p_id = quote_detail.p_id,                
                                p_name = product_associated.p_name,           
                                q_num = new_q_num,
                                p_num = product_associated.p_number,
                                quantity = quote_detail.quantity,
                                discount = quote_detail.discount,
                                q_price = quote_detail.q_price,
                                option = quote_detail.option)
                                
        try:
            # add new quotation_detail to the database
            db.session.add(new_quote_detail)
            db.session.commit()
            flash('You have successfully added a new quotation_detail.')
        except:
            # in case Quotation_Detail already exists
            flash('Error: Quotation_Detail already exists.')
            return redirect(url_for('admin.list_quotations', page_num=1))

    # redirect to quotations page
    return redirect(url_for('admin.view_quotation', id=new_q_id))


@admin.route('/quotations/copy/<int:id>', methods=['GET'])
@login_required
def _copy_quotation(id):
    # Get the relevant db objects to make a copy of the Quotation
    quotation = Quotation.query.get_or_404(id)
    customer = Customer.query.get_or_404(quotation.c_id)
    contact = Contact.query.get_or_404(quotation.contact_id)    

    # Prepend a C to indicate that it is a copy. 
    new_q_num = 'C' + quotation.q_num

    # Recreate the new Quotation
    new_quotation = Quotation(c_id = quotation.c_id,           
                                acc_code = quotation.acc_code,
                                contact_id = quotation.contact_id,
                                q_num = new_q_num,
                                e_id = quotation.e_id,           
                                date = quotation.date,
                                revision = quotation.revision,
                                pay_terms = quotation.pay_terms,
                                title = quotation.title,
                                f_name = quotation.f_name,
                                l_name = quotation.l_name,
                                address = quotation.address,
                                city = quotation.city,
                                state = quotation.state,
                                country = quotation.country,
                                postal = quotation.postal,
                                tel = quotation.tel,
                                s_sched = quotation.s_sched,
                                s_term = quotation.s_term,
                                q_title = quotation.q_title,
                                q_note = quotation.q_note,
                                q_amount = quotation.q_amount)
                                
    try:
        # add new quotation to the database
        db.session.add(new_quotation)
        db.session.commit()
        flash('You have successfully copied a quotation.')
    except:
        # in case Quotation already exists
        flash('Error: Quotation already exists.')

    # Get the new quotation id
    new_q_id = Quotation.query.filter_by(q_num=new_q_num).first().q_id
    # Get all the quote details attached to this quotation
    quote_details = Quotation_Detail.query.filter_by(q_id=id).all()

    # Recreate each quote detail to be used in the new quotation
    for quote_detail in quote_details:
        product_associated = Product.query.get_or_404(quote_detail.p_id)
        new_quote_detail = Quotation_Detail(q_id = new_q_id,     
                                p_id = quote_detail.p_id,                
                                p_name = product_associated.p_name,           
                                q_num = new_q_num,
                                p_num = product_associated.p_number,
                                quantity = quote_detail.quantity,
                                discount = quote_detail.discount,
                                q_price = quote_detail.q_price,
                                option = quote_detail.option)
                                
        try:
            # add new quotation_detail to the database
            db.session.add(new_quote_detail)
            db.session.commit()
        except:
            # in case Quotation_Detail already exists
            flash('Error: Quotation_Detail already exists.')

    # redirect to quotations page
    return redirect(url_for('admin.view_quotation', id=new_q_id))
    

@admin.route('/quotations/view/<int:id>', methods=['GET'])
@login_required
def view_quotation(id):
    """
    View a quotation
    """
    check_admin()

    quotation = Quotation.query.filter_by(q_id=id).first()
    quote_details = Quotation_Detail.query.filter_by(q_id=id).all()

    return render_template('admin/quotations/view_quotation.html', action="View",
                           quotation=quotation, quote_details=quote_details, title="View Quotation")


@admin.route('/quotations/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_quotations(page_num):
    """
    List all quotations
    """
    check_admin()

    # quotations = Quotation.query.all()
    # quotations = Quotation.query.paginate(per_page=5, page=page_num, error_out=True)

    quotations = Quotation.query.order_by(Quotation.q_num).all()
    form = SearchForm()
    if form.validate_on_submit():
        quotations = Quotation.query.filter(or_(Quotation.acc_code.like("%" + form.search_string.data + "%"), 
                                        Quotation.q_num.like("%" + form.search_string.data + "%"))).all()

    return render_template('admin/quotations/quotations.html', form=form,
                           quotations=quotations, title="Quotations")


@admin.route('/quotations/add', methods=['GET', 'POST'])
@login_required
def add_quotation():
    """
    Add a quotation to the database
    """
    check_admin()

    add_quotation = True

    form = QuotationForm()
    form.contact.choices = [(contact.contact_id, str(contact.f_name + ' ' + contact.l_name)) for contact in Contact.query.all()]
    form.acc_code.choices = [(customer.c_id, str(customer.acc_code)) for customer in Customer.query.all()]
    if form.validate_on_submit():
        c_id = form.acc_code.data
        customer = Customer.query.filter_by(c_id=c_id).first()
        acc_code = customer.acc_code
        # if form.qnum.data = 18100 -> 18100R0
        revision = (lambda rev: rev if rev else '0')(form.revision.data)
        q_num = str(form.q_num.data) + (lambda x: 'R' + x if x else 'R0')(revision)
        quotation = Quotation(c_id = c_id,           
                                acc_code = acc_code,
                                contact_id = form.contact.data,
                                q_num = q_num,
                                e_id = form.e_id.data.username,           
                                date = form.date.data,
                                revision = revision,
                                pay_terms = form.pay_terms.data,
                                title = form.title.data,
                                f_name = form.f_name.data,
                                l_name = form.l_name.data,
                                address = form.address.data,
                                city = form.city.data,
                                state = form.state.data,
                                country = form.country.data,
                                postal = form.postal.data,
                                tel = form.tel.data,
                                s_sched = form.s_sched.data,
                                s_term = form.s_term.data,
                                q_title = form.q_title.data,
                                q_note = form.q_note.data)
                                #q_amount = form.q_amount.data)
                                
        try:
            # add quotation to the database
            db.session.add(quotation)
            db.session.commit()
            flash('You have successfully added a new quotation.')
        except:
            # in case Quotation already exists
            flash('Error: Quotation already exists.')

        # redirect to quotations page
        return redirect(url_for('admin.list_quotations', page_num=1))

    # load quotation template
    return render_template('admin/quotations/quotation.html', action="Add",
                           add_quotation=add_quotation, form=form,
                           title="Add Quotation")


@admin.route('/quotations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quotation(id):
    """
    Edit a quotation
    """
    check_admin()

    add_quotation = False

    quotation = Quotation.query.get_or_404(id)
    form = QuotationForm(obj=quotation)
    form.contact.choices = [(contact.contact_id, str(contact.f_name + ' ' + contact.l_name)) for contact in Contact.query.all()]
    form.acc_code.choices = [(customer.c_id, str(customer.acc_code)) for customer in Customer.query.all()]
    if form.validate_on_submit():
        c_id = form.acc_code.data
        customer = Customer.query.filter_by(c_id=c_id).first()
        acc_code = customer.acc_code
        quotation.c_id = c_id
        quotation.acc_code = acc_code
        quotation.contact_id = form.contact.data
        quotation.q_num = form.q_num.data        
        quotation.e_id = form.e_id.data.username         
        quotation.date = form.date.data
        quotation.revision = form.revision.data
        quotation.pay_terms = form.pay_terms.data
        quotation.title = form.title.data
        quotation.f_name = form.f_name.data
        quotation.l_name = form.l_name.data
        quotation.address = form.address.data
        quotation.city = form.city.data
        quotation.state = form.state.data
        quotation.country = form.country.data
        quotation.postal = form.postal.data
        quotation.tel = form.tel.data
        quotation.s_sched = form.s_sched.data
        quotation.s_term = form.s_term.data
        quotation.q_title = form.q_title.data
        quotation.q_note = form.q_note.data

        db.session.commit()
        flash('You have successfully edited the quotation.')

        # redirect to the quotations page
        return redirect(url_for('admin.list_quotations', page_num=1))

    # fill the form with current data to show what changes are to be made
    # Find the value corresponding to the selected account code so when they edit it doesnt default to a-tech
    form.acc_code.default = quotation.c_id
    # Call to process the form to default to the last used acc code from list
    form.process()
    form.q_num.data = quotation.q_num
    form.e_id.data = quotation.e_id
    form.date.data = quotation.date
    form.revision.data = quotation.revision
    form.pay_terms.data = quotation.pay_terms
    form.title.data = quotation.title
    form.f_name.data = quotation.f_name
    form.l_name.data = quotation.l_name
    form.address.data = quotation.address
    form.city.data = quotation.city
    form.state.data = quotation.state
    form.country.data = quotation.country 
    form.postal.data = quotation.postal
    form.tel.data = quotation.tel
    form.s_sched.data = quotation.s_sched
    form.s_term.data = quotation.s_term
    form.q_title.data = quotation.q_title
    form.q_note.data = quotation.q_note

    return render_template('admin/quotations/quotation.html', action="Edit",
                           add_quotation=add_quotation, form=form,
                           quotation=quotation, title="Edit Quotation")


@admin.route('/quotations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quotation(id):
    """
    Delete a quotation from the database
    """
    check_admin()

    quotation = Quotation.query.get_or_404(id)
    if quotation.locked:
        flash('Can not delete locked quotation.')
        return redirect(url_for('admin.list_quotations', page_num=1))


    quote_details = Quotation_Detail.query.filter_by(q_id=id).all()
    for quote_detail in quote_details:

        db.session.delete(quote_detail)
        db.session.commit()
        flash('You have successfully deleted the associated quotation details.')

    db.session.delete(quotation)
    db.session.commit()
    flash('You have successfully deleted the quotation.')

    # redirect to the quotations page
    return redirect(url_for('admin.list_quotations', page_num=1))

    return render_template(title="Delete Quotation")


@admin.route('/quotations/pdf/<int:id>/', methods=['GET', 'POST'])
@login_required
def gen_pdf(id):

    # Get the quotation from its unique id
    quotation = Quotation.query.filter_by(q_id=id).first()

    # Get the customer from the Quotation's Customer ID
    customer = Customer.query.filter_by(c_id=quotation.c_id).first()    

    # Get the contact frmo the Quotation's Contact ID
    contact = Contact.query.filter_by(contact_id=quotation.contact_id).first()

    # Get all of the Quotation Details that are tied to this Quotation
    quote_details = Quotation_Detail.query.filter_by(q_id=id).all()
    # Get each product associated with each Quote Detail and save to dictionary
    products = {}
    subtotal = 0
    total = 0
    for detail in quote_details:
        qd_id = detail.quote_detail_id
        product = Product.query.filter_by(p_id=detail.p_id).first()
        # products[qd_id] = product
        detail.product = product

        if detail.discount:
            total += detail.quantity * detail.q_price * (1 - detail.discount)
        else:
            total += detail.quantity * detail.q_price

        subtotal += detail.quantity * detail.q_price

    return render_template('admin/quotations/pdf.html', 
                            quotation=quotation,
                            contact=contact,
                            customer=customer,
                            quote_details=quote_details,
                            products=products,
                            # optional=optional,
                            title="PDF",
                            total=total,
                            subtotal=subtotal)
# Opportunity Views


@admin.route('/opportunities/view/<int:id>', methods=['GET'])
@login_required
def view_opportunity(id):
    """
    View a opportunity
    """
    check_admin()

    opportunity = Opportunity.query.filter_by(o_id=id).first()

    return render_template('admin/opportunities/view_opportunity.html', action="View",
                           opportunity=opportunity, title="View Opportunity")


@admin.route('/opportunities/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_opportunities(page_num):
    """
    List all opportunities
    """
    check_admin()

    # opportunities = Opportunity.query.all()
    # opportunities = Opportunity.query.paginate(per_page=5, page=page_num, error_out=True)
    opportunities = Opportunity.query.order_by(Opportunity.q_num).all()
    form = SearchForm()
    if form.validate_on_submit():
        opportunities = Opportunity.query.filter(or_(Opportunity.q_num.like("%" + form.search_string.data + "%"), 
                                        Opportunity.integrator.like("%" + form.search_string.data + "%"),
                                        Opportunity.source_of_lead.like("%" + form.search_string.data + "%"))).all()

    return render_template('admin/opportunities/opportunities.html', form=form,
                           opportunities=opportunities, title="Opportunities")


@admin.route('/opportunities/add', methods=['GET', 'POST'])
@login_required
def add_opportunity():
    """
    Add an opportunity to the database
    """
    check_admin()

    add_opportunity = True

    form = OpportunityForm()
    if form.validate_on_submit():
        q_num = form.q_num.data.q_num           # Select form returns quotation object, not q_num field
        q_id = form.q_num.data.q_id
        opportunity = Opportunity(q_id = q_id,           # special
                                    q_num = q_num,
                                    source_of_lead = form.source_of_lead.data,           
                                    sale_ref_fee = form.sale_ref_fee.data,
                                    competitors = form.competitors.data,
                                    sales_stage = form.sales_stage.data,
                                    close_date = form.close_date.data,
                                    probability = form.probability.data,
                                    rev_category = form.rev_category.data,
                                    proj_note = form.proj_note.data,
                                    application = form.application.data,
                                    family = form.family.data,
                                    potential_money = form.potential_money.data,
                                    probable_money = form.probable_money.data,
                                    actual_money = form.actual_money.data,
                                    revenue = form.revenue.data,
                                    integrator = form.integrator.data,
                                    region = form.region.data)
                                
        try:
            # add opportunity to the database
            db.session.add(opportunity)
            db.session.commit()
            flash('You have successfully added a new opportunity.')
        except:
            # in case Opportunity already exists
            flash('Error: Opportunity already exists.')

        # redirect to opportunities page
        return redirect(url_for('admin.list_opportunities', page_num=1))

    # load opportunity template
    return render_template('admin/opportunities/opportunity.html', action="Add",
                           add_opportunity=add_opportunity, form=form,
                           title="Add Opportunity")


@admin.route('/opportunities/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_opportunity(id):
    """
    Edit an opportunity
    """
    check_admin()

    add_opportunity = False

    opportunity = Opportunity.query.get_or_404(id)
    form = OpportunityForm(obj=opportunity)
    if form.validate_on_submit():
        opportunity.q_id = form.q_num.data.q_id      # special
        opportunity.q_num = form.q_num.data.q_num
        opportunity.source_of_lead = form.source_of_lead.data,          
        opportunity.sale_ref_fee = form.sale_ref_fee.data
        opportunity.competitors = form.competitors.data
        opportunity.sales_stage = form.sales_stage.data
        opportunity.close_date = form.close_date.data
        opportunity.probability = form.probability.data
        opportunity.rev_category = form.rev_category.data
        opportunity.proj_note = form.proj_note.data
        opportunity.application = form.application.data
        opportunity.family = form.family.data
        opportunity.potential_money = form.potential_money.data
        opportunity.probable_money = form.probable_money.data
        opportunity.actual_money = form.actual_money.data
        opportunity.revenue = form.revenue.data
        opportunity.integrator = form.integrator.data
        opportunity.region = form.region.data

        db.session.commit()
        flash('You have successfully edited the opportunity.')

        # redirect to the opportunities page
        return redirect(url_for('admin.list_opportunities', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.q_num.data = opportunity.q_num       
    form.source_of_lead.data = opportunity.source_of_lead       
    form.sale_ref_fee.data = opportunity.sale_ref_fee
    form.competitors.data = opportunity.competitors
    form.sales_stage.data = opportunity.sales_stage
    form.close_date.data = opportunity.close_date
    form.probability.data = opportunity.probability
    form.rev_category.data = opportunity.rev_category
    form.proj_note.data = opportunity.proj_note
    form.application.data = opportunity.application
    form.family.data = opportunity.family
    form.potential_money.data = opportunity.potential_money 
    form.probable_money.data = opportunity.probable_money
    form.actual_money.data = opportunity.actual_money 
    form.revenue.data = opportunity.revenue
    form.integrator.data = opportunity.integrator 
    form.region.data = opportunity.region

    return render_template('admin/opportunities/opportunity.html', action="Edit",
                           add_opportunity=add_opportunity, form=form,
                           opportunity=opportunity, title="Edit Opportunity")


@admin.route('/opportunities/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_opportunity(id):
    """
    Delete an opportunity from the database
    """
    check_admin()

    opportunity = Opportunity.query.get_or_404(id)
    db.session.delete(opportunity)
    db.session.commit()
    flash('You have successfully deleted the opportunity.')

    # redirect to the opportunities page
    return redirect(url_for('admin.list_opportunities', page_num=1))

    return render_template(title="Delete Opportunity")


# Quotation_Detail Views

@admin.route('/quotation_details/toggle/<int:id>/<int:option>', methods=['GET', 'POST'])
@login_required
def optional_quotation_detail(id, option):
    # Modify the option parameter of the quotation detail to boolean value: option
    quotation_detail = Quotation_Detail.query.filter_by(quote_detail_id=id).first()
    quotation_detail.option = bool(option)
    db.session.commit()
    # return "hello world" + str(id) + str(option)

    # redirect to quotation_details page
    return redirect(url_for('admin.list_quotation_details', page_num=1))



@admin.route('/quotation_details/view/<int:id>', methods=['GET'])
@login_required
def view_quotation_detail(id):
    """
    View a quotation_detail
    """
    check_admin()

    quotation_detail = Quotation_Detail.query.filter_by(quote_detail_id=id).first()

    return render_template('admin/quotation_details/view_quotation_detail.html', action="View",
                           quotation_detail=quotation_detail, title="View Quotation Detail")


@admin.route('/quotation_details/<int:page_num>', methods=['GET', 'POST'])
@login_required
def list_quotation_details(page_num):
    """
    List all quotation_details
    """
    check_admin()

    # quotation_details = Quotation_Detail.query.all()
    # quotation_details = Quotation_Detail.query.paginate(per_page=5, page=page_num, error_out=True)
    quotation_details = Quotation_Detail.query.order_by(Quotation_Detail.q_num).all()
    form = SearchForm()
    if form.validate_on_submit():
        quotation_details = Quotation_Detail.query.filter(or_(Quotation_Detail.q_num.like("%" + form.search_string.data + "%"), 
                                        Quotation_Detail.p_num.like("%" + form.search_string.data + "%"),
                                        Quotation_Detail.p_name.like("%" + form.search_string.data + "%"))).all()

    return render_template('admin/quotation_details/quotation_details.html', form=form,
                           quotation_details=quotation_details, title="Quotation_Details")


@admin.route('/quotation_details/add/<int:q_id>', methods=['GET', 'POST'])
@login_required
def add_quotation_detail(q_id):
    """
    Add a quotation_detail to the database
    """
    check_admin()

    add_quotation_detail = True

    form = Quotation_DetailForm()
    form.p_num.choices = [(product.p_id, str(product.p_number)) for product in Product.query.all()]
    # index each q_num choice by its q_id (exlcude locked quotations)
    form.q_num.choices = [(quotation.q_id, str(quotation.q_num)) for quotation in Quotation.query.filter_by(locked=False).all()]
    if q_id is not None:
        form.q_num.data = q_id
    if form.validate_on_submit():
        q_id = form.q_num.data
        quotation = Quotation.query.filter_by(q_id=q_id).first()
        q_num = quotation.q_num
        p_id = form.p_num.data
        product = Product.query.filter_by(p_id=p_id).first()
        p_num = product.p_number
        quotation_detail = Quotation_Detail(q_id = q_id,     
                                p_id = p_id,                
                                p_name = product.p_name,           
                                q_num = q_num,
                                p_num = p_num,
                                quantity = form.quantity.data,
                                discount = form.discount.data,
                                q_price = form.q_price.data,
                                option = form.option.data)
                                
        try:
            # add quotation_detail to the database
            db.session.add(quotation_detail)
            db.session.commit()
            flash('You have successfully added a new quotation_detail.')
        except:
            # in case Quotation_Detail already exists
            flash('Error: Quotation_Detail already exists.')

        # Update the quote amount for the parent quote to reflect this new quotation detail
        quotation = Quotation.query.get_or_404(q_id)
        quotation.q_amount = 0
        quote_details = Quotation_Detail.query.filter_by(q_id=q_id).all()

        for quote_detail in quote_details:
            if quote_detail.option is False:
                quotation.q_amount += quote_detail.quantity * quote_detail.q_price * (1 - quote_detail.discount)

        db.session.commit()

        # redirect to quotation_details page
        return redirect(url_for('admin.list_quotation_details', page_num=1))

    # load quotation_detail template
    return render_template('admin/quotation_details/quotation_detail.html', action="Add",
                           add_quotation_detail=add_quotation_detail, form=form,
                           title="Add Quotation_Detail")


@admin.route('/quotation_details/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quotation_detail(id):
    """
    Edit a quotation_detail
    """
    check_admin()

    add_quotation_detail = False

    quotation_detail = Quotation_Detail.query.get_or_404(id)

    # First check if this is a locked quotation before proceeding
    quotation = Quotation.query.get_or_404(quotation_detail.q_id)
    if quotation.locked:
        flash('Error, can not edit a detail of a locked quotation')
        return redirect(url_for('admin.list_quotation_details', page_num=1))

    form = Quotation_DetailForm(obj=quotation_detail)
    form.p_num.choices = [(product.p_id, str(product.p_number)) for product in Product.query.all()]
    # index each q_num by its q_id
    form.q_num.choices = [(quotation.q_id, str(quotation.q_num)) for quotation in Quotation.query.filter_by(locked=False).all()]
    if form.validate_on_submit():
        q_id = form.q_num.data
        quotation = Quotation.query.filter_by(q_id=q_id).first()
        q_num = quotation.q_num
        p_id = form.p_num.data
        product = Product.query.filter_by(p_id=p_id).first()
        p_num = product.p_number
        quotation_detail.q_num = q_num
        quotation_detail.p_num = p_num
        quotation_detail.q_id = q_id
        quotation_detail.p_id = p_id
        quotation_detail.p_name = product.p_name
        quotation_detail.quantity = form.quantity.data
        quotation_detail.discount = form.discount.data
        quotation_detail.q_price = form.q_price.data
        quotation_detail.option = form.option.data

        db.session.commit()
        flash('You have successfully edited the quotation_detail.')


        # Update the quote amount for the parent quote to reflect this new quotation detail
        quotation = Quotation.query.get_or_404(q_id)
        quotation.q_amount = 0
        quote_details = Quotation_Detail.query.filter_by(q_id=q_id).all()

        for quote_detail in quote_details:
            if quote_detail.option is False:
                quotation.q_amount += quote_detail.quantity * quote_detail.q_price * (1 - quote_detail.discount)

        db.session.commit()

        # redirect to the quotation_details page
        return redirect(url_for('admin.list_quotation_details', page_num=1))

    # fill the form with current data to show what changes are to be made
    form.q_num.data = quotation_detail.q_id
    form.p_num.data = quotation_detail.p_id               
    form.quantity.data = quotation_detail.quantity
    form.discount.data = quotation_detail.discount

    
    form.q_price.data = quotation_detail.q_price 
    form.option.data = quotation_detail.option

    return render_template('admin/quotation_details/quotation_detail.html', action="Edit",
                           add_quotation_detail=add_quotation_detail, form=form,
                           quotation_detail=quotation_detail, title="Edit Quotation_Detail")


@admin.route('/quotation_details/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quotation_detail(id):
    """
    Delete a quotation_detail from the database
    """
    check_admin()

    quotation_detail = Quotation_Detail.query.get_or_404(id)
    # get the details quotation
    q_id = quotation_detail.q_id
    quotation = Quotation.query.get_or_404(q_id)

    # Make sure you don't modify a locked quotation
    if quotation.locked:
        flash('Error, can not delete detail of locked quotation!')
        return redirect(url_for('admin.list_quotation_details', page_num=1))

    # Only delete if its unlocked
    db.session.delete(quotation_detail)
    db.session.commit()
    flash('You have successfully deleted the quotation_detail.')

    # Update the quote amount for the parent quote to reflect this new quotation detail deletion
    quotation = Quotation.query.get_or_404(q_id)
    quotation.q_amount = 0
    quote_details = Quotation_Detail.query.filter_by(q_id=q_id).all()

    for quote_detail in quote_details:
        if quote_detail.option is False:
            quotation.q_amount += quote_detail.quantity * quote_detail.q_price * (1 - quote_detail.discount)

    db.session.commit()

    # redirect to the quotation_details page
    return redirect(url_for('admin.list_quotation_details', page_num=1))

    return render_template(title="Delete Quotation_Detail")


@admin.route('/quotation_details/background_process')
@login_required
def _get_unit_price():
    p_num = request.args.get('product_num', '1', type=str)
    product = Product.query.filter_by(p_number=p_num).first()
    print(p_num, product.unit_price, product.p_name)
    try:
        if current_user.language == 'ja':
            price = product.japanese_unit_price
            name = product.japanese_p_name
            currency = 'YEN'
        else:
            price = product.unit_price
            name = product.p_name
            currency = 'USD'
    except Exception as e:
        price = 0

    result = {'price': price, 'name': name, 'currency': currency}
    return jsonify(result)












