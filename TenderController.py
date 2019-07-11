# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl
import json
from BaseController import BaseController

"""
Конструктор для tender app
"""


class TenderController(BaseController):
    """
    index страница
    """

    def indexPage(self, environ, start_response):
        title = 'Главная'
        template = 'index.html'
        start_response(status='200 OK', headers=[("Content-type", "text/html; charset=utf-8")])
        path_index = self.collectTemplatePath(template)
        html_index = self.checkOpenFile(path_index)
        if html_index is False:
            return [b'']
        return [self.collectTemplate(html_index, title)]

    """
    Статистика
    """

    def statPage(self, environ, start_response):
        title = 'Статистика комментариев'
        template = 'stat.html'
        template_stat_el = 'stat_el.html'

        start_response(status='200 OK', headers=[("Content-type", "text/html; charset=utf-8")])

        path_stat = self.collectTemplatePath(template)
        html_stat = self.checkOpenFile(path_stat)

        path_stat_el = self.collectTemplatePath(template_stat_el)
        html_stat_el = self.checkOpenFile(path_stat_el)

        if html_stat is False or html_stat_el is False:
            return [b'']

        region_stat = self.model.getRegionStat()
        region_more = ''
        all_reg_stat = ''
        if region_stat is not False:
            for el in region_stat:

                if el[2] > 5:
                    region_more += html_stat_el.format(
                        region_id=el[0],
                        region_name=el[1],
                        comment_count=el[2]
                    )

                all_reg_stat += html_stat_el.format(
                    region_id=el[0],
                    region_name=el[1],
                    comment_count=el[2]
                )
            if not region_more:
                region_more = '<h2 class="error">Пока нет таких регионов</h2>'
            if not all_reg_stat:
                all_reg_stat = '<h2 class="error">Пока нет комментариев</h2>'
        else:
            region_more = '<h2 class="error">Нет данных</h2>'
            all_reg_stat = '<h2 class="error">Нет данных</h2>'

        html_stat = html_stat.format(all_reg_stat=all_reg_stat, region_more=region_more)
        return [self.collectTemplate(html_stat, title)]

    """
    Комментарии
    """

    def commentPage(self, environ, start_response):
        title = 'Оставить комментарий'
        template = 'comment.html'

        start_response(status='200 OK', headers=[("Content-type", "text/html; charset=utf-8")])

        path_comment = self.collectTemplatePath(template)
        html_comment = self.checkOpenFile(path_comment)

        if html_comment is False:
            return [b'']

        regions = self.model.getRegions()
        city_select = '<option selected value="1">Не указано</option>'
        reg_select = '<option selected value="0">Не указано</option>'

        if regions is not False:
            for region in regions:
                reg_select += '<option value="{id}">{name}</option>'.format(id=region[0], name=region[1])
        else:
            city_select = '<option selected>Нет данных</option>'
            reg_select = '<option selected>Нет данных</option>'

        body_html = html_comment.format(region=reg_select, city=city_select)
        return [self.collectTemplate(body_html, title)]

    """
    Просмотр комментариев
    """

    def viewPage(self, environ, start_response):
        title = 'Просмотр комментариев'
        template_elem = 'comment_elem.html'
        template = 'view.html'
        start_response(status='200 OK', headers=[("Content-type", "text/html; charset=utf-8")])

        path_view = self.collectTemplatePath(template)
        view_view = self.checkOpenFile(path_view)

        path_elem = self.collectTemplatePath(template_elem)
        view_elem = self.checkOpenFile(path_elem)
        if view_elem is False:
            return [b'']

        comments = self.model.getComments()
        all_comments = ''
        if comments is not False:
            for comment in comments:
                all_comments += view_elem.format(
                    id=comment[0],
                    name='%s %s %s' % (comment[2], comment[1], comment[3]),
                    contacts='%s %s' % (comment[5], comment[4]),
                    location='%s, %s' % (comment[7], comment[8]),
                    text=comment[6],
                )

            if not all_comments:
                all_comments = '<h2 class="error">Пока нет комментариев</h2>'
        else:
            all_comments = '<h2 class="error">Нет данных</h2>'

        html_view = view_view.format(comments=all_comments)
        return [self.collectTemplate(html_view, title)]

    """
    Сборка шаблона для 404 страницы
    """

    def get404(self):
        title = '404 Not Found'
        template = '_404.html'
        _404 = self.collectTemplatePath(template)
        html_404 = self.checkOpenFile(_404)
        if html_404 is False:
            return b'404 Not Found'
        else:
            return self.collectTemplate(html_404, title)

    """
    Обработчик для ajax запросов
    """

    def ajax(self, environ, start_response):
        data = dict(parse_qsl(environ['QUERY_STRING']))
        start_response('200 OK', [('Content-Type', 'text/json')])

        if 'region_id' in data:
            data = self.model.getCities(data['region_id'])

        if 'comment_id' in data:
            if self.model.delComment(data['comment_id']):
                data = {'del': 1}
            else:
                data = {'del': 0}

        if 'stat_region' in data:
            data = self.model.getCityStat(data['stat_region'])

        json_string = json.dumps(data)
        return [json_string.encode()]

    """
    Отправка текстовых файлов на http запрос
    """

    def giveFile(self, environ, start_response):
        headers = [('Content-Type', 'text/html')]
        file = self.checkOpenFile(environ['PATH_INFO'][1:])
        if file is not False:
            status = '200 OK'
            if 'js' in environ['url_args']:
                headers = [('Content-Type', 'application/javascript')]
            elif 'css' in environ['url_args']:
                headers = [('Content-Type', 'text/css')]
        else:
            file = ''
            status = '404 NOT FOUND'
            print('Ошибка с файлом ' + environ['PATH_INFO'][1:])

        start_response(status, headers)
        return [file.encode()]

    """
    Обработчик для form
    """

    def submitForm(self, environ, start_response):
        data = dict(parse_qsl(environ['QUERY_STRING']))
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8"')])
        if 'send_comment' in data:
            if self.model.addComent(data):
                body = '<h1 class="status_subm">Ваш комментарий добавлен</h1>'
                return [self.collectTemplate(body, 'Успех')]
            else:
                body = '<h1 class="status_subm">Ваш комментарий не добавлен - возникла ошибка</h1>'
                return [self.collectTemplate(body, 'Неудача')]
        return []
