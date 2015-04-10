"""BAIP Munger UI views abstraction.
"""
import flask

import baip_munger_ui


@baip_munger_ui.app.route('/munger/health')
def health():
    """Quick health check response

    """
    return flask.render_template('health.html')


@baip_munger_ui.app.route('/munger/dashboard')
def dashboard():
    """Munger dashboard.

    """
    return flask.render_template('dashboard/layout.html')


@baip_munger_ui.app.route('/munger/upload')
def upload():
    """Munger upload.

    """
    return flask.render_template('dashboard/upload.html')
