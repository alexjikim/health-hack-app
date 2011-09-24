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
from persistence import get_tasks_for_patient, get_all_patients



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
        
        q = db.GqlQuery("SELECT * FROM Task")
        tasks = q.fetch(limit=50)


        open_tasks = []
        closed_tasks = []
        for task in tasks:
            if task.when_completed:
                closed_tasks.append(task)
            else:
                open_tasks.append(task)

        template_values = {}
        template_values['open_tasks'] = open_tasks
        template_values['closed_tasks'] = closed_tasks
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
        
        r1 = model.Room()
        r1.name = "Room 1"
        r1.zone = "Zone 1"
        r1.put()
        
        r2 = model.Room()
        r2.name = "Room 2"
        r2.zone = "Zone 2"
        r2.put()

        p1 = model.Patient()
        p1.name = "Patient 1"
        p1.room = r1
        p1.doctor = d1
        p1.put()

        p2 = model.Patient()
        p2.name = "Patient 2"
        p2.room = r1
        p2.doctor = d1
        p2.put()
        
        t1 = model.Task()
        t1.name = 'Task 1'
        t1.description = 'Task 1 description'
        t1.deadline = datetime.datetime.strptime("09/24/2011 10:30 PM", "%m/%d/%Y %I:%M %p")
        t1.priority = 1
        t1.patient = p1
        t1.assigned_to = d1
        t1.put()
        
        t2 = model.Task()
        t2.name = 'Task 2'
        t2.description = 'Task 2 description'
        t2.deadline = datetime.datetime.strptime("09/24/2011 11:30 PM", "%m/%d/%Y %I:%M %p")
        t2.priority = 1
        t2.patient = p1
        t2.assigned_to = d1
        t2.put()
        
        t3 = model.Task()
        t3.name = 'Task 3'
        t3.description = 'Task 3 description'
        t3.deadline = datetime.datetime.strptime("09/24/2011 10:30 PM", "%m/%d/%Y %I:%M %p")
        t3.priority = 1
        t3.patient = p2
        t3.assigned_to = d1
        t3.put()
        
        t4 = model.Task()
        t4.name = 'Task 4'
        t4.description = 'Task 4 description'
        t4.deadline = datetime.datetime.strptime("09/24/2011 11:30 PM", "%m/%d/%Y %I:%M %p")
        t4.priority = 1
        t4.patient = p2
        t4.assigned_to = d1
        t4.put()

class GetAllTasksByPatientsHandler(webapp.RequestHandler):
    def get(self):
        output = "All Tasks By Patient:<br\>"
        patients = get_all_patients()
        for patient in patients:
            output += "\tPatient Name: %s<br/>" % patient.name
            for task in patient.task_set:
                output += "\t\t%s\tPriority: %s\tDeadline: %s<br/>" %\
                        (task.name, task.priority, task.deadline)
        
        self.response.out.write(output)
        
def main():
    application = webapp.WSGIApplication([('/myTasks', MyTasks),
                                          ('/myPatients', MyPatients),
                                          ('/taskDetails', TaskDetails),
                                          ('/createNewTask', CreateNewTask),
    
                                          ('/dummyDataSetup', DummyDataSetup),
    
                                          ('/dummyHandler', JustAnotherHandler),
                                          ('/getAllTasks', GetAllTasksByPatientsHandler)
    
                                         ], debug=True)
    run_wsgi_app(application)




if __name__ == '__main__':
    main()




