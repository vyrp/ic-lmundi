import webapp2
from controllers import ClassesHandler, ClassHandler, HomeHandler, SettingsHandler, StudentHandler, StudentsHandler, TeacherHandler, TeachersHandler
from controllers import handler_404, handler_500

app = webapp2.WSGIApplication([
    ('/(?:home)?', HomeHandler),
    ('/alunos', StudentsHandler),
    ('/aluno/(\w+)', StudentHandler),
    ('/professores', TeachersHandler),
    ('/professor/(\w+)', TeacherHandler),
    ('/turmas', ClassesHandler),
    ('/turma/(\w+)', ClassHandler),
    ('/configuracoes', SettingsHandler),
], debug=True)

app.error_handlers[404] = handler_404
app.error_handlers[500] = handler_500
