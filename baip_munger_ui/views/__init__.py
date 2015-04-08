"""BAIP Munger UI views abstraction.
"""
import flask

import baip_munger_ui


@baip_munger_ui.app.route('/munger/health')
def health():
    """Quick health check response

    """
    return 'OK!'


@baip_munger_ui.app.route('/munger/dashboard')
def dashboard():
    """Munger dashboard.

    """
    return flask.render_template('dashboard.html')
