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


@trols_munger_ui.app.route('/robots.txt')
@trols_munger_ui.app.route('/sitemap.xml')
def static_from_root():
    return flask.send_from_directory(trols_munger_ui.app.static_folder,
                                     flask.request.path[1:])


@trols_munger_ui.app.route('/munger/health')
def health():
    """Quick health check response.
    """
    return flask.render_template('health.html')


@trols_munger_ui.app.route('/munger/google106c89d55f3c6c6f.html')
def google():
    return flask.render_template('google106c89d55f3c6c6f.html')


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

        team = terms.get('team')
        if team is not None:
            team = team[0]

        kwargs = {
            'competition': 'saturday_am_spring_2015',
            'competition_type': comp_type,
            'section': section,
            'team': team
        }
        player_tokens = reporter.get_players(**kwargs)
        all_stats = reporter.get_player_stats(player_tokens,
                                              last_fixture=True,
                                              event=event)
        filtered_stats = reporter.sort_stats(all_stats,
                                             event=event,
                                             key='percentage',
                                             reverse=True,
                                             limit=None)

        stats['comp_type'] = comp_type
        stats['event'] = event
        stats['section'] = section
        stats['team'] = team
        stats['players'] = filtered_stats
    trols_munger_ui.app.logger.debug('stats: %s', stats)

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

    fixtures = {}
    if terms.get('token') is not None:
        token = terms.get('token')[0]
        singles = [x() for x in reporter.get_player_singles(token)]
        doubles = [x() for x in reporter.get_player_doubles(token)]
        fixtures['singles'] = singles
        fixtures['doubles'] = doubles

        player_details = player_ids_dict([token])
        if len(player_details):
            fixtures.update(player_details[0])

    r = {}
    r['stats'] = stats
    r['fixtures'] = fixtures

    return flask.render_template('stats/layout.html', result=r)


@trols_munger_ui.app.route('/munger/results')
def results():
    terms = query_terms_to_dict(flask.request.url)

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    fixtures = {}
    if terms.get('token') is not None:
        token = terms.get('token')[0]
        singles = [x() for x in reporter.get_player_singles(token)]
        doubles = [x() for x in reporter.get_player_doubles(token)]
        fixtures['singles'] = singles
        fixtures['doubles'] = doubles

        player_details = player_ids_dict([token])
        if len(player_details):
            fixtures.update(player_details[0])
    trols_munger_ui.app.logger.debug('fixtures: %s', fixtures)

    if terms.get('json') is not None and terms.get('json')[0] == 'true':
        response = flask.json.jsonify(fixtures)
    else:
        response = flask.render_template('results/layout.html',
                                         result=fixtures)

    return response

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
    shelve_db = trols_munger_ui.app.config.get('SHELVE_DB')
    last_upd_utc_time = {
        'last_update': get_file_time_in_utc(shelve_db)
    }
    trols_munger_ui.app.logger.debug('"%s" last updated: "%s"',
                                     shelve_db, last_upd_utc_time)

    return flask.jsonify(last_upd_utc_time)


@trols_munger_ui.app.route('/_teams')
def _teams():
    terms = query_terms_to_dict(flask.request.url)

    competition = terms.get('competition')
    if competition is not None:
        competition = competition[0]

    comp_type = terms.get('type')
    if comp_type is not None:
        comp_type = comp_type[0]

    section = terms.get('section')
    if section is not None:
        section = section[0]

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    kwargs = {
        'competition': competition,
        'competition_type': comp_type,
        'section': section
    }
    teams = reporter.get_teams(**kwargs)

    return flask.jsonify({'teams': teams})


@trols_munger_ui.app.route('/_sections')
def _sections():
    terms = query_terms_to_dict(flask.request.url)

    competition = terms.get('competition')
    if competition is not None:
        competition = competition[0]

    comp_type = terms.get('type')
    if comp_type is not None:
        comp_type = comp_type[0]

    db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=db)

    kwargs = {
        'competition': competition,
        'competition_type': comp_type,
    }
    sections = reporter.get_sections(**kwargs)

    return flask.jsonify({'sections': sections})
