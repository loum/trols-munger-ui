"""Global fixture arrangement for the `trols_munger_ui` package level.
"""
import os
import pytest

import trols_munger_ui


@pytest.fixture(scope='session')
def test_client():
    """Munger test client.
    """
    shelve_dir = os.path.join('trols_munger_ui', 'tests', 'files')
    trols_munger_ui.app.config['SHELVE'] = shelve_dir

    shelve_db = os.path.join(shelve_dir, 'trols_stats.db')
    trols_munger_ui.app.config['SHELVE_DB'] = shelve_db

    return trols_munger_ui.app.test_client()
