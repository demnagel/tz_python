# -*- coding: utf-8 -*-
import re

"""
Класс для роутинга
"""


class Router():
    urls = []  # Доступные адреса

    def __init__(self, urls, template_404=b''):
        self.urls = urls
        self.template_404 = template_404

    """
    Рендер 404 страницы, на отсутствующий url
    """

    def page404(self, environ, start_response):
        start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
        return [self.template_404]

    """
    Роутер
    """

    def start(self, environ, start_response):
        path = environ.get('PATH_INFO', '').lstrip('/')
        for regex, callback in self.urls:
            match = re.search(regex, path)
            if match is not None:
                environ['url_args'] = match.groups()
                return callback(environ, start_response)

        return self.page404(environ, start_response)
