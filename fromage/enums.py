__all__ = [
	'Element','Community','Forum','Section','Location','DisplayState','InboxLocale','MessageState',
	'ContentState','Role','SearchType','SearchLocation','SectionIcon','ListRole','ForumTitle',
	'TopicIcon','Gender','RecruitmentState','Misc','resolveEnum','getTitleFromId'
]

from .errors import InvalidEnum, EnumOutOfRange

def resolveEnum(value, enum, getValue=False):
	if isinstance(value, str):
		if value not in enum:
			raise InvalidEnum()
		return enum[value] if getValue else value
	elif isinstance(value, int):
		for k,v in enum():
			if v==value:
				return v if getValue else k
		raise EnumOutOfRange()
	else:
		raise TypeError('Excepted an `int` or `string` got `{}`'.format(type(v)))

_enums = []
_methods = ['__setitem__', '__lock_enum__']
def enum(cls, dict_=None):
	global _enums, _methods
	if isinstance(cls, str):
		cls = type(cls, (), dict_ or {})

	name = cls.__name__
	c = cls

	def lock_enum(s):
		for f in _methods:
			delattr(c,f)
		c.__setattr__ = None

	setattr(cls, '__iter__', lambda s: (k for k in dir(cls) if k[:2]!='__'))
	setattr(cls, '__call__', lambda s: ((k,s[k]) for k in s))
	setattr(cls, '__getitem__', lambda s,key: getattr(s,key, None))
	setattr(cls, '__setitem__', lambda s,k,v: setattr(s,k,v))
	setattr(cls, '__lock_enum__', lock_enum)
	setattr(cls, '__repr__', lambda s: '<enum {}>'.format(name))
	setattr(cls, '__doc__', 'Enumeration for {}.'.format(name))

	cls = cls()
	_enums.append(cls)

	for k in cls:
		if type(cls[k]) is type:
			cls[k] = enum(cls[k])

	return cls

@enum
class Element:
	"""The id of each forum element"""
	topic           = 3
	message         = 4
	tribe           = 9
	profile         = 10
	private_message = 12
	poll            = 34
	image           = 45

@enum
class Community:
	"""The id of each forum server community"""
	xx = 1
	fr = 2
	br = 4
	es = 5
	cn = 6
	tr = 7
	vk = 8
	pl = 9
	hu = 10
	nl = 11
	ro = 12
	id = 13
	de = 14
	en = 15
	gb = 15
	ar = 16
	sa = 16
	ph = 17
	lt = 18
	jp = 19
	fi = 21
	cz = 22
	hr = 23
	bu = 25
	lv = 26
	he = 27
	il = 27
	it = 28
	ee = 29
	az = 30

@enum
class Forum:
	"""The id of each forum"""
	atelier801   = 5
	transformice = 6
	boumboum     = 7
	fortoresse   = 8
	nekodancer   = 508574

@enum
class Section:
	"""The official section names"""
	announcements   = "announcements"
	discussions     = "discussions"
	off_topic       = "off_topic"
	forum_games     = "forum_games"
	tribes          = "tribes"
	map_submissions = "map_submissions"
	map_editor      = "map_editor"
	modules         = "modules"
	fanart          = "fanart"
	suggestions     = "suggestions"
	bugs            = "bugs"
	archives        = "archives"

@enum
class SectionID:
	class fr:
		atelier801   = 8
		transformice = 4
		others       = 1
	class br:
		atelier801   = 16
		transformice = 18
		others       = 3
	class es:
		atelier801   = 20
		transformice = 25
		others       = 4
	class cn:
		atelier801   = 24
		transformice = 32
		others       = 5
	class tr:
		atelier801   = 28
		transformice = 39
		others       = 6
	class vk:
		atelier801   = 32
		transformice = 46
		others       = 7
	class pl:
		atelier801   = 36
		transformice = 53
		others       = 8
	class hu:
		atelier801   = 40
		transformice = 60
		others       = 9
	class nl:
		atelier801   = 44
		transformice = 67
		others       = 10
	class ro:
		atelier801   = 48
		transformice = 74
		others       = 11
	class id:
		atelier801   = 52
		transformice = 81
		others       = 12
	class de:
		atelier801   = 56
		transformice = 88
		others       = 13
	class en:
		atelier801   = 60
		transformice = 95
		others       = 14
	class ar:
		atelier801   = 77
		transformice = 104
		others       = 15
	class ph:
		atelier801   = 81
		transformice = 111
		others       = 16
	class lt:
		atelier801   = 85
		transformice = 118
		others       = 17
	class jp:
		atelier801   = 89
		transformice = 125
		others       = 18
	class fi:
		atelier801   = 93
		transformice = 132
		others       = 19
	class cz:
		atelier801   = 123
		transformice = 176
		others       = 22
	class hr:
		atelier801   = 127
		transformice = 183
		others       = 23
	class bu:
		atelier801   = 135
		transformice = 197
		others       = 25
	class lv:
		atelier801   = 139
		transformice = 204
		others       = 26
	class he:
		atelier801   = 101
		transformice = 146
		others       = 21
	class it:
		atelier801   = 97
		transformice = 139
		others       = 20
	class ee:
		atelier801   = 143
		transformice = 211
		others       = 27
	class az:
		atelier801   = 147
		transformice = 218
		others       = 28

@enum
class SectionValue:
	class atelier801:
		announcements = -1
		discussions   = 0
		off_topic     = 1
		forum_games   = 2
		tribes        = 3
	class transformice:
		map_submissions = -1
		discussions     = 0
		map_editor      = 1
		modules         = 2
		fanart          = 3
		suggestions     = 4
		bugs            = 5
		archives        = 6
	class bouboum:
		discussions = 0
	class fortoresse:
		discussions = 0
	class nekodancer:
		discussions = 0

@enum
class Location: pass

for community in SectionID:
	commu = enum(community)
	Location[community] = commu

	for forum in SectionValue:
		fofo = enum(forum)
		commu[forum] = fofo

		id = SectionID[community][forum]
		if id is None:
			id = SectionID[community].others

		for name in SectionValue[forum]:
			value = SectionValue[forum][name]
			if value>=0:
				fofo[name] = value+id

Location.xx = enum('xx')
Location.xx.atelier801 = enum('atelier801', dict(announcements=1))
Location.xx.transformice = enum('transformice', dict(map_submissions=102))

@enum
class DisplayState:
	"""The ids of the available display states of an element. (Topic)"""
	active  = 0
	locked  = 1
	deleted = 2

@enum
class InboxLocale:
	"""The ids of the available locales on the inbox."""
	inbox    = 0
	archives = 1
	bin      = 2

@enum
class MessageState:
	"""The ids of the available display states of a message."""
	active    = 0
	moderated = 1

@enum
class ContentState:
	"""The content state situations."""
	restricted   = "true"
	unrestricted = "false"

@enum
class Role:
	"""The discriminator role ids"""
	administrator = 1
	moderator     = 10
	sentinel      = 15
	mapcrew       = 20

@enum
class SearchType:
	"""The search type ids"""
	message_topic = 4
	tribe         = 9
	player        = 10

@enum
class SearchLocation:
	"""Search locations for `SearchType.message_topic`."""
	posts  = 1
	titles = 2
	both   = 3

@enum
class SectionIcon:
	"""The available icons for sections"""
	nekodancer     = "nekodancer.png"
	fortoresse     = "fortoresse.png"
	balloon_cheese = "bulle-fromage.png"
	transformice   = "transformice.png"
	balloon_dots   = "bulle-pointillets.png"
	wip            = "wip.png"
	megaphone      = "megaphone.png"
	skull          = "crane.png"
	atelier801     = "atelier801.png"
	brush          = "pinceau.png"
	grass          = "picto.png"
	bouboum        = "bouboum.png"
	hole           = "trou-souris.png"
	deadmaze       = "deadmaze.png"
	cogwheel       = "roue-dentee.png"
	dice           = "de.png"
	flag           = "drapeau.png"
	runforcheese   = "runforcheese.png"

@enum
class ListRole:
	"""The available role ids for the staff-list."""
	moderator         = 1
	super_moderator   = None # 2
	sentinel          = 4
	arbitre           = 8
	mapcrew           = 16
	module_team       = 32
	anti_hack_brigade = 64
	administrator     = 128
	fashion_squad     = None # 256
	votecrew          = 512
	translator        = 1024
	funcorp           = 2048

@enum
class ForumTitle:
	"""The forum titles."""
	citizen = 0
	censor  = 1
	consul  = 2
	senator = 3
	archon  = 4
	heliast = 5

def getTitleFromId(id):
	for k,v in ForumTitle():
		if v==id:
			return k

@enum
class TopicIcon:
	"""The available icons for a topic."""
	poll               = r"sondage\.png"
	private_discussion = r"bulle-pointillets\.png"
	private_message    = r"enveloppe\.png"
	postit             = r"postit\.png"
	locked             = r"cadenas\.png"
	deleted            = r"/no\.png"

@enum
class Gender:
	"""The available genders on profile."""
	none   = 0
	female = 1
	male   = 2

@enum
class RecruitmentState:
	"""The recruitment state for tribes."""
	closed = 0
	open   = 1

@enum
class Misc:
	"""Miscellaneous values.
	`non_member` -> Tribe section permission to allow non members to have access to something."""
	non_member = -2

for e in _enums:
	e.__lock_enum__()
del _enums
del _methods