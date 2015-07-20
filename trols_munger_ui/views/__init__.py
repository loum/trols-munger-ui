"""TROLS Munger UI views abstraction.
"""
import flask
import urlparse

import trols_munger_ui
import trols_stats.interface
from trols_munger_ui.utils import query_terms_to_dict


@trols_munger_ui.app.route('/munger/health')
def health():
    """Quick health check response.
    """
    return flask.render_template('health.html')


@trols_munger_ui.app.route('/munger/dashboard')
def dashboard():
    """Dashboard.
    """
    return flask.render_template('dashboard/layout.html')

@trols_munger_ui.app.route('/munger/search')
def search():
    terms = query_terms_to_dict(flask.request.url)
    trols_munger_ui.app.logger.debug('Free text search: "%s"', terms)

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    players = []
    if terms.get('q') is not None:
        players = reporter.get_players(terms.get('q'))
        trols_munger_ui.app.logger.debug('Players: "%s"', players)

    return flask.json.jsonify({'players': [p for p in players]})
