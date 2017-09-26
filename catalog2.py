from flask import Flask, render_template, request, redirect,jsonify, url_for, flash, abort
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from db_setup2 import Base, Category, Item, User

#New imports for this step
from flask import session as login_session
import random
import string

#IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)


#Connect to Database and create database session
engine = create_engine('sqlite:///catalog2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create anti-forgery state token
@app.route('/catalog/login', methods = ['GET', 'POST'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            error = 'Username and Password Required'
        if session.query(User).filter_by(username = username).first() is None or not user.verify(password):
            error = 'Invalid username or password'
        user = session.query(User).filter_by(username = username).first()
        print user
        #if user.verify_password(password):
            #login_session['username'] = username
            #print jsonify({'username': user.username}), 201
        return render_template('login.html', STATE=state, error = error)
    else:
        return render_template('login.html', STATE=state, error = error)

@app.route('/logout')
def logout():
    if 'username' in login_session:
        del login_session['username']
        return redirect(url_for('showCatalog'))

# Add user registration and authentication functionality. These three following functions were taken from
# Udacity Fullstack Nanodegree
@app.route('/catalog/user-signup', methods = ['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            abort(400) #missing input
        if session.query(User).filter_by(username = username).first() is not None:
            abort(400) #existing user
        user = User(username = username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        print jsonify({'username': user.username}), 201
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newUser.html')

#JSON APIs to view category Information
@app.route('/catalog/<category_name>/JSON')
def categoryJSON(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(category_name = category_name).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemJSON(category_name, item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    return jsonify(Item = item.serialize)

@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [c.serialize for c in categories])


#Show the catalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(desc(Item.created)).limit(8)
    return render_template('catalog.html', categories = categories, items = items)


#Show a category
@app.route('/catalog/<category_name>/')
def showCategory(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name = category_name)
    items = session.query(Item).filter_by(category_name = category_name).all()
    if 'username' not in login_session:
        return render_template('publicCategory.html', categories = categories, items = items, category =
            category, category_name = category_name)
    else:
        return render_template('category.html', categories = categories, items = items, category =
            category, category_name = category_name)


@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    item = session.query(Item).filter_by(name = item_name, category_name = category_name).one()
    if 'username' not in login_session:
        return render_template('publicItem.html', category = category, category_name = category_name, item = item, item_name = item_name)
    else:
        return render_template('item.html', category = category, category_name = category_name, item = item, item_name = item_name)



#Create a new menu item
@app.route('/catalog/<category_name>/new_item/', methods=['GET','POST'])
def newItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name = category_name).one()
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], category_name = category_name, category = category)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_name = category_name))
    else:
        return render_template('newItem.html', category_name = category_name)

#Edit a menu item
@app.route('/catalog/<category_name>/<item_name>/edit/', methods=['GET','POST'])
def editItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(name = item_name, category_name = category_name).one()
    category = session.query(Category).filter_by(name = category_name).one()
    if request.method == 'POST':
        if request.form['name']:
            print request.form['name']
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category = category
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCategory', category_name = category_name))
    else:
        return render_template('editItem.html', item_name = item_name, item = editedItem, category_name = category_name, category = category)


#Delete a menu item
@app.route('/catalog/<category_name>/<item_name>/delete/', methods = ['GET','POST'])
def deleteItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name = category_name).one()
    itemToDelete = session.query(Item).filter_by(name = item_name, category_name = category_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCategory', category_name = category_name))
    else:
        return render_template('deleteItem.html', category_name = category_name, item_name = item_name, item = itemToDelete)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)