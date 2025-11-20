"""sync models

Revision ID: 094040a3bb21
Revises: add_hashed_password
Create Date: 2025-11-19 08:30:40.085642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = "094040a3bb21"
down_revision: Union[str, None] = "add_hashed_password"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(inspector, table: str, column: str) -> bool:
    columns = [c["name"] for c in inspector.get_columns(table)]
    return column in columns


def _add_column_if_missing(table: str, column: sa.Column) -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if not _column_exists(inspector, table, column.name):
        op.add_column(table, column)


def _alter_nullable_if_exists(table: str, column: str, nullable: bool) -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if _column_exists(inspector, table, column):
        op.alter_column(
            table,
            column,
            existing_type=sa.DOUBLE_PRECISION(precision=53),
            nullable=nullable,
        )


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    _add_column_if_missing("default_settings", sa.Column("created_at", sa.Float(), nullable=False))
    _add_column_if_missing("default_settings", sa.Column("updated_at", sa.Float(), nullable=False))

    _alter_nullable_if_exists("goals", "created_at", False)
    _alter_nullable_if_exists("goals", "updated_at", False)

    _add_column_if_missing("session_pauses", sa.Column("created_at", sa.Float(), nullable=False))
    _add_column_if_missing("session_pauses", sa.Column("updated_at", sa.Float(), nullable=False))

    _alter_nullable_if_exists("sessions", "created_at", False)
    _alter_nullable_if_exists("sessions", "updated_at", False)

    _add_column_if_missing("statistics_cache", sa.Column("created_at", sa.Float(), nullable=False))
    _add_column_if_missing("statistics_cache", sa.Column("updated_at", sa.Float(), nullable=False))
    _add_column_if_missing("streak_records", sa.Column("created_at", sa.Float(), nullable=False))
    _add_column_if_missing("streak_records", sa.Column("updated_at", sa.Float(), nullable=False))

    _add_column_if_missing("task_sessions", sa.Column("updated_at", sa.Float(), nullable=False))
    _alter_nullable_if_exists("task_sessions", "created_at", False)

    _alter_nullable_if_exists("tasks", "created_at", False)
    _alter_nullable_if_exists("tasks", "updated_at", False)

    _alter_nullable_if_exists("user_settings", "created_at", False)
    _alter_nullable_if_exists("user_settings", "updated_at", False)

    if not _column_exists(inspector, "users", "updated_at"):
        op.add_column("users", sa.Column("updated_at", sa.Float(), nullable=False))
    _alter_nullable_if_exists("users", "created_at", False)

    # ensure unique email index exists
    indexes = [idx["name"] for idx in inspector.get_indexes("users")]
    if "ix_users_email" in indexes:
        op.drop_index("ix_users_email", table_name="users")
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    _alter_nullable_if_exists("users_base", "created_at", False)
    _alter_nullable_if_exists("users_base", "updated_at", False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    _alter_nullable_if_exists("users_base", "updated_at", True)
    _alter_nullable_if_exists("users_base", "created_at", True)

    indexes = [idx["name"] for idx in inspector.get_indexes("users")]
    if op.f("ix_users_email") in indexes:
        op.drop_index(op.f("ix_users_email"), table_name="users")
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    _alter_nullable_if_exists("users", "created_at", True)
    if _column_exists(inspector, "users", "updated_at"):
        op.drop_column("users", "updated_at")

    _alter_nullable_if_exists("user_settings", "updated_at", True)
    _alter_nullable_if_exists("user_settings", "created_at", True)

    _alter_nullable_if_exists("tasks", "updated_at", True)
    _alter_nullable_if_exists("tasks", "created_at", True)

    _alter_nullable_if_exists("task_sessions", "created_at", True)
    if _column_exists(inspector, "task_sessions", "updated_at"):
        op.drop_column("task_sessions", "updated_at")

    if _column_exists(inspector, "streak_records", "updated_at"):
        op.drop_column("streak_records", "updated_at")
    if _column_exists(inspector, "streak_records", "created_at"):
        op.drop_column("streak_records", "created_at")

    if _column_exists(inspector, "statistics_cache", "updated_at"):
        op.drop_column("statistics_cache", "updated_at")
    if _column_exists(inspector, "statistics_cache", "created_at"):
        op.drop_column("statistics_cache", "created_at")

    _alter_nullable_if_exists("sessions", "updated_at", True)
    _alter_nullable_if_exists("sessions", "created_at", True)

    if _column_exists(inspector, "session_pauses", "updated_at"):
        op.drop_column("session_pauses", "updated_at")
    if _column_exists(inspector, "session_pauses", "created_at"):
        op.drop_column("session_pauses", "created_at")

    _alter_nullable_if_exists("goals", "updated_at", True)
    _alter_nullable_if_exists("goals", "created_at", True)

    if _column_exists(inspector, "default_settings", "updated_at"):
        op.drop_column("default_settings", "updated_at")
    if _column_exists(inspector, "default_settings", "created_at"):
        op.drop_column("default_settings", "created_at")
