class InvalidVersion(Exception):
	"""Exception thrown when a version a dependecy is not supported."""
	def __init__(self, module, version):
		message = 'The installed version of {} is not supported. Use the version {} instead.'
		super().__init__(message.format(module, version))

class FromageError(Exception):
	"""Base exception class for Fromage."""
	def __init__(self, **params):
		message = self.__doc__.format(**params)
		super().__init__(message)

class AlreadyConnected(FromageError):
	"""This instance is already connected, disconnect first."""
class EnumOutOfRange(FromageError):
	"""Enum value out of range."""
class ImageIdError(FromageError):
	"""An image id can not be a number."""
class InternalError(FromageError):
	"""Internal error. (0x{:x})"""
class InvalidDate(FromageError):
	"""Invalid date format. Expected: dd/mm/yyyy"""
class InvalidEnum(FromageError):
	"""Invalid enum."""
class InvalidExtension(FromageError):
	"""Provided file url or name does not have a valid extension."""
class InvalidFile(FromageError):
	"""Provided file does not exist."""
class InvalidForumUrl(FromageError):
	"""Invalid Atelier801's url. ({})"""
class InvalidId(FromageError):
	"""Invalid id."""
class InvalidUser(FromageError):
	"""The user does not exist or was not found."""
class NoPollResponses(FromageError):
	"""Missing poll responses. There must be at least two responses."""
class NoRequiredFields(FromageError):
	"""The fields {} are needed."""
class NoTribeError(FromageError):
	"""This instance does not have a tribe."""
class NoUrlLocation(FromageError):
	"""Missing location."""
class NoUrlLocationPrivate(FromageError):
	"""The fields {} are needed if the object is private."""
class NotConnected(FromageError):
	"""This instance is not connected yet, connect first."""
class NotPollError(FromageError):
	"""Invalid topic. Poll not detected."""
class NotVerifiedError(FromageError):
	"""This instance has not a certificate yet. Valid the account first."""
class PollIdError(FromageError):
	"""A poll id can not be a string."""
class PollOptionNotFound(FromageError):
	"""Invalid poll option."""
class SecretKeyNotFound(FromageError):
	"""Secret keys could not be found."""
class UnaivalableEnum(FromageError):
	"""This function does not accept this enum."""
class Unauthorized(FromageError):
	"""You don't have rights to see this info."""

# Create all errors based on ErrorString Enum
# for name in vars(ErrorString):
# 	if not name[:2]=='__':
# 		msg  = getattr(ErrorString, name)
# 		name = ''.join([n.capitalize() for n in name.split('_')]) + 'Error'

# 		def init(self, *args):
# 			super(FromageError, self).__init__(self.__doc__.format(*args))
# 		error = type(name, (FromageError,), dict(__init__=init))
# 		error.__doc__ = msg

# 		globals()[name] = error
# 		__all__.append(name)