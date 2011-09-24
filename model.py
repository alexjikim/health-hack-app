import cgi
import os
import logging

from google.appengine.ext import db

class Doctor(db.Model):
    name = db.StringProperty()
    
class Room(db.Model):
    name = db.StringProperty()
    zone = db.StringProperty()
    
class Patient(db.Model):
    name = db.StringProperty()
    room = db.ReferenceProperty(reference_class=Room)
    doctor = db.ReferenceProperty(reference_class=Doctor)
    
class Tasks(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    when_added = db.DateTimeProperty(auto_now_add=True)
    deadline = db.DateTimeProperty()
    priority = db.IntegerProperty()
    patient = db.ReferenceProperty(reference_class=Patient)
    when_completed = db.DateTimeProperty()
    completed_by = db.ReferenceProperty(reference_class=Doctor, collection_name="completed_tasks")
    assigned_to = db.ReferenceProperty(reference_class=Doctor, collection_name="assigned_tasks")
    
    
    

    
    

