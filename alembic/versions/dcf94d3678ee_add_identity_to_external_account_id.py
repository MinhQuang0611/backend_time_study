"""add identity to external_account_id

Revision ID: dcf94d3678ee
Revises: merge_heads_20251119
Create Date: 2025-12-16 05:51:53.056463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcf94d3678ee'
down_revision: Union[str, None] = 'merge_heads_20251119'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
