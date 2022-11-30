from datetime import datetime
from typing import List

from .email import Email


class Account:
    emails: List[Email] = []

    def __init__(self, email) -> None:
        self.fio = ''
        first_email = Email(email, True)
        self.emails.append(first_email)
        self.created = datetime.utcnow()
