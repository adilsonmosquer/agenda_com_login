"""Adiciona origem aos itens do cronograma

Revision ID: 362646603920
Revises: c9951124f47f
Create Date: 2026-08-03 15:11:52.662801

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "362646603920"
down_revision = "c9951124f47f"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("cronograma_itens") as batch_op:

        batch_op.add_column(
            sa.Column(
                "origem",
                sa.String(20),
                nullable=False,
                server_default="IMPORTACAO",
            )
        )

        batch_op.alter_column(
            "importacao_id",
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade():

    with op.batch_alter_table("cronograma_itens") as batch_op:

        batch_op.alter_column(
            "importacao_id",
            existing_type=sa.Integer(),
            nullable=False,
        )

        batch_op.drop_column("origem")