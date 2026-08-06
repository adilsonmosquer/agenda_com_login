"""Cria tabela usuarios

Revision ID: 7b8d0f1c9a01
Revises: 690d0dfc0f33
Create Date: 2026-08-06
"""

from alembic import op
import sqlalchemy as sa

revision = "7b8d0f1c9a01"
down_revision = "690d0dfc0f33"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("usuario", sa.String(50), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(255), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("administrador", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade():
    op.drop_table("usuarios")
