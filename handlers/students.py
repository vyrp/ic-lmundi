import datetime
import logging
import messages
import re
import urllib
import webapp2

from google.appengine.ext import ndb
from helpers import active, get_m, render, update_m


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
    @active("alunos")
    def get(self, id, values):
        values["show_form"] = True

        m = get_m(self.request)

        if m == messages.UNKNOWN_ACTION:
            values["show_form"] = False
            self.response.status = 400
        elif id:
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
        if "edit" in self.request.arguments():
            self.create_or_edit_student(id)
        elif "delete" in self.request.arguments():
            self.delete_student(id)
        else:
            logging.warning("Unknown action: " + str(self.request.arguments()))
            arguments = urllib.urlencode({"m": messages.UNKNOWN_ACTION})
            self.redirect("/aluno/" + id + "?" + arguments)

    def create_or_edit_student(self, id):
        if id:
            student = Student.get_by_id(long(id))
            if not student:
                self.redirect("/aluno/" + id)
                return
        else:
            student = Student()

        try:
            r = self.request

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

            m = messages.STUDENT_UPDATE_SUCCESS if id else messages.STUDENT_CREATE_SUCCESS
            self.redirect("/aluno/" + str(student.key.id()) + "?" + urllib.urlencode({"m": m}))
        except ValueError as ex:
            logging.warning("ValueError: " + ex.message)
            m = messages.STUDENT_UPDATE_ERROR if id else messages.STUDENT_CREATE_ERROR
            self.redirect("/aluno/?" + urllib.urlencode({"m": m}))

    def delete_student(self, id):
        student = Student.get_by_id(long(id))
        if student:
            student.key.delete()
            self.redirect("/alunos?" + urllib.urlencode({"m": messages.STUDENT_DELETE_SUCCESS}))
        else:
            self.redirect("/aluno/" + id)


class StudentsHandler(webapp2.RequestHandler):
    @active("alunos")
    def get(self, values):
        values["students"] = Student.query().fetch()
        update_m(values, get_m(self.request))
        self.response.write(render("templates/alunos.html", values))
