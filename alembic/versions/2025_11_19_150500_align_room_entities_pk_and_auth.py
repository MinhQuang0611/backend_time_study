"""align room entities pk and add user auth fields

Revision ID: align_room_entities_pk_and_auth
Revises: initial
Create Date: 2025-11-19 15:05:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = "align_room_entities_pk_and_auth"
down_revision: Union[str, None] = "initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PK_TABLE_MAPPINGS = {
    "users": "user_id",
    "goals": "goal_id",
    "sessions": "session_id",
    "session_pauses": "pause_id",
    "tasks": "task_id",
    "task_sessions": "task_session_id",
    "user_settings": "setting_id",
    "default_settings": "default_setting_id",
    "statistics_cache": "cache_id",
    "streak_records": "streak_id",
}


def _ensure_pk(bind, table_name: str, pk_column: str) -> None:
    inspector = inspect(bind)
    pk_constraint = inspector.get_pk_constraint(table_name)
    columns = [column["name"] for column in inspector.get_columns(table_name)]

    if pk_constraint and pk_constraint.get("constrained_columns") == ["id"]:
        pk_name = pk_constraint.get("name")
        if pk_name:
            op.drop_constraint(pk_name, table_name, type_="primary")
        op.create_primary_key(f"pk_{table_name}_{pk_column}", table_name, [pk_column])

    if "id" in columns:
        op.drop_column(table_name, "id")


def upgrade() -> None:
    bind = op.get_bind()

    # Align primary key/ID columns across room-DB tables
    for table, pk_column in PK_TABLE_MAPPINGS.items():
        _ensure_pk(bind, table, pk_column)

    # Add hashed_password to users (UserEntity) table if missing
    inspector = inspect(bind)
    user_columns = [column["name"] for column in inspector.get_columns("users")]
    if "hashed_password" not in user_columns:
        op.add_column(
            "users",
            sa.Column("hashed_password", sa.String(length=255), nullable=True),
        )


def downgrade() -> None:
    raise NotImplementedError("Downgrade is not supported for this migration")

