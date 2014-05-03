from flask import Flask

# initialize the flask application
app = Flask(__name__)

# load application settings
app.config.from_object('settings')
