import datetime
import logging
import messages
import urllib
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

        m = self.request.get("m")
        if m:
            values["message"] = messages.messages[m]
            values["message_type"] = messages.types[m]

        self.response.write(render("templates/aluno.html", values))

    def post(self, id):
        r = self.request

        if "edit" in r.arguments():
            student = Student.get_by_id(long(id)) if id else Student()

            first_contact = datetime.datetime.strptime(
                r.get("first_contact"),
                "%d/%m/%Y"
            ).date()

            student.populate(
                name=r.get("name"),
                surname=r.get("surname"),
                first_contact=first_contact,
                telephone=r.get("telephone"),
                email=r.get("email"),
            )
            student.put()

            arguments = urllib.urlencode({"m": messages.STUDENT_CREATE_SUCCESS})
            self.redirect("/aluno/" + str(student.key.id()) + "?" + arguments)
        elif "delete" in r.arguments():
            ndb.Key(Student, long(id)).delete()
            arguments = urllib.urlencode({"m": messages.STUDENT_DELETE_SUCCESS})
            self.redirect("/alunos?" + arguments)
        else:
            logging.warning("Unknown action: " + str(r.arguments()))
            arguments = urllib.urlencode({"m": messages.UNKNOWN_ACTION})
            self.redirect("/aluno/" + id + "?" + arguments)


class StudentsHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "alunos",
            "students": Student.query().fetch()
        }

        m = self.request.get("m")
        if m:
            values["message"] = messages.messages[m]
            values["message_type"] = messages.types[m]

        self.response.write(render("templates/alunos.html", values))
