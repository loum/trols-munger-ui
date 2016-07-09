import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SHELVE = os.path.join('trols_munger_ui', 'tests', 'files')

SHELVE_DB = os.path.join(SHELVE, 'trols_stats.db')
