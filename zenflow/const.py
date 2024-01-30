from typing import Literal



HTTP_METHODS = Literal[
    'GET',      # Retrieve data
    'HEAD',     # Retrieve data, but only the headers
    'POST',     # Create new data
    'PUT',      # Update existing data
    'DELETE',   # Delete data
    'PATCH',    # Apply partial modifications to a resource
]

STATUS_CODES = Literal[
    '200 OK',
    '301 Moved Permanently',
    '302 Found',
    '401 Unauthorized',
    '403 Forbidden',
    '404 Not Found',
    '405 Method Not Allowed',
    '500 Internal Server Error',
    '501 Not Implemented',
    '502 Bad Gateway',
    '503 Service Unavailable',
    '504 Gateway Timeout',
    '505 HTTP Version Not Supported'
]


DEFAULT_HEADERS = {
    'Content-Type': 'text/html',
    'Server': 'Zenflow/0.1',
    'Connection': 'close'
}


