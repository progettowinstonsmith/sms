import time
import ipaddress
import logging
LOGGER = logging.getLogger(__file__)

def now_to_epoch():
    return int(time.mktime(time.gmtime()))

def to_epoch(indate, format='%Y-%m-%d'):
    return int(time.mktime(time.strptime(indate, pattern)))

def from_epoch(epoch):
    pass

### functors
#
def stringify(trn, x):
    if x:
        return "\""+trn.db.cnx.converter.escape(x)+"\""
    return "\"\""

def now(trn, x):
    return now_to_epoch()

def ip2int(trn, addr):              
    return int(ipaddress.IPv4Address(addr))

def int2ip(trn, addr):
    return str(ipaddress.IPv4Address(addr))

def not_null(trn, value):
    if value is not None:
        return value
    return 0

def new_id(trn, value):
    if not hasattr(trn,'new_id'):
        trn.new_id = []
    if value in trn.new_id:
        return trn.new_id.index(value)
    else:
        trn.new_id.append(value)
        return trn.new_id.index(value)

### Adding func (get record)

def new_pwd(trn, record):
    return '"b415c79db9e0dced3e10a22978576aef"'

def birthday(trn, record):
    if record['bday_year']:
        return "\"{bday_year}-{bday_month}-{bday_day}\"".format(**record)
    return ""

def test_email(trn, record):
    return "\"me@torrentpier.com\""

        
