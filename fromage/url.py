import re

from .errors import InvalidForumUrl, EnumOutOfRange
from .enums import resolveEnum, Forum, Community, Section, Location

def match(pattern, string):
	match = re.search(pattern, string)
	if match is None:
		return
	groups = match.groups()
	if len(groups)==0:
		return match.group(0)
	elif len(groups)==1:
		return groups[0]
	else:
		return groups

class Url:
	def __init__(self, href):
		match = re.match(r'/?([^?]+)\??(.*)$', href)
		if match is None:
			raise InvalidForumUrl(href)

		self.uri  = match.group(1)
		self.raw_data = match.group(2)

		matches = re.findall(r'([^&]+)=([^&#]+)', self.raw_data)
		self.data = {k:int(v) if v.isalnum() else v for k,v in matches}

		self.id = match(r'#(.+)$', self.raw_data)
		self.num_id = int(match(r'#.*?(\d+).*$', self.raw_data) or -1)

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

def formatNickname(nickname):
	assert isinstance(nickname, str)

	return nickname.replace('%23','#', 1).capitalize()