from datetime import datetime
from typing import List

from .email import Email
from ..security import get_secret_hash


class Account:
    emails: List[Email] = []

    def __init__(self, email, password) -> None:
        self.fio = ''
        first_email = Email(email, is_main=True)
        self.emails.append(first_email)
        self.hashed_password = get_secret_hash(password)
        self.created = datetime.utcnow()

    def get_main_email(self):
        for email in self.emails:
            if email.is_main:
                return email.email
        return None

    def set_main_email(self, main_email):
        if main_email not in [email.email for email in self.emails]:
            return False
        for email in self.emails:
            if email.email == main_email:
                email.set_main()
            else:
                email.unset_main()
        return main_email

    def get_hashed_password(self):
        return self.hashed_password
