from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..domain import model
from . import orm

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ"
    )
)


class SQLAlchemyAccountsRepository:
    def __init__(self, session=DEFAULT_SESSION_FACTORY):
        self.session_factory = session

    def add(self, account: model.Account):
        self.session.add(account)

    def get_by_email(self, email) -> model.Account:
        return (
            self.session.query(model.Account)
            .join(model.Email)
            .filter(orm.emails.c.email == email)
            .first()
        )

    def __enter__(self, *args):
        self.session = self.session_factory()

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SQLAlchemyEmailsRepository:
    def __init__(self, session=DEFAULT_SESSION_FACTORY):
        self.session_factory = session

    def add(self, email: model.Email):
        self.session.add(email)

    def get_by_email(self, email) -> model.Email:
        return (
            self.session.query(model.Email)
            .filter(orm.emails.c.email == email)
            .first()
        )

    def __enter__(self, *args):
        self.session = self.session_factory()

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
