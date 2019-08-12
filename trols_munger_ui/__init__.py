"""TROLS Munger web interface.

"""
import os
import sys
import flask
import logging

import trols_stats


ROOT = logging.getLogger()
ROOT.setLevel(logging.INFO)

if not ROOT.hasHandlers():
    HANDLER = logging.StreamHandler(sys.stdout)
    HANDLER.setLevel(logging.INFO)
    FORMATTER = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    HANDLER.setFormatter(FORMATTER)
    ROOT.addHandler(HANDLER)

app = flask.Flask(__name__)
if os.environ.get('TROLSUI_CONF'):
    app.config.from_envvar('TROLSUI_CONF')
else:
    app.config.from_object('trols_munger_ui.config')
import trols_munger_ui.views

MODEL = None
if app.config.get('SHELVE') is not None:
    logging.info('SHELVE: %s', app.config.get('SHELVE'))
    logging.info('Reading TROLS stats in memory ...')
    MODEL = trols_stats.DataModel(shelve=app.config.get('SHELVE'))
    logging.info('TROLS stats read OK.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = flask._app_ctx_stack.top
    if not hasattr(top, 'shelve'):
        top.shelve = MODEL

    return top.shelve
