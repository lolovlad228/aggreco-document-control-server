"""empty message

Revision ID: bc019c4b9b66
Revises: 901c59955a35
Create Date: 2024-01-11 13:11:54.425419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc019c4b9b66'
down_revision: Union[str, None] = '901c59955a35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_to_document_id_document_fkey', 'user_to_document', type_='foreignkey')
    op.drop_constraint('user_to_document_id_user_fkey', 'user_to_document', type_='foreignkey')
    op.create_foreign_key(None, 'user_to_document', 'document', ['id_document'], ['id'])
    op.create_foreign_key(None, 'user_to_document', 'user', ['id_user'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_to_document', type_='foreignkey')
    op.drop_constraint(None, 'user_to_document', type_='foreignkey')
    op.create_foreign_key('user_to_document_id_user_fkey', 'user_to_document', 'document', ['id_user'], ['id'])
    op.create_foreign_key('user_to_document_id_document_fkey', 'user_to_document', 'user', ['id_document'], ['id'])
    # ### end Alembic commands ###
