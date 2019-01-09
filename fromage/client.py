__all__ = ['Client']

import asyncio
import re
import time

from .errors import AlreadyConnected, NotConnected
from .strings import CookieState, ForumUri, HtmlChunk, FORUM_LINK
from .utils.shakikoo import shakikoo
from .user import User
from .http import HTTPClient

class Client:
	# TODO: __doc__
	def __init__(self, loop=None):
		self.connected = False
		self.user = None

		self.cookieState = CookieState.login
		self._connectionTime = -1

		# Whether the account has a validated its account with a code
		self.hasCertificate = False

		if loop is None:
			loop = asyncio.get_event_loop()
		self.loop = loop

		self.http = HTTPClient(loop=loop)

	@property
	def connectionTime(self):
		if self._connectionTime<0:
			return self._connectionTime
		return time.clock() - self._connectionTime

	async def close(self):
		await self.http.close()

	async def _getBigList(self, uri, pageNumber, f, _totalPages=None):
		async with self.getPage('{}&p={}'.format(uri, max(1, pageNumber))) as r:
			body = await r.text()

			if _totalPages is None:
				match = re.search(HtmlChunk.total_pages, body)
				_totalPages = 1 if match is None else int(match.group(1))

			out = []
			if pageNumber==0:
				# TODO: Async range
				for i in range(1,_totalPages):
					page = await self._getBigList(i, uri, f, _totalPages)
					out.extend(page)

				return out

			# TODO: Should be an asynchronous function
			f(out, body, pageNumber, _totalPages)
			return out

	async def _getList(self, uri, pageNumber, f, html):
		def wrapper(li, body, page, total_pages):
			for match in re.finditer(html, body):
				li.append(f(match))

		return await self._getBigList(uri, pageNumber, wrapper)

	async def connect(self, username, password, encrypted=False):
		if self.connected:
			raise AlreadyConnected()

		data = {
			'rester_connecter': 'on',
			'id': username,
			'pass': password if encrypted else shakikoo(password),
			'redirect': FORUM_LINK[:-1]
		}
		data = await self.http.performAction(ForumUri.identification, data, ForumUri.login, is_json=True)
		if data.get('supprime', '')=='*':
			self.connected = True
			self.cookieState = CookieState.after_login

			self.user = await User.get(username)
			self._connectionTime = time.clock()

	async def logout(self):
		if not self.connected:
			raise NotConnected()

		await self.http.performAction(ForumUri.disconnection, ajaxUri=ForumUri.acc)
		self.connected = False
		self.user = None
		self.cookieState = CookieState.login
		self.hasCertificate = False
		self._connectionTime = -1

	def run(self, *args, **kwargs):
		self.loop.run_until_complete(self.connect(*args, **kwargs))
		self.loop.run_forever()
