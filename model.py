from google.appengine.ext import db

class Doctor(db.Model):
    name = db.StringProperty()
    pending_tasks = [] # Tasks needed to be completed, of patients of the doctor
    closed_tasks = [] # Tasks completed, of patients of the doctor
    
class Room(db.Model):
    name = db.StringProperty()
    zone = db.StringProperty()
    
class Patient(db.Model):
    name = db.StringProperty()
    room = db.ReferenceProperty(reference_class=Room)
    doctor = db.ReferenceProperty(reference_class=Doctor)
    pending_tasks = [] # Tasks needed to be completed, of patients of the doctor
    closed_tasks = []  # Tasks completed, of patients of the doctor
        
class Task(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    when_added = db.DateTimeProperty(auto_now_add=True)
    deadline = db.DateTimeProperty()
    priority = db.IntegerProperty()
    patient = db.ReferenceProperty(reference_class=Patient)
    when_completed = db.DateTimeProperty()
    completed_by = db.ReferenceProperty(reference_class=Doctor, collection_name="completed_tasks")
    assigned_to = db.ReferenceProperty(reference_class=Doctor, collection_name="assigned_tasks")
    def __cmp__(self, other):
        #open tasks are before completed tasks
        if not self.when_completed and other.when_completed:
            return -1
        if self.when_completed and not other.when_completed:
            return 1
        #If open, order first by priority, then by deadline
        if not self.when_completed:
            if self.priority == other.priority:
                if self.deadline < other.deadline:
                    return -1
                elif self.deadline > other.deadline:
                    return 1
                else:
                    return 0
            elif self.priority < other.priority:
                return -1
            else: #self.priority > other.priority
                return 1
        #If closed, order by when_closed
        else:
            if self.when_completed < other.when_completed:
                return -1
            elif self.when_completed > other.when_completed:
                return 1
        return 0
            
        
    
    
    

    
    

