import logging
import traceback

from helpers import render


def handler_400(request, response, exception):
    logging.exception(exception)
    response.write(exception.message)
    response.set_status(400)


def handler_404(request, response, exception):
    response.write(render("templates/404.html"))
    response.set_status(404)


def handler_500(request, response, exception):
    logging.exception(exception)
    values = {"stack_trace": traceback.format_exc().strip()}
    response.write(render("templates/500.html", values))
    response.set_status(500)
