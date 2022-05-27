import http.client as hc


class Responses:
    UNAUTHORIZED = hc.UNAUTHORIZED, "Unauthorized Request."
    INVALID_CREDENTIALS = hc.BAD_REQUEST, "Non-existent or Invalid Credentials."
    SUCCESS = 200, "Success."
    CREATED = hc.CREATED, "Created."
    CONFLICT = hc.CONFLICT, "Credentials/Resource already exists."
    NOT_FOUND = hc.NOT_FOUND, "Resource not found."