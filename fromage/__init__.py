"""Fromaige is an implementationin python of Fromage API, an API for the Atelier801's forums

Example:
import fromaige
import asyncio
import aiohttp

bot = fromaige.Client('Username#0000', 'p455w0rd')

@bot.event
async def on_new_pm(msg):
	print('You got a new private message from {.author} !'.format(msg))

bot.run()"""

# __all__ = [] # TODO

import aiohttp
import logging
import warnings

from .__version__ import __author__, __title__, __description__
from .__version__ import __url__, __version__, __credits__

from .errors import InvalidVersion

def check_compatibility(aiohttp_version):
	# Check aiohttp version
	major, minor, patch = map(int, aiohttp_version.split('.'))

	if major<3:
		raise InvalidVersion('aiohttp', '3.0.1 or higher')

	# Check discord.py version
	# discord.py is not required.
	try:
		from discord import __version__ as discord_version
	except:
		pass
	else:
		if discord_version!='1.0.0a':
			msg = 'Fromaige is not compatible with this version of discord.py: "{}" use discord.py rewrite instead.'
			warnings.warn(msg.format(discord_version), InvalidVersion)

check_compatibility(aiohttp.__version__)

from .client import Client
from .user import User, Profile

logging.getLogger(__name__).addHandler(logging.NullHandler())