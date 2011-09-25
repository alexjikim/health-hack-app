from model import Doctor, Room, Patient, Task
from google.appengine.ext import db


def patient_key(patient_name=None):
  """Constructs a datastore key for a Patient entity with patient_name."""
  return db.Key.from_path('Patient', patient_name or 'default_patient')

def task_key(task_name=None):
  """Constructs a datastore key for a Task entity with task_name."""
  return db.Key.from_path('Task', task_name or 'default_task')


def complete_doctor_tasks(doctor):
    tasks = []
    for patient in doctor.patient_set():
        tasks.append(patient.task_set)
    for task in tasks:
        if task.when_completed:
            doctor.completed_tasks.put(task)
        else:
            doctor.pending_tasks.put(task)
            
def get_doctor(doctor_name):
    doctor = Doctor.gql("WHERE name = :name ", name = doctor_name)[0]
    complete_doctor_tasks(doctor)
    return doctor
            
def complete_patient_tasks(patient):
    tasks = []
    for task in tasks:
        if task.when_completed:
            patient.completed_tasks.put(task)
        else:
            patient.pending_tasks.put(task)
    
    
def get_tasks_for_patient(patient):
    tasks = Task.gql("WHERE patient = :patient ",
            ancestor = task_key(), patient = patient)
    #tasks = Task.gql("WHERE ANCESTOR IS :ancestor AND patient = :patient ",
            #ancestor = task_key(), patient = patient)
    return tasks

def get_all_patients():
    patients = Patient.all()
    for patient in patients:
        complete_patient_tasks(patient)
    return patients
    
def get_patients_for_doctor(doctor):
    patients = Patient.gql("WHERE doctor = :doctor ",
            ancestor = patient_key(), doctor = doctor)
    #patients = Patient.gql("WHERE ANCESTOR IS :ancestor AND doctor = :doctor ",
            #ancestor = patient_key(), doctor = doctor)
            
    for patient in patients:
        complete_patient_tasks(patient)
    return patients
    
def handover_patients(from_doctor, to_doctor):
    patients = get_patients_for_doctor(from_doctor)
    for patient in patients:
        patient.doctor = to_doctor
        patient.put()
    

    
    
    
