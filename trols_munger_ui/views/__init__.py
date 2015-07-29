"""TROLS Munger UI views abstraction.
"""
import flask
import urlparse

import trols_munger_ui
import trols_stats.interface
from trols_munger_ui.utils import (query_terms_to_dict,
                                   player_ids_dict)


@trols_munger_ui.app.route('/munger/health')
def health():
    """Quick health check response.
    """
    return flask.render_template('health.html')


@trols_munger_ui.app.route('/munger')
def dashboard():
    """Munger
    """
    return flask.render_template('layout.html')


@trols_munger_ui.app.route('/munger/players')
@trols_munger_ui.app.route('/munger/players/<league>/<year>/<season>')
def players(league='nejta', year='2015', season='spring'):
    terms = query_terms_to_dict(flask.request.url)

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    players = []
    if terms.get('q') is not None:
        players = reporter.get_players(terms.get('q'))
        trols_munger_ui.app.logger.debug('Players: "%s"', players)

    search_terms = str()
    if terms.get('q') is not None:
        search_terms = ' '.join(terms.get('q'))

    return flask.render_template('players/layout.html',
                                 result=player_ids_dict(players),
                                 search_terms=search_terms)
    

@trols_munger_ui.app.route('/munger/stats')
def stats():
    terms = query_terms_to_dict(flask.request.url)

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    stats = reporter.get_player_stats(terms.get('token'))

    return flask.render_template('stats/layout.html', result=stats)

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

    return flask.json.jsonify({'players': player_ids_dict(players)})
