from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    FetchedValue
)

from ..domain import model

from sqlalchemy.orm import registry, relationship

mapper_registry = registry()

accounts = Table(
    'accounts', mapper_registry.metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
        server_default=FetchedValue()
    ),
    Column('fio', String),
    Column('hashed_password', String),
    Column('created', DateTime)
)

emails = Table(
    'emails', mapper_registry.metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
        server_default=FetchedValue()
    ),
    Column('email', String),
    Column('check_code', String, nullable=False),
    Column('created', DateTime),
    Column('account', Integer, ForeignKey('accounts.id')),
    Column('is_main', Boolean),
    Column('is_checked', Boolean)
)


def start_mappers():
    emails_mapper = mapper_registry.map_imperatively(model.Email, emails)
    mapper_registry.map_imperatively(
        model.Account,
        accounts,
        properties={
            "emails": relationship(emails_mapper, uselist=True),
        }
    )
