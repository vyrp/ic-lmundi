import webapp2

from helpers import render

class TeacherHandler(webapp2.RequestHandler):
    def get(self, id):
        values = {
            "active": "professores",
        }
        self.response.write(render("templates/aluno.html", values))

class TeachersHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "professores",
        }
        self.response.write(render("templates/alunos.html", values))
