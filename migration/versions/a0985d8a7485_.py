"""empty message

Revision ID: a0985d8a7485
Revises: 44044ed411f5
Create Date: 2024-07-15 18:04:06.012322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a0985d8a7485'
down_revision: Union[str, None] = '44044ed411f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('state_event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_finish', sa.Date(), nullable=False),
    sa.Column('id_state_event', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_state_event'], ['state_event.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('accident',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=True),
    sa.Column('id_object', sa.Integer(), nullable=True),
    sa.Column('datetime_start', sa.DateTime(), nullable=False),
    sa.Column('datetime_end', sa.DateTime(), nullable=True),
    sa.Column('time_line', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('causes_of_the_emergency', sa.Text(), nullable=False),
    sa.Column('damaged_equipment_material', sa.Text(), nullable=False),
    sa.Column('additional_material', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_object'], ['object.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('additional_material'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('equipment_to_accident',
    sa.Column('id_accident', sa.Integer(), nullable=False),
    sa.Column('id_equipment', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_accident'], ['accident.id'], ),
    sa.ForeignKeyConstraint(['id_equipment'], ['equipment.id'], ),
    sa.PrimaryKeyConstraint('id_accident', 'id_equipment')
    )
    op.create_table('type_brake_to_accident',
    sa.Column('id_accident', sa.Integer(), nullable=False),
    sa.Column('id_type_brake', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_accident'], ['accident.id'], ),
    sa.ForeignKeyConstraint(['id_type_brake'], ['type_brake.id'], ),
    sa.PrimaryKeyConstraint('id_accident', 'id_type_brake')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('type_brake_to_accident')
    op.drop_table('equipment_to_accident')
    op.drop_table('accident')
    op.drop_table('event')
    op.drop_table('state_event')
    # ### end Alembic commands ###
