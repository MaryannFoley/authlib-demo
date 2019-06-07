import authlib
from authlib.client import OAuth2Session
import flask

app = flask.Flask(__name__)
app.secret_key = "idk what this is"

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

try:
    f=open("./key.txt","r")
except FileNotFoundError as e:
    raise Exception('Error: key.txt file not found')

k=f.read().rstrip("\n")
f.close()

try:
    f2=open("./secret.txt","r")
except FileNotFoundError as e:
    raise Exception('Error: secret.txt file not found')

s=f2.read().rstrip("\n")
f2.close()

@app.route("/")
def home():
    session = OAuth2Session(k, s,scope="profile email",redirect_uri='http://localhost:5000/second')

    uri,state=session.authorization_url(AUTHORIZATION_URL)

    flask.session.permanent=True
    flask.session["auth_state"]=state
    print(flask.session)

    return flask.redirect(uri,code=302)

@app.route("/second")
def redirect():
    state=flask.request.args.get("state",default=None,type=None)
    print(flask.session)
    # if state != flask.session["auth_state"]:
    #     return flask.render_template("oauth.html",something="Uhh you done messed up")
    session = OAuth2Session(k, s,redirect_uri='http://localhost:5000/second')

    oauth2_tokens = session.fetch_access_token(ACCESS_TOKEN_URI,authorization_response=flask.request.url)
    print("OAUTH TOKEN:  ")
    print(oauth2_tokens)
    flask.session["auth_token"]=oauth2_tokens
    h=session.get("https://people.googleapis.com/v1/people/me?personFields=emailAddresses")
    print(h)
    try:
        email=h.json()["emailAddresses"][0]["value"]
        return flask.render_template("oauth.html",something=email)
    except:
        return flask.redirect("/")

if __name__ == "__main__":
    app.debug = True
app.run()
