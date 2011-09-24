import cgi
import os
import logging

from google.appengine.ext import db


class Tasks(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    phone_number = db.StringProperty()

