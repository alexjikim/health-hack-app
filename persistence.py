from model import Doctor, Room, Patient, Task
from google.appengine.ext import db
import Queue

import logging


def complete_doctor_tasks(doctor):
    tasks = Queue.PriorityQueue()
        
    doctor.closed_tasks = []
    doctor.pending_tasks = []
    
    for patient in doctor.patient_set:
        for task in patient.task_set:
            tasks.put(task)

    while not tasks.empty():
        task = tasks.get()
        if task.when_completed:
            doctor.closed_tasks.append(task)
        else:
            doctor.pending_tasks.append(task)
    
    logging.info(doctor.pending_tasks)
    
    
def get_doctor(doctor_name):
    doctor = Doctor.gql("WHERE name = :name ", name = doctor_name)[0]
    complete_doctor_tasks(doctor)
    return doctor
            
def complete_patient_tasks(patient):
    tasks = Queue.PriorityQueue()
    
    for task in patient.task_set:
        tasks.put(task)
    
    while not tasks.empty():
        task = tasks.get()
        if task.when_completed:
            patient.closed_tasks.append(task)
        else:
            patient.pending_tasks.append(task)

    
def get_tasks_for_patient(patient):
    tasks = Task.gql("WHERE patient = :patient ",
            patient = patient)
    return tasks

def get_all_patients():
    patients = Patient.all()
    for patient in patients:
        complete_patient_tasks(patient)
    return patients
    
def get_patients_for_doctor(doctor):
    patients = Patient.gql("WHERE doctor = :doctor ",
            doctor = doctor)
    for patient in patients:
        complete_patient_tasks(patient)
    return patients
    
def handover_patients(from_doctor, to_doctor):
    patients = get_patients_for_doctor(from_doctor)
    for patient in patients:
        patient.doctor = to_doctor
        patient.put()
    

    
    
    
