"""Initial migration

Revision ID: 7f57c694ed93
Revises: 
Create Date: 2025-04-11 02:27:36.718590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f57c694ed93'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('serial_number', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_devices_id'), 'devices', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('measurements',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('device_id', sa.UUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('x', sa.Float(), nullable=False),
    sa.Column('y', sa.Float(), nullable=False),
    sa.Column('z', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_measurements_device_id'), 'measurements', ['device_id'], unique=False)
    op.create_index(op.f('ix_measurements_id'), 'measurements', ['id'], unique=False)
    op.create_index(op.f('ix_measurements_timestamp'), 'measurements', ['timestamp'], unique=False)
    op.create_table('user_device_association',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('device_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'device_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_device_association')
    op.drop_index(op.f('ix_measurements_timestamp'), table_name='measurements')
    op.drop_index(op.f('ix_measurements_id'), table_name='measurements')
    op.drop_index(op.f('ix_measurements_device_id'), table_name='measurements')
    op.drop_table('measurements')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_devices_id'), table_name='devices')
    op.drop_table('devices')
    # ### end Alembic commands ###
