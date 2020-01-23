import json
import os
import sqlite3

# Third-party libraries
from flask import Flask, redirect, request, url_for,render_template,flash
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from newschannel import *
from collections import defaultdict
from flask_socketio import SocketIO,send,emit
from jinja2 import Environment as env ,FileSystemLoader as fs_loader

from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from flask_bcrypt import Bcrypt

# Internal imports
from sqldb import init_db_command
from user import User
from forms import *


with open("creds.json") as f:
    config=json.load(f)
# Configuration
GOOGLE_CLIENT_ID = config.get("cid")
GOOGLE_CLIENT_SECRET = config.get("secret")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


app=Flask(__name__)
app.secret_key=GOOGLE_CLIENT_SECRET
login_manager=LoginManager()
login_manager.init_app(app)
bcrypt=Bcrypt(app)



# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get_from_id(user_id)

#Flask-Login unauthorized handler 
@login_manager.unauthorized_handler
def unauthorized():
    flash("you need to login before you access homepage","warning")
    return redirect(url_for("signin"))

socketio=SocketIO(app)
mychannel=Newschannel('cnn')
topnews=mychannel.get_top_news(5)
news_src={}
jinjaenv = env(loader=fs_loader('templates'))
for k in Newschannel.COUNTRY_CODE.keys():
    news_src.update({k: Newschannel.get_all_srcs(k)})



#  homepage

@app.route("/signin",methods=["GET","POST"])
def signin():
    loginform=Loginform()
    
    if loginform.validate_on_submit():
        user=User.get(loginform.email.data)
        if user and bcrypt.check_password_hash(user.password,loginform.password.data):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html",form=loginform)
  

@app.route("/")
@login_required
def index():
    print(current_user.__dict__)
    return render_template("index.html",user=current_user,title="Dash34",articles=topnews,srcs=news_src)
    

@app.route("/signup",methods=["GET","POST"])
def register():
    signupform=Signupform()
    if signupform.validate_on_submit():
        passhash=bcrypt.generate_password_hash(signupform.password.data).decode("utf8")
        if(User.get(signupform.email.data)):
            flash(f"there is a user already with the email {signupform.email.data}","error")
        else:
            User.create(signupform.username.data,signupform.email.data,password=passhash,acctype="local")
            flash(f"user created {signupform.username.data}","success")
            return redirect(url_for("signin"))
    return render_template("register.html",form=signupform)



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@socketio.on('connected')
def coneected(data):
    print(data)

@socketio.on('newschannel selected')
def newchannel(data):
    newschannel=Newschannel(data["data"])
    newnews=newschannel.get_top_news(5)
    sendnews=''
    for article in newnews:
        sendnews=sendnews+(jinjaenv.get_template('article').render(article=article))
    emit("news recieved",{"news": sendnews })



@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    # Doesn't exist? Add it to the database.
    if not User.get(users_email):
        flash(f"this email is not registered  {users_email} just added ","info")
        User.create(name=users_name,email=users_email,profile_pic=picture,acctype="google")
        
        
    user=User.get(users_email)
        

    # Begin user session by logging the user 
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__=="__main__":
      socketio.run(app,debug=True,ssl_context="adhoc")