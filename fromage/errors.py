class InvalidVersion(Exception):
	"""Exception thrown when a version a dependecy is not supported."""
	def __init__(self, module, version):
		message = 'The installed version of {} is not supported. Use the version {} instead.'
		super().__init__(message.format(module, version))

class FromaigeError(Exception):
	"""Base exception class for Fromaige."""
	def __init__(self, **params):
		message = self.__doc__.format(**params)
		super().__init__(message)

class AlreadyConnected(FromaigeError):
	"""This instance is already connected, disconnect first."""
class EnumOutOfRange(FromaigeError):
	"""Enum value out of range."""
class ImageIdError(FromaigeError):
	"""An image id can not be a number."""
class InternalError(FromaigeError):
	"""Internal error."""
class InvalidDate(FromaigeError):
	"""Invalid date format. Expected: dd/mm/yyyy"""
class InvalidEnum(FromaigeError):
	"""Invalid enum."""
class InvalidExtension(FromaigeError):
	"""Provided file url or name does not have a valid extension."""
class InvalidFile(FromaigeError):
	"""Provided file does not exist."""
class InvalidForumUrl(FromaigeError):
	"""Invalid Atelier801's url."""
class InvalidId(FromaigeError):
	"""Invalid id."""
class InvalidUser(FromaigeError):
	"""The user does not exist or was not found."""
class NoPollResponses(FromaigeError):
	"""Missing poll responses. There must be at least two responses."""
class NoRequiredFields(FromaigeError):
	"""The fields {fields} are needed."""
class NoTribeError(FromaigeError):
	"""This instance does not have a tribe."""
class NoUrlLocation(FromaigeError):
	"""Missing location."""
class NoUrlLocationPrivate(FromaigeError):
	"""The fields {fields} are needed if the object is private."""
class NotConnected(FromaigeError):
	"""This instance is not connected yet, connect first."""
class NotPollError(FromaigeError):
	"""Invalid topic. Poll not detected."""
class NotVerifiedError(FromaigeError):
	"""This instance has not a certificate yet. Valid the account first."""
class PollIdError(FromaigeError):
	"""A poll id can not be a string."""
class PollOptionNotFound(FromaigeError):
	"""Invalid poll option."""
class SecretKeyNotFound(FromaigeError):
	"""Secret keys could not be found."""
class UnaivalableEnum(FromaigeError):
	"""This function does not accept this enum."""
class Unauthorized(FromaigeError):
	"""You don't have rights to see this info."""

# Create all errors based on ErrorString Enum
# for name in vars(ErrorString):
# 	if not name[:2]=='__':
# 		msg  = getattr(ErrorString, name)
# 		name = ''.join([n.capitalize() for n in name.split('_')]) + 'Error'

# 		def init(self, *args):
# 			super(FromaigeError, self).__init__(self.__doc__.format(*args))
# 		error = type(name, (FromaigeError,), dict(__init__=init))
# 		error.__doc__ = msg

# 		globals()[name] = error
# 		__all__.append(name)