"""Configuration for trols_munger_ui
"""
import os
import pathlib

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# SHELVE = os.path.join(pathlib.Path.home(), 'trols_shelve')
SHELVE = os.path.join(os.sep, 'var', 'tmp', 'trols_shelve')
SHELVE_DB = os.path.join(SHELVE, 'trols_stats.db')
