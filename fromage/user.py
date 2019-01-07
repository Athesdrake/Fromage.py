import re

from .http import HTTPClient
from .errors import InvalidUser
# from tribe import Tribe
from .strings import ForumUri, HtmlChunk
from .enums import Gender, getTitleFromId

class Profile:
	def __init__(self, **kw):
		self._avatarUrl        = kw.get('avatarUrl', None)
		self._birthday         = kw.get('birthday', None)
		self._community        = kw.get('community', 'xx')
		self._gender           = Gender[kw.get('gender', 'none')]
		self._level            = kw.get('level', 0)
		self._location         = kw.get('location', None)
		self._presentation     = kw.get('presentation', '')
		self._registrationDate = kw.get('registrationDate', '0/0/0')
		self._soulmate         = kw.get('soulmate', None)
		self._title            = getTitleFromId(self.level)
		self._totalMessages    = kw.get('totalMessages', 0)
		self._totalPrestige    = kw.get('totalPrestige', 0)
		self._tribeId          = kw.get('tribeId', -1)

	def __repr__(self):
		infos = []

		for k,v in vars(self).items():
			k, sv = k[1:], str(v)
			if v is not None and len(sv)>0:
				if len(sv)>16:
					sv = sv[:13]+'...'
				if isinstance(v, str):
					sv = repr(sv)
				infos.append('='.join((k,sv)))

		return '<Profile {}>'.format(' '.join(infos))

	@property
	def avatarUrl(self):
		return self._avatarUrl
	@property
	def birthday(self):
		return self._birthday
	@property
	def community(self):
		return self._community
	@property
	def gender(self):
		return self._gender
	@property
	def level(self):
		return self._level
	@property
	def location(self):
		return self._location
	@property
	def presentation(self):
		return self._presentation
	@property
	def registrationDate(self):
		return self._registrationDate
	@property
	def soulmate(self):
		return self._soulmate
	@property
	def title(self):
		return self._title
	@property
	def totalMessages(self):
		return self._totalMessages
	@property
	def totalPrestige(self):
		return self._totalPrestige
	@property
	def tribeId(self):
		return self._tribeId

class User:
	http = None
	def __init__(self, name:str=None, hashtag:int=None, id:int=0, **kw):
		self.name = name
		self.hashtag = hashtag
		self.id = id

		self._profile = None
		if len(kw)>0:
			self._profile = Profile(**kw)

	def __repr__(self):
		id = 'id={.id}'.format(self)
		name = 'name={.name}'.format(self)
		hashtag = 'hashtag={.hashtag}'.format(self)
		return '<User {} {} {}>'.format(id, name, hashtag)

	@classmethod
	async def get(cls, username=None, id=0):
		"""Return the User with it's profile."""
		if username is None and id==0:
			raise InvalidUser()
		if cls.http is None:
			cls.http = HTTPClient()

		url = ForumUri.profile
		if id!=0:
			params = dict(pr=id)
		else:
			params = dict(pr=username)
		data = {}
		r = await cls.http.getPage(url, params=params)
		body = await r.text()
		regex = HtmlChunk.hidden_value.pattern.format(ForumUri.element_id)
		match_id = re.search(regex, body)
		if match_id:
			id = int(match_id.group(1))

		match_name = HtmlChunk.nickname.search(body)
		hashtag = 0
		if match_name:
			username, hashtag = match_name.groups()
			hashtag = int(hashtag)

		regex = r'.*?'.join(getattr(HtmlChunk[chunk], 'pattern') for chunk in ['date', 'community', 'profile_data'])
		match_info = re.search(regex, body)
		if match_info:
			data['registrationDate'], data['community'], messages, prestige, level = match_info.groups()
			data['totalMessages'] = 0 if messages=='-' else int(messages)
			data['totalPrestige'] = int(prestige)
			data['level'] = int(level)

		match_gender = HtmlChunk.profile_gender.search(body)
		if match_gender:
			data['gender'] = match_gender.group(1).lower()

		match_location = HtmlChunk.profile_location.search(body)
		if match_location:
			data['location'] = match_location.group(1)

		match_bd = HtmlChunk.profile_birthday.search(body)
		if match_bd:
			data['birthday'] = match_bd.group(1)

		match_presentation = HtmlChunk.profile_presentation.search(body)
		if match_presentation:
			data['presentation'] = match_presentation.group(1)

		match_soulmate = re.search(HtmlChunk.profile_soulmate.pattern+HtmlChunk.nickname.pattern, body)
		if match_soulmate:
			data['soulmate'] = match_soulmate.group(1)+'#'+match_soulmate.group(2)

		match_tribe = HtmlChunk.profile_tribe.search(body)
		if match_tribe:
			data['tribeId'] = match_tribe.group(2)

		match_avatar = HtmlChunk.profile_avatar.search(body)
		if match_avatar:
			data['avatarUrl'] = match_avatar.group(0)

		return cls(username, hashtag, id, **data)

	# @property
	# def tribe(self):
	# 	return Tribe(self.tribeId, client=self._client)

	@property
	def username(self):
		name, hashtag = self.name, self.hashtag
		return '{}#{:0>4}'.format(name or '', hashtag or 0)

	@property
	def profile(self):
		return self._profile

	@property
	def avatarUrl(self):
		return self.profile._avatarUrl
	@property
	def birthday(self):
		return self.profile._birthday
	@property
	def community(self):
		return self.profile._community
	@property
	def gender(self):
		return self.profile._gender
	@property
	def level(self):
		return self.profile._level
	@property
	def location(self):
		return self.profile._location
	@property
	def presentation(self):
		return self.profile._presentation
	@property
	def registrationDate(self):
		return self.profile._registrationDate
	@property
	def soulmate(self):
		return self.profile._soulmate
	@property
	def title(self):
		return self.profile._title
	@property
	def totalMessages(self):
		return self.profile._totalMessages
	@property
	def totalPrestige(self):
		return self.profile._totalPrestige
	@property
	def tribeId(self):
		return self.profile._tribeId