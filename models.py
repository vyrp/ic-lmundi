from google.appengine.ext import ndb

class Student(ndb.Model):
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    first_contact = ndb.DateProperty()
    telephone = ndb.StringProperty()
    email = ndb.StringProperty()
