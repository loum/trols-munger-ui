"""TROLS Munger UI views abstraction.

"""
import os
import flask

import trols_munger_ui
from trols_munger_ui.utils import query_terms_to_dict
import trols_stats.interface
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
    """Munger.
    """
    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

    terms = query_terms_to_dict(flask.request.url)

    _stats = {}
    if terms.keys():
        competition = terms.get('competition')
        if competition is not None:
            competition = competition[0]

        section = terms.get('section')
        if section is not None:
            section = section[0]

        comp_type = orig_comp_type = terms.get('type')
        if comp_type is not None:
            if comp_type[0] == 'mens':
                orig_comp_type = 'mens'
                comp_type = None
            elif comp_type[0] == 'womens':
                orig_comp_type = 'womens'
                comp_type = None
            elif comp_type[0] == 'mixed':
                orig_comp_type = 'mixed'
                comp_type = None
            else:
                comp_type = orig_comp_type = comp_type[0]

        event = terms.get('event')
        if event is not None:
            event = event[0]
        else:
            event = 'doubles'

        team = terms.get('team')
        if team is not None:
            team = team[0]

        kwargs = {
            'competition': competition,
            'competition_type': comp_type,
            'section': section,
            'team': team
        }
        player_details = reporter.get_players(**kwargs)
        player_tokens = [x.get('token') for x in player_details]
        all_stats = reporter.get_player_stats(player_tokens,
                                              last_fixture=True,
                                              event=event)
        filtered_stats = reporter.sort_stats(all_stats,
                                             event=event,
                                             key='percentage',
                                             reverse=True,
                                             limit=None)
        ranked_stats = reporter.rank_stats(filtered_stats,
                                           event=event,
                                           key='percentage')

        _stats['competition'] = competition
        _stats['comp_type'] = orig_comp_type
        _stats['event'] = event
        _stats['section'] = section
        _stats['team'] = team
        _stats['players'] = ranked_stats

    if terms.get('json') is not None and terms.get('json')[0] == 'true':
        response = flask.json.jsonify(_stats)
    else:
        response = flask.render_template('munger/layout.html',
                                         result=_stats)

    return response


@trols_munger_ui.app.route('/munger/players')
@trols_munger_ui.app.route('/munger/players/<league>/<year>/<season>')
def players(league=None, year=None, season=None):
    terms = query_terms_to_dict(flask.request.url)

    competition = None
    if league == 'nejta':
        competition = 'nejta_saturday_am_{}_{}'.format(season, year)

    trols_munger_ui.app.logger.debug('competition: %s', competition)

    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

    players = []
    search_terms = str()
    if terms.get('q') is not None:
        search_terms = ' '.join(terms.get('q'))

        players = reporter.get_players(names=terms.get('q'),
                                       competition=competition)
        for search_team in terms.get('q'):
            players.extend(reporter.get_players(team=search_team,
                                                competition=competition))

    result = {
        'players': players,
        'search_terms': search_terms,
        'competition': competition,
    }

    if terms.get('json') is not None and terms.get('json')[0] == 'true':
        response = flask.json.jsonify(result)
    else:
        response = flask.render_template('players/layout.html',
                                         result=result)

    return response


@trols_munger_ui.app.route('/munger/stats')
def stats():
    terms = query_terms_to_dict(flask.request.url)

    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

    _stats = reporter.get_player_stats(terms.get('token'))

    if terms.get('json') is not None and terms.get('json')[0] == 'true':
        response = flask.json.jsonify(_stats)
    else:
        response = flask.render_template('stats/layout.html',
                                         result=_stats)

    return response


@trols_munger_ui.app.route('/munger/results')
def results():
    terms = query_terms_to_dict(flask.request.url)

    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

    match_results = {}
    if terms.get('token') is not None:
        token = terms.get('token')[0]
        match_results = reporter.get_player_results_compact([token])

        player_details = reporter.player_ids_dict([token])
        if len(player_details):
            match_results[token].update(player_details[0])

    if terms.get('json') is not None and terms.get('json')[0] == 'true':
        response = flask.json.jsonify(match_results)
    else:
        response = flask.render_template('results/layout.html',
                                         result=match_results)

    return response


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
        if 'mens' in comp_type[0]:
            comp_type = None
        elif comp_type[0] == 'mixed':
            comp_type = None
        else:
            comp_type = comp_type[0]

    section = terms.get('section')
    if section is not None:
        section = section[0]

    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

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
        if 'mens' in comp_type[0]:
            comp_type = None
        elif comp_type[0] == 'mixed':
            comp_type = None
        else:
            comp_type = comp_type[0]

    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

    kwargs = {
        'competition': competition,
        'competition_type': comp_type,
    }
    sections = reporter.get_sections(**kwargs)

    return flask.jsonify({'sections': sections})


@trols_munger_ui.app.route('/_compdetails')
def _compdetails():
    terms = query_terms_to_dict(flask.request.url)

    competition = terms.get('competition')
    if competition is not None:
        competition = competition[0]

    _db = trols_munger_ui.get_db()
    reporter = trols_stats.interface.Reporter(db=_db)

    kwargs = {
        'competition': competition,
    }
    details = reporter.get_competition_details(**kwargs)

    return flask.jsonify(details)
