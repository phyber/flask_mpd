import socket
import mpd
from flask import current_app
from .exceptions import InvalidCommand

try:
	from flask import _app_ctx_stack as stack
except ImportError:
	from flask import _request_ctx_stack as stack

# Commands not in this list will be rejected by the execute method.
VALID_COMMANDS = (
		# Control commands
		'pause',
		'play',
		# Info commands
		'currentsong',
		'idle',
		'playlistinfo',
		'stats',
		'status',
		)

IDLE_HANDLERS = {
		'player': (
			'currentsong',
			'status',
			),
		}

class MPD(object):
	"""
	MPD client class.

	>>> mpc = MPC(app.config)
	"""
	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		app.config.setdefault('MPD_HOST', '127.0.0.1')
		app.config.setdefault('MPD_PORT', '6600')
		app.config.setdefault('MPD_PASS', None)
		if hasattr(app, 'teardown_appcontext'):
			app.teardown_appcontext(self.teardown)
		else:
			app.teardown_request(self.teardown)

	def teardown(self, exception):
		ctx = stack.top
		if hasattr(ctx, 'mpd_client'):
			self.disconnect()
			delattr(ctx, 'mpd_client')

	def connect(self):
		"""
		Connect to MPD using the credentials the class was initialized
		with.

		>>> connect()
		True

		Returns True on success and False on any error.
		"""
		conn_info = {
				'host': current_app.config['MPD_HOST'],
				'port': current_app.config['MPD_PORT'],
				}
		client = mpd.MPDClient()
		client.connect(**conn_info)
		return client

	def disconnect(self):
		"""
		Disconnect from MPD.
		"""
		ctx = stack.top
		if hasattr(ctx, 'mpd_client'):
			ctx.mpd_client.disconnect()

	def execute(self, func_name, args=None):
		"""
		Execute a command on the MPD.

		Connects to MPD if necessary.

		Given commands are checked against the VALID_COMMANDS tuple.
		mpyc.exceptions.InvalidCommand is raised if it's not a
		valid command.

		If the command is valid, it's passed to MPD and the results
		returned to the caller.

		>>> execute('stats')
		{"uptime":"3700562","db_update":"1370545488",,...}
		"""
		ctx = stack.top
		if ctx is not None:
			if not hasattr(ctx, 'mpd_client'):
				ctx.mpd_client = self.connect()

		if func_name in VALID_COMMANDS:
			try:
				func = getattr(ctx.mpd_client, func_name)
				if args is None:
					ret = func()
				else:
					ret = func(*args)
				return ret
			except socket.error as e:
				self.disconnect()
				raise
		else:
			raise InvalidCommand("Invalid command: '{}'".format(func_name))

	def idle(self):
		for subsystem in self.execute('idle'):
			ret = {}
			for handler in IDLE_HANDLERS.get(subsystem, ()):
				ret[handler] = self.execute(handler)
			return ret
