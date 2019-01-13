__all__ = ['HTTPClient']

import asyncio
import json
import re

from aiohttp import ClientSession

from .strings import HtmlChunk, ForumUri
from .errors import SecretKeyNotFound

class Route:
	FORUM_LINK = 'https://atelier801.com/'

	def __init__(self, method, uri, **params):
		self.method = method.upper()
		self.uri = uri
		self.params = params

	@property
	def url(self):
		if re.search(r'^https?://', self.uri):
			return self.uri
		return self.FORUM_LINK + self.uri

	@classmethod
	def get(cls, uri, **params):
		return cls('GET', uri, **params)
	GET = get

	@classmethod
	def post(cls, uri, **params):
		return cls('POST', uri, **params)
	POST = post

def do_not_steal_my_cookies(_loop=None):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		'Accept-Language': 'en-US,en;q=0.9'
	}

	if _loop is None:
		_loop = asyncio.get_event_loop()

	session = ClientSession(headers=headers, loop=_loop)

	class HTTPClient:
		"""Perform requests."""
		instance = None

		def __new__(cls, *a, **kw):
			if cls.instance is None:
				cls.instance = super().__new__(cls)

			return cls.instance

		def __init__(self, loop=None):
			if loop is None:
				loop = _loop
			if loop is not _loop:
				raise ValueError('HTTPClient is in a wrong loop')

			self.headers = headers
			self._loop = loop
			self.loop.set_exception_handler(self.on_error)

		@property
		def loop(self):
			"""Do not overwrite the loop. It could break everything."""
			return self._loop

		def on_error(self, loop, context):
			"""Prevent "Unclosed Session" error."""
			print(loop, context)
			loop.run_until_complete(self.close())
			loop.call_default_exception_handler(context)

		async def close(self):
			"""Close the session."""
			if not session.closed:
				await session.close()

		async def request(self, route):
			"""Make a request."""
			# print('[{0.method}] {0.url} {0.params}'.format(route))
			return await session.request(route.method, route.url, **route.params)

		async def request_content(self, route):
			"""Make a request and return it's content."""
			r = await self.request(route)
			return await r.text()

		async def getSecretKeys(self, uri=ForumUri.index):
			"""Return the secret keys of the url."""
			body = await self.request_content(Route.get(uri))
			return HtmlChunk.secret_keys.search(body).groups()

		async def performAction(self, uri, data={}, ajaxUri=None, file=False, is_json=False):
			"""Perform an action and return the response"""
			if file:
				raise NotImplementedError

			secret_keys = await self.getSecretKeys(ajaxUri)
			if len(secret_keys)==0:
				raise SecretKeyNotFound(ajaxUri)
			data[secret_keys[0]] = secret_keys[1]

			headers = self.headers.copy()
			if ajaxUri is not None:
				headers.update({
					'Accept': 'application/json, text/javascript, */*; q=0.01',
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
					'Referer': Route.FORUM_LINK + ajaxUri if isinstance(ajaxUri, str) else ForumUri.index,
					'Connection': 'keep-alive'
				})

			r = await self.request(Route.post(uri, headers=headers, data=data))
			if is_json:
				return json.loads(await r.text())
			return r

		async def getPage(self, url, **kw):
			return await self.request(Route.get(url, **kw))

		async def getPageContent(self, url, **kw):
			return await self.request_content(Route.get(url, **kw))

	return HTTPClient

HTTPClient = do_not_steal_my_cookies()