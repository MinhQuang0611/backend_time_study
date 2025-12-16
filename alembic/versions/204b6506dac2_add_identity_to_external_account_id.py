"""add identity to external_account_id

Revision ID: 204b6506dac2
Revises: dcf94d3678ee
Create Date: 2025-12-16 05:55:04.554608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '204b6506dac2'
down_revision: Union[str, None] = 'dcf94d3678ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add IDENTITY to external_account_id
    op.execute(
        """
        ALTER TABLE external_accounts
        ALTER COLUMN external_account_id
        ADD GENERATED ALWAYS AS IDENTITY
        """
    )


def downgrade():
    # Remove IDENTITY
    op.execute(
        """
        ALTER TABLE external_accounts
        ALTER COLUMN external_account_id
        DROP IDENTITY IF EXISTS
        """
    )