#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import (
    Flask, render_template, request, redirect,
    jsonify, url_for, flash)
from database_setup import Catalog, User, Catalog_Item, Base, engine
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random
from functools import wraps
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, redirect, url_for, flash
import requests


# connect to database and make a session object
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# creating a login decorator function
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if login_session.get("username"):
            return f(*args, **kwargs)
        else:
            flash('You are trying to access page for registered users only.\
                  Please log in before continuing..')
            return redirect(url_for("home_page"))
    return wrap


# endpoint for homepage at  root "/"
@app.route('/')
def home_page():
    # returns a random alphanumeric string
    # which is sent as a variable in home.html template
    state = showLogin()
    try:
        # this block is executed if tables already exist
        results = session.query(Catalog).all()
        latest_catalog_items = session.query(
            Catalog_Item).order_by(
            Catalog_Item.created_date.desc()).all()
        count = len(results)
        return render_template('home.html', catalog_results=results,
                               STATE=state, LATEST=latest_catalog_items)
    except:
        # this block is executed when all tables do not exist
        return render_template('home.html', STATE=state)


# endpoint for page for creating items
@app.route("/create_catalog_main")
@login_required
def create_catalog_main():
    if login_session.get("username") is not None:
        return render_template('create_catalog_main.html')
    else:
        response = make_response(
            json.dumps('Not Authorised.Please log in'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response


# endpoint for receiving request from form which
# creates the category
@app.route("/add_category", methods=['POST'])
@login_required
def add_category():
    if request.form:
        category = request.form.get("ct_name")
        category_image = request.form.get("ct_image")
        catalog = session.query(Catalog).all()
        logged_user = login_session['email']
        user_db = session.query(User).filter(User.email == logged_user).first()
        for items in catalog:
            if category == items.name:
                flash("Name taken.Please choose another!")
                return render_template("create_catalog_main.html")
        try:
            id_check = session.query(Catalog).order_by(
                                     Catalog.id.desc()).first()
            new_id = id_check.id + 1
        except:
            new_id = 1
        query = Catalog(id=new_id, name=category, image=category_image,
                        user=user_db)
        session.add(query)
        session.commit()
        flash("Category" + " " + category + " " + "created")
    return render_template("create_catalog_main.html")


# endpoint for receiving request from form which
# creates the category items
@app.route("/add_category_item", methods=['POST'])
@login_required
def add_category_item():
    if request.form:
        category = request.form.get("item_category")
        item = request.form.get("item_name")
        description_item = request.form.get("item_description")
        image_item = request.form.get("item_image")
        # if the user has already saved item in the category
        # check for same name
        try:
            query = session.query(
                Catalog_Item).filter(
                Catalog_Item.name == item).all()
            if len(query) != 0:
                # app.logger.info(query[0].name)
                flash("Item name exists." + " " +
                      "Either use another name or edit the already saved")
                return render_template("create_catalog_main.html")
            else:
                # including id in this way to avoid manual
                # inclusion
                id_check = session.query(Catalog_Item).order_by(
                    Catalog_Item.id.desc()).first()
                new_id = id_check.id + 1
        except:
            pass
            # initialising first item in database
            new_id = 1
        creator = session.query(User).filter(
            User.email == login_session["email"]).first()
        parent = session.query(Catalog).filter(
            Catalog.name == category).first()
        query = Catalog_Item(
            id=new_id, name=item,
            user=creator, catalog=parent,
            description=description_item,
            image=image_item)
        session.add(query)
        session.commit()
        flash("Item" + " " + item + " " + "created")
    return render_template("create_catalog_main.html")


# endpoint that returns json for all the items in
# catalog table
@app.route("/get_all_categories")
def get_all_categories():
    result = session.query(Catalog).all()
    return json.dumps([items.serialize for items in result])


@app.route("/catalog/json")
def get_all_json():
    result = session.query(Catalog_Item).all()
    return json.dumps([items.serialize for items in result])


@app.route("/del/<category>/")
@login_required
def del_category(category):
    try:
        result = session.query(Catalog).filter(Catalog.name == category).one()
        app.logger.info(result.user.name)
        creator = result.user.email
        deleter = login_session['email']
        app.logger.info(creator)
        app.logger.info(deleter)
        if creator == deleter:
            session.delete(result)
            session.commit()
            flash("Category" + " " + category + " " + "deleted")
            return redirect(url_for("home_page"))
        elif creator != deleter:
            flash("Permission denied:Not Authorised")
            return redirect(url_for("home_page"))
    except:
        flash("The category doesnt exist")
        return redirect(url_for("home_page"))


@app.route("/catalog/<catalog_item>/edit",
           methods=['GET', 'POST'])
def edit_catalog_item(catalog_item):
    user_session = login_session["email"]
    user_db = session.query(Catalog_Item).filter(
        Catalog_Item.user.has(
            email=user_session)).first()
    app.logger.info(user_db.user.email)
    user_db_email = user_db.user.email
    app.logger.info(user_db_email)
    result = session.query(Catalog_Item).filter(
        Catalog_Item.name == catalog_item).first()
    if user_session == user_db_email:
        return render_template("edit_item.html", RESULT=result)
    else:
        return "Not authorised"


@app.route('/modify_catalog_item/<item_original_name>',
           methods=['GET', 'POST'])
@login_required
def modify_catalog_item(item_original_name):
    if request.method == 'POST':
        if request.form:
            item = request.form.get('item_name')
            description = request.form.get('item_description')
            image = request.form.get('item_image')
            category = request.form.get('item_category')
            app.logger.info(category)
            user_session = login_session["email"]
            query = session.query(Catalog_Item).filter(
                Catalog_Item.name == item_original_name).first()
            category = session.query(Catalog).filter(
                Catalog.name == category).first()
            user_db_email = query.user.email
            if user_session == user_db_email:
                id = query.id
                query_user = session.query(User).filter(
                    User.email == login_session["email"]).first()
                query.name = item
                query.description = description
                query.image = image
                query.user = query_user
                query.catalog = category
                app.logger.info(query.catalog)
                session.add(query)
                session.commit()
                flash(item_original_name + " " + "has been modified")
                return redirect(url_for("home_page"))


@app.route('/delete_catalog_item/<item_name>', methods=['GET', 'POST'])
@login_required
def delete_item(item_name):
    if request.method == 'POST':
        if request.form:
            item = request.form.get('item_name')
            user_session = login_session["email"]
            query = session.query(Catalog_Item).filter(
                Catalog_Item.name == item_name).first()
            app.logger.info(query)
            user_db_email = query.user.email
            if user_session == user_db_email:
                session.delete(query)
                session.commit()
                flash(item_name + " " + "has been deleted")
                return redirect(url_for("home_page"))


@app.route("/catalog/<category>", methods=["GET"])
def view_all_items(category):
    result = session.query(Catalog_Item).filter(
                           Catalog_Item.catalog.has(name=category)).all()
    for items in result:
        parent = items.catalog.name
        app.logger.info(parent)
    return render_template("view_catalog_items.html", RESULT=result)


@app.route("/catalog/<category>/<catalog_item>/<owner>", methods=["GET"])
def view_items(category, catalog_item, owner):
    query = session.query(Catalog_Item)
    app.logger.info(category)
    app.logger.info(catalog_item)
    result = query.filter(Catalog_Item.name == catalog_item).all()
    if login_session.get("username") is not None:
        user_session_email = login_session["email"]
        user_db = query.filter(Catalog_Item.user.has(id=owner)).first()
        app.logger.info(user_db)
        app.logger.info(user_session_email)
        user_db_email = user_db.user.email
        # app.logger.info(user_session)
        # print user_db.user
        # app.logger.info(user_db.user.email)
        # app.logger.info(result)
        if user_session_email == user_db_email:
            login_session["edit_auth"] = True
    return render_template("view_items.html", RESULT=result)


# Create anti-forgery state token
# TODO remove the route

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return state


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.',
                                 login_session['state']), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have tosplit the token first on commas and select the first index
        which gives us the key : valuefor the server access token then we split
        it on colons to pull out the actual token value and replace the remaining
        quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    app.logger.info(data)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    # no email key in response,temporary hack
    login_session['email'] = data["name"]+"@test.com"
    login_session['facebook_id'] = data["id"]
    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token
    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]
    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += 'Welcome, '
    output += login_session['username']
    output += '<br>Redirecting...'
    print "done!"
    return output
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['access_token']
    del login_session['username']
    del login_session['provider']
    del login_session['email']
    del login_session['facebook_id']
    if login_session.get('edit_auth'):
        del login_session["edit_auth"]
    else:
        pass
    return redirect(url_for('home_page'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    state_token = request.args.get('state')
    app.logger.info(state_token)
    if state_token != login_session['state']:
        response = make_response(json.dumps(login_session['state']), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    app.logger.info(code)
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        app.logger.info(credentials.access_token)
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
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
    app.logger.info(data)
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
    output += 'Welcome, '
    output += login_session['username']
    output += '<br>Redirecting...'
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
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


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        if login_session.get('edit_auth'):
            del login_session["edit_auth"]
        else:
            pass
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('home_page'))
    else:
        login_session.clear()
        response = make_response(json.dumps(
                                 'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash("Succesfully Signed Out")
        return redirect(url_for("home_page"))


app.secret_key = 'jkjko90890898'


app.run(debug='true', port=8000)
