from flask import jsonify


class ValidationException(Exception):
    status_code = 420

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = 'Validation error: ' + str(message)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv