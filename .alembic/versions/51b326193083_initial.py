"""Initial

Revision ID: 51b326193083
Revises: 
Create Date: 2022-11-30 17:12:15.890357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51b326193083'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), server_default=sa.FetchedValue(), autoincrement=True, nullable=False),
    sa.Column('fio', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emails',
    sa.Column('id', sa.Integer(), server_default=sa.FetchedValue(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('account', sa.Integer(), nullable=False),
    sa.Column('is_main', sa.Boolean(), nullable=True),
    sa.Column('is_checked', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['account'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emails')
    op.drop_table('accounts')
    # ### end Alembic commands ###
