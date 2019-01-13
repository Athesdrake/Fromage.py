__all__ = ['Client']

import asyncio
import re
import time

from .errors import AlreadyConnected, NotConnected, NotVerifiedError
from .strings import CookieState, ForumUri, HtmlChunk, FORUM_LINK
from .utils.shakikoo import shakikoo
from .user import User
from .http import HTTPClient
from .enums import resolveEnum, Community
from .conversation import Conversation, PrivateMessage

def needAccount(func):
	"""Wrap a function that raise when called but not connected"""
	def wrapper(self, *a, **kw):
		if not self.connected:
			raise NotConnected()
		return func(self, *a, **kw)
	wrapper.__doc__ = func.__doc__
	return wrapper

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

	async def ajax(self, *args, **kwargs):
		return await self.http.performAction(*args, **kwargs)

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
		data = await self.ajax(ForumUri.identification, data, ForumUri.login, is_json=True)
		if data.get('supprime', '')=='*':
			self.connected = True
			self.cookieState = CookieState.after_login

			self.user = await User.get(username)
			self._connectionTime = time.clock()

	@needAccount
	async def logout(self):
		await self.ajax(ForumUri.disconnection, ajaxUri=ForumUri.acc)
		self.connected = False
		self.user = None
		self.cookieState = CookieState.login
		self.hasCertificate = False
		self._connectionTime = -1

	def run(self, *args, **kwargs):
		self.loop.run_until_complete(self.connect(*args, **kwargs))
		self.loop.run_forever()

	@needAccount
	async def requestValidationCode(self):
		return await self.ajax(ForumUri.get_cert, ajaxUri=ForumUri.acc)

	@needAccount
	async def submitValidationCode(self, code):
		result = await self.ajax(ForumUri.set_cert, dict(code=code), ForumUri.acc, is_json=True)
		self.hasCertificate = result=={}

		return self.hasCertificate, result

	@needAccount
	async def setEmail(self, email, registration=None):
		if registration is None and not self.hasCertificate:
			raise NotVerifiedError()

		return await self.ajax(ForumUri.set_email, dict(mail=email), ForumUri.acc)

	@needAccount
	async def setPassword(self, password, encrypted=False, disconnect=False):
		if not self.hasCertificate:
			raise NotVerifiedError()

		data = dict(mdp3=password if encrypted else shakikoo(password))
		if disconnect:
			data['deco'] = 'on'

		return await self.ajax(ForumUri.set_pw, data, ForumUri.acc)

	@needAccount
	async def changeAvatar(self, image):
		raise NotImplementedError()

	@needAccount
	async def removeAvatar(self):
		return await self.ajax(ForumUri.remove_avatar, dict(pr=self.user.id), self.user.profileUri)

	@needAccount
	async def updateProfile(self, **kwargs):
		commu = kwargs.get('community', Community.xx)

		data = {
			'communaute': commu if isinstance(commu, str) else resolveEnum(Community, commu),
			'anniversaire': kwargs.get('birthday', None),
			'localisation': kwargs.get('location', None),
			'genre': kwargs.get('gender', None),
			'presentation': kwargs.get('presentation', None)
		}
		for k in ['anniversaire', 'localisation', 'genre', 'presentation']:
			if data[k] is None:
				del data[k]
			else:
				data['b_'+k] = 'on'

		return await self.ajax(ForumUri.update_profile, data, self.user.profileUri)

	@needAccount
	async def showOnline(self, online):
		data = {
			'pr': self.user.id
		}
		if online:
			data['afficher_en_ligne'] = 'on'

		return await self.ajax(ForumUri.update_parameters, data, self.user.profileUri)

	@needAccount
	async def getConversation(self, id, ignoreFirstMessage=False):
		return Conversation.get(id, ignoreFirstMessage)

	@needAccount
	async def newPM(self, *args, **kwargs):
		return await PrivateMessage.new(self, *args, **kwargs)