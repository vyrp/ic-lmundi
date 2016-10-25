import jinja2
import os
import webapp2

jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'])

def render(template, values):
    return jinja.get_template(template).render(values)

def handler_404(request, response, exception):
    response.write(render('templates/404.html', {}))

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(render('templates/home.html', {}))
