import cgi
import datetime
import urllib
import urllib2
import wsgiref.handlers
import os
import logging
import time
import re
import base64

# local imports
import model

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.dist import use_library
from google.appengine.api import images
from google.appengine.api import mail

from django.utils import simplejson as json

use_library('django', '1.2')

from gaesessions import get_current_session


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')



class JustAnotherHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


class MyTasks(webapp.RequestHandler):
    def get(self):
        
        task = model.Task()
        task.name = 'name'
        task.description = 'description'
        task.deadline = datetime.datetime.now()
        task.priority = 1
        #task.patient = 'description'
        task.when_completed = datetime.datetime.now()
        #task.completed_by = 'description'
        #task.assigned_to = 'description'

        

        template_values = {}
        template_values['open_tasks'] = []
        template_values['closed_tasks'] = []
        path = os.path.join(os.path.dirname(__file__), 'html/TasksView.html')
        self.response.out.write(template.render(path, template_values))

class MyPatients(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/PatientsView.html')
        self.response.out.write(template.render(path, template_values))
        
class TaskDetails(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/TaskDetails.html')
        self.response.out.write(template.render(path, template_values))
        
class CreateNewTask(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/CreateNewTask.html')
        self.response.out.write(template.render(path, template_values))

class DummyDataSetup(webapp.RequestHandler):
    def get(self):
        
        d1 = model.Doctor()
        d1.name = "Doctor 1"
        d1.put()
        
        d2 = model.Doctor()
        d2.name = "Doctor 2"
        d2.put()
        
        r1 = model.Room()
        r1.name = "Room 1"
        r1.zone = "Zone 1"
        r1.put()
        
        r1 = model.Room()
        r1.name = "Room 1"
        r1.zone = "Zone 1"
        r1.put()

        path = os.path.join(os.path.dirname(__file__), 'html/CreateNewTask.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/myTasks', MyTasks),
                                          ('/myPatients', MyPatients),
                                          ('/taskDetails', TaskDetails),
                                          ('/createNewTask', CreateNewTask),
    
                                          ('/dummyDataSetup', DummyDataSetup),
    
    
                                          ('/dummyHandler', JustAnotherHandler)
    
                                         ], debug=True)
    run_wsgi_app(application)




if __name__ == '__main__':
    main()




