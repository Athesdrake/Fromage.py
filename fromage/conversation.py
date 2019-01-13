from .http import HTTPClient
from .strings import ForumUri, HtmlChunk, FORUM_LINK
from .errors import InternalError, InvalidForumUrl, NotConnected
from .url import Url

class Conversation:
	http = None
	def __init__(self, id, title, users, isLocked, pages, totalMessages):
		self.id = id
		self.title = title
		self.users = users
		self.isLocked = isLocked
		self.pages = pages
		self.totalMessages = totalMessages

	@classmethod
	async def get(cls, co, ignoreFirstMessage=False):
		if cls.http is None:
			cls.http = http = HTTPClient()
		body = await http.getPageContent(ForumUri.conversation, co=id)

		isDiscussion, isPrivateMessage = False, False

		match = HtmlChunk.title.search(body)
		if match is None:
			raise InternalError(1)
		title = match.group(1)

		match = HtmlChunk.conversation_icon.search(body)
		if not match:
			raise InternalError(2)
		titleIcon = match.group(1)

class PrivateMessage(Conversation):
	@classmethod
	async def new(cls, client, to, subject, message):
		if not client.isConnected:
			raise NotConnected()

		data = {
			'destinataire': to,
			'objet': subject,
			'message': message
		}
		result = await client.ajax(ForumUri.create_dialog, data, ForumUri.new_dialog)
		url = Url.redirect(result)

		return cls(int(url.params['co']), subject, to, False, 1, 1)