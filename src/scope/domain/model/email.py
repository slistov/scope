from datetime import datetime


class Email:
    def __init__(self, email, is_main: bool = False) -> None:
        self.email = email
        self.check_code = 'code'
        self.is_checked = False
        self.is_main = is_main
        self.created = datetime.utcnow()

    def get_check_code(self):
        return self.check_code

    def set_checked(self):
        self.is_checked = True
