import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SHELVE = os.path.join(os.sep, 'home', 'lupco', 'trols_shelve')

SHELVE_DB = os.path.join(SHELVE, 'trols_stats.db')
