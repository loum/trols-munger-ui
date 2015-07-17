"""GeoLib web interface.

"""
import flask


app = flask.Flask(__name__)
app.config.from_object('config')

from trols_munger_ui import views
