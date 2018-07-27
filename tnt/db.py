from pprint import pprint
import json
from mysql.connector import connect

import logging
LOGGER = logging.getLogger(__file__)

class TNTdb:

    def __init__(self):
        pass

    def connect(self):
        self.cnx = connect(user='root', 
                           password='root',
                           host='127.0.0.1', 
                           port='8889',
                           database='db_tnt_forum1')
        self.cursor = self.cnx.cursor(dictionary=True)
        # self.cursor = self.cnx.cursor()

    def get(self, name, fields, tables, where, 
            order, LIMIT="", WHERE=""):
        if len(WHERE)==0:
            WHERE = ""
        GROUPS = []
        FLDS = ','.join(fields)
        if order:
            order = "ORDER BY {order}".format(order=order)
        else:
            order = ""
        sql = """SELECT {fields} FROM {tables} {where} {order} {limit}""".format(fields = FLDS, tables=tables, order=order, 
            where=WHERE, limit=LIMIT
        )
        ret = self.sql(sql)
        return {name: ret}

    def sql(self,sql):
        LOGGER.debug("SQL: {}".format(sql))
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def load(self, *sections):
        ret = {}
        for sect in sections:
            data = sect()
            ret.update(data)
        return ret

    def save_data(self,fname,data):
        with open('{}'.format(fname), 'w') as fp:
            json.dump(data,fp, indent='\t')

    def save_json(self, fname, *sections):
        data = self.load(*sections)
        self.save_data(fname,data)
        return data

def test_TNTdb():
    tnt = TNTdb()
    tnt.connect()
    groups = tnt.get_groups()
    tnt.save_json('out',tnt.get_groups)



