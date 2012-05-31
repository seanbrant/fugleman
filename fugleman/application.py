import os

from django.conf import settings
from django.template.loader import render_to_string
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response


class Application(object):

    def __init__(self, **kwargs):
        settings.configure(**kwargs)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)

    def dispatch(self, request):
        if not request.path.endswith('/'):
            return redirect('%s/' % request.path)
        return Response(self.render(request.path))

    def render(self, path):
        path = path[1:-1]
        return render_to_string(['%s.html' % path, os.path.join(path, 'index.html')])
