"""Setup script for the TROLS Stats project.
"""
import os
import setuptools

PROJECT_NAME = os.path.basename(os.path.abspath(os.curdir))

PROD_PACKAGES = [
    'configa>=1.0.0',
    'filer>=1.0.0',
    'flask>=1.1.1',
    'trols-stats>=1.0.2',
]

DEV_PACKAGES = [
    'pylint',
    'pytest',
    'pytest-cov',
    'sphinx_rtd_theme',
    'twine',
    'Sphinx',
]

PACKAGES = list(PROD_PACKAGES)
if (os.environ.get('APP_ENV') is not None and
        'dev' in os.environ.get('APP_ENV')):
    PACKAGES += DEV_PACKAGES

SETUP_KWARGS = {
    'name': PROJECT_NAME,
    'version': '1.0.2',
    'description': 'TROLS Munger UI',
    'author': 'Lou Markovski',
    'author_email': 'lou.markovski@gmail.com',
    'url': 'https://github.com/loum/trols-munger-ui',
    'install_requires': PACKAGES,
    'packages': setuptools.find_packages(),
    'package_data': {
        'trols_munger_ui': [
        ],
    },
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
}

setuptools.setup(**SETUP_KWARGS)
