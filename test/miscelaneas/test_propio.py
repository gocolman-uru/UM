import flask


import json
import os
import flask
#from flask import Flask, render_template, request, redirect, url_for, session, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash




dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = flask.Flask(__name__)

print(app)