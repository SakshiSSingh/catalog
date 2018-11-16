from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from sqlalchemy.orm import scoped_session
from flask import session as login_session
import random
import string
import datetime
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
  open('client_secrets.json', 'r').read())['web']['client_id']


"""Connect to Database and create database session"""
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['picture']
        del login_session['provider']

        flash('You are logged out Successfully')
        return redirect(url_for('showcatalog'))
    else:
        flash('You are not login')
        return redirect(url_for('showcatalog'))


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
            json.dumps('Failed to upgrade the authorization code'), 401)
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
    #  print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

# See if user exists or if it doesn't make a new one
    print 'User email is' + str(login_session['email'])
    try:
        user = session.query(User).filter_by(email=email).first()
        user_id = user.id
    except Exception:
        user_id = None
    if user_id:
        print 'Existing user#' + str(user_id) + 'matches this email'
    else:
        newUser = User(name=login_session['username'], email=login_session[
            'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    user_id = user.id
    print 'New user_id#' + str(user_id) + 'created'
    login_session['user_id'] = user_id
    print 'Login session is  tied to :id#' + str(login_session['user_id'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px; - \
        webkit-border-radius: 150px; -moz-border-radius: 150px; " > '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        # del login_session['access_token']
        # del login_session['gplus_id']
        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to \
        revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    """ creates new user in db and extracts al necessary fields t populate it
    with the info gathered from the login_session, i then returns the user id
    of the new user created."""

    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user_id


def getUserInfo(user_id):
    """ returns the user object associated with this ID number. """

    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """ takes an email address and return an ID nummber if that email address
    belongs to a user stored in our db if not, it returns none """

    try:
        user = session.query(User).filter_by(email=email).one()
        return user_id
    except Exception:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("Please log in to add, edit and delete content")
            return redirect('/login')
    return decorated_function


@app.route('/catalog/<int:category_id>/in/<int:item_id>/JSON')
def categoryItem(category_id, item_id):
    CategoryItem = session.query(Item).filter_by(id=item_id).one()
    return jsonify(CategoryItem=CategoryItem.serialize)


@app.route('/catalog/<int:category_id>/in/JSON')
def category(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(
        categories=[category.serialize for category in categories])


@app.route('/')
@app.route('/catalog/')
def showcatalog():
    """show catalog of categories"""

    categories = session.query(Category).order_by(asc(Category.name))
    latest = session.query(Item).order_by(Item.created.desc())
    return render_template('homepage.html',
                           categories=categories,
                           latest=latest)


@app.route('/catalog/<int:category_id>/in')
def showcategory(category_id):
    """show in category items"""

    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('inCategory.html', items=items, category=category)


@app.route('/catalog/<int:category_id>/in/<int:item_id>')
def desc_item(category_id, item_id):
    """description of item"""

    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('inItem.html', item=item, category=category)


@app.route('/catalog/<int:category_id>/in/new/', methods=['GET', 'POST'])
@login_required
def newItem(category_id):
    """Create a new item"""

    category = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form[
            'description'],  category_id=category_id,
            created=datetime.datetime.now(), user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showcategory', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


@app.route('/catalog/<int:category_id>/in/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    """edit item"""

    categories = session.query(Category).order_by(asc(Category.name))
    editedItem = session.query(Item).filter_by(id=item_id).one()

    if editedItem.user_id != login_session['user_id']:
        return """<script>function unauth()
        {alert('You are not authorized to edit this item.');}
        </script><body onload='unauth()''>"""

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
            flash('Item successfully Edited')
        session.add(editedItem)
        session.commit()
        flash('Item edited successfully')
        return redirect(url_for('showcategory', category_id=category_id))
    else:
        return render_template('editItem.html',
                               category_id=category_id,
                               item=editedItem)


@app.route('/catalog/<int:category_id>/in/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def delete_item(category_id, item_id):
    """delete item"""

    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return"""<script>function unauth()
        {alert('You are not authorized to delete this item.');}
        </script><body onload='unauth()''>"""

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showcategory', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=3010)
