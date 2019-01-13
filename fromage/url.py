import re

from .errors import InvalidForumUrl, EnumOutOfRange
from .enums import resolveEnum, Forum, Community, Section, Location
from .strings import FORUM_LINK

class Url:
	def __init__(self, uri, anchor=None, **params):
		self.uri = uri
		self.anchor = anchor
		self.params = params

	def __str__(self):
		p = ['{}={}'.format(k,v) for k,v in self.params.items()]
		p = '?'+'&'.join(p) if len(p) else ''
		return '{}{}{}'.format(FORUM_LINK, self.uri, p)

	@classmethod
	def parse(cls, href):
		match = re.search(r'/?([^?]+)\??(.*)$', href.replace(FORUM_LINK, ''))
		if match is None:
			raise InvalidForumUrl(href)
		uri, raw_params = match.groups()

		params = {m.group(1):m.group(2) for m in re.finditer(r'([^&]+)=([^&#]+)') if m is not None}

		match = re.search(r'#(.*?)$', href)
		anchor = match.group(1) if match else None

		return cls(uri, anchor, **params)

	@classmethod
	def redirect(cls, result):
		match = re.search(r'"redirection":"(.*?)"', result)
		if match is None:
			raise InvalidForumUrl()
		return cls.parse(match.group(1))

def getLocation(forum, community, section):
	forum     = resolveEnum(forum, Forum)
	community = resolveEnum(community, Community)
	section   = resolveEnum(section, Section, True)

	s = None
	try:
		s = Location[community][forum][section]
	except:
		pass

	if s is None:
		raise EnumOutOfRange()

	return {
		'f': resolveEnum(forum, Forum, True),
		's': s
	}