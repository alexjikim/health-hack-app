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
import persistence
    



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




class Login(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'html/Login.html')
        self.response.out.write(template.render(path, {}))
    
    def post(self):
        name = self.request.get('name')
        doctors = model.Doctor.gql("WHERE name = :name ", name = name)
        if doctors.count() < 1:
            self.redirect('/')
        else:
            get_current_session()['current_doc_key'] = str(doctors[0].key())
            self.redirect('/myTasks')


class MyTasks(webapp.RequestHandler):
    def get(self):
        if not get_current_session().has_key('current_doc_key'):
            self.redirect('/')
        doc_key = get_current_session()['current_doc_key']
        cur_doctor = db.get(db.Key(doc_key))

        
        #task = doctor.assigned_tasks
        

        #open_tasks = []
        #closed_tasks = []
        #for task in tasks:
        #    if task.when_completed:
        #        closed_tasks.append(task)
        #    else:
        #        open_tasks.append(task)

        template_values = {}
        #template_values['open_tasks'] = open_tasks
        #template_values['closed_tasks'] = closed_tasks
        path = os.path.join(os.path.dirname(__file__), 'html/TasksView.html')
        self.response.out.write(template.render(path, template_values))

class MyPatients(webapp.RequestHandler):
    def get(self):
        if not get_current_session().has_key('current_doc_key'):
            self.redirect('/')
        doc_key = get_current_session()['current_doc_key']
        cur_doctor = db.get(db.Key(doc_key))
        
        patients = persistence.get_patients_for_doctor(cur_doctor)
        template_values = {}
        template_values['patients'] = patients
        path = os.path.join(os.path.dirname(__file__), 'html/PatientsView.html')
        self.response.out.write(template.render(path, template_values))
        
class TaskDetails(webapp.RequestHandler):
    def get(self):
        keyString = self.request.get('key')
        k = db.Key(keyString)
        task = db.get(k)
        
        template_values = {'task' : task}
        path = os.path.join(os.path.dirname(__file__), 'html/TaskDetails.html')
        self.response.out.write(template.render(path, template_values))
        
class CreateNewTask(webapp.RequestHandler):
    def get(self):
        template_values = {}
        template_values['patients'] = persistence.get_all_patients()
        path = os.path.join(os.path.dirname(__file__), 'html/CreateNewTask.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        if not get_current_session().has_key('current_doc_key'):
            self.redirect('/')
        doc_key = get_current_session()['current_doc_key']
        cur_doctor = db.get(db.Key(doc_key))

        task_name = self.request.get('task-name')
        task_desc = self.request.get('task-desc')
        priority = int(self.request.get('priority'))
        patient_key = self.request.get('patient')
        patient = db.get(db.Key(patient_key))
        deadline_str = self.request.get('deadline')

        t = model.Task()
        t.name = task_name
        t.description = task_desc
        t.deadline = datetime.datetime.strptime(deadline_str, "%m/%d/%Y %I:%M %p")
        t.priority = priority
        t.patient = patient
        t.assigned_to = cur_doctor
        t.put()

        self.redirect('/myTasks')

class PatientDetails(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/PatientDetails.html')
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
        p2.doctor = d2
        p2.put()
        
        p3 = model.Patient()
        p3.name = "Patient 3"
        p3.room = r2
        p3.doctor = d1
        p3.put()
        
        t1 = model.Task()
        t1.name = 'Emergent task'
        t1.description = 'Really important'
        t1.deadline = datetime.datetime.strptime("09/25/2011 1:30 PM", "%m/%d/%Y %I:%M %p")
        t1.priority = 1
        t1.patient = p1
        t1.assigned_to = d1
        t1.put()
        
        t2 = model.Task()
        t2.name = 'Change Wound Dressing'
        t2.description = 'Change Bandage'
        t2.deadline = datetime.datetime.strptime("09/25/2011 11:30 AM", "%m/%d/%Y %I:%M %p")
        t2.priority = 4
        t2.patient = p1
        t2.assigned_to = d1
        t2.put()
        
        t3 = model.Task()
        t3.name = 'Pain Meds'
        t3.description = 'This patient is in pain!'
        t3.deadline = datetime.datetime.strptime("09/25/2011 10:30 AM", "%m/%d/%Y %I:%M %p")
        t3.priority = 2
        t3.patient = p2
        t3.assigned_to = d1
        t3.put()
        
        t4 = model.Task()
        t4.name = 'Change Foley Catheter'
        t4.description = 'Good Times'
        t4.deadline = datetime.datetime.strptime("09/25/2011 5:30 PM", "%m/%d/%Y %I:%M %p")
        t4.priority = 3
        t4.patient = p2
        t4.assigned_to = d1
        t4.completed_by = d1
        t4.when_completed = datetime.datetime.now()
        t4.put()

        t5 = model.Task()
        t5.name = 'Chest X-Ray'
        t5.description = 'TB or not TB?'
        t5.deadline = datetime.datetime.strptime("09/25/2011 10:30 PM", "%m/%d/%Y %I:%M %p")
        t5.priority = 2
        t5.patient = p1
        t5.assigned_to = d1
        t5.put()
        
        t2 = model.Task()
        t2.name = ''
        t2.description = 'Task 6 description'
        t2.deadline = datetime.datetime.strptime("09/25/2011 11:30 PM", "%m/%d/%Y %I:%M %p")
        t2.priority = 1
        t2.patient = p1
        t2.assigned_to = d1
        t2.put()
        
        t3 = model.Task()
        t3.name = 'Check Coagulation Status'
        t3.description = 'Blood is thicker than water'
        t3.deadline = datetime.datetime.strptime("09/25/2011 10:30 PM", "%m/%d/%Y %I:%M %p")
        t3.priority = 3
        t3.patient = p2
        t3.assigned_to = d1
        t3.put()
        
        t4 = model.Task()
        t4.name = 'Change head position to 30deg'
        t4.description = 'Carefully!'
        t4.deadline = datetime.datetime.strptime("09/26/2011 11:30 PM", "%m/%d/%Y %I:%M %p")
        t4.priority = 5
        t4.patient = p2
        t4.assigned_to = d1
        t4.completed_by = d1
        t4.when_completed = datetime.datetime.now()
        t4.put()

def tasks_output(tasks):
    output = ""
    for task in tasks:
        output += "\t\t%s\tPriority: %s\tDeadline: %s<br/>" %\
                (task.name, task.priority, task.deadline)
    return output
    
def tasks_output_by_patients(patients):
    output = ""
    for patient in patients:
        output += "\tPatient Name: %s<br/>" % patient.name
        output += tasks_output(patient.task_set)
    return output
    
class GetAllTasksByPatientsHandler(webapp.RequestHandler):
    def get(self):
        output = "All Tasks By Patient:<br\>"
        patients = persistence.get_all_patients()
        output += tasks_output_by_patients(patients)
        self.response.out.write(output)

class GetAllTasksForDoctorHandler(webapp.RequestHandler):
    def get(self):
        doctor_name = self.request.get('doctor')
        doctor = persistence.get_doctor(doctor_name)
        patients = persistence.get_patients_for_doctor(doctor)
        output = "All Tasks By Patient for Doctor %s:<br/>" % doctor.name
        output += tasks_output_by_patients(patients)
        self.response.out.write(output)

class GetAllTasksForPatientHandler(webapp.RequestHandler):
    def get(self):
        patient_name = self.request.get('patient')
        patient = model.Patient.gql("WHERE name = :name ", name = patient_name)[0]
        tasks = persistence.get_tasks_for_patient(patient)
        output = "All Tasks for Patient %s:<br/>" % patient.name
        output += tasks_output(tasks)
        self.response.out.write(output)
        
class CloseTaskHandler(webapp.RequestHandler):
    def post(self):
        if not get_current_session().has_key('current_doc_key'):
            self.redirect('/')
        doc_key = get_current_session()['current_doc_key']
        cur_doctor = db.get(db.Key(doc_key))
        task_key = self.request.get('task')
        task = model.Task.get_by_id(task_key)
        persistence.close_task(task, cur_doctor)
        
        
        
def main():
    application = webapp.WSGIApplication([('/', Login),
                                          ('/myTasks', MyTasks),
                                          ('/myPatients', MyPatients),
                                          ('/taskDetails', TaskDetails),
                                          ('/createNewTask', CreateNewTask),
                                          ('/patientDetails', PatientDetails),
                                          
    
                                          ('/dummyDataSetup', DummyDataSetup),
    
                                          ('/tasks/all', GetAllTasksByPatientsHandler),
                                          ('/tasks/doctor', GetAllTasksForDoctorHandler),
                                          ('/tasks/patient', GetAllTasksForPatientHandler),
                                          ('/task/close', CloseTaskHandler),
                                          
    
                                         ], debug=True)
    run_wsgi_app(application)




if __name__ == '__main__':
    main()





