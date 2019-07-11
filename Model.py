# -*- coding: utf-8 -*-
import os.path
import sqlite3

"""
Класс модели для tenderController
"""


class Model:
    db_name = ''
    db_shema = ''
    status = {}

    """
    Конструктор
    """

    def __init__(self, db_name, db_shema):
        self.db_name = db_name
        self.db_shema = db_shema
        if not os.path.exists(db_name) and not os.path.exists(db_shema):
            self.status = {'error': 'База и схема не найдены'}
        elif not os.path.exists(db_name) and os.path.exists(db_shema):
            if self._crDb(db_name):
                self.status = {'success': 'Бд создана'}
            else:
                self.status = {'error': 'Не удалось создать бд'}
        else:
            self.status = {'success': 'Бд найдена'}

    """
    Приватный метод для проверки подключения/создания бд
    """

    def _crDb(self, db_name):
        connection = sqlite3.connect(db_name)
        cur = connection.cursor()
        shema = open(self.db_shema, encoding='utf-8').read()
        try:
            cur.executescript(shema)
        except:
            return False
        else:
            return True
        finally:
            cur.close()
            connection.close()

    """
    Приватный метод для получения данных по запросу
    """

    def _getQuery(self, query):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        try:
            cur.execute(query)
        except:
            print('Ошибка при запросе ' + query)
            return False
        else:
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
            connection.close()

    """
    Приватный метод для отправки запроса на добавление/изменения
    """

    def _sendQuery(self, query, args=False):
        connection = sqlite3.connect(self.db_name)
        cur = connection.cursor()
        try:
            if args:
                cur.execute(query, args)
            else:
                cur.execute(query)
        except:
            print('Ошибка при запросе ' + query)
            return False
        else:
            connection.commit()
            return True
        finally:
            cur.close()
            connection.close()

    """
    Метод для загрузки комментариев
    """

    def addData(self, data):
        query = """
            INSERT INTO comment('name', 'city_id', 'region_id', 'patronymic', 'surname', 'email', 'phone', 'comment')
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        args = (
            data['name'],
            data['city_id'],
            data['region_id'],
            data['patronymic'],
            data['surname'],
            data['email'],
            data['phone'],
            data['comment']
        )
        try:
            connection = sqlite3.connect(self.db_name)
            cur = connection.cursor()
            cur.execute(query, args)
            connection.commit()
        except:
            self.status = {'error': 'Ошибка при добавлении данных в бд'}
            return False
        else:
            return True
        finally:
            cur.close()
            connection.close()

    """
    Метод для получения городов по ид региона
    """

    def getCities(self, region_id):
        query = "SELECT id, name FROM city WHERE region_id=%s" % region_id
        data = self._getQuery(query)
        return {row[0]: row[1] for row in data}

    """
    Метод для удаления комментария
    """

    def delComment(self, comment_id):
        query = 'DELETE FROM comments WHERE id=%s' % comment_id
        if self._sendQuery(query):
            return True
        else:
            return False

    """
    Метод для добавления комментария
    """

    def addComent(self, data):
        query = """
            INSERT INTO comments('name', 'city_id', 'region_id', 'patronymic', 'surname', 'email', 'phone', 'text')
             VALUES(?,?,?,?,?,?,?,?)
        """
        args = (
            data['name'],
            data['city_id'],
            data['region_id'],
            data['patronymic'] if 'patronymic' in data else '',
            data['surname'],
            data['email'] if 'email' in data else '',
            data['phone'] if 'phone' in data else '',
            data['comment']
        )
        return self._sendQuery(query, args)

    """
    Метод для получения всех комментариев
    """

    def getComments(self):
        query = """
            SELECT comments.id, comments.name, surname, patronymic, email, phone, text, region.name, city.name 
            FROM comments 
            LEFT JOIN region ON comments.region_id = region.id 
            LEFT JOIN city ON comments.city_id = city.id
        """
        data = self._getQuery(query)
        return data

    """
    Метод для получения статистики для регионов
    """

    def getRegionStat(self):
        query = """
            SELECT region.id, region.name, count(*) AS count_comment FROM comments 
            INNER JOIN region ON comments.region_id = region.id GROUP BY region.name
        """
        data = self._getQuery(query)
        return data

    """
    Метод для получения статистики для городов
    """

    def getCityStat(self, region_id):
        query = """        
            SELECT city.id, city.name, count(*) AS count_comment FROM comments
            INNER JOIN region ON comments.region_id = region.id 
            INNER JOIN city ON comments.city_id = city.id
            WHERE region.id = %s
            GROUP BY city.name
        """ % region_id
        data = self._getQuery(query)
        return data

    """
    Метод для получения всех регионов
    """

    def getRegions(self):
        query = """        
            SELECT * FROM region WHERE id > 0
        """
        data = self._getQuery(query)
        return data
