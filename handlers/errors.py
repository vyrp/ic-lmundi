import logging

from helpers import render

def handler_404(request, response, exception):
    response.write(render("templates/404.html"))
    response.set_status(404)

def handler_500(request, response, exception):
    logging.exception(exception)
    response.write(render("templates/500.html", {"stack_trace": traceback.format_exc().strip()}))
    response.set_status(500)
