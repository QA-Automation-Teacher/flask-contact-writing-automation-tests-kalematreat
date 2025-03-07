import json
from flask import jsonify, Flask, redirect, url_for, render_template, request, flash
from models import db, Contacts
from forms import ContactForm

# Flask
app = Flask(__name__)
app.secret_key = 'my secret'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('contacts'))


@app.route("/new_contact", methods=('GET', 'POST'))
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Get form
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        # Save in database
        try:
            my_contact = Contacts(name, surname, email, phone)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Contact created correctly', 'success')
            return redirect(url_for('contacts'))
        except:
            db.session.rollback()
            flash('Error generating contact.', 'danger')

    return render_template('web/new_contact.html', form=form)


@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''
    form = ContactForm()
    my_contact = Contacts.query.filter_by(id=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        # Get form
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        try:
            # Update contact
            my_contact.name = name
            my_contact.surname = surname
            my_contact.email = email
            my_contact.phone = phone
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update contact.', 'danger')
    return render_template(
        'web/edit_contact.html',
        form=form,
        my_contact=my_contact)




@app.get("/contacts")
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contacts.query.order_by(Contacts.name).all()
    return jsonify([c.to_dict() for c in contacts])




# @app.route("/contacts")
# def contacts():
#     '''
#     Show alls contacts
#     '''
#     contacts = Contacts.query.order_by(Contacts.name).all()
#     return render_template('web/contacts.html', contacts=contacts)


@app.route("/search")
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_contacts = Contacts.query.filter(
        Contacts.name.contains(name_search)
        ).order_by(Contacts.name).all()
    return render_template('web/contacts.html', contacts=all_contacts)


@app.route("/contacts/delete/<id>")
def contacts_delete(id):
    '''
    Delete contact

    :param id: Id from contact
    '''
    try:
        mi_contacto = Contacts.query.filter_by(id=id).first()
        db.session.delete(mi_contacto)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('contacts'))


if __name__ == "__main__":
    app.debug = True
    app.run()