# -*- coding: UTF-8 -*-


class QantyError(Exception):
    fmt = "An unspecified error occurred"

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


class ApiError(QantyError):
    fmt = "Qanty API error {code}: {msg}"

    def __init__(self, code: str, msg: str, payload=None):
        super().__init__(code=code, msg=msg)
        self.code = code
        self.msg = msg
        self.payload = payload


class InvalidUserIdentifier(QantyError):
    fmt = "Invalid user identifier: '{user_id}'"


class BranchNotFound(QantyError):
    fmt = "Branch '{branch_id}' not found"


class UserNotFound(QantyError):
    fmt = "User '{user_id}' not found"


class UserAlreadyExists(QantyError):
    fmt = "User '{user_id}' already exists"
