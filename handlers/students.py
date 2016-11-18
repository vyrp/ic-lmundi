import logging
import messages
import urllib
import webapp2

from datetime import datetime
from helpers import active, get_m, render, secure, update_m
from models.student import Student


class StudentHandler(webapp2.RequestHandler):
    @secure
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

    @secure
    def post(self, id):
        r = self.request
        logging.info(
            "### Arguments:\n" +
            "\n".join("%s => %s" % (arg, r.get_all(arg)) for arg in r.arguments()))

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

            name = r.get("name")
            if name:
                student.name = name
            else:
                raise ValueError("Student name must be non-empty.")

            surname = r.get("surname")
            if surname:
                student.surname = surname

            email = r.get("email")
            if email:
                student.email = email

            status = int(r.get("status"))
            if status:
                student.status = status

            first_contact = r.get("first_contact")
            if first_contact:
                student.first_contact = datetime.strptime(
                    first_contact,
                    "%d/%m/%Y"
                ).date()

            telephones = filter(bool, r.get_all("telephones[]"))
            if telephones:
                student.telephones = telephones
            else:
                raise ValueError("There must be at least one telephone.")

            languages = filter(bool, r.get_all("languages[]"))
            if languages:
                student.languages = map(int, languages)
            else:
                raise ValueError("There must be at least one language.")

            student.modalities = map(int, filter(bool, r.get_all("modalities[]")))

            made_test = r.get("made_test")
            if made_test:
                student.made_test = bool(int(made_test))

            student.obs = r.get("obs")

            student.lvl = r.get("lvl")

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
    @secure
    @active("alunos")
    def get(self, values):
        values["students"] = Student.query().fetch()
        update_m(values, get_m(self.request))
        self.response.write(render("templates/alunos.html", values))
