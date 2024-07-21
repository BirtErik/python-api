from datetime import datetime

class BaseError(Exception):
    def __init__(self, status="error", error_code=500, error_message="An error occurred", timestamp=None):
        self.status = status
        self.error_code = error_code
        self.error_message = error_message
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        super().__init__(self.error_message)
    
    def to_dict(self):
        return {
            "response": {
                "status": self.status,
                "errorCode": self.error_code,
                "errorMessage": self.error_message,
                "timestamp": self.timestamp
            } 
        }

class InvalidAuthorizationHeader(BaseError):
    def __init__(self, message="Invalid Authorization header format"):
        super().__init__(status="error", error_code=400, error_message=message)
        
class Unauthorized(BaseError):
    def __init__(self, message="Unauthorized"):
        super().__init__(status="error", error_code=401, error_message=message)
        
class NotFound(BaseError):
    def __init__(self, message="Not found"):
        super().__init__(status="error", error_code=404, error_message=message)

class DatabaseError(BaseError):
    def __init__(self, status, error_code, error_message, timestamp=None):
        super().__init__(status=status, error_code=error_code, error_message=error_message, timestamp=timestamp)
