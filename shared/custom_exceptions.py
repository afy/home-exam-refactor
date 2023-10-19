class Boomerang_InvalidArgException(Exception):
    "Raised when instantiating server/client from invalid args"
    pass

class Boomerang_UserNotFoundByIdException(Exception):
    "Raised when server cant find user by given ID"
    pass

class Boomerang_CardNotFoundByCodeException(Exception):
    "Raised when server cant find card by given site code"
    pass

class Boomerang_NetworkError(Exception):
    "Catch-all network error for boomerang netcode. Does not apply to socket connections or other netcode"
    pass

class Boomerang_UnidentifiedMessage(Exception):
    "Raised when an invalid message or message with json key is sent over sockets"
    pass

class Boomerang_UndefinedLogicError(Exception):
    "Called when invalid logic is detected; for example less cards in deck than required"
    pass