import datetime
import logging
import messages
import re
import urllib
import webapp2

from google.appengine.ext import ndb
from helpers import get_m, render, update_m


class Student(ndb.Model):
    _telephone_regex = re.compile(r"^\+\d{1,2} \(\d+\) \d+\-\d+$")

    def validate_telephone(self, value):
        value = value.strip()
        if Student._telephone_regex.match(value):
            return value
        raise ValueError(
            "Value '%s' doesn't match telephone regex '%s'."
            % (value, Student._telephone_regex.pattern)
        )

    def non_empty(self, value):
        value = value.strip()
        if value:
            return value
        raise ValueError("Value for '%s' is empty." % self._name)

    name = ndb.StringProperty(required=True, validator=non_empty)
    surname = ndb.StringProperty(required=True, validator=non_empty)
    first_contact = ndb.DateProperty(required=True)
    telephone = ndb.StringProperty(required=True, validator=validate_telephone)
    email = ndb.StringProperty(required=True, validator=non_empty)


class StudentHandler(webapp2.RequestHandler):
    def get(self, id):
        values = {
            "active": "alunos",
            "show_form": True,
        }

        m = get_m(self.request)

        if id:
            student = Student.get_by_id(long(id))
            if student:
                values["student"] = student
                values["id"] = id
            else:
                m = messages.STUDENT_ID_NOT_FOUND
                values["show_form"] = False

        update_m(values, m)

        self.response.write(render("templates/aluno.html", values))

    def post(self, id):
        r = self.request

        if "edit" in r.arguments():
            if id:
                student = Student.get_by_id(long(id))
                if not student:
                    self.response.status = 400
                    return
            else:
                student = Student()

            try:
                first_contact = datetime.datetime.strptime(
                    r.get("first_contact"),
                    "%d/%m/%Y"
                ).date()
            except ValueError:
                self.response.status = 400
                return

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

        m = get_m(self.request)
        update_m(values, m)

        self.response.write(render("templates/alunos.html", values))
