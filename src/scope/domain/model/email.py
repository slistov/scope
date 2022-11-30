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

    def set_main(self):
        self.is_main = True

    def unset_main(self):
        self.is_main = False

    def confirm(self, code):
        if self.is_checked:
            return True
        if self.get_check_code() == code:
            self.set_checked()
            return True
        else:
            return False
