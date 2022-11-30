from ..domain import model


def get_email_check_code(email):
    e = model.Email(email)
    return e.get_check_code()
