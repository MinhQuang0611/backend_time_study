"""add hashed_password column to users table

Revision ID: add_hashed_password_to_user_entity
Revises: initial
Create Date: 2025-11-19 12:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_hashed_password"
down_revision: Union[str, None] = "initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "hashed_password")

