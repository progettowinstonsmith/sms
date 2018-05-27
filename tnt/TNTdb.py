import json
import mysql.connector

class TNTdb:

    def __init__(self):
        pass

    def connect(self):
        self.cnx = mysql.connector.connect(user='root', password='root',
                                           host='127.0.0.1', port='8889',
                                           database='db_tnt_forum1')
        # cursor = cnx.cursor(dictionary=True)
        self.cursor = self.cnx.cursor()

    def get_groups(self):
        GROUPS = []
        sql = """SELECT g_id, g_title FROM Trck_groups """
        self.cursor.execute(sql)
        for (g_id, g_title) in self.cursor.fetchall():
            group = {
                'g_id': g_id,
                'g_title': g_title,
            }
            GROUPS.append(group)
        return {'groups' : GROUPS}
        
    def save_json(self, fname, *sections):
        with open('{}.json'.format(fname), 'w') as fp:
            for sect in sections:
                data = sect()
                json.dump(data,fp, indent='\t')

def test_TNTdb():
    tnt = TNTdb()
    tnt.connect()
    groups = tnt.get_groups()
    tnt.save_json('out',tnt.get_groups)


