STATUS_CODES = {
    "200: Everything is OK.": 200,
    "201: Created": 201,
    "202: Accepted": 202,
    "203: Non-Authoritative Information": 203,
    "204: No Content": 204,
    "205: Reset Content": 205,
    "206: Partial Content": 206,
    "300: Multiple Choices": 300,
    "301: The requested resource has been moved permanently": 300,
    "302: The requested resource has moved, but was found": 302,
    "303: See Other": 303,
    "304: The requested resource has not been modified since the last time you accessed it": 304,
    "307: Temporary Redirect": 307,
    "308: Permanent Redirect": 308,
    "400: Bad Request": 400,
    "401: Unauthorized": 401,
    "402: Payment Required": 402,
    "403: Access to that resource is forbidden": 403,
    "404: The requested resource was not found.": 404,
    "405: Method not allowed": 405,
    "406: Not acceptable response": 406,
    "407: Proxy Authentication Required": 407,
    "408: The server timed out waiting for the rest of the request from the browser": 408,
    "409: Conflict": 409,
    "410: The requested resource is gone and won’t be coming back": 409,
    "411: Length Required": 411,
    "412: Precondition Failed": 412,
    "413: Payload Too Large": 413,
    "414: URI Too Long": 414,
    "415: Unsupported Media Type": 415,
    "416: Range Not Satisfiable": 416,
    "417: Expectation Failed": 417,
    "418: I’m a teapot": 418,
    "422: Unprocessable Entity": 422,
    "425: Too Early": 425,
    "426: Upgrade Required": 426,
    "428: Precondition Required": 428,
    "429: Too many requests": 429,
    "431: Request Header Fields Too Large": 431,
    "451: Unavailable for Legal Reasons": 451,
    "499: Client closed request": 499,
    "500: There was an error on the server and the request could not be completed": 500,
    "501: Not Implemented": 501,
    "502: Bad Gateway": 502,
    "503: The server is unavailable to handle this request right now": 503,
    "504: The server, acting as a gateway, timed out waiting for another server to respond": 504,
    "505: HTTP Version Not Supported": 505,
    "511: Network Authentication Required": 511,
    "521: Web server is down": 521,
    "525: SSL Handshake Failed": 525
}

CONTENT_TYPES = [
    "application/java-archive",
    "application/EDI-X12 ",
    "application/EDIFACT",
    "application/javascript",
    "application/octet-stream",
    "application/ogg",
    "application/pdf",
    "application/xhtml+xml",
    "application/x-shockwave-flash",
    "application/json",
    "application/ld+json",
    "application/xml",
    "application/zip",
    "application/x-www-form-urlencoded",
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/tiff",
    "image/vnd.microsoft.icon",
    "image/x-icon",
    "image/vnd.djvu",
    "image/svg+xml",
    "multipart/mixed",
    "multipart/alternative",
    "multipart/related (using by MHTML (HTML mail).)",
    "multipart/form-data",
    "text/css",
    "text/csv",
    "text/csv",
    "text/plain",
    "text/xml",
    "video/mpeg",
    "video/mp4",
    "video/quicktime",
    "video/x-ms-wmv",
    "video/x-msvideo",
    "video/x-flv",
    "video/webm",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.mozilla.xul+xml",
]

RULES_FOR = {
    "s": "Server",
    "u": "Url",
    "p": "Path"
}

OPERATORS = {
    "e": "Equal",
    "c": "Contains",
    "w": "Wildcard",
    "p": "Prefix",
    "s": "Suffix"
}

ACTIONS = {
    "r": "Redirect",
    "d": "Mock Data",
    "b": "Block"
}

HTTP_METHODS = {
    "al": "ALL",
    "ge": "GET",
    "po": "POST",
    "pu": "PUT",
    "de": "DELETE",
    "pa": "PATCH"
}

FILTER_BY_OPTIONS = {
    "q": "Query",
    "b": "Body",
    "h": "Header",
}

RESOURCE_TYPES = [
    "font",
    "image",
    "main_frame",
    "media",
    "object",
    "script",
    "stylesheet",
    "sub_frame",
    "xmlhttprequest",
    "other"
]
