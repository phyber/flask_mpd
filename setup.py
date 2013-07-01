"""
Flask-MPD
---------

Flask extension for communicating with an MPD instance.
"""
from setuptools import setup

setup(
	name='Flask-MPD',
	version='0.1',
	url='https://github.com/phyber/flask-mpd/',
	author='phyber',
	author_email=None,
	description='MPD extension for Flask.',
	long_description=__doc__,
	packages=['flask_mpd'],
	zip_safe=False,
	include_package_data=True,
	platforms='any',
	install_requires=[
		'Flask',
		'python-mpd',
	],
	classifiers=[
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
