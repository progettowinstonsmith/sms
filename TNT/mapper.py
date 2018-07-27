from collections import OrderedDict
from pprint import pprint
from TNT.utils import Singleton
import json
import logging
from pathlib import Path

LOGGER = logging.getLogger(__file__)

LOAD_PATH=Path('~/.tnt').expanduser()

class Mapper():

    def __init__(self):
        self.data = {}
        self.idata = {}

    def upload(self, section, last, values):
        if section in self.data:
            LOGGER.error('Sectin %s exists in mapper' % section)
            # raise Error
            return
        self.data[section]=OrderedDict()
        self.idata[section]=OrderedDict()
        n = last
        for value in values:
            if value != -1:
                self.data[section][str(n)] = value
                self.idata[section][str(value)] = n
                n += 1
        LOGGER.debug("Preloaded list {} with {} values beginning from {}".format(section,n,last))
        # LOGGER.debug(" MAP: "+' '.join([ "{}={}".format(k,v) for k,v in sorted(self.data[section].items())]))
        # LOGGER.debug("IMAP: "+' '.join([ "{}={}".format(k,v) for k,v in sorted(self.idata[section].items())]))

    def map(self, trn, num, sect):
        if num == -1:
            return -1
        try:
            return self.data[sect][str(num)]
        except:
            LOGGER.error('Error in map for {section} in num {num}'.format(section=sect,num=num))
            raise

    def imap(self, trn, num, sect):
        if num == -1:
            return -1
        try:
            return self.idata[sect][str(num)]
        except:
            LOGGER.error('Error in imap for {section} in num {num}'.format(section=sect,num=num))
            raise

    def load_maps(self,*maps):
        psect = LOAD_PATH
        if psect.exists():
            for fmap in sorted(psect.glob('*.map')):
                if len(maps)==0 or fmap.name in maps:
                    LOGGER.info("Loading: map file for "+fmap.name)
                    with fmap.open('r') as fh:
                        data =  json.load(fh)
                        self.data.update( data )
            self.sync_idata()

    def sync_idata(self):
        for key, aDict in self.data.items():
            rDict = [ { str(v):k } for k,v in aDict.items() ]
            self.idata.update( {key: rDict})

    def save(self,mapfile,sect=None):
        with open(mapfile,'w') as fh:
            json.dump(self.data,
                      fh,indent='\t')

MAPPER = Mapper()


class Map():

    def __init__(self, section):
        self.section = section

    def __call__(self,trn, num):
        return MAPPER.map(trn,num,self.section)

class IMap():

    def __init__(self, section):
        self.section = section

    def __call__(self,trn, num):
        return MAPPER.imap(trn,num,self.section)

def test_mapper():
    import random
    from pprint import pprint 
    arange = list(range(0,100))
    random.shuffle(arange)
    renum = Mapper('test')
    renums = map(renum, arange)
    pprint(list(zip(arange, renums)))
    return renum
