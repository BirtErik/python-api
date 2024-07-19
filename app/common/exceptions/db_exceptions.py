class DatabaseError(Exception):
    def __init__(self, status, error_code, error_message, timestamp):
        self.status = status
        self.error_code = error_code
        self.error_message = error_message
        self.timestamp = timestamp
        super().__init__(self)
        
    def to_dict(self):
        """Convert the error details to a dictionary."""
        error_dict = {
            "status": self.status,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
            "timestamp": self.timestamp
        }
        error_dict.update(self.details)
        return error_dict