# -*- coding: utf-8 -*-
import os.path
from abc import ABC, abstractmethod
from Model import Model

"""
Абстрактный базовый класс для контроллеров
"""


class BaseController(ABC):
    template_path = ''
    model = object()

    def __init__(self, model, template=''):
        if template:
            self.template_path = template

        if isinstance(model, Model):
            self.model = model
        else:
            print('model не является ожидаемым объектом "Model"')

    """
    Хелпер для проверки и получения текстового файла
    """

    def checkOpenFile(self, file):
        if os.path.exists(file):
            with open(file, encoding='utf-8') as on_file:
                return on_file.read()
        else:
            print(file + ' Не найден')
            return False

    """
    Хелпер для сборки пути шаблона
    """

    def collectTemplatePath(self, file_html):
        path = file_html
        if self.template_path:
            path = self.template_path + '/' + path
        return path

    """
    Хелпер для сборки шаблона
    """

    def collectTemplate(self, body, title):

        header_path = 'header.html'
        footer_path = 'footer.html'

        if self.template_path:
            header_path = self.template_path + '/' + header_path
            footer_path = self.template_path + '/' + footer_path

        header = self.checkOpenFile(header_path)
        if header is False:
            return False

        footer = self.checkOpenFile(footer_path)
        if footer is False:
            return False

        html = header + body + footer
        html = html.format(title=title)
        return html.encode('utf-8')

    """
    Абстрактный метод для index страницы
    """

    @abstractmethod
    def indexPage(self, environ, start_response):
        pass

    """
    Абстрактный метод для обработки ajax
    """

    @abstractmethod
    def ajax(self, environ, start_response):
        pass

    """
    Абстрактный метод для обработки submit
    """

    @abstractmethod
    def submitForm(self, environ, start_response):
        pass

    """
    Абстрактный метод для отдачи файла на http запрос
    """

    @abstractmethod
    def giveFile(self, environ, start_response):
        pass
