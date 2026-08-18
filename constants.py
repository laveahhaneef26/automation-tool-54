class ErrorMessages:
    FILE_NOT_FOUND = 'The specified file was not found.'
    INVALID_INPUT = 'The input provided is invalid.'
    CONNECTION_TIMEOUT = 'The connection has timed out.'
    UNAUTHORIZED_ACCESS = 'Access is denied due to unauthorized credentials.'
    SERVER_ERROR = 'The server encountered an internal error.'

ERROR_CODES = {
    404: ErrorMessages.FILE_NOT_FOUND,
    400: ErrorMessages.INVALID_INPUT,
    408: ErrorMessages.CONNECTION_TIMEOUT,
    401: ErrorMessages.UNAUTHORIZED_ACCESS,
    500: ErrorMessages.SERVER_ERROR,
}

class ErrorHandler:
    @staticmethod
    def get_error_message(code):
        return ERROR_CODES.get(code, 'An unknown error occurred.')

    @staticmethod
    def raise_error(code):
        message = ErrorHandler.get_error_message(code)
        raise Exception(message)  

# Example usage:
# try:
#     ErrorHandler.raise_error(404)
# except Exception as e:
#     print(e)