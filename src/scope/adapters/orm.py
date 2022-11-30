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
# from sqlalchemy import event

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
    Column('created', DateTime),
    Column('account', Integer, ForeignKey('account.id'), nullable=False),
    Column('is_main', Boolean),
    Column('is_checked', Boolean)    
)


def start_mappers():
    emails_mapper = mapper_registry.map_imperatively(model.Email, emails)    
    accounts_mapper = mapper_registry.map_imperatively(
        model.Account,
        accounts,
        properties={
            "emails": relationship(emails_mapper, uselist=True),
        }
    )
