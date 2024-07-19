class InvalidAuthorizationHeader(Exception):
    def __init__(self, message="Invalid Authorization header format"):
        self.message = message
        super().__init__(self.message)
        
class Unauthorized(Exception):
       def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)