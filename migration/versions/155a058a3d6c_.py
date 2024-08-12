"""empty message

Revision ID: 155a058a3d6c
Revises: 6967fde9664e
Create Date: 2024-06-12 16:50:34.537574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '155a058a3d6c'
down_revision: Union[str, None] = '6967fde9664e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'profession', ['name'])
    op.create_unique_constraint(None, 'type_user', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'type_user', type_='unique')
    op.drop_constraint(None, 'profession', type_='unique')
    # ### end Alembic commands ###
