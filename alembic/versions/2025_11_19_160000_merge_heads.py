"""merge heads align pk and hashed password sync

Revision ID: merge_heads_20251119
Revises: align_room_entities_pk_and_auth, 094040a3bb21
Create Date: 2025-11-19 16:00:00
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "merge_heads_20251119"
down_revision: Union[str, Sequence[str], None] = (
    "align_room_entities_pk_and_auth",
    "094040a3bb21",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

