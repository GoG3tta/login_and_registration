from flask import Flask

DATABASE = 'login_and_registration_schema' # CHANGE PROJECT_SCHEMA TO SQL SCHEMA

app = Flask(__name__)
app.secret_key = 'it is Go Time'