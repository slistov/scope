from ..domain import model
from . import orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .. import config

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ"
    )
)


class SQLAlchemyAccountsRepository:
    def __init__(self, session=DEFAULT_SESSION_FACTORY):
        self.session = session()

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
