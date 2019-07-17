'''
    Flask-Pbj
    -----------

    Flask-Pbj provides support for protobuf and json formatted request and
    response data. The pbj decorator serializes and deserializes json or
    protobuf formatted messages to and from a python dictionary.

    Flask-Pbj seems to somewhat work with protobuf 3.x

    Links
    `````
    * `development version
    <https://github.com/rrbutani/flask-pbj>`_
    * `Google Protobuf
    <https://pypi.org/project/protobuf/>`_
    * `Google Protobuf Developer guide
    <https://developers.google.com/protocol-buffers/docs/overview>`_
'''
import os
from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'flask_pbj', '__init__.py')
version_line = list(filter(lambda l: l.startswith('__version_info__'),
                      open(module_path)))[0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

setup(
    name='Flask-Pbj',
    version=__version__,
    url='https://github.com/rrbutani/flask-pbj',
    license='MIT',
    author='Keen Browne',
    author_email='keen.browne@gmail.com',
    description='Simplifies the use of Protobuf in Flask app.routes',
    long_description=__doc__,
	packages=[
        'flask_pbj'
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'protobuf',
        'Werkzeug',
    ],
    package_data={
        "flask_pbj": ["py.typed"]
    },
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
