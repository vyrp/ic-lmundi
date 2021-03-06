import jinja2
import messages
import os

from functools import wraps
from google.appengine.api import users
from models.settings import Settings

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)


def render(template, values={}):
    return jinja.get_template(template).render(values)


def get_m(request):
    m = request.get("m")
    try:
        m = int(m)
    except ValueError:
        m = 0

    if m in messages.messages:
        return m

    return 0


def update_m(values, m):
    if m:
        values["message"] = messages.messages[m]
        values["message_type"] = messages.types[m]


def active(active_section):
    def active_decorator(func):
        @wraps(func)
        def func_wrapper(*args):
            return func(*args, values={"active": active_section})
        return func_wrapper
    return active_decorator


def secure(func):
    @wraps(func)
    def func_wrapper(self, *args):
        user = users.get_current_user()
        if user and user.email() in Settings.get_instance()["emails"].values.values():
            return func(self, *args)
        self.response.set_status(403)
        self.response.write(
            'Move along, nothing to do here! Move along...<br><a href="%s">Logout</a>' %
            users.create_logout_url("/"))
    return func_wrapper
