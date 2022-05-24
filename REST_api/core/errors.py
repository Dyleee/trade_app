import http.client as hc

class Responses:
    UNAUTHORIZED = hc.UNAUTHORIZED, "Unauthorized Request."
    INVALID_CREDENTIALS = hc.BAD_REQUEST, "Non-existent or Invalid Credentials."
    SUCCESS = 200, "Success"
    CONFLICT = hc.CONFLICT, "Credentials already exist."