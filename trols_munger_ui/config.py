import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SHELVE = os.path.join(os.sep, 'var', 'www')

SHELVE_DB = os.path.join(SHELVE, 'trols_stats.db')
