import datetime
import logging
import webapp2

from google.appengine.ext import ndb
from helpers import render

class Student(ndb.Model):
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    first_contact = ndb.DateProperty()
    telephone = ndb.StringProperty()
    email = ndb.StringProperty()

class StudentHandler(webapp2.RequestHandler):
    def get(self, id):
        values = {
            "active": "alunos",
        }

        if id:
            student = Student.get_by_id(long(id))
            values["student"] = student
            values["id"] = id

        self.response.write(render("templates/aluno.html", values))

    def post(self, id):
        student = Student.get_by_id(long(id)) if id else Student()
        student.populate(
            name=self.request.get("name"),
            surname=self.request.get("surname"),
            first_contact=datetime.datetime.strptime(self.request.get("first_contact"), "%d/%m/%Y").date(),
            telephone=self.request.get("telephone"),
            email=self.request.get("email"),
        )
        student.put()

        self.redirect("/aluno/" + str(student.key.id()))

    def delete(self, id):
        ndb.Key(Student, long(id)).delete()

class StudentsHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "alunos",
            "students": Student.query().fetch()
        }
        self.response.write(render("templates/alunos.html", values))
