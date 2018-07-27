import json
import re
import time
from datetime import date
from pprint import pformat


from TNT.mapper import MAPPER
from TNT.db import TNTdb
from TNT.utils import printProgressBar

import logging
LOGGER = logging.getLogger(__file__)

def i(v):
    if v is None or (isinstance(v,str) and len(v)==0):
        v = "NULL"
    return v


class Transformer:
    DROP = []
    RULES = {}
    ADDITIONS = {}
    
    def __init__(self, args):
        self.args = args
        self.data = []
        self.db = None
        self.db_results = []
        self.data = {}
        self._record = None

    def get(self):
        if hasattr(self,"DB_SQL"):
            sql = self.DB_SQL
            if self.args.where:
                sql = re.sub(' WHERE ',' WHERE ' + self.args.where + " AND ",sql)
            res = { self.SUB : self.db.sql(sql) }
        else:
            LIMIT = ""
            WHERE = []
            if hasattr(self,'DB_LIMIT'):
                LIMIT = self.DB_LIMIT
            if self.args.limits:
                LIMIT = " LIMIT " + self.args.limits
            if self.args.where:
                WHERE.append(self.args.where)
            if hasattr(self,'DB_WHERE'):
                WHERE.append( self.DB_WHERE )
            if len(WHERE)>0:
                WHERE = " WHERE " + ' AND '.join(WHERE)
            ORDER = None
            if hasattr(self,'DB_ORDER'):
                ORDER =  self.DB_ORDER 
            res = self.db.get(self.SUB, self.DB_FIELDS, 
                              self.DB_TABLES, None, 
                              ORDER, 
                              LIMIT=LIMIT, WHERE=WHERE)
        self.db_results = res
        LOGGER.info('got {} results'.format(len(res[self.SUB])))
        return res

    def map(self):
        if hasattr(self,'PREMAPS'):
            for field, name, last  in self.PREMAPS:
                map_values = self.db.sql(
                    'SELECT {} FROM {} order by {}'.format(
                        field, self.DB_TABLES, field) )
                MAPPER.upload(name, last,
                              [ row[field] for row in map_values ])
        if not self.args.nomap:
            MAPPER.load_maps(*self.args.maps)
        else:
            LOGGER.info('Not loading maps')
        
    def with_db_results(self):
        return None

    def record(self, info):
        record = info
        for rkey, rfunc in self.RULES.items():
            record[rkey] = rfunc(self, info[rkey])
        for akey, afunc in self.ADDITIONS.items():
            record[akey] = afunc(self, record)
        for dkey in self.DROP:
            if dkay in record:
                del record[dkey]
        return record

    # MODES
    def insert(self):
        return "INSERT INTO {table}({fields}) VALUES\t".format(table=self.TABLE,
                                                            fields=self.fields_string())

    def update(self):
        self.UPDATE_MODELS = []
        for vars, key  in self.OUT_UPDATE:
            vmodel = ', '.join([ 
                "%s = {%s}" % (var,var) 
                for var in vars])
            model = "UPDATE {table} SET {vars} WHERE {condition};".format(
                table=self.TABLE,
                vars=vmodel,
                condition="%s = {%s}" % (key,key))
            self.UPDATE_MODELS.append(model)
    #
    # END MODES
            
    def values_string(self):
        return ','.join(
            [ list(x.values())[0] for x in self.FIELDS ]
        )

    def fields_string(self):
        return ','.join(
            [ list(x.keys())[0] for x in self.FIELDS ]
        )

    def update_values(self, info):
        res = []
        for model in self.UPDATE_MODELS:
            line = model.format(**info)
            res.append(line)
        return '\n'.join(res)

    def insert_values(self, info):
        info = self.record(info)  
        einfo = { k:i(v) for k,v in info.items() }
        values = "(" + self.values_string() + ")"
        values = values.format(**einfo)
        return values

    def values(self, info):
        if not hasattr(self, "OUT_UPDATE"):
            return self.insert_values(info)
        return self.update_values(info)
        
    def transform(self):
        begin = ""
        if not hasattr(self, "OUT_UPDATE"):
            begin = self.insert()
            sep = ",\n\t"
            lst = ";"
        else:            
            self.update()
            sep = "\n"
            lst = ""
        values = []
        N = len(self.data[self.SUB])        
        printProgressBar(0, N, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i,info in enumerate(self.data[self.SUB]):
            if hasattr(self,'ID_LABEL') and \
               hasattr(self,'GOOD_ID'):
                if info[self.ID_LABEL] not in self.GOOD_ID:
                    continue
            try:
                self._record = info
                values.append(self.values(info))
            except:
                LOGGER.error('EXCEPTION in {sub} at element {info}'.format(sub=self.SUB,info=info))
                raise
            printProgressBar(i + 1, N, prefix = 'Progress:', suffix = 'Complete', length = 50)
        self.trans = begin + sep.join(values) + lst + "\n\n###\n\n\n"

    def save(self,sqlfile):
        with open(sqlfile,'w') as fh:
            if hasattr(self,'ALTER'):
                fh.write('\n'.join(self.ALTER))
                fh.write('\n')
            fh.write(self.trans)
            ending = self.with_db_results()
            if ending:
                fh.write("\n\n"+ending)
        from TNT.bbcode import RESIDUALS
        if len(RESIDUALS) > 0:
            with open(sqlfile[:-3]+"-residuals.txt",'w') as fh:
                for pid, residual, pre, post in RESIDUALS:
                    fh.write('8<---------------------------------------- ' + str(pid) + '\n')
                    fh.write(residual)
                    fh.write('\n\n')
                    fh.write(' PRE ------------------------------------- ' + str(pid) + '\n')
                    fh.write(pre)
                    fh.write('\n\n')
                    fh.write(' POST ------------------------------------ ' + str(pid) + '\n')
                    fh.write(post)
                    fh.write('\n\n')
                    
            

    def load(self):
        retval = self.db.load(self.get)
        self.data = retval
        return retval

    def save_json(self, name):
        self.premap()
        if not self.data:
            retval = self.db.save_json(name+'.json', self.get)
            self.data = retval
        else:
            self.db.save_data(name+".json")
        return retval

    def premap(self):
        self.db = TNTdb()
        self.db.connect()
        self.map()
        

        
