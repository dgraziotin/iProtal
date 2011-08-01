__author__ = 'Daniel Graziotin, 4801; Massimiliano Pergher 5821'

"""
Module that holds the class responsible for object persistency
"""
from storm.locals import *
import os.path

class DBManager(object):
    """
    Database manager class. It encapsulates operations over the pickle module and utility methods over the
    actual user. The objects are saved in a hash-map like data structure
    """
    _database = None
    _store = None
    def store(self):
        """
        returns the database representation
        """
        if not os.path.exists("/tmp/iProtal.db"):
            _database = create_database("sqlite:/tmp/iProtal.db")
            _store = Store(_database)
            _store.execute("CREATE TABLE band "
                  "(id INTEGER PRIMARY KEY, name VARCHAR, genre VARCHAR, origin VARCHAR)")
        else:
            _database = create_database("sqlite:/tmp/iProtal.db")
            _store = Store(_database)
        return _store