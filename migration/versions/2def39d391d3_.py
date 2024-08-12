"""empty message

Revision ID: 2def39d391d3
Revises: a0985d8a7485
Create Date: 2024-07-17 10:30:50.762751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2def39d391d3'
down_revision: Union[str, None] = 'a0985d8a7485'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('id_accident', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'accident', ['id_accident'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'id_accident')
    # ### end Alembic commands ###
