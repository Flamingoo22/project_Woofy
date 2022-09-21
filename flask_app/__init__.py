from flask import Flask
from flask_bcrypt import Bcrypt
DATABASE = 'woofy'

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'dsadsa'