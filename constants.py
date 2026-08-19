class Constants:
    BASE_URL = 'https://api.example.com/'
    TIMEOUT = 30
    RETRY_LIMIT = 5
    HEADERS = {'Content-Type': 'application/json'}
    STATUS_CODES = {
        'success': 200,
        'not_found': 404,
        'server_error': 500
    }

    @classmethod
    def get_status_message(cls, code):
        messages = {
            cls.STATUS_CODES['success']: 'Request was successful',
            cls.STATUS_CODES['not_found']: 'Resource not found',
            cls.STATUS_CODES['server_error']: 'Internal server error'
        }
        return messages.get(code, 'Unknown status code')

    @classmethod
    def is_valid_code(cls, code):
        return code in cls.STATUS_CODES.values()