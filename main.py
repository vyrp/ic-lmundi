import os
import sys
import threading
import webapp2

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handlers import ajax, basic, classes, errors, students, teachers  # noqa: E402

app = webapp2.WSGIApplication([
    ('/(?:home)?', basic.HomeHandler),
    ('/alunos', students.StudentsHandler),
    ('/aluno/(\d+)?', students.StudentHandler),
    ('/professores', teachers.TeachersHandler),
    ('/professor/(\d+)?', teachers.TeacherHandler),
    ('/turmas', classes.ClassesHandler),
    ('/turma/(\d+)?', classes.ClassHandler),
    ('/configuracoes', basic.SettingsHandler),
    ('/ajax/(emails|languages|modalities|payments)/(add|edit|remove)', ajax.AjaxHandler),
], debug=True)

app.registry["settings_lock"] = threading.Lock()

app.error_handlers[400] = errors.handler_400
app.error_handlers[404] = errors.handler_404
app.error_handlers[500] = errors.handler_500
