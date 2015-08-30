"""TROLS Munger UI views abstraction.
"""
import flask
import urlparse
import os

import trols_munger_ui
import trols_stats.interface
from trols_munger_ui.utils import (query_terms_to_dict,
                                   player_ids_dict)
from filer.files import get_file_time_in_utc


@trols_munger_ui.app.route('/munger/health')
def health():
    """Quick health check response.
    """
    return flask.render_template('health.html')


@trols_munger_ui.app.route('/munger')
def munger():
    """Munger
    """
    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    terms = query_terms_to_dict(flask.request.url)

    stats = {}
    if terms.keys():
        section = terms.get('section')
        if section is not None:
            section = section[0]

        comp_type = terms.get('type')
        if comp_type is not None:
            comp_type = comp_type[0]

        event = terms.get('event')
        if event is not None:
            event = event[0]
        else:
            event = 'doubles'

        kwargs = {
            'competition': 'saturday_am_spring_2015',
            'competition_type': comp_type,
            'section': section
        }
        player_tokens = reporter.get_players(**kwargs)
        all_stats = reporter.get_player_stats(player_tokens)
        filtered_stats = reporter.sort_stats(all_stats,
                                             event=event,
                                             key='percentage',
                                             reverse=True,
                                             limit=None)

        stats['comp_type'] = comp_type
        stats['event'] = event
        stats['section'] = section
        stats['players'] = filtered_stats

    return flask.render_template('munger/layout.html', result=stats)


@trols_munger_ui.app.route('/munger/players')
@trols_munger_ui.app.route('/munger/players/<league>/<year>/<season>')
def players(league='nejta', year='2015', season='spring'):
    terms = query_terms_to_dict(flask.request.url)

    competition = None
    if league == 'nejta':
        competition = 'saturday_am_{}_{}'.format(season, year)

    trols_munger_ui.app.logger.debug('competition: %s', competition)

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    players = []
    if terms.get('q') is not None:
        players = reporter.get_players(names=terms.get('q'),
                                       competition=competition)
        trols_munger_ui.app.logger.debug('Players: "%s"', players)

    search_terms = str()
    if terms.get('q') is not None:
        search_terms = ' '.join(terms.get('q'))

    return flask.render_template('players/layout.html',
                                 result=player_ids_dict(players),
                                 search_terms=search_terms,
                                 competition=competition)
    

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

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    players = []
    if terms.get('q') is not None:
        players = reporter.get_players(terms.get('q'))
        trols_munger_ui.app.logger.debug('Players: "%s"', players)

    return flask.json.jsonify({'players': player_ids_dict(players)})


@trols_munger_ui.app.route('/_last_update')
def _last_update():
    shelve_db = os.path.join(trols_munger_ui.app.config.get('SHELVE'),
                             'trols_stats.db')
    last_upd_utc_time = {'last_update': get_file_time_in_utc(shelve_db)}
    trols_munger_ui.app.logger.debug('Last updated: "%s"',
                                     last_upd_utc_time)

    return flask.jsonify(last_upd_utc_time)
