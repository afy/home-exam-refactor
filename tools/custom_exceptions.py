class Boomerang_InvalidArgLengthException(Exception):
    "Raised when instantiating server/client from args goes wrong"
    pass

class Boomerang_UserNotFoundById(Exception):
    "Raised when server cant find user by given ID"
    pass

class Boomerang_CardNotFoundByCode(Exception):
    "Raised when server cant find card by given site code"
    pass