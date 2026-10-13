"""add user role

Revision ID: c3a1f2d4e5b6
Revises: b2110736e4ec
Create Date: 2026-08-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3a1f2d4e5b6'
down_revision: Union[str, None] = 'b2110736e4ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # server_default='member' lets the NOT NULL column be added even if
    # the users table already has rows (they all become 'member').
    op.add_column(
        'users',
        sa.Column('role', sa.String(), nullable=False, server_default='member'),
    )


def downgrade() -> None:
    op.drop_column('users', 'role')
