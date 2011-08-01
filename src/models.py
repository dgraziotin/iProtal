from storm.locals import *
import dbmanager
class Band(object):
    __storm_table__ = "band"
    __storm_primary__ = "id"
    _create_table = ""
    id = Int()
    name = Unicode()
    genre = Unicode()
    origin = Unicode()