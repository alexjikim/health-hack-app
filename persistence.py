from model import Doctor, Room, Patient, Task
from google.appengine.ext import db


def patient_key(patient_name=None):
  """Constructs a datastore key for a Patient entity with patient_name."""
  return db.Key.from_path('Patient', patient_name or 'default_patient')

def task_key(task_name=None):
  """Constructs a datastore key for a Task entity with task_name."""
  return db.Key.from_path('Task', task_name or 'default_task')

def get_tasks_for_patient(patient):
    tasks = Task.gql("WHERE patient = :patient ",
            ancestor = task_key(), patient = patient)
    #tasks = Task.gql("WHERE ANCESTOR IS :ancestor AND patient = :patient ",
            #ancestor = task_key(), patient = patient)
    return tasks

def get_all_patients():
    patients = Patient.all()
    return patients
    
def get_patients_for_doctor(doctor):
    patients = Patient.gql("WHERE doctor = :doctor ",
            ancestor = patient_key(), doctor = doctor)
    #patients = Patient.gql("WHERE ANCESTOR IS :ancestor AND doctor = :doctor ",
            #ancestor = patient_key(), doctor = doctor)
            
    return patients
    

    
    
    
