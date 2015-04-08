"""BAIP Munger UI views abstraction.
"""
import baip_munger_ui


@baip_munger_ui.app.route('/health')
def health():
    """Quick health check response

    """
    return 'OK!'
