"""TROLS Munger UI views abstraction.
"""
import flask

import trols_munger_ui


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
