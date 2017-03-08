"""TROLS Munger web interface.

"""
import os
import flask
from logga import log

import trols_stats


app = flask.Flask(__name__)
if os.environ.get('TROLSUI_CONF'):
    app.config.from_envvar('TROLSUI_CONF')
else:
    app.config.from_object('trols_munger_ui.config')
import trols_munger_ui.views

MODEL = None
if app.config.get('SHELVE') is not None:
    log.info('SHELVE: %s', app.config.get('SHELVE'))
    # session = trols_stats.DBSession(shelve=app.config.get('SHELVE'))
    # session.connect()
    log.info('Reading TROLS stats in memory ...')
    # db = session.connection['trols']
    MODEL = trols_stats.DataModel(shelve=app.config.get('SHELVE'))
    log.info('TROLS stats read OK.')
    # session.close()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = flask._app_ctx_stack.top
    if not hasattr(top, 'shelve'):
        top.shelve = MODEL

    return top.shelve
