"""email-account - nullable

Revision ID: b3bffa9af75d
Revises: 51b326193083
Create Date: 2022-11-30 17:24:25.297378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3bffa9af75d'
down_revision = '51b326193083'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('emails', 'account',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('emails', 'account',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###