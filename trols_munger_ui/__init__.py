"""GeoLib web interface.

"""
import flask

import trols_stats
from logga.log import log


app = flask.Flask(__name__)
app.config.from_object('config')
import trols_munger_ui.views

db = None
if app.config.get('SHELVE') is not None:
    session = trols_stats.DBSession(shelve=app.config.get('SHELVE'))
    session.connect()
    log.info('Reading TROLS stats in memory ...')
    db = session.connection['trols']
    log.info('TROLS stats read OK.')
    session.close()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = flask._app_ctx_stack.top
    if not hasattr(top, 'shelve'):
        top.shelve = db
    return top.shelve
