class DatabaseError(Exception):
    def __init__(self, status, error_code, error_message, timestamp):
        self.status = status
        self.error_code = error_code
        self.error_message = error_message
        self.timestamp = timestamp
        super().__init__(self)
