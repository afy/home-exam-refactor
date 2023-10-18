class Boomerang_InvalidArgLengthException(Exception):
    "Raised when instantiating server/client from args goes wrong"
    pass

class Boomerang_UserNotFoundByIdException(Exception):
    "Raised when server cant find user by given ID"
    pass

class Boomerang_CardNotFoundByCodeException(Exception):
    "Raised when server cant find card by given site code"
    pass

class Boomerang_NetworkError(Exception):
    "Catch-all network error for boomerang netcode. Does not apply to socket connections"
    pass