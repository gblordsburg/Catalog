from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash, abort
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc, and_
from sqlalchemy.orm import sessionmaker
from db_setup2 import Base, Category, Item, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item-Catalog"


# Connect to the database and create database session
engine = create_engine('sqlite:///catalog2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# These following functions were taken from Udacity Fullstack Nanodegree
# Backend: Databases & Applications lessons and modified.


# Create anti-forgery state token
@app.route('/catalog/login', methods=['GET', 'POST'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        print(username, password, user.username)
        if username is None or password is None:
            error = 'Username and Password Required'
        if user is None or not user.verify_password(password):
            error = 'Invalid username or password'
        if user.verify_password(password):
            login_session['username'] = username
            print(jsonify({'username': user.username}), 201)
            return redirect(url_for('showCatalog'))
        return render_template('login.html', STATE=state, error=error)
    else:
        return render_template('login.html', STATE=state, error=error)


@app.route('/logout')
def logout():
    if 'username' in login_session:
        del login_session['username']
        return redirect(url_for('showCatalog'))


# Add user registration and authentication functionality.
@app.route('/catalog/user-signup', methods=['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            abort(400)  # missing input
        if session.query(User).filter_by(
                    username=username).first() is not None:
            abort(400)  # existing user
        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        print(jsonify({'username': user.username}), 201)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newUser.html')


# JSON APIs to view category Information
@app.route('/catalog/<category_name>/JSON')
def categoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_name=category_name).all()
    return jsonify(Items=[item.serialize for item in items])


@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemJSON(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])

#Following third party authentication and authorization taken from
#Authentication and Authorization coursework of Udacity Fullstack
#Nanodegree


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# User Helper Functions snipped from Udacity's FSND Backend Lesson 17: Securing your API
def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response



# Show the catalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(desc(Item.created)).limit(8)
    return render_template('catalog.html', categories=categories, items=items)


# Show a category
@app.route('/catalog/<category_name>/')
def showCategory(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name)
    items = session.query(Item).filter_by(category_name=category_name).all()
    numitems = len(items)
    if 'username' not in login_session:
        return render_template(
                    'publicCategory.html', categories=categories,
                    items=items, category=category,
                    category_name=category_name, numitems=numitems)
    else:
        return render_template(
                    'category.html',
                    categories=categories,
                    items=items, category=category,
                    category_name=category_name,
                    numitems=numitems)


@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name,
                                         category_name=category_name).one()
    if 'username' not in login_session:
        return render_template(
                    'publicItem.html',
                    category=category,
                    category_name=category_name,
                    item=item,
                    item_name=item_name)
    else:
        return render_template(
                    'item.html',
                    category=category,
                    category_name=category_name, item=item,
                    item_name=item_name)


# Create a new menu item
@app.route('/catalog/<category_name>/new_item/', methods=['GET', 'POST'])
def newItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
        newItem = Item(
                    name=request.form['name'],
                    description=request.form['description'],
                    category_name=category_name,
                    category=category)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('newItem.html', category_name=category_name)


# Edit an item
@app.route('/catalog/<category_name>/<item_name>/edit/',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(
                                        name=item_name,
                                        category_name=category_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
        if request.form['name']:
            print(request.form['name'])
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category = category
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template(
                    'editItem.html',
                    item_name=item_name,
                    item=editedItem,
                    category_name=category_name,
                    category=category)


# Delete an item
@app.route('/catalog/<category_name>/<item_name>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    deleteItem = session.query(Item).filter_by(
                                        name=item_name,
                                        category_name=category_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template(
                    'deleteItem.html', category_name=category_name,
                    item_name=item_name, item=deleteItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run()
