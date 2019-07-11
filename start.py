# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from TenderController import TenderController
from Model import Model
from Router import Router
import config

# Создание объекта модели
model = Model(config.DB_NAME, config.DB_SHEMA)
# Создание контроллера и подключение модели
controller = TenderController(model, config.TEMPLATES_PATH)
# Доступные адреса
urls = [
    (r'^$', controller.indexPage),
    (r'comment/?$', controller.commentPage),
    (r'view/?$', controller.viewPage),
    (r'stat/?$', controller.statPage),
    (r'ajax/?$', controller.ajax),
    (r'sendform/?$', controller.submitForm),
    (r'.+\.(js|css)$', controller.giveFile),
]
# Создание объекта для роутинга
router = Router(urls, controller.get404())

if __name__ == '__main__':
    srv = make_server(config.IP, config.PORT, router.start)
    print('Приложение запущено на на {ip}:{port}'.format(ip=config.IP, port=config.PORT))
    srv.serve_forever()
