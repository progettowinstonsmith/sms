import argparse
import logging

from TNT.mapper import MAPPER
from TNT.utils import Timer

LOGGER = logging.getLogger(__file__)

def _i(*args,**kwargs):
    return args, kwargs

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def app(name, klass, arguments=[]):
    logging.basicConfig(level=logging.DEBUG)  
    parser = argparse.ArgumentParser(
        description='Export {} SQL table.'.format(name))
    parser.add_argument('--maps', type=str, nargs='+',
                        default=[], dest='maps', 
                        help="json or sql")
    parser.add_argument('--no-map', type=str2bool, nargs='?',
                        const=True, default=True, dest='nomap', 
                        help="json or sql")
    parser.add_argument('--operation', type=str, default='sql', 
                        help="json or sql")
    parser.add_argument('--limits', type=str, default=None, 
                        help="limit or offset, limit")
    parser.add_argument('--where', type=str, default=None, 
                        help="where")
    parser.add_argument('-O','--output', dest="output",
                        metavar='fname', type=str, help='output \
                        name without extension', default=name)
    parser.add_argument('-f','--input', dest="input", 
                        metavar='fname', nargs="+",
                        type=str, help='input name with \
                        extension', default=[])
    if arguments:
        for args,kargs in arguments:
            parser.add_argument(*args, **kargs)

    args = parser.parse_args()
    ug = klass(args)
    name = args.output

    LOGGER.debug('OP: maps: ' + ','.join(args.maps))


    with Timer(name):
        ug.premap()
        if args.operation in ['premap']:
            MAPPER.save(name+'.map') 
            return
        ug.load()
        if args.operation == 'json':
            ug.save_json(name)
        ug.transform()
        if args.operation == 'sql':
            ug.save(name + '.sql')


